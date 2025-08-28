---
version: 1.0.0
tags: [rust, performance, benchmarking, profiling]
---

# Rust Bench

Comprehensive performance benchmarking and profiling suite for Rust applications. Sets up criterion benchmarks, analyzes performance bottlenecks, and tracks regressions.

## Usage
```
/rust-bench [benchmark-type] [options]
```

## Benchmark Types

### Quick Benchmark
```
/rust-bench                    # Run existing benchmarks
/rust-bench quick             # Quick performance check
```

### Comprehensive Analysis
```
/rust-bench full              # Full benchmark suite with profiling
/rust-bench compare [commit]  # Compare against baseline
/rust-bench profile           # CPU and memory profiling
/rust-bench flame            # Generate flamegraphs
```

## Pre-flight Checks

1. Check for existing benchmarks
2. Verify criterion or built-in bench
3. Ensure release profile configured
4. Check for profiling tools availability

## Implementation

Given the context: $ARGUMENTS

### 1. Setup Benchmarking Infrastructure

First, check and setup benchmark dependencies:

```toml
# Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }
proptest = "1.0"  # For property-based benchmark inputs

[profile.release]
debug = true  # Enable debug symbols for profiling
lto = "fat"   # Link-time optimization
codegen-units = 1  # Single codegen unit for consistency

[profile.bench]
inherits = "release"
```

### 2. Generate Benchmark Template

For components without benchmarks:

```rust
// benches/[component]_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use your_crate::{Component, Input};

fn benchmark_component(c: &mut Criterion) {
    let mut group = c.benchmark_group("component_operations");
    
    // Benchmark different input sizes
    for size in [100, 1_000, 10_000, 100_000].iter() {
        group.bench_with_input(
            BenchmarkId::new("process", size), 
            size, 
            |b, &size| {
                let input = generate_input(size);
                b.iter(|| {
                    Component::process(black_box(&input))
                });
            }
        );
    }
    
    // Benchmark different scenarios
    group.bench_function("worst_case", |b| {
        let input = generate_worst_case();
        b.iter(|| Component::process(black_box(&input)));
    });
    
    group.bench_function("best_case", |b| {
        let input = generate_best_case();
        b.iter(|| Component::process(black_box(&input)));
    });
    
    group.finish();
}

// Memory allocation benchmark
fn benchmark_memory(c: &mut Criterion) {
    c.bench_function("allocation_pattern", |b| {
        b.iter(|| {
            let mut vec = Vec::with_capacity(1000);
            for i in 0..1000 {
                vec.push(black_box(i));
            }
            vec
        });
    });
}

criterion_group!(benches, benchmark_component, benchmark_memory);
criterion_main!(benches);
```

### 3. Run Benchmarks

```bash
# Run all benchmarks
cargo bench

# Run specific benchmark
cargo bench component_operations

# Save baseline
cargo bench -- --save-baseline main

# Compare against baseline
cargo bench -- --baseline main

# Generate HTML report
cargo bench -- --plotting-backend gnuplot
```

### 4. CPU Profiling

```bash
# Install profiling tools
cargo install flamegraph
cargo install cargo-profiler

# Generate flamegraph
cargo flamegraph --bench component_benchmark

# Use perf (Linux)
cargo bench --no-run
perf record --call-graph=dwarf target/release/deps/benchmark-*
perf report

# Use Instruments (macOS)
cargo instruments -t "Time Profiler" --bench component_benchmark
```

### 5. Memory Profiling

```bash
# Using valgrind (Linux)
cargo bench --no-run
valgrind --tool=massif --massif-out-file=massif.out \
    target/release/deps/benchmark-*
ms_print massif.out

# Using heaptrack
heaptrack target/release/deps/benchmark-*
heaptrack --analyze heaptrack.benchmark.*.gz

# Memory allocation tracking
DHAT_HEAP=1 cargo bench
```

### 6. Advanced Benchmarking Patterns

#### Throughput Benchmarking
```rust
fn benchmark_throughput(c: &mut Criterion) {
    let mut group = c.benchmark_group("throughput");
    group.throughput(criterion::Throughput::Bytes(1_000_000));
    
    group.bench_function("process_mb", |b| {
        let data = vec![0u8; 1_000_000];
        b.iter(|| process_data(black_box(&data)));
    });
}
```

#### Concurrent Performance
```rust
use std::sync::Arc;
use std::thread;

fn benchmark_concurrency(c: &mut Criterion) {
    let mut group = c.benchmark_group("concurrency");
    
    for num_threads in [1, 2, 4, 8, 16].iter() {
        group.bench_with_input(
            BenchmarkId::new("parallel", num_threads),
            num_threads,
            |b, &num_threads| {
                let data = Arc::new(generate_data());
                b.iter(|| {
                    let handles: Vec<_> = (0..num_threads)
                        .map(|_| {
                            let data = Arc::clone(&data);
                            thread::spawn(move || {
                                process_parallel(black_box(&data))
                            })
                        })
                        .collect();
                    
                    for handle in handles {
                        handle.join().unwrap();
                    }
                });
            }
        );
    }
}
```

