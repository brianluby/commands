---
version: 1.0.0
tags: [rust, fuzzing, testing, security]
---

# Rust Fuzz

Set up and run comprehensive fuzzing infrastructure for Rust projects. Finds edge cases, crashes, and security vulnerabilities through automated testing.

## Usage
```
/rust-fuzz [target] [fuzzer-type]
```

## Fuzzer Types

### Quick Start
```
/rust-fuzz                     # Auto-detect and set up fuzzing
/rust-fuzz my_function cargo   # Fuzz specific function with cargo-fuzz
```

### Advanced Fuzzing
```
/rust-fuzz all afl            # Use AFL++ for all targets
/rust-fuzz parser libfuzzer   # Use libFuzzer for parser
/rust-fuzz network honggfuzz  # Use Honggfuzz for network code
```

## Pre-flight Checks

1. Check Rust nightly availability
2. Verify fuzzing tools installed
3. Ensure sanitizers available
4. Check for existing fuzz targets

## Implementation

Given the context: $ARGUMENTS

### 1. Setup Fuzzing Infrastructure

```bash
# Install fuzzing tools
cargo install cargo-fuzz
cargo install afl cargo-afl
cargo install honggfuzz

# Initialize fuzz directory
cargo fuzz init

# Project structure
mkdir -p fuzz/corpus/{initial,crashes,hangs}
```

### 2. Analyze Code for Fuzz Targets

```rust
// Identify good fuzzing candidates:
// 1. Functions that parse input
// 2. Functions with complex logic
// 3. Unsafe code blocks
// 4. Network/file I/O handlers
// 5. Serialization/deserialization

// Example targets for rustcopy:
pub fn parse_path(input: &[u8]) -> Result<PathBuf, Error>
pub fn copy_with_options(src: &[u8], dst: &[u8], opts: &[u8]) -> Result<(), Error>
pub fn validate_permissions(path: &[u8]) -> Result<(), Error>
```

### 3. Generate Fuzz Targets

#### Cargo-fuzz (LibFuzzer) Target
```rust
// fuzz/fuzz_targets/parse_path.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use rustcopy::parse_path;

fuzz_target!(|data: &[u8]| {
    // Fuzz the parse_path function
    let _ = parse_path(data);
});
```

#### Property-based Fuzzing
```rust
// fuzz/fuzz_targets/copy_properties.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use arbitrary::{Arbitrary, Unstructured};

#[derive(Arbitrary, Debug)]
struct CopyInput {
    src_path: String,
    dst_path: String,
    buffer_size: usize,
    follow_symlinks: bool,
}

fuzz_target!(|data: &[u8]| {
    if let Ok(mut u) = Unstructured::new(data) {
        if let Ok(input) = CopyInput::arbitrary(&mut u) {
            // Property: copy should preserve file contents
            test_copy_preserves_content(input);
            
            // Property: copy should handle errors gracefully
            test_copy_error_handling(input);
        }
    }
});
```

#### AFL++ Target
```rust
// fuzz/afl_targets/main.rs
use afl::fuzz;
use rustcopy::{parse_path, copy_file};

fn main() {
    fuzz!(|data: &[u8]| {
        // Split input for multiple parameters
        if data.len() > 2 {
            let mid = data.len() / 2;
            let src = &data[..mid];
            let dst = &data[mid..];
            
            // Test parsing
            if let Ok(src_path) = parse_path(src) {
                if let Ok(dst_path) = parse_path(dst) {
                    // Don't actually copy files during fuzzing
                    // Just validate the logic
                    let _ = validate_copy(&src_path, &dst_path);
                }
            }
        }
    });
}
```

### 4. Corpus Generation

```rust
// tools/generate_corpus.rs
use std::fs;
use std::path::Path;

fn generate_initial_corpus() {
    let corpus_dir = Path::new("fuzz/corpus/initial");
    fs::create_dir_all(corpus_dir).unwrap();
    
    // Valid inputs
    save_input(corpus_dir, "valid_path", b"/home/user/file.txt");
    save_input(corpus_dir, "relative_path", b"../file.txt");
    save_input(corpus_dir, "unicode_path", "文件.txt".as_bytes());
    
    // Edge cases
    save_input(corpus_dir, "empty", b"");
    save_input(corpus_dir, "null_bytes", b"file\0.txt");
    save_input(corpus_dir, "long_path", &[b'a'; 4096]);
    
    // Invalid inputs
    save_input(corpus_dir, "invalid_utf8", &[0xFF, 0xFE, 0xFD]);
    
    // Special paths
    save_input(corpus_dir, "dots", b"...");
    save_input(corpus_dir, "root", b"/");
    save_input(corpus_dir, "device", b"/dev/null");
}
```

### 5. Run Fuzzing Campaigns

```bash
# Cargo-fuzz with sanitizers
RUSTFLAGS="-Zsanitizer=address" \
    cargo +nightly fuzz run parse_path -- \
    -max_len=4096 \
    -timeout=30 \
    -dict=fuzz/dictionary.txt

# AFL++ with persistent mode
cargo afl build --release
AFL_SKIP_CPUFREQ=1 AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1 \
    cargo afl fuzz -i fuzz/corpus/initial -o fuzz/output \
    target/release/afl_target

# Honggfuzz with threading
cargo hfuzz run network_fuzz -- \
    --threads 8 \
    --timeout 30 \
    --max_file_size 1048576
```

### 6. Structured Fuzzing

```rust
// For complex inputs, use structured fuzzing
#[derive(Arbitrary, Debug)]
struct FileOperation {
    op_type: OperationType,
    source: PathInput,
    destination: Option<PathInput>,
    options: CopyOptions,
}

#[derive(Arbitrary, Debug)]
enum OperationType {
    Copy,
    Move,
    Link,
    Remove,
}

#[derive(Arbitrary, Debug)]
struct PathInput {
    components: Vec<PathComponent>,
}

#[derive(Arbitrary, Debug)]
enum PathComponent {
    Normal(String),
    Parent,
    Current,
    Root,
}

// Implement custom generation logic
impl PathInput {
    fn to_path(&self) -> PathBuf {
        let mut path = PathBuf::new();
        for component in &self.components {
            match component {
                PathComponent::Normal(s) => path.push(s),
                PathComponent::Parent => path.push(".."),
                PathComponent::Current => path.push("."),
                PathComponent::Root => path = PathBuf::from("/"),
            }
        }
        path
    }
}
```

### 7. Crash Analysis

```bash
# Minimize crash input
cargo fuzz tmin parse_path fuzz/artifacts/parse_path/crash-*

# Get detailed crash info
RUST_BACKTRACE=1 cargo fuzz run parse_path \
    fuzz/artifacts/parse_path/crash-* \
    -- -runs=1

# Analyze with debugger
rust-lldb target/x86_64-*/release/parse_path \
    -o "run < fuzz/artifacts/parse_path/crash-*"
```

### 8. Coverage Analysis

```bash
# Generate coverage report
cargo fuzz coverage parse_path
cargo cov -- show target/x86_64-*/release/parse_path \
    -instr-profile=fuzz/coverage/parse_path/coverage.profdata \
    > coverage_report.txt

# Visual coverage with grcov
grcov . --binary-path ./target/x86_64-*/release/ \
    -s . -t html --branch --ignore-not-existing \
    -o ./coverage/
```

### 9. Continuous Fuzzing

```yaml
# .github/workflows/fuzz.yml
name: Continuous Fuzzing
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  fuzz:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        target: [parse_path, copy_file, permissions]
        
    steps:
      - uses: actions/checkout@v3
      - uses: dtolnay/rust-toolchain@nightly
      
      - name: Install cargo-fuzz
        run: cargo install cargo-fuzz
        
      - name: Fuzz ${{ matrix.target }}
        run: |
          timeout 3600 cargo fuzz run ${{ matrix.target }} || true
          
      - name: Check for crashes
        run: |
          if [ -d fuzz/artifacts/${{ matrix.target }} ]; then
            echo "::error::Fuzzing found crashes"
            exit 1
          fi
```

### 10. Generate Fuzzing Report

```markdown
# Fuzzing Report

## Summary
- **Total Executions**: 12,847,392
- **Unique Paths**: 3,421
- **Crashes Found**: 2
- **Hangs Found**: 0
- **Coverage**: 87.3%

## Crashes Found

### Crash 1: Integer Overflow
- **Target**: buffer_size_calculation
- **Input**: [minimized to 12 bytes]
- **Impact**: Panic in release mode
- **Fix**: Use checked arithmetic

### Crash 2: Path Traversal
- **Target**: parse_path  
- **Input**: "../../../../etc/passwd"
- **Impact**: Security vulnerability
- **Fix**: Canonicalize and validate paths

## Coverage Gaps

Uncovered code sections:
1. Error handling for ENOSPC
2. Symbolic link cycle detection
3. Extended attributes copying

## Performance Metrics

| Fuzzer | Exec/sec | Coverage | Time to First Crash |
|--------|----------|----------|---------------------|
| LibFuzzer | 15,234 | 87.3% | 4m 23s |
| AFL++ | 8,421 | 84.1% | 12m 51s |
| Honggfuzz | 12,873 | 86.2% | 7m 14s |

## Recommendations

1. Add dictionary with file system terms
2. Implement custom mutators for path strings  
3. Increase corpus with real-world paths
4. Add assertion-based invariant checking
```

## Error Handling

If fuzzing setup fails:
```
❌ Fuzzing setup failed: [error]

Common issues:
- Rust nightly required: rustup default nightly
- Missing fuzzer: cargo install cargo-fuzz
- No fuzz targets: cargo fuzz init

Quick fix:
rustup default nightly
cargo install cargo-fuzz
cargo fuzz init
```

## Related Commands

- `/rust-analyzer` - Identify code to fuzz
- `/security-scan` - Security vulnerability analysis
- `/test-harness` - Generate test cases from fuzz inputs
- `/rust-unsafe-audit` - Audit unsafe code for fuzzing priority