---
version: 1.0.0
tags: [rust, error-handling, design, architecture]
---

# Rust Error Design

Design robust error handling systems for Rust applications. Creates comprehensive error hierarchies, implements proper error propagation, and ensures excellent user experience.

## Usage
```
/rust-error-design [error-strategy] [application-type]
```

## Error Strategies

### Quick Design
```
/rust-error-design                    # Analyze and recommend error strategy
/rust-error-design anyhow cli        # Use anyhow for CLI app
/rust-error-design thiserror library # Use thiserror for library
```

### Advanced Patterns
```
/rust-error-design custom api        # Custom error types for API
/rust-error-design mixed application # Mixed strategy for large app
/rust-error-design no-std embedded   # no_std compatible errors
```

## Pre-flight Checks

1. Analyze current error handling
2. Identify error categories
3. Check dependencies
4. Determine target audience (library vs application)

## Implementation

Given the context: $ARGUMENTS

### 1. Analyze Current Error Patterns

```rust
// Common anti-patterns to identify:

// 1. String errors (poor for programmatic handling)
Err("Something went wrong".to_string())

// 2. Unwrap/expect in library code
file.read_to_string(&mut contents).unwrap();

// 3. Loss of error context
database_op().map_err(|_| "Database error")?;

// 4. Overly broad error types
Result<T, Box<dyn Error>>

// 5. Poor error messages
Err(Error::InvalidInput) // What input? Why invalid?
```

### 2. Error Strategy Selection

#### For Libraries: thiserror
```toml
[dependencies]
thiserror = "1.0"
```

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum RustCopyError {
    #[error("Failed to read source file: {path}")]
    SourceReadError {
        path: PathBuf,
        #[source]
        source: io::Error,
    },
    
    #[error("Failed to write to destination: {path}")]
    DestinationWriteError {
        path: PathBuf,
        #[source]
        source: io::Error,
    },
    
    #[error("Invalid path: {path:?}")]
    InvalidPath {
        path: PathBuf,
        reason: PathValidationError,
    },
    
    #[error("Permission denied for {operation} on {path}")]
    PermissionDenied {
        operation: FileOperation,
        path: PathBuf,
    },
    
    #[error("File system error: {context}")]
    FileSystemError {
        context: String,
        #[source]
        source: io::Error,
    },
    
    #[error("Operation cancelled by user")]
    Cancelled,
    
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

#[derive(Error, Debug)]
pub enum PathValidationError {
    #[error("Path contains null bytes")]
    NullBytes,
    
    #[error("Path is not UTF-8")]
    InvalidUtf8,
    
    #[error("Path traversal detected")]
    PathTraversal,
    
    #[error("Path is too long ({length} > {max})")]
    TooLong { length: usize, max: usize },
}

#[derive(Debug, Clone, Copy)]
pub enum FileOperation {
    Read,
    Write,
    Create,
    Delete,
    Copy,
    Move,
}

impl fmt::Display for FileOperation {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Read => write!(f, "read"),
            Self::Write => write!(f, "write"),
            Self::Create => write!(f, "create"),
            Self::Delete => write!(f, "delete"),
            Self::Copy => write!(f, "copy"),
            Self::Move => write!(f, "move"),
        }
    }
}
```

#### For Applications: anyhow with Context
```toml
[dependencies]
anyhow = "1.0"
```

```rust
use anyhow::{anyhow, bail, Context, Result};

pub fn copy_file(src: &Path, dst: &Path) -> Result<()> {
    // Rich context for debugging
    let src_file = File::open(src)
        .with_context(|| format!("Failed to open source file: {}", src.display()))?;
    
    let metadata = src_file.metadata()
        .with_context(|| format!("Failed to read metadata for: {}", src.display()))?;
    
    // Validation with clear errors
    if !metadata.is_file() {
        bail!("Source is not a regular file: {}", src.display());
    }
    
    // Check available space
    let available = get_available_space(dst.parent().unwrap())?;
    if available < metadata.len() {
        bail!(
            "Insufficient space: need {} bytes, have {} bytes",
            metadata.len(),
            available
        );
    }
    
    // Actual copy with context
    std::fs::copy(src, dst)
        .with_context(|| {
            format!(
                "Failed to copy {} to {}",
                src.display(),
                dst.display()
            )
        })?;
    
    Ok(())
}
```

### 3. Custom Error Types with Rich Information

```rust
use std::fmt;

#[derive(Debug)]
pub struct CopyError {
    kind: CopyErrorKind,
    source_path: Option<PathBuf>,
    dest_path: Option<PathBuf>,
    context: Vec<String>,
    source_error: Option<Box<dyn Error + Send + Sync>>,
    suggestions: Vec<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CopyErrorKind {
    SourceNotFound,
    DestinationExists,
    InsufficientPermissions,
    InsufficientSpace,
    InvalidPath,
    IoError,
    Interrupted,
}

impl CopyError {
    pub fn new(kind: CopyErrorKind) -> Self {
        Self {
            kind,
            source_path: None,
            dest_path: None,
            context: Vec::new(),
            source_error: None,
            suggestions: Vec::new(),
        }
    }
    
    pub fn with_source_path(mut self, path: impl Into<PathBuf>) -> Self {
        self.source_path = Some(path.into());
        self
    }
    
    pub fn with_dest_path(mut self, path: impl Into<PathBuf>) -> Self {
        self.dest_path = Some(path.into());
        self
    }
    
    pub fn with_context(mut self, context: impl Into<String>) -> Self {
        self.context.push(context.into());
        self
    }
    
    pub fn with_source_error(mut self, error: impl Error + Send + Sync + 'static) -> Self {
        self.source_error = Some(Box::new(error));
        self
    }
    
    pub fn suggest(mut self, suggestion: impl Into<String>) -> Self {
        self.suggestions.push(suggestion.into());
        self
    }
    
    pub fn kind(&self) -> CopyErrorKind {
        self.kind
    }
    
    pub fn is_recoverable(&self) -> bool {
        matches!(
            self.kind,
            CopyErrorKind::DestinationExists | CopyErrorKind::Interrupted
        )
    }
}

impl fmt::Display for CopyError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        // Main error message
        write!(f, "Copy operation failed: ")?;
        
        match self.kind {
            CopyErrorKind::SourceNotFound => write!(f, "source file not found")?,
            CopyErrorKind::DestinationExists => write!(f, "destination already exists")?,
            CopyErrorKind::InsufficientPermissions => write!(f, "insufficient permissions")?,
            CopyErrorKind::InsufficientSpace => write!(f, "insufficient disk space")?,
            CopyErrorKind::InvalidPath => write!(f, "invalid path")?,
            CopyErrorKind::IoError => write!(f, "I/O error")?,
            CopyErrorKind::Interrupted => write!(f, "operation interrupted")?,
        }
        
        // Add paths if available
        if let Some(src) = &self.source_path {
            write!(f, "\n  Source: {}", src.display())?;
        }
        if let Some(dst) = &self.dest_path {
            write!(f, "\n  Destination: {}", dst.display())?;
        }
        
        // Add context
        if !self.context.is_empty() {
            write!(f, "\n\nContext:")?;
            for ctx in &self.context {
                write!(f, "\n  - {}", ctx)?;
            }
        }
        
        // Add suggestions
        if !self.suggestions.is_empty() {
            write!(f, "\n\nSuggestions:")?;
            for (i, suggestion) in self.suggestions.iter().enumerate() {
                write!(f, "\n  {}. {}", i + 1, suggestion)?;
            }
        }
        
        Ok(())
    }
}

impl Error for CopyError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.source_error
            .as_ref()
            .map(|e| e.as_ref() as &(dyn Error + 'static))
    }
}
```

### 4. Error Recovery and Retry Logic

```rust
use std::time::Duration;
use backoff::{ExponentialBackoff, Error as BackoffError};

pub trait Recoverable {
    fn is_transient(&self) -> bool;
    fn can_retry(&self) -> bool;
    fn retry_after(&self) -> Option<Duration>;
}

impl Recoverable for CopyError {
    fn is_transient(&self) -> bool {
        matches!(
            self.kind,
            CopyErrorKind::IoError | CopyErrorKind::Interrupted
        )
    }
    
    fn can_retry(&self) -> bool {
        self.is_transient() || self.kind == CopyErrorKind::InsufficientSpace
    }
    
    fn retry_after(&self) -> Option<Duration> {
        match self.kind {
            CopyErrorKind::InsufficientSpace => Some(Duration::from_secs(30)),
            CopyErrorKind::IoError => Some(Duration::from_millis(100)),
            _ => None,
        }
    }
}

pub async fn copy_with_retry<F, T, E>(
    operation: F,
    max_retries: u32,
) -> Result<T, E>
where
    F: Fn() -> Result<T, E>,
    E: Recoverable + fmt::Display,
{
    let backoff = ExponentialBackoff {
        max_elapsed_time: Some(Duration::from_secs(60)),
        ..Default::default()
    };
    
    let mut attempts = 0;
    
    loop {
        attempts += 1;
        
        match operation() {
            Ok(result) => return Ok(result),
            Err(e) => {
                if !e.can_retry() || attempts >= max_retries {
                    return Err(e);
                }
                
                eprintln!("Attempt {} failed: {}. Retrying...", attempts, e);
                
                if let Some(duration) = e.retry_after() {
                    tokio::time::sleep(duration).await;
                }
            }
        }
    }
}
```

### 5. Error Reporting and Logging

```rust
use tracing::{error, warn, info, debug};

pub trait ErrorReport {
    fn report(&self);
    fn report_with_telemetry(&self, span_id: &str);
}

impl ErrorReport for CopyError {
    fn report(&self) {
        match self.kind {
            CopyErrorKind::SourceNotFound => {
                error!(
                    path = ?self.source_path,
                    "Source file not found"
                );
            }
            CopyErrorKind::InsufficientPermissions => {
                error!(
                    source = ?self.source_path,
                    dest = ?self.dest_path,
                    "Permission denied during copy operation"
                );
            }
            CopyErrorKind::InsufficientSpace => {
                warn!(
                    dest = ?self.dest_path,
                    "Insufficient disk space for copy operation"
                );
            }
            _ => {
                error!(
                    kind = ?self.kind,
                    source = ?self.source_path,
                    dest = ?self.dest_path,
                    "Copy operation failed"
                );
            }
        }
        
        // Log underlying error
        if let Some(source) = &self.source_error {
            error!(error = %source, "Underlying error");
        }
    }
    
    fn report_with_telemetry(&self, span_id: &str) {
        // Send to error tracking service
        #[cfg(feature = "telemetry")]
        {
            telemetry::report_error(ErrorEvent {
                span_id: span_id.to_string(),
                error_kind: format!("{:?}", self.kind),
                source_path: self.source_path.clone(),
                dest_path: self.dest_path.clone(),
                context: self.context.clone(),
                timestamp: std::time::SystemTime::now(),
            });
        }
        
        self.report();
    }
}
```

### 6. User-Friendly Error Messages

```rust
pub struct UserError {
    technical: Box<dyn Error + Send + Sync>,
    user_message: String,
    help_url: Option<String>,
}

impl UserError {
    pub fn from_copy_error(error: CopyError) -> Self {
        let user_message = match error.kind() {
            CopyErrorKind::SourceNotFound => {
                format!(
                    "Cannot find the file you're trying to copy. \
                     Please check that the file exists and you typed the path correctly."
                )
            }
            CopyErrorKind::DestinationExists => {
                format!(
                    "A file already exists at the destination. \
                     Use --force to overwrite or choose a different name."
                )
            }
            CopyErrorKind::InsufficientPermissions => {
                format!(
                    "You don't have permission to perform this operation. \
                     Try running with administrator privileges or check file permissions."
                )
            }
            CopyErrorKind::InsufficientSpace => {
                format!(
                    "Not enough disk space to complete the copy. \
                     Free up some space and try again."
                )
            }
            _ => format!("The copy operation failed. Error: {}", error),
        };
        
        Self {
            technical: Box::new(error),
            user_message,
            help_url: Some("https://example.com/help/copy-errors".to_string()),
        }
    }
}

// Pretty printing for terminal
impl fmt::Display for UserError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        use termcolor::{ColorChoice, ColorSpec, StandardStream, WriteColor};
        
        // This is for demonstration - actual implementation would write to terminal
        writeln!(f, "\n❌ {}\n", self.user_message)?;
        
        if let Some(url) = &self.help_url {
            writeln!(f, "💡 For more help, visit: {}\n", url)?;
        }
        
        if std::env::var("RUST_COPY_DEBUG").is_ok() {
            writeln!(f, "Debug info: {:?}", self.technical)?;
        }
        
        Ok(())
    }
}
```

### 7. Error Testing Helpers

```rust
#[cfg(test)]
mod test_helpers {
    use super::*;
    
    /// Helper to test error scenarios
    pub struct ErrorScenario {
        pub name: &'static str,
        pub setup: Box<dyn Fn() -> Result<(), CopyError>>,
        pub expected_kind: CopyErrorKind,
        pub should_be_recoverable: bool,
    }
    
    pub fn test_error_scenarios(scenarios: Vec<ErrorScenario>) {
        for scenario in scenarios {
            println!("Testing: {}", scenario.name);
            
            let result = (scenario.setup)();
            assert!(result.is_err(), "Expected error for: {}", scenario.name);
            
            let error = result.unwrap_err();
            assert_eq!(
                error.kind(),
                scenario.expected_kind,
                "Wrong error kind for: {}",
                scenario.name
            );
            assert_eq!(
                error.is_recoverable(),
                scenario.should_be_recoverable,
                "Wrong recoverability for: {}",
                scenario.name
            );
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use test_helpers::*;
    
    #[test]
    fn test_copy_errors() {
        let scenarios = vec![
            ErrorScenario {
                name: "source not found",
                setup: Box::new(|| {
                    Err(CopyError::new(CopyErrorKind::SourceNotFound)
                        .with_source_path("/nonexistent"))
                }),
                expected_kind: CopyErrorKind::SourceNotFound,
                should_be_recoverable: false,
            },
            ErrorScenario {
                name: "destination exists",
                setup: Box::new(|| {
                    Err(CopyError::new(CopyErrorKind::DestinationExists)
                        .with_dest_path("/existing"))
                }),
                expected_kind: CopyErrorKind::DestinationExists,
                should_be_recoverable: true,
            },
        ];
        
        test_error_scenarios(scenarios);
    }
}
```

### 8. Integration with Result and Option

```rust
// Extension traits for better error handling
pub trait ResultExt<T, E> {
    fn with_path_context(self, path: &Path) -> Result<T, CopyError>
    where
        E: Into<CopyError>;
    
    fn or_continue(self) -> Option<T>;
}

impl<T, E> ResultExt<T, E> for Result<T, E> {
    fn with_path_context(self, path: &Path) -> Result<T, CopyError>
    where
        E: Into<CopyError>,
    {
        self.map_err(|e| {
            e.into().with_context(format!("Operation on path: {}", path.display()))
        })
    }
    
    fn or_continue(self) -> Option<T> {
        match self {
            Ok(val) => Some(val),
            Err(_) => None,
        }
    }
}

// Usage
fn process_files(paths: Vec<PathBuf>) -> Vec<ProcessResult> {
    paths.iter()
        .map(|path| {
            open_file(path)
                .with_path_context(path)
                .and_then(|file| process_file(file))
                .or_continue()
        })
        .flatten()
        .collect()
}
```

### 9. Error Aggregation

```rust
#[derive(Debug)]
pub struct MultiError {
    errors: Vec<Box<dyn Error + Send + Sync>>,
}

impl MultiError {
    pub fn new() -> Self {
        Self { errors: Vec::new() }
    }
    
    pub fn add(&mut self, error: impl Error + Send + Sync + 'static) {
        self.errors.push(Box::new(error));
    }
    
    pub fn is_empty(&self) -> bool {
        self.errors.is_empty()
    }
    
    pub fn into_result(self) -> Result<(), Self> {
        if self.is_empty() {
            Ok(())
        } else {
            Err(self)
        }
    }
}

impl fmt::Display for MultiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "Multiple errors occurred ({}):", self.errors.len())?;
        for (i, error) in self.errors.iter().enumerate() {
            writeln!(f, "  {}. {}", i + 1, error)?;
        }
        Ok(())
    }
}

impl Error for MultiError {}
```

### 10. Generate Error Design Report

```markdown
# Error Design Report

## Strategy Summary
- **Library/Application**: Application
- **Primary Crate**: anyhow with custom types
- **Error Categories**: 7 distinct error types
- **Recovery Strategy**: Automatic retry with backoff

## Error Hierarchy

```
RustCopyError (root)
├── IoError
│   ├── SourceReadError
│   ├── DestinationWriteError
│   └── FileSystemError
├── ValidationError
│   ├── InvalidPath
│   └── PathValidationError
├── PermissionError
│   └── PermissionDenied
├── ResourceError
│   └── InsufficientSpace
└── UserError
    └── Cancelled
```

## Implementation Checklist

- [x] Define error types with thiserror
- [x] Add context propagation
- [x] Implement Display with helpful messages
- [x] Add error recovery traits
- [x] Create retry logic
- [x] Add error reporting/logging
- [x] Implement user-friendly messages
- [x] Add test helpers
- [x] Create error aggregation

## Best Practices Applied

1. **Rich Context**: Every error includes path and operation context
2. **Suggestions**: Errors provide actionable suggestions
3. **Recoverability**: Clear distinction between fatal and recoverable
4. **Debugging**: Debug mode shows technical details
5. **Telemetry**: Optional error reporting integration

## Usage Examples

```rust
// Simple error propagation
let file = File::open(&path)
    .context("Failed to open source file")?;

// Rich error construction
return Err(CopyError::new(CopyErrorKind::InsufficientSpace)
    .with_source_path(&src)
    .with_dest_path(&dst)
    .with_context("Copying large video file")
    .suggest("Free up disk space or choose different destination"));

// Automatic retry
copy_with_retry(|| perform_copy(&src, &dst), 3).await?;
```
```

## Related Commands

- `/rust-analyzer` - Analyze current error patterns
- `/test-harness` - Generate error scenario tests
- `/rust-cli` - CLI error formatting
- `/doc-generate` - Document error types