### 7. I/O Performance (for rustcopy)

```rust
// Specific benchmarks for file operations
fn benchmark_file_copy(c: &mut Criterion) {
    let mut group = c.benchmark_group("file_operations");
    
    // Different file sizes
    for size in [1_024, 1_048_576, 104_857_600].iter() {
        group.bench_with_input(
            BenchmarkId::new("copy_size", format_bytes(*size)),
            size,
            |b, &size| {
                let src = create_temp_file(size);
                let dst = temp_path();
                
                b.iter(|| {
                    std::fs::copy(black_box(&src), black_box(&dst)).unwrap();
                    std::fs::remove_file(&dst).unwrap();
                });
                
                cleanup_temp_file(src);
            }
        );
    }
    
    // Different copy strategies
    group.bench_function("std_copy", |b| {
        let (src, dst) = setup_files();
        b.iter(|| std_copy(black_box(&src), black_box(&dst)));
    });
    
    group.bench_function("mmap_copy", |b| {
        let (src, dst) = setup_files();
        b.iter(|| mmap_copy(black_box(&src), black_box(&dst)));
    });
    
    group.bench_function("sendfile_copy", |b| {
        let (src, dst) = setup_files();
        b.iter(|| sendfile_copy(black_box(&src), black_box(&dst)));
    });
}
```

### 8. Performance Regression Detection

```bash
# CI/CD Integration
cargo bench -- --save-baseline pr-$PR_NUMBER

# Compare against main
cargo bench -- --baseline main --load-baseline pr-$PR_NUMBER

# Generate comparison report
critcmp main pr-$PR_NUMBER
```

### 9. Generate Performance Report

```markdown
# Performance Benchmark Report

## Executive Summary
- **Overall Performance**: ✅ No regressions detected
- **Best Performer**: mmap_copy (47% faster than baseline)
- **Memory Usage**: Stable (peak: 127MB)

## Benchmark Results

### File Operations
| Operation | Time (main) | Time (current) | Change | Status |
|-----------|-------------|----------------|--------|--------|
| copy_1KB  | 1.2µs ± 0.1 | 1.1µs ± 0.1   | -8.3%  | ✅     |
| copy_1MB  | 423µs ± 12  | 398µs ± 10    | -5.9%  | ✅     |
| copy_100MB| 41ms ± 2.1  | 38ms ± 1.8    | -7.3%  | ✅     |

### Memory Allocation
| Pattern          | Allocations | Peak Memory | Change |
|------------------|-------------|-------------|--------|
| Vec growth       | 12          | 4KB         | 0%     |
| Buffer pool      | 1           | 64KB        | -25%   |
| String building  | 234         | 18KB        | +2%    |

## Flamegraph Analysis
[Include flamegraph image or link]

Key hotspots:
1. `memcpy` - 34% of CPU time
2. `syscall::read` - 21% of CPU time
3. `allocator::alloc` - 8% of CPU time

## Recommendations

### High Impact
1. Implement zero-copy for large files
2. Use `copy_file_range` syscall on Linux
3. Pre-allocate buffers for known sizes

### Medium Impact
1. Align buffer sizes to page boundaries
2. Use SIMD for checksum calculation
3. Implement adaptive buffer sizing

### Low Impact
1. Remove unnecessary error checking in hot path
2. Inline small functions
3. Reduce string allocations
```

## Optimization Workflow

After benchmarking, apply optimizations:

```rust
// Before optimization
fn copy_file(src: &Path, dst: &Path) -> Result<()> {
    let content = std::fs::read(src)?;
    std::fs::write(dst, content)?;
    Ok(())
}

// After optimization
fn copy_file_optimized(src: &Path, dst: &Path) -> Result<()> {
    use std::io::{BufReader, BufWriter};
    
    let src_file = File::open(src)?;
    let dst_file = File::create(dst)?;
    
    let mut reader = BufReader::with_capacity(64 * 1024, src_file);
    let mut writer = BufWriter::with_capacity(64 * 1024, dst_file);
    
    std::io::copy(&mut reader, &mut writer)?;
    Ok(())
}
```

## Related Commands

- `/rust-analyzer` - Code analysis and optimization suggestions
- `/rust-profile` - Deep profiling analysis
- `/rust-io-optimize` - I/O specific optimizations
- `/test-harness` - Generate performance tests