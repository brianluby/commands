---
version: 1.0.0
tags: [rust, unsafe, security, audit, memory-safety]
---

# Rust Unsafe Audit

Comprehensive audit tool for unsafe Rust code. Identifies risks, validates safety invariants, and ensures sound unsafe usage.

## Usage
```
/rust-unsafe-audit [audit-level] [report-format]
```

## Audit Levels

### Quick Scan
```
/rust-unsafe-audit              # Basic unsafe usage scan
/rust-unsafe-audit quick        # Quick safety check
```

### Comprehensive Audit
```
/rust-unsafe-audit full         # Deep analysis with Miri
/rust-unsafe-audit strict       # Strictest checks, flag all concerns
/rust-unsafe-audit ffi          # Focus on FFI boundaries
```

## Pre-flight Checks

1. Locate all unsafe blocks
2. Check for safety documentation
3. Identify unsafe traits/functions
4. Verify project compiles

## Implementation

Given the context: $ARGUMENTS

### 1. Unsafe Code Discovery

```bash
# Find all unsafe blocks and functions
echo "🔍 Scanning for unsafe code..."

# Count unsafe occurrences
UNSAFE_BLOCKS=$(rg "unsafe\s*\{" --type rust -c | awk -F: '{sum += $2} END {print sum}')
UNSAFE_FNS=$(rg "unsafe\s+fn" --type rust -c | awk -F: '{sum += $2} END {print sum}')
UNSAFE_TRAITS=$(rg "unsafe\s+trait" --type rust -c | awk -F: '{sum += $2} END {print sum}')
UNSAFE_IMPLS=$(rg "unsafe\s+impl" --type rust -c | awk -F: '{sum += $2} END {print sum}')

echo "Found:"
echo "  - Unsafe blocks: $UNSAFE_BLOCKS"
echo "  - Unsafe functions: $UNSAFE_FNS"
echo "  - Unsafe traits: $UNSAFE_TRAITS"
echo "  - Unsafe impl blocks: $UNSAFE_IMPLS"
```

### 2. Safety Documentation Check

```rust
// Tool to analyze safety comments
use regex::Regex;
use std::collections::HashMap;

pub struct SafetyCommentAnalyzer {
    safety_pattern: Regex,
    invariant_pattern: Regex,
}

impl SafetyCommentAnalyzer {
    pub fn new() -> Self {
        Self {
            safety_pattern: Regex::new(r"(?i)(safety|safe):\s*(.+)").unwrap(),
            invariant_pattern: Regex::new(r"(?i)(invariant|guarantee):\s*(.+)").unwrap(),
        }
    }
    
    pub fn analyze_file(path: &Path) -> SafetyReport {
        let content = std::fs::read_to_string(path).unwrap();
        let lines: Vec<&str> = content.lines().collect();
        
        let mut unsafe_blocks = Vec::new();
        let mut current_unsafe = None;
        
        for (idx, line) in lines.iter().enumerate() {
            if line.contains("unsafe") && line.contains("{") {
                current_unsafe = Some(UnsafeBlock {
                    start_line: idx + 1,
                    end_line: 0,
                    has_safety_comment: false,
                    safety_comment: None,
                    code: String::new(),
                });
            }
            
            if let Some(ref mut block) = current_unsafe {
                block.code.push_str(line);
                block.code.push('\n');
                
                // Check for safety comment in previous 5 lines
                if !block.has_safety_comment {
                    for i in 1..=5 {
                        if idx >= i {
                            let prev_line = lines[idx - i];
                            if self.safety_pattern.is_match(prev_line) {
                                block.has_safety_comment = true;
                                block.safety_comment = Some(prev_line.to_string());
                                break;
                            }
                        }
                    }
                }
                
                if line.contains("}") {
                    block.end_line = idx + 1;
                    unsafe_blocks.push(block.clone());
                    current_unsafe = None;
                }
            }
        }
        
        SafetyReport {
            file: path.to_path_buf(),
            unsafe_blocks,
            total_unsafe: unsafe_blocks.len(),
            documented_unsafe: unsafe_blocks.iter().filter(|b| b.has_safety_comment).count(),
        }
    }
}

#[derive(Debug, Clone)]
struct UnsafeBlock {
    start_line: usize,
    end_line: usize,
    has_safety_comment: bool,
    safety_comment: Option<String>,
    code: String,
}

#[derive(Debug)]
struct SafetyReport {
    file: PathBuf,
    unsafe_blocks: Vec<UnsafeBlock>,
    total_unsafe: usize,
    documented_unsafe: usize,
}
```

### 3. Common Unsafe Patterns Analysis

```rust
pub enum UnsafePattern {
    // Memory manipulation
    Transmute { from: String, to: String },
    RawPointer { operation: PointerOp },
    UnintializedMemory,
    
    // FFI
    FfiCall { function: String },
    CString { unchecked: bool },
    
    // Concurrency
    StaticMut,
    SendSyncImpl,
    
    // Lifetime extension
    LifetimeTransmute,
    SelfReferential,
}

pub fn analyze_unsafe_patterns(code: &str) -> Vec<(UnsafePattern, Severity, String)> {
    let mut findings = Vec::new();
    
    // Check for transmute
    if code.contains("std::mem::transmute") || code.contains("transmute::<") {
        findings.push((
            UnsafePattern::Transmute {
                from: extract_type_param(code, 0),
                to: extract_type_param(code, 1),
            },
            Severity::High,
            "Transmute can violate type safety. Consider safer alternatives.".to_string(),
        ));
    }
    
    // Check for uninitialized memory
    if code.contains("MaybeUninit::uninit().assume_init()") {
        findings.push((
            UnsafePattern::UnintializedMemory,
            Severity::Critical,
            "Reading uninitialized memory is undefined behavior!".to_string(),
        ));
    }
    
    // Check for raw pointer dereferencing
    if code.contains("*const") || code.contains("*mut") {
        if code.contains("*") && !code.contains("*/") { // Not a comment
            findings.push((
                UnsafePattern::RawPointer { operation: PointerOp::Deref },
                Severity::High,
                "Ensure pointer is valid, aligned, and points to initialized memory".to_string(),
            ));
        }
    }
    
    // Check for static mut
    if code.contains("static mut") {
        findings.push((
            UnsafePattern::StaticMut,
            Severity::High,
            "Static mutable variables can cause data races. Consider Mutex or atomic types.".to_string(),
        ));
    }
    
    findings
}

#[derive(Debug)]
enum Severity {
    Info,
    Medium,
    High,
    Critical,
}
```

### 4. FFI Boundary Validation

```rust
pub struct FfiBoundaryChecker;

impl FfiBoundaryChecker {
    pub fn check_ffi_safety(code: &str) -> Vec<FfiIssue> {
        let mut issues = Vec::new();
        
        // Check for null pointer handling
        if code.contains(".as_ptr()") && !code.contains("is_null()") {
            issues.push(FfiIssue {
                kind: FfiIssueKind::MissingNullCheck,
                message: "FFI pointer should be checked for null".to_string(),
                suggestion: "Add null check before dereferencing".to_string(),
            });
        }
        
        // Check CString usage
        if code.contains("CString::new") && code.contains(".unwrap()") {
            issues.push(FfiIssue {
                kind: FfiIssueKind::UncheckedCString,
                message: "CString::new can fail on interior nuls".to_string(),
                suggestion: "Handle the error case explicitly".to_string(),
            });
        }
        
        // Check for proper lifetime handling
        if code.contains("extern") && code.contains("&") && !code.contains("'static") {
            issues.push(FfiIssue {
                kind: FfiIssueKind::LifetimeBound,
                message: "FFI function with borrowed data needs careful lifetime management".to_string(),
                suggestion: "Ensure borrowed data outlives FFI call".to_string(),
            });
        }
        
        // Check for repr(C) on structs
        if code.contains("extern") && code.contains("struct") && !code.contains("#[repr(C)]") {
            issues.push(FfiIssue {
                kind: FfiIssueKind::MissingReprC,
                message: "Struct used in FFI should have #[repr(C)]".to_string(),
                suggestion: "Add #[repr(C)] to ensure ABI compatibility".to_string(),
            });
        }
        
        issues
    }
}

#[derive(Debug)]
struct FfiIssue {
    kind: FfiIssueKind,
    message: String,
    suggestion: String,
}

#[derive(Debug)]
enum FfiIssueKind {
    MissingNullCheck,
    UncheckedCString,
    LifetimeBound,
    MissingReprC,
    UnalignedAccess,
}
```

### 5. Miri Integration

```rust
pub async fn run_miri_tests() -> Result<MiriReport, Error> {
    // Install Miri if needed
    let miri_check = Command::new("cargo")
        .args(&["+nightly", "miri", "--version"])
        .output()
        .await?;
        
    if !miri_check.status.success() {
        println!("Installing Miri...");
        Command::new("rustup")
            .args(&["component", "add", "miri", "--toolchain", "nightly"])
            .status()
            .await?;
    }
    
    // Run Miri on tests
    let miri_output = Command::new("cargo")
        .args(&["+nightly", "miri", "test"])
        .env("MIRIFLAGS", "-Zmiri-backtrace=full")
        .output()
        .await?;
    
    parse_miri_output(&miri_output.stdout, &miri_output.stderr)
}

fn parse_miri_output(stdout: &[u8], stderr: &[u8]) -> Result<MiriReport, Error> {
    let stderr_str = String::from_utf8_lossy(stderr);
    
    let mut undefined_behaviors = Vec::new();
    let mut memory_leaks = Vec::new();
    let mut data_races = Vec::new();
    
    for line in stderr_str.lines() {
        if line.contains("undefined behavior") {
            undefined_behaviors.push(extract_ub_details(line));
        } else if line.contains("memory leaked") {
            memory_leaks.push(extract_leak_details(line));
        } else if line.contains("data race") {
            data_races.push(extract_race_details(line));
        }
    }
    
    Ok(MiriReport {
        undefined_behaviors,
        memory_leaks,
        data_races,
        clean: undefined_behaviors.is_empty() && memory_leaks.is_empty() && data_races.is_empty(),
    })
}
```

### 6. Safety Proof Generation

```rust
pub struct SafetyProofGenerator;

impl SafetyProofGenerator {
    pub fn generate_safety_proof(unsafe_block: &UnsafeBlock) -> SafetyProof {
        let mut preconditions = Vec::new();
        let mut invariants = Vec::new();
        let mut guarantees = Vec::new();
        
        // Analyze code to extract conditions
        let code = &unsafe_block.code;
        
        // Pointer dereferencing
        if code.contains("*") && (code.contains("*const") || code.contains("*mut")) {
            preconditions.push("Pointer must be non-null".to_string());
            preconditions.push("Pointer must be properly aligned".to_string());
            preconditions.push("Pointed-to value must be initialized".to_string());
            preconditions.push("Memory must be valid for the duration of access".to_string());
        }
        
        // Array/slice access
        if code.contains("get_unchecked") || code.contains("from_raw_parts") {
            preconditions.push("Index must be within bounds".to_string());
            preconditions.push("Length must not exceed allocation".to_string());
        }
        
        // Transmute
        if code.contains("transmute") {
            preconditions.push("Source and target types must have same size".to_string());
            preconditions.push("Target type must be valid for all bit patterns of source".to_string());
            invariants.push("Type safety is maintained after transmute".to_string());
        }
        
        SafetyProof {
            preconditions,
            invariants,
            guarantees,
            requires_review: true,
        }
    }
}

#[derive(Debug)]
struct SafetyProof {
    preconditions: Vec<String>,
    invariants: Vec<String>,
    guarantees: Vec<String>,
    requires_review: bool,
}

// Generate safety documentation template
impl SafetyProof {
    pub fn to_comment(&self) -> String {
        let mut comment = String::from("// SAFETY:\n");
        
        if !self.preconditions.is_empty() {
            comment.push_str("// Preconditions:\n");
            for pre in &self.preconditions {
                comment.push_str(&format!("// - {}\n", pre));
            }
        }
        
        if !self.invariants.is_empty() {
            comment.push_str("// Invariants maintained:\n");
            for inv in &self.invariants {
                comment.push_str(&format!("// - {}\n", inv));
            }
        }
        
        if !self.guarantees.is_empty() {
            comment.push_str("// Guarantees:\n");
            for guarantee in &self.guarantees {
                comment.push_str(&format!("// - {}\n", guarantee));
            }
        }
        
        comment
    }
}
```

### 7. Automated Safety Fixes

```rust
pub fn suggest_safe_alternatives(pattern: &UnsafePattern) -> Option<SafeAlternative> {
    match pattern {
        UnsafePattern::Transmute { from, to } => {
            if from.contains("&[u8]") && to.contains("&str") {
                Some(SafeAlternative {
                    pattern: "transmute::<&[u8], &str>".to_string(),
                    safe_version: "std::str::from_utf8".to_string(),
                    explanation: "Use from_utf8 for safe string conversion".to_string(),
                })
            } else if is_numeric_transmute(from, to) {
                Some(SafeAlternative {
                    pattern: format!("transmute::<{}, {}>", from, to),
                    safe_version: format!("{}.to_ne_bytes()", from),
                    explanation: "Use to_ne_bytes/from_ne_bytes for numeric conversions".to_string(),
                })
            } else {
                None
            }
        }
        
        UnsafePattern::UnintializedMemory => {
            Some(SafeAlternative {
                pattern: "MaybeUninit::uninit().assume_init()".to_string(),
                safe_version: "MaybeUninit::zeroed().assume_init() or proper initialization".to_string(),
                explanation: "Initialize memory before reading".to_string(),
            })
        }
        
        UnsafePattern::StaticMut => {
            Some(SafeAlternative {
                pattern: "static mut".to_string(),
                safe_version: "use std::sync::Mutex or atomic types".to_string(),
                explanation: "Thread-safe alternatives prevent data races".to_string(),
            })
        }
        
        _ => None,
    }
}

#[derive(Debug)]
struct SafeAlternative {
    pattern: String,
    safe_version: String,
    explanation: String,
}
```

### 8. Generate Comprehensive Audit Report

```rust
pub fn generate_audit_report(
    findings: Vec<AuditFinding>,
    miri_report: Option<MiriReport>,
) -> String {
    let mut report = String::new();
    
    report.push_str("# Unsafe Code Audit Report\n\n");
    report.push_str(&format!("Generated: {}\n\n", chrono::Local::now().format("%Y-%m-%d %H:%M:%S")));
    
    // Executive Summary
    let critical_count = findings.iter().filter(|f| matches!(f.severity, Severity::Critical)).count();
    let high_count = findings.iter().filter(|f| matches!(f.severity, Severity::High)).count();
    
    report.push_str("## Executive Summary\n\n");
    
    if critical_count > 0 {
        report.push_str(&format!("🚨 **CRITICAL**: Found {} critical safety issues that require immediate attention.\n\n", critical_count));
    } else if high_count > 0 {
        report.push_str(&format!("⚠️ **WARNING**: Found {} high severity issues that should be addressed.\n\n", high_count));
    } else {
        report.push_str("✅ **GOOD**: No critical safety issues found.\n\n");
    }
    
    // Statistics
    report.push_str("## Statistics\n\n");
    report.push_str(&format!("- Total unsafe blocks: {}\n", total_unsafe));
    report.push_str(&format!("- Documented unsafe: {} ({:.0}%)\n", 
        documented_unsafe, 
        (documented_unsafe as f64 / total_unsafe as f64 * 100.0)
    ));
    report.push_str(&format!("- Safety issues found: {}\n", findings.len()));
    
    // Miri Results
    if let Some(miri) = &miri_report {
        report.push_str("\n## Miri Analysis\n\n");
        
        if miri.clean {
            report.push_str("✅ Miri detected no issues in test suite.\n");
        } else {
            if !miri.undefined_behaviors.is_empty() {
                report.push_str(&format!("❌ Undefined behaviors: {}\n", miri.undefined_behaviors.len()));
            }
            if !miri.memory_leaks.is_empty() {
                report.push_str(&format!("❌ Memory leaks: {}\n", miri.memory_leaks.len()));
            }
            if !miri.data_races.is_empty() {
                report.push_str(&format!("❌ Data races: {}\n", miri.data_races.len()));
            }
        }
    }
    
    // Detailed Findings
    report.push_str("\n## Detailed Findings\n\n");
    
    // Group by file
    let mut findings_by_file: HashMap<PathBuf, Vec<&AuditFinding>> = HashMap::new();
    for finding in &findings {
        findings_by_file
            .entry(finding.file.clone())
            .or_default()
            .push(finding);
    }
    
    for (file, file_findings) in findings_by_file {
        report.push_str(&format!("### {}\n\n", file.display()));
        
        for finding in file_findings {
            let severity_icon = match finding.severity {
                Severity::Critical => "🚨",
                Severity::High => "⚠️",
                Severity::Medium => "⚠",
                Severity::Info => "ℹ️",
            };
            
            report.push_str(&format!(
                "{} **Line {}-{}**: {}\n\n",
                severity_icon,
                finding.line_start,
                finding.line_end,
                finding.issue
            ));
            
            if let Some(suggestion) = &finding.suggestion {
                report.push_str(&format!("   **Suggestion**: {}\n\n", suggestion));
            }
            
            if let Some(safe_alt) = &finding.safe_alternative {
                report.push_str(&format!("   **Safe Alternative**:\n   ```rust\n   {}\n   ```\n\n", safe_alt));
            }
            
            // Code snippet
            report.push_str("   **Code**:\n   ```rust\n");
            for line in finding.code_snippet.lines() {
                report.push_str(&format!("   {}\n", line));
            }
            report.push_str("   ```\n\n");
        }
    }
    
    // Recommendations
    report.push_str("## Recommendations\n\n");
    report.push_str("1. Add safety documentation to all unsafe blocks\n");
    report.push_str("2. Consider safe alternatives where available\n");
    report.push_str("3. Run Miri on test suite regularly\n");
    report.push_str("4. Use `#![forbid(unsafe_op_in_unsafe_fn)]` for better granularity\n");
    report.push_str("5. Consider using `cargo-geiger` for dependency analysis\n");
    
    report
}

#[derive(Debug)]
struct AuditFinding {
    file: PathBuf,
    line_start: usize,
    line_end: usize,
    severity: Severity,
    issue: String,
    suggestion: Option<String>,
    safe_alternative: Option<String>,
    code_snippet: String,
}
```

### 9. Integration with CI/CD

```yaml
# .github/workflows/unsafe-audit.yml
name: Unsafe Code Audit
on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@nightly
        with:
          components: miri
      
      - name: Install audit tools
        run: |
          cargo install cargo-geiger
          cargo install cargo-audit
      
      - name: Run unsafe audit
        run: |
          # Count unsafe usage
          echo "## Unsafe Usage Statistics" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
          cargo geiger --format GitHubMarkdown >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
      
      - name: Run Miri
        run: |
          cargo +nightly miri test
      
      - name: Check safety comments
        run: |
          ./scripts/check-safety-comments.sh
```

### 10. Summary Dashboard

```markdown
# Unsafe Audit Summary

## 📊 Project Safety Score: B+ (85/100)

### Breakdown:
- ✅ Documentation: 90% of unsafe blocks have safety comments
- ⚠️ Patterns: 3 high-risk patterns detected
- ✅ Testing: Miri passes on all tests
- ⚠️ Dependencies: 2 dependencies use significant unsafe

### Top Risks:
1. **Transmute Usage** (3 instances)
   - File: src/core/convert.rs
   - Risk: Type safety violation
   - Action: Replace with safe conversions

2. **Raw Pointer Arithmetic** (5 instances)
   - File: src/io/buffer.rs
   - Risk: Out-of-bounds access
   - Action: Add bounds checking

3. **Static Mutable** (1 instance)
   - File: src/global.rs
   - Risk: Data races
   - Action: Use Mutex or OnceCell

### Recommendations:
1. Enable `#![forbid(unsafe_op_in_unsafe_fn)]`
2. Add Miri to CI pipeline
3. Document safety invariants for all unsafe blocks
4. Consider safe alternatives for 60% of unsafe usage

### Unsafe Trends:
```
Month    | Unsafe Blocks | Safety Docs | Issues
---------|---------------|-------------|--------
Jan 2024 | 45           | 67%         | 12
Feb 2024 | 42           | 78%         | 8
Mar 2024 | 38           | 90%         | 3
```

Good progress on reducing unsafe usage! 📈
```

## Error Handling

If audit fails:
```
❌ Unsafe audit error: [specific issue]

Common issues:
- Project doesn't compile: Fix compilation errors first
- Miri not installed: rustup component add miri --toolchain nightly
- Too many files: Use --filter flag to audit specific modules

Quick fix:
cargo check && cargo +nightly miri setup
```

## Related Commands

- `/rust-analyzer` - General code analysis
- `/security-scan` - Security vulnerability scanning
- `/rust-fuzz` - Fuzz testing for unsafe code
- `/test-harness` - Generate tests for unsafe code