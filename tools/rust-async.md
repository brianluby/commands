---
version: 1.0.0
tags: [rust, async, concurrency, performance, tokio]
---

# Rust Async

Optimize async Rust code for performance and correctness. Covers runtime selection, task management, channel optimization, and async patterns.

## Usage
```
/rust-async [optimization-type] [runtime]
```

## Optimization Types

### General Analysis
```
/rust-async                      # Analyze and optimize async code
/rust-async runtime             # Runtime selection and configuration
/rust-async channels            # Optimize channel usage
/rust-async spawning            # Task spawning strategies
```

### Specific Patterns
```
/rust-async streams tokio       # Stream processing with Tokio
/rust-async parallel async-std  # Parallel execution patterns
/rust-async cancellation        # Graceful shutdown and cancellation
```

## Pre-flight Checks

1. Detect async runtime in use
2. Analyze async patterns
3. Check for blocking operations
4. Identify performance bottlenecks

## Implementation

Given the context: $ARGUMENTS

### 1. Runtime Selection and Configuration

#### Runtime Comparison
```rust
// Tokio - Best for I/O-heavy workloads
[dependencies]
tokio = { version = "1", features = ["full"] }

// async-std - Familiar std-like API
[dependencies]
async-std = { version = "1", features = ["attributes"] }

// smol - Minimal and fast
[dependencies]
smol = "1"

// For rustcopy, Tokio is recommended for:
// - Mature ecosystem
// - Excellent file I/O support  
// - Built-in fs module with async operations
```

#### Optimized Tokio Configuration
```rust
use tokio::runtime::Builder;

pub fn create_optimized_runtime() -> tokio::runtime::Runtime {
    Builder::new_multi_thread()
        .worker_threads(num_cpus::get())
        .thread_name("rustcopy-worker")
        .thread_stack_size(2 * 1024 * 1024) // 2MB stack
        .max_blocking_threads(512) // For file I/O
        .enable_all()
        .build()
        .expect("Failed to create runtime")
}

// For CLI applications, consider current_thread runtime
pub fn create_cli_runtime() -> tokio::runtime::Runtime {
    Builder::new_current_thread()
        .enable_all()
        .build()
        .expect("Failed to create runtime")
}
```

### 2. Async File Operations

```rust
use tokio::fs::{File, OpenOptions};
use tokio::io::{AsyncRead, AsyncWrite, AsyncReadExt, AsyncWriteExt, BufReader, BufWriter};
use futures::stream::{Stream, StreamExt};

// Basic async copy
pub async fn async_copy(src: &Path, dst: &Path) -> io::Result<u64> {
    let mut src_file = File::open(src).await?;
    let mut dst_file = File::create(dst).await?;
    
    tokio::io::copy(&mut src_file, &mut dst_file).await
}

// Buffered async copy with progress
pub async fn buffered_copy_with_progress<F>(
    src: &Path,
    dst: &Path,
    mut progress: F,
) -> io::Result<u64>
where
    F: FnMut(u64) + Send,
{
    let src_file = File::open(src).await?;
    let src_size = src_file.metadata().await?.len();
    
    let dst_file = File::create(dst).await?;
    
    let mut reader = BufReader::with_capacity(256 * 1024, src_file);
    let mut writer = BufWriter::with_capacity(256 * 1024, dst_file);
    
    let mut buffer = vec![0u8; 64 * 1024];
    let mut total_copied = 0u64;
    
    loop {
        let n = reader.read(&mut buffer).await?;
        if n == 0 {
            break;
        }
        
        writer.write_all(&buffer[..n]).await?;
        total_copied += n as u64;
        
        progress(total_copied);
    }
    
    writer.flush().await?;
    Ok(total_copied)
}

// Parallel chunk copying for large files
pub async fn parallel_async_copy(
    src: &Path,
    dst: &Path,
    chunk_size: u64,
) -> io::Result<()> {
    let src_meta = tokio::fs::metadata(src).await?;
    let file_size = src_meta.len();
    
    // Pre-create destination file
    let dst_file = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .open(dst)
        .await?;
    dst_file.set_len(file_size).await?;
    drop(dst_file);
    
    // Calculate chunks
    let num_chunks = (file_size + chunk_size - 1) / chunk_size;
    let mut tasks = Vec::new();
    
    for i in 0..num_chunks {
        let src = src.to_path_buf();
        let dst = dst.to_path_buf();
        let offset = i * chunk_size;
        let len = chunk_size.min(file_size - offset);
        
        let task = tokio::spawn(async move {
            copy_chunk(&src, &dst, offset, len).await
        });
        
        tasks.push(task);
    }
    
    // Wait for all chunks
    let results: Vec<io::Result<()>> = futures::future::join_all(tasks)
        .await
        .into_iter()
        .map(|r| r.unwrap())
        .collect();
    
    // Check for errors
    for result in results {
        result?;
    }
    
    Ok(())
}

async fn copy_chunk(
    src: &Path,
    dst: &Path,
    offset: u64,
    length: u64,
) -> io::Result<()> {
    use tokio::io::{AsyncSeekExt, SeekFrom};
    
    let mut src_file = File::open(src).await?;
    src_file.seek(SeekFrom::Start(offset)).await?;
    
    let mut dst_file = OpenOptions::new()
        .write(true)
        .open(dst)
        .await?;
    dst_file.seek(SeekFrom::Start(offset)).await?;
    
    // Use take to limit reading
    let limited_reader = src_file.take(length);
    let mut buf_reader = BufReader::new(limited_reader);
    let mut buf_writer = BufWriter::new(dst_file);
    
    tokio::io::copy(&mut buf_reader, &mut buf_writer).await?;
    buf_writer.flush().await?;
    
    Ok(())
}
```

### 3. Channel Optimization

```rust
use tokio::sync::{mpsc, oneshot};
use crossbeam_channel as crossbeam;

// File operation commands for worker pool
#[derive(Debug)]
enum FileOp {
    Copy { src: PathBuf, dst: PathBuf },
    Delete { path: PathBuf },
    Move { src: PathBuf, dst: PathBuf },
}

// Optimized channel-based worker pool
pub struct AsyncFileWorkerPool {
    sender: mpsc::Sender<(FileOp, oneshot::Sender<io::Result<()>>)>,
    workers: Vec<tokio::task::JoinHandle<()>>,
}

impl AsyncFileWorkerPool {
    pub fn new(num_workers: usize) -> Self {
        let (sender, receiver) = mpsc::channel(1000); // Bounded channel
        let receiver = Arc::new(Mutex::new(receiver));
        
        let mut workers = Vec::new();
        
        for i in 0..num_workers {
            let receiver = Arc::clone(&receiver);
            
            let worker = tokio::spawn(async move {
                loop {
                    let (op, response_tx) = {
                        let mut rx = receiver.lock().await;
                        match rx.recv().await {
                            Some(item) => item,
                            None => break, // Channel closed
                        }
                    };
                    
                    let result = match op {
                        FileOp::Copy { src, dst } => {
                            tokio::fs::copy(&src, &dst).await.map(|_| ())
                        }
                        FileOp::Delete { path } => {
                            tokio::fs::remove_file(&path).await
                        }
                        FileOp::Move { src, dst } => {
                            tokio::fs::rename(&src, &dst).await
                        }
                    };
                    
                    let _ = response_tx.send(result);
                }
                
                debug!("Worker {} shutting down", i);
            });
            
            workers.push(worker);
        }
        
        Self { sender, workers }
    }
    
    pub async fn execute(&self, op: FileOp) -> io::Result<()> {
        let (tx, rx) = oneshot::channel();
        
        self.sender.send((op, tx)).await
            .map_err(|_| io::Error::new(io::ErrorKind::Other, "Worker pool shut down"))?;
            
        rx.await
            .map_err(|_| io::Error::new(io::ErrorKind::Other, "Worker dropped"))?
    }
}

// For CPU-bound operations, use crossbeam with blocking tasks
pub async fn process_files_parallel<T, F>(
    paths: Vec<PathBuf>,
    processor: F,
) -> Vec<Result<T, io::Error>>
where
    F: Fn(PathBuf) -> Result<T, io::Error> + Send + Sync + 'static,
    T: Send + 'static,
{
    let (tx, rx) = crossbeam::bounded(100);
    let processor = Arc::new(processor);
    
    // Spawn blocking task for CPU-bound work
    let handle = tokio::task::spawn_blocking(move || {
        use rayon::prelude::*;
        
        paths.par_iter()
            .map(|path| {
                let result = processor(path.clone());
                let _ = tx.send((path.clone(), result));
            })
            .collect::<Vec<_>>();
    });
    
    // Collect results asynchronously
    let mut results = Vec::new();
    for _ in 0..paths.len() {
        if let Ok((path, result)) = rx.recv() {
            results.push(result);
        }
    }
    
    handle.await.unwrap();
    results
}
```

### 4. Stream Processing

```rust
use futures::stream::{self, Stream, StreamExt, TryStreamExt};
use tokio_stream::wrappers::ReadDirStream;

// Async directory traversal with streams
pub fn walk_dir_stream(path: PathBuf) -> impl Stream<Item = io::Result<PathBuf>> {
    stream::unfold(vec![path], |mut paths| async move {
        let path = paths.pop()?;
        
        match tokio::fs::read_dir(&path).await {
            Ok(read_dir) => {
                let mut stream = ReadDirStream::new(read_dir);
                let mut entries = Vec::new();
                
                while let Some(entry) = stream.next().await {
                    match entry {
                        Ok(entry) => {
                            let path = entry.path();
                            if path.is_dir() {
                                paths.push(path.clone());
                            }
                            entries.push(Ok(path));
                        }
                        Err(e) => entries.push(Err(e)),
                    }
                }
                
                Some((stream::iter(entries), paths))
            }
            Err(e) => Some((stream::iter(vec![Err(e)]), paths)),
        }
    })
    .flatten()
}

// Process files with concurrent limit
pub async fn process_files_stream<F, T>(
    paths: impl Stream<Item = PathBuf>,
    processor: F,
    concurrency: usize,
) -> Vec<Result<T, io::Error>>
where
    F: Fn(PathBuf) -> futures::future::BoxFuture<'static, Result<T, io::Error>>,
{
    paths
        .map(|path| processor(path))
        .buffer_unordered(concurrency)
        .collect()
        .await
}

// Example: Copy all files from directory with concurrency control
pub async fn copy_directory_concurrent(
    src_dir: &Path,
    dst_dir: &Path,
    max_concurrent: usize,
) -> Result<usize, io::Error> {
    tokio::fs::create_dir_all(dst_dir).await?;
    
    let src_dir = src_dir.to_path_buf();
    let dst_dir = dst_dir.to_path_buf();
    
    let files = walk_dir_stream(src_dir.clone())
        .try_filter(|path| futures::future::ready(path.is_file()));
    
    let copy_count = files
        .map(|result| {
            result.and_then(|src_path| {
                let relative = src_path.strip_prefix(&src_dir)
                    .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
                let dst_path = dst_dir.join(relative);
                Ok((src_path, dst_path))
            })
        })
        .try_for_each_concurrent(max_concurrent, |(src, dst)| async move {
            if let Some(parent) = dst.parent() {
                tokio::fs::create_dir_all(parent).await?;
            }
            tokio::fs::copy(&src, &dst).await?;
            Ok(())
        })
        .await?;
    
    Ok(copy_count)
}
```

### 5. Cancellation and Timeouts

```rust
use tokio::time::{timeout, Duration};
use tokio_util::sync::CancellationToken;

pub struct CancellableOperation {
    token: CancellationToken,
}

impl CancellableOperation {
    pub fn new() -> Self {
        Self {
            token: CancellationToken::new(),
        }
    }
    
    pub fn cancel(&self) {
        self.token.cancel();
    }
    
    pub async fn copy_with_cancellation(
        &self,
        src: &Path,
        dst: &Path,
    ) -> Result<u64, CopyError> {
        let token = self.token.clone();
        let src = src.to_path_buf();
        let dst = dst.to_path_buf();
        
        tokio::select! {
            result = async_copy(&src, &dst) => {
                result.map_err(|e| e.into())
            }
            _ = token.cancelled() => {
                // Clean up partial file
                let _ = tokio::fs::remove_file(&dst).await;
                Err(CopyError::Cancelled)
            }
        }
    }
    
    pub async fn copy_with_timeout(
        src: &Path,
        dst: &Path,
        timeout_secs: u64,
    ) -> Result<u64, CopyError> {
        match timeout(
            Duration::from_secs(timeout_secs),
            async_copy(src, dst)
        ).await {
            Ok(Ok(bytes)) => Ok(bytes),
            Ok(Err(e)) => Err(e.into()),
            Err(_) => {
                // Timeout - clean up partial file
                let _ = tokio::fs::remove_file(dst).await;
                Err(CopyError::Timeout)
            }
        }
    }
}

// Graceful shutdown pattern
pub struct AsyncCopyService {
    shutdown: broadcast::Sender<()>,
    workers: Vec<tokio::task::JoinHandle<()>>,
}

impl AsyncCopyService {
    pub async fn shutdown(self) {
        // Signal shutdown
        let _ = self.shutdown.send(());
        
        // Wait for workers with timeout
        let shutdown_timeout = Duration::from_secs(30);
        
        if timeout(
            shutdown_timeout,
            futures::future::join_all(self.workers)
        ).await.is_err() {
            eprintln!("Warning: Some workers didn't shutdown gracefully");
        }
    }
}
```

### 6. Async Performance Patterns

```rust
// Avoid blocking the runtime
pub async fn process_file_content(path: &Path) -> io::Result<String> {
    // BAD: Blocks the async runtime
    // let content = std::fs::read_to_string(path)?;
    
    // GOOD: Use async version
    let content = tokio::fs::read_to_string(path).await?;
    
    // For CPU-intensive processing, use spawn_blocking
    tokio::task::spawn_blocking(move || {
        // Heavy computation here
        expensive_transform(content)
    })
    .await
    .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?
}

// Batch operations for efficiency
pub async fn batch_delete(paths: Vec<PathBuf>, batch_size: usize) -> Vec<io::Result<()>> {
    use futures::stream::{self, StreamExt};
    
    stream::iter(paths)
        .chunks(batch_size)
        .map(|batch| async move {
            // Process batch concurrently
            let tasks: Vec<_> = batch.into_iter()
                .map(|path| tokio::fs::remove_file(path))
                .collect();
            
            futures::future::join_all(tasks).await
        })
        .buffered(num_cpus::get())
        .flatten()
        .collect()
        .await
}

// Smart polling with exponential backoff
pub async fn wait_for_file(
    path: &Path,
    max_wait: Duration,
) -> io::Result<()> {
    let start = Instant::now();
    let mut delay = Duration::from_millis(10);
    
    loop {
        if path.exists() {
            return Ok(());
        }
        
        if start.elapsed() > max_wait {
            return Err(io::Error::new(
                io::ErrorKind::TimedOut,
                "File not found within timeout"
            ));
        }
        
        tokio::time::sleep(delay).await;
        delay = (delay * 2).min(Duration::from_secs(1));
    }
}
```

### 7. Testing Async Code

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[tokio::test]
    async fn test_async_copy() {
        let temp_dir = TempDir::new().unwrap();
        let src = temp_dir.path().join("source.txt");
        let dst = temp_dir.path().join("dest.txt");
        
        // Create source file
        tokio::fs::write(&src, b"test data").await.unwrap();
        
        // Copy
        let bytes = async_copy(&src, &dst).await.unwrap();
        assert_eq!(bytes, 9);
        
        // Verify
        let content = tokio::fs::read(&dst).await.unwrap();
        assert_eq!(content, b"test data");
    }
    
    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn test_concurrent_operations() {
        let operations = (0..100).map(|i| {
            tokio::spawn(async move {
                // Simulate work
                tokio::time::sleep(Duration::from_millis(10)).await;
                i
            })
        });
        
        let results: Vec<_> = futures::future::join_all(operations)
            .await
            .into_iter()
            .map(|r| r.unwrap())
            .collect();
            
        assert_eq!(results.len(), 100);
    }
    
    #[tokio::test]
    async fn test_cancellation() {
        let op = CancellableOperation::new();
        let token = op.token.clone();
        
        // Start operation
        let handle = tokio::spawn(async move {
            tokio::time::sleep(Duration::from_secs(10)).await;
        });
        
        // Cancel after 100ms
        tokio::time::sleep(Duration::from_millis(100)).await;
        token.cancel();
        
        // Should complete quickly due to cancellation
        let result = timeout(Duration::from_millis(200), handle).await;
        assert!(result.is_ok());
    }
}
```

### 8. Generate Async Optimization Report

```markdown
# Async Optimization Report

## Performance Summary
- **Sync Baseline**: 523 MB/s
- **Async Optimized**: 4.2 GB/s
- **Concurrency Improvement**: 8x with parallel chunks
- **Memory Usage**: Reduced by 45% with streaming

## Optimizations Applied

### 1. Runtime Configuration
- Tuned worker threads to CPU count
- Increased max blocking threads for I/O
- Optimized thread stack size

### 2. Concurrent I/O
- Parallel chunk processing for large files
- Stream-based directory traversal
- Bounded channels to prevent memory bloat

### 3. Resource Management
- Graceful cancellation support
- Timeout handling with cleanup
- Backpressure via bounded channels

## Code Improvements

```rust
// Before: Sequential and blocking
for file in files {
    std::fs::copy(&file.src, &file.dst)?;
}

// After: Concurrent and async
stream::iter(files)
    .map(|file| async move {
        tokio::fs::copy(&file.src, &file.dst).await
    })
    .buffer_unordered(32)
    .try_collect()
    .await?;
```

## Benchmarks

| Operation | Sync Time | Async Time | Speedup |
|-----------|-----------|------------|---------|
| Copy 1000 files | 12.3s | 1.8s | 6.8x |
| Directory walk | 890ms | 145ms | 6.1x |
| Parallel copy 1GB | 1.91s | 238ms | 8.0x |

## Recommendations

1. Use Tokio for I/O-heavy operations
2. Implement proper cancellation for long operations  
3. Add progress reporting via channels
4. Use streaming for large datasets
5. Profile with `tokio-console` for runtime insights
```

## Related Commands

- `/rust-io-optimize` - I/O-specific optimizations
- `/rust-bench` - Benchmark async performance
- `/test-harness` - Generate async tests
- `/rust-analyzer` - Analyze async antipatterns