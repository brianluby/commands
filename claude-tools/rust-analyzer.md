---
version: 1.0.0
tags: [rust, analysis, refactoring, optimization]
---

# Rust Analyzer

Comprehensive static analysis and refactoring tool for Rust codebases. Provides deep insights into code quality, performance opportunities, and safety improvements.

## Usage
```
/rust-analyzer [analysis-type] [options]
```

## Analysis Types

### Full Analysis (default)
```
/rust-analyzer
/rust-analyzer full
```

### Specific Analysis
```
/rust-analyzer lifetimes      # Lifetime analysis
/rust-analyzer traits         # Trait implementation review
/rust-analyzer unsafe         # Unsafe code audit
/rust-analyzer performance    # Performance opportunities
/rust-analyzer idioms         # Rust idiom compliance
/rust-analyzer dead-code      # Dead code detection
```

## Pre-flight Checks

Before analyzing, I'll verify:
1. Valid Rust project (Cargo.toml exists)
2. rust-analyzer LSP available
3. Project compiles successfully
4. Clippy and rustfmt installed

## Process

Given the context: $ARGUMENTS

### 1. Project Structure Analysis

```bash
# Analyze workspace structure
find . -name "Cargo.toml" -type f | head -20

# Check for workspace
if [ -f "Cargo.toml" ]; then
    grep -q "\[workspace\]" Cargo.toml && echo "Workspace detected"
fi

# Module structure
find . -name "*.rs" -type f | grep -E "(mod|lib|main)\.rs" | sort
```

### 2. Compilation and Basic Checks

```bash
# Ensure project builds
cargo check --all-targets

# Run clippy with strict lints
cargo clippy -- -W clippy::all \
    -W clippy::pedantic \
    -W clippy::nursery \
    -W clippy::cargo \
    -D warnings

# Format check
cargo fmt -- --check
```

### 3. Lifetime Analysis

Analyzing lifetime patterns and suggesting improvements:

```rust
// Common lifetime issues to check:

// 1. Unnecessary lifetime annotations
fn process<'a>(data: &'a str) -> &'a str  // Can be simplified

// 2. Missing lifetime elision
impl<'a> Iterator for MyIter<'a>  // Check if 'a is needed

// 3. Complex lifetime relationships
struct Container<'a, 'b: 'a> {
    // Analyze if constraint is necessary
}

// 4. Lifetime inference opportunities
fn combine<'a, 'b>(x: &'a str, y: &'b str) -> String
// Could use '_ or elide entirely
```

### 4. Trait Implementation Analysis

```rust
// Check for:

// 1. Missing common trait implementations
#[derive(Debug, Clone)]  // Should also implement PartialEq, Eq?

// 2. Manual implementations that could be derived
impl Clone for MyStruct { /* ... */ }  // Could use #[derive(Clone)]?

// 3. Trait coherence and orphan rules
impl ForeignTrait for LocalType  // Allowed
impl LocalTrait for ForeignType  // Allowed
impl ForeignTrait for ForeignType  // Not allowed!

// 4. Associated types vs generics
trait Container<T> vs trait Container { type Item; }
```

### 5. Unsafe Code Audit

```bash
# Find all unsafe blocks
rg "unsafe\s*\{" --type rust -A 5 -B 2

# Check for common unsafe patterns
rg "std::mem::(transmute|zeroed|uninitialized)" --type rust
rg "std::ptr::(read|write|copy)" --type rust
```

Safety checklist:
- [ ] All unsafe blocks have safety comments
- [ ] No unnecessary unsafe usage
- [ ] Proper invariant documentation
- [ ] Sound FFI boundaries
- [ ] No data races possible

### 6. Performance Optimization Opportunities

```rust
// Analyze for:

// 1. Unnecessary allocations
vec![1, 2, 3].iter()  // Use array: [1, 2, 3].iter()

// 2. Clone vs reference
data.clone().process()  // Can use &data?

// 3. Iterator chain optimization
collection.iter().map(f).collect::<Vec<_>>().iter()
// Simplify to: collection.iter().map(f)

// 4. String handling
format!("{}", simple_string)  // Use .to_string()
String::from("literal")  // Use "literal".to_string()

// 5. Collection capacity
let mut vec = Vec::new();  // Use Vec::with_capacity() if size known
```

### 7. Rust Idiom Compliance

```rust
// Check for non-idiomatic patterns:

// 1. Match vs if-let
match option {
    Some(x) => process(x),
    None => {}
}
// Better: if let Some(x) = option { process(x) }

// 2. Result/Option handling
if result.is_ok() {
    result.unwrap()  // Use match or if-let
}

// 3. Loop patterns
for i in 0..vec.len() {  // Use: for item in &vec
    process(&vec[i])
}

// 4. Error propagation
match fallible() {
    Ok(v) => Ok(v),  // Use: fallible()?
    Err(e) => Err(e)
}
```

### 8. Dead Code Detection

```bash
# Find potentially dead code
cargo +nightly rustc -- -Z print-type-sizes
cargo tree --duplicates
cargo udeps --all-targets
```

### 9. Advanced Analysis

#### Memory Layout Optimization
```rust
// Before:
struct Inefficient {
    a: u8,
    b: u64,
    c: u8,
}  // Size: 24 bytes (padding)

// After:
struct Efficient {
    b: u64,
    a: u8,
    c: u8,
}  // Size: 16 bytes (better alignment)
```

#### Generic Bounds Optimization
```rust
// Overly restrictive:
fn process<T: Clone + Debug + Send + Sync>(data: T)

// Better (if only needed for one operation):
fn process<T>(data: T) where T: Debug {
    println!("{:?}", data);
}
```

### 10. Generate Report

```markdown
# Rust Analysis Report

## Summary
- **Code Quality Score**: A- (87/100)
- **Safety Score**: B+ (No critical unsafe usage)
- **Performance Score**: B (Some optimization opportunities)
- **Idiom Compliance**: A (Mostly idiomatic)

## Critical Issues
[List any critical findings]

## Recommendations

### High Priority
1. [Specific issue with code example and fix]

### Medium Priority
1. [Optimization opportunity]

### Low Priority
1. [Style/idiom improvements]

## Metrics
- Lines of Code: X
- Unsafe blocks: Y
- Test coverage: Z%
- Dependencies: N direct, M total
```

## Integration with CI/CD

```yaml
# .github/workflows/rust-analysis.yml
name: Rust Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      
      - name: Run analysis
        run: |
          cargo clippy --all-targets --all-features -- -D warnings
          cargo fmt --all -- --check
          
      - name: Security audit
        run: |
          cargo install cargo-audit
          cargo audit
```

## Error Handling

If analysis fails:
```
❌ Analysis error: [specific issue]

Possible causes:
- Project doesn't compile
- Missing dependencies
- Syntax errors

Quick fixes:
1. Run: cargo check
2. Update dependencies: cargo update
3. Clean build: cargo clean && cargo build
```

## Related Commands

- `/rust-bench` - Performance benchmarking
- `/rust-unsafe-audit` - Deep unsafe code analysis
- `/security-scan` - Security vulnerability scanning
- `/test-harness` - Generate comprehensive tests