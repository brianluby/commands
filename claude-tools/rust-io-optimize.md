---
version: 1.0.0
tags: [rust, io, performance, optimization, file-operations]
---

# Rust I/O Optimize

Optimize file I/O operations in Rust for maximum performance. Specializes in zero-copy techniques, platform-specific optimizations, and efficient buffer management.

## Usage
```
/rust-io-optimize [operation-type] [file-size-hint]
```

## Operation Types

### General Optimization
```
/rust-io-optimize                     # Analyze and optimize all I/O
/rust-io-optimize copy               # Optimize file copying
/rust-io-optimize read               # Optimize file reading
/rust-io-optimize write              # Optimize file writing
```

### Specific Scenarios
```
/rust-io-optimize streaming large    # Optimize for streaming large files
/rust-io-optimize random-access      # Optimize for random access patterns
/rust-io-optimize network           # Optimize for network file systems
```

## Pre-flight Checks

1. Analyze current I/O patterns
2. Check platform capabilities
3. Measure baseline performance
4. Identify bottlenecks

## Implementation

Given the context: $ARGUMENTS

### 1. Analyze Current I/O Implementation

```rust
// Common I/O patterns to identify:

// 1. Basic read/write (inefficient for large files)
let contents = std::fs::read(&path)?;
std::fs::write(&dest, contents)?;

// 2. Buffered I/O (better but not optimal)
let mut reader = BufReader::new(File::open(&path)?);
let mut writer = BufWriter::new(File::create(&dest)?);

// 3. Manual buffer management
let mut buffer = vec![0; 8192];
loop {
    let n = reader.read(&mut buffer)?;
    if n == 0 { break; }
    writer.write_all(&buffer[..n])?;
}
```

### 2. Platform-Specific Optimizations

#### Linux - Zero-Copy Operations
```rust
use std::os::unix::io::AsRawFd;

#[cfg(target_os = "linux")]
pub fn copy_file_range_linux(src: &File, dst: &File, len: usize) -> io::Result<usize> {
    use libc::{copy_file_range, off_t};
    
    let ret = unsafe {
        copy_file_range(
            src.as_raw_fd(),
            std::ptr::null_mut::<off_t>(),
            dst.as_raw_fd(),
            std::ptr::null_mut::<off_t>(),
            len,
            0
        )
    };
    
    if ret < 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(ret as usize)
    }
}

#[cfg(target_os = "linux")]
pub fn sendfile_copy(src: &File, dst: &File) -> io::Result<u64> {
    use libc::{sendfile, off_t};
    
    let src_fd = src.as_raw_fd();
    let dst_fd = dst.as_raw_fd();
    let len = src.metadata()?.len();
    
    let ret = unsafe {
        sendfile(dst_fd, src_fd, std::ptr::null_mut::<off_t>(), len as usize)
    };
    
    if ret < 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(ret as u64)
    }
}
```

#### macOS - F_NOCACHE and copyfile
```rust
#[cfg(target_os = "macos")]
pub fn copyfile_macos(src: &Path, dst: &Path) -> io::Result<()> {
    use libc::{copyfile, copyfile_state_t};
    use std::ffi::CString;
    
    let src_c = CString::new(src.as_os_str().as_bytes())?;
    let dst_c = CString::new(dst.as_os_str().as_bytes())?;
    
    let ret = unsafe {
        copyfile(
            src_c.as_ptr(),
            dst_c.as_ptr(),
            std::ptr::null_mut::<copyfile_state_t>(),
            libc::COPYFILE_ALL
        )
    };
    
    if ret < 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(())
    }
}

// Disable caching for large sequential reads
#[cfg(target_os = "macos")]
pub fn set_nocache(file: &File) -> io::Result<()> {
    use libc::{fcntl, F_NOCACHE, F_SETFL};
    
    let fd = file.as_raw_fd();
    let ret = unsafe { fcntl(fd, F_SETFL, F_NOCACHE) };
    
    if ret < 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(())
    }
}
```

#### Windows - CopyFileEx
```rust
#[cfg(target_os = "windows")]
pub fn copy_file_windows(src: &Path, dst: &Path) -> io::Result<()> {
    use std::os::windows::ffi::OsStrExt;
    use winapi::um::winbase::CopyFileExW;
    
    let src_wide: Vec<u16> = src.as_os_str().encode_wide().chain(Some(0)).collect();
    let dst_wide: Vec<u16> = dst.as_os_str().encode_wide().chain(Some(0)).collect();
    
    let ret = unsafe {
        CopyFileExW(
            src_wide.as_ptr(),
            dst_wide.as_ptr(),
            None,
            std::ptr::null_mut(),
            std::ptr::null_mut(),
            0
        )
    };
    
    if ret == 0 {
        Err(io::Error::last_os_error())
    } else {
        Ok(())
    }
}
```

### 3. Memory-Mapped I/O

```rust
use memmap2::{Mmap, MmapMut, MmapOptions};

pub fn mmap_copy(src_path: &Path, dst_path: &Path) -> io::Result<()> {
    let src_file = File::open(src_path)?;
    let src_meta = src_file.metadata()?;
    let src_len = src_meta.len() as usize;
    
    // Create destination file with correct size
    let dst_file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(true)
        .open(dst_path)?;
    dst_file.set_len(src_meta.len())?;
    
    // Memory map both files
    unsafe {
        let src_mmap = MmapOptions::new().map(&src_file)?;
        let mut dst_mmap = MmapOptions::new().map_mut(&dst_file)?;
        
        // Copy data
        dst_mmap.copy_from_slice(&src_mmap[..]);
        
        // Ensure data is flushed to disk
        dst_mmap.flush()?;
    }
    
    Ok(())
}

// For large files, use chunked mmap
pub fn mmap_copy_chunked(src_path: &Path, dst_path: &Path, chunk_size: usize) -> io::Result<()> {
    let src_file = File::open(src_path)?;
    let src_meta = src_file.metadata()?;
    let total_size = src_meta.len();
    
    let dst_file = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(true)
        .open(dst_path)?;
    dst_file.set_len(total_size)?;
    
    let mut offset = 0u64;
    while offset < total_size {
        let chunk_len = chunk_size.min((total_size - offset) as usize);
        
        unsafe {
            let src_mmap = MmapOptions::new()
                .offset(offset)
                .len(chunk_len)
                .map(&src_file)?;
                
            let mut dst_mmap = MmapOptions::new()
                .offset(offset)
                .len(chunk_len)
                .map_mut(&dst_file)?;
            
            dst_mmap.copy_from_slice(&src_mmap[..]);
            dst_mmap.flush()?;
        }
        
        offset += chunk_len as u64;
    }
    
    Ok(())
}
```

### 4. Adaptive Buffer Management

```rust
use std::sync::Arc;
use crossbeam::channel::{bounded, Sender, Receiver};

pub struct AdaptiveBuffer {
    min_size: usize,
    max_size: usize,
    current_size: AtomicUsize,
}

impl AdaptiveBuffer {
    pub fn new() -> Self {
        Self {
            min_size: 4 * 1024,        // 4KB
            max_size: 16 * 1024 * 1024, // 16MB
            current_size: AtomicUsize::new(64 * 1024), // Start with 64KB
        }
    }
    
    pub fn optimal_size(&self, file_size: u64, available_ram: u64) -> usize {
        let ideal_size = if file_size < 1024 * 1024 {
            // Small files: use 25% of file size
            (file_size / 4) as usize
        } else if file_size < 100 * 1024 * 1024 {
            // Medium files: use fixed percentage of RAM
            (available_ram / 1000) as usize
        } else {
            // Large files: use larger buffers
            (available_ram / 100) as usize
        };
        
        ideal_size.clamp(self.min_size, self.max_size)
    }
    
    pub fn adjust(&self, throughput: f64, target_throughput: f64) {
        let current = self.current_size.load(Ordering::Relaxed);
        let ratio = throughput / target_throughput;
        
        let new_size = if ratio < 0.8 {
            // Performance is low, increase buffer
            (current as f64 * 1.5) as usize
        } else if ratio > 1.2 {
            // Performance is good, can decrease buffer
            (current as f64 * 0.9) as usize
        } else {
            current
        };
        
        let clamped = new_size.clamp(self.min_size, self.max_size);
        self.current_size.store(clamped, Ordering::Relaxed);
    }
}
```

### 5. Parallel I/O Operations

```rust
use rayon::prelude::*;

pub fn parallel_copy(src: &Path, dst: &Path, num_threads: usize) -> io::Result<()> {
    let file_size = src.metadata()?.len();
    let chunk_size = file_size / num_threads as u64;
    
    // Pre-create destination file
    let dst_file = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .open(dst)?;
    dst_file.set_len(file_size)?;
    drop(dst_file);
    
    // Parallel copy chunks
    (0..num_threads).into_par_iter().try_for_each(|i| {
        let start = i as u64 * chunk_size;
        let end = if i == num_threads - 1 {
            file_size
        } else {
            (i + 1) as u64 * chunk_size
        };
        
        copy_range(src, dst, start, end - start)
    })?;
    
    Ok(())
}

fn copy_range(src: &Path, dst: &Path, offset: u64, length: u64) -> io::Result<()> {
    let mut src_file = File::open(src)?;
    src_file.seek(SeekFrom::Start(offset))?;
    
    let mut dst_file = OpenOptions::new()
        .write(true)
        .open(dst)?;
    dst_file.seek(SeekFrom::Start(offset))?;
    
    let mut buffer = vec![0u8; 1024 * 1024]; // 1MB buffer
    let mut remaining = length;
    
    while remaining > 0 {
        let to_read = buffer.len().min(remaining as usize);
        let n = src_file.read(&mut buffer[..to_read])?;
        if n == 0 {
            break;
        }
        dst_file.write_all(&buffer[..n])?;
        remaining -= n as u64;
    }
    
    Ok(())
}
```

### 6. Direct I/O for Large Files

```rust
#[cfg(target_os = "linux")]
pub fn direct_io_copy(src: &Path, dst: &Path) -> io::Result<()> {
    use std::os::unix::fs::OpenOptionsExt;
    use libc::O_DIRECT;
    
    // Aligned buffer for O_DIRECT
    const ALIGN: usize = 4096;
    const BUFFER_SIZE: usize = 1024 * 1024; // 1MB
    
    let layout = Layout::from_size_align(BUFFER_SIZE, ALIGN).unwrap();
    let buffer = unsafe {
        let ptr = alloc::alloc(layout);
        std::slice::from_raw_parts_mut(ptr, BUFFER_SIZE)
    };
    
    let src_file = OpenOptions::new()
        .read(true)
        .custom_flags(O_DIRECT)
        .open(src)?;
        
    let mut dst_file = OpenOptions::new()
        .write(true)
        .create(true)
        .truncate(true)
        .custom_flags(O_DIRECT)
        .open(dst)?;
    
    loop {
        let n = src_file.read(buffer)?;
        if n == 0 {
            break;
        }
        
        // O_DIRECT requires aligned writes
        let aligned_n = (n + ALIGN - 1) / ALIGN * ALIGN;
        dst_file.write_all(&buffer[..aligned_n])?;
    }
    
    // Truncate to correct size
    dst_file.set_len(src.metadata()?.len())?;
    
    unsafe {
        alloc::dealloc(buffer.as_mut_ptr(), layout);
    }
    
    Ok(())
}
```

### 7. Optimize for Specific Patterns

#### Sequential Read Optimization
```rust
pub fn optimize_sequential_read(file: &File) -> io::Result<()> {
    #[cfg(unix)]
    {
        use libc::{posix_fadvise, POSIX_FADV_SEQUENTIAL, POSIX_FADV_WILLNEED};
        use std::os::unix::io::AsRawFd;
        
        let fd = file.as_raw_fd();
        let len = file.metadata()?.len() as i64;
        
        unsafe {
            // Advise kernel about access pattern
            posix_fadvise(fd, 0, len, POSIX_FADV_SEQUENTIAL);
            posix_fadvise(fd, 0, len, POSIX_FADV_WILLNEED);
        }
    }
    
    Ok(())
}
```

#### Random Access Optimization
```rust
pub struct CachedRandomAccess {
    file: File,
    cache: LruCache<u64, Vec<u8>>,
    block_size: usize,
}

impl CachedRandomAccess {
    pub fn new(file: File, cache_blocks: usize) -> Self {
        Self {
            file,
            cache: LruCache::new(cache_blocks),
            block_size: 4096,
        }
    }
    
    pub fn read_at(&mut self, offset: u64, buf: &mut [u8]) -> io::Result<usize> {
        let block_idx = offset / self.block_size as u64;
        
        if let Some(block) = self.cache.get(&block_idx) {
            let block_offset = (offset % self.block_size as u64) as usize;
            let available = self.block_size - block_offset;
            let to_copy = buf.len().min(available);
            buf[..to_copy].copy_from_slice(&block[block_offset..block_offset + to_copy]);
            return Ok(to_copy);
        }
        
        // Cache miss - read full block
        let mut block = vec![0u8; self.block_size];
        self.file.seek(SeekFrom::Start(block_idx * self.block_size as u64))?;
        self.file.read_exact(&mut block)?;
        
        let block_offset = (offset % self.block_size as u64) as usize;
        let available = self.block_size - block_offset;
        let to_copy = buf.len().min(available);
        buf[..to_copy].copy_from_slice(&block[block_offset..block_offset + to_copy]);
        
        self.cache.put(block_idx, block);
        Ok(to_copy)
    }
}
```

### 8. Progress Reporting

```rust
use indicatif::{ProgressBar, ProgressStyle};

pub struct ProgressReader<R> {
    inner: R,
    progress: ProgressBar,
    bytes_read: u64,
}

impl<R: Read> Read for ProgressReader<R> {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = self.inner.read(buf)?;
        self.bytes_read += n as u64;
        self.progress.set_position(self.bytes_read);
        Ok(n)
    }
}

pub fn copy_with_progress(src: &Path, dst: &Path) -> io::Result<()> {
    let src_file = File::open(src)?;
    let file_size = src_file.metadata()?.len();
    
    let pb = ProgressBar::new(file_size);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{bar:40.cyan/blue}] {bytes}/{total_bytes} ({eta})")
            .progress_chars("#>-")
    );
    
    let mut reader = ProgressReader {
        inner: BufReader::with_capacity(1024 * 1024, src_file),
        progress: pb,
        bytes_read: 0,
    };
    
    let mut writer = BufWriter::with_capacity(1024 * 1024, File::create(dst)?);
    io::copy(&mut reader, &mut writer)?;
    
    reader.progress.finish_with_message("Copy complete");
    Ok(())
}
```

### 9. Generate Optimization Report

```markdown
# I/O Optimization Report

## Performance Summary
- **Baseline**: 145 MB/s
- **Optimized**: 2.3 GB/s  
- **Improvement**: 15.8x faster

## Optimizations Applied

### 1. Platform-Specific Zero-Copy
- Linux: `copy_file_range()` syscall
- macOS: `copyfile()` with F_NOCACHE
- Windows: `CopyFileExW()` API
- **Impact**: 10x improvement for large files

### 2. Memory-Mapped I/O
- Used for files 10MB-2GB
- Chunked mmap for files >2GB
- **Impact**: 3x improvement

### 3. Adaptive Buffering
- Dynamic buffer sizing based on throughput
- Buffer pool to reduce allocations
- **Impact**: 25% improvement

### 4. Direct I/O
- Bypass page cache for very large files
- Aligned buffers for O_DIRECT
- **Impact**: 50% improvement for >1GB files

## Code Changes

```rust
// Before
std::fs::copy(src, dst)?;

// After
match file_size {
    0..=1_048_576 => buffered_copy(src, dst),
    1_048_577..=104_857_600 => mmap_copy(src, dst),
    _ => platform_optimal_copy(src, dst),
}
```

## Benchmark Results

| File Size | Method | Time | Throughput |
|-----------|--------|------|------------|
| 1 KB | std::fs::copy | 0.1ms | 10 MB/s |
| 1 KB | optimized | 0.05ms | 20 MB/s |
| 1 MB | std::fs::copy | 7ms | 143 MB/s |
| 1 MB | mmap | 2ms | 500 MB/s |
| 100 MB | std::fs::copy | 690ms | 145 MB/s |
| 100 MB | zero-copy | 43ms | 2.3 GB/s |
| 1 GB | std::fs::copy | 7s | 146 MB/s |
| 1 GB | direct I/O | 425ms | 2.4 GB/s |

## Recommendations

1. Use platform-specific APIs when available
2. Implement fallback chain for compatibility
3. Add runtime feature detection
4. Consider async I/O for concurrent operations
5. Profile on target hardware
```

## Error Handling

If optimization fails:
```
❌ I/O optimization error: [specific issue]

Fallback strategy:
- Using standard library implementation
- Performance may be reduced
- Consider manual buffer tuning

Debug with:
strace -e trace=read,write,sendfile cargo run
```

## Related Commands

- `/rust-bench` - Benchmark I/O performance
- `/rust-async` - Async I/O patterns
- `/test-harness` - Generate I/O test cases
- `/rust-analyzer` - Identify I/O bottlenecks