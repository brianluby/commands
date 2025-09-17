---
version: 1.0.0
tags: [rust, cli, clap, user-interface, commands]
---

# Rust CLI

Build robust command-line applications in Rust. Covers argument parsing, subcommands, configuration, progress reporting, and distribution.

## Usage
```
/rust-cli [framework] [features]
```

## Framework Options

### Quick Start
```
/rust-cli                    # Recommend CLI framework
/rust-cli clap              # Use clap v4 with derive
/rust-cli clap builder      # Use clap builder pattern
```

### Advanced Features
```
/rust-cli interactive       # Interactive prompts and menus
/rust-cli config           # Configuration file support
/rust-cli completions      # Shell completions
/rust-cli distribution     # Packaging and distribution
```

## Pre-flight Checks

1. Analyze CLI requirements
2. Check for existing CLI structure
3. Determine feature needs
4. Plan command hierarchy

## Implementation

Given the context: $ARGUMENTS

### 1. CLI Framework Setup with Clap

```toml
[dependencies]
clap = { version = "4", features = ["derive", "cargo", "env", "unicode", "wrap_help"] }
clap_complete = "4"
clap_mangen = "0.2"
anyhow = "1"
colored = "2"
indicatif = "0.17"
dialoguer = "0.11"
directories = "5"
serde = { version = "1", features = ["derive"] }
toml = "0.8"
env_logger = "0.10"
log = "0.4"
```

### 2. Modern Clap Derive Pattern

```rust
use clap::{Parser, Subcommand, Args, ValueEnum};
use std::path::PathBuf;

/// A fast and reliable file copy utility
#[derive(Parser, Debug)]
#[command(name = "rustcopy")]
#[command(author, version, about, long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    /// Enable verbose output
    #[arg(short, long, global = true)]
    verbose: bool,

    /// Suppress all output except errors
    #[arg(short, long, global = true, conflicts_with = "verbose")]
    quiet: bool,

    /// Number of parallel operations
    #[arg(short = 'j', long, global = true, default_value_t = num_cpus::get())]
    parallel: usize,

    /// Configuration file path
    #[arg(short, long, global = true, value_name = "FILE")]
    config: Option<PathBuf>,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Copy files or directories
    Copy(CopyArgs),
    
    /// Move files or directories
    Move(MoveArgs),
    
    /// Synchronize directories
    Sync(SyncArgs),
    
    /// Verify file integrity
    Verify {
        /// Files to verify
        #[arg(required = true)]
        files: Vec<PathBuf>,
        
        /// Checksum algorithm
        #[arg(short, long, value_enum, default_value_t = ChecksumType::Sha256)]
        algorithm: ChecksumType,
    },
    
    /// Generate shell completions
    Completions {
        /// Shell to generate completions for
        #[arg(value_enum)]
        shell: clap_complete::Shell,
    },
}

#[derive(Args, Debug)]
struct CopyArgs {
    /// Source file or directory
    #[arg(value_name = "SOURCE")]
    source: PathBuf,
    
    /// Destination path
    #[arg(value_name = "DEST")]
    destination: PathBuf,
    
    /// Copy mode
    #[arg(short, long, value_enum, default_value_t = CopyMode::Auto)]
    mode: CopyMode,
    
    /// Preserve attributes
    #[arg(short, long)]
    preserve: bool,
    
    /// Follow symbolic links
    #[arg(short = 'L', long)]
    dereference: bool,
    
    /// Interactive mode
    #[arg(short, long)]
    interactive: bool,
    
    /// Force overwrite
    #[arg(short, long)]
    force: bool,
    
    /// Exclude patterns
    #[arg(short, long, value_name = "PATTERN")]
    exclude: Vec<String>,
    
    /// Show progress bar
    #[arg(short = 'P', long)]
    progress: bool,
    
    /// Dry run - don't actually copy
    #[arg(long)]
    dry_run: bool,
}

#[derive(ValueEnum, Clone, Debug)]
enum CopyMode {
    /// Automatically select best method
    Auto,
    /// Standard copy
    Standard,
    /// Memory-mapped I/O
    Mmap,
    /// Zero-copy (Linux only)
    ZeroCopy,
    /// Direct I/O
    Direct,
}

#[derive(ValueEnum, Clone, Debug)]
enum ChecksumType {
    Md5,
    Sha1,
    Sha256,
    Sha512,
    Blake3,
}
```

### 3. Enhanced CLI Features

#### Progress Reporting
```rust
use indicatif::{ProgressBar, ProgressStyle, MultiProgress};
use std::time::Duration;

pub struct ProgressReporter {
    multi: MultiProgress,
    main_bar: ProgressBar,
    current_file: Option<ProgressBar>,
}

impl ProgressReporter {
    pub fn new(total_files: u64, total_bytes: u64) -> Self {
        let multi = MultiProgress::new();
        
        let main_bar = multi.add(ProgressBar::new(total_files));
        main_bar.set_style(
            ProgressStyle::with_template(
                "{spinner:.green} [{elapsed_precise}] {bar:40.cyan/blue} {pos}/{len} files ({percent}%)"
            )
            .unwrap()
            .progress_chars("##-")
        );
        
        Self {
            multi,
            main_bar,
            current_file: None,
        }
    }
    
    pub fn start_file(&mut self, name: &str, size: u64) {
        if let Some(bar) = &self.current_file {
            bar.finish_and_clear();
        }
        
        let file_bar = self.multi.add(ProgressBar::new(size));
        file_bar.set_style(
            ProgressStyle::with_template(
                "  {msg:.green} [{bar:30.yellow/blue}] {bytes}/{total_bytes} ({bytes_per_sec})"
            )
            .unwrap()
            .progress_chars("=>-")
        );
        file_bar.set_message(name.to_string());
        
        self.current_file = Some(file_bar);
    }
    
    pub fn update(&self, bytes: u64) {
        if let Some(bar) = &self.current_file {
            bar.inc(bytes);
        }
    }
    
    pub fn finish_file(&mut self) {
        if let Some(bar) = &self.current_file {
            bar.finish_with_message("✓");
        }
        self.main_bar.inc(1);
    }
}

// Spinner for indeterminate operations
pub fn with_spinner<F, T>(message: &str, f: F) -> T
where
    F: FnOnce() -> T,
{
    let spinner = ProgressBar::new_spinner();
    spinner.set_style(
        ProgressStyle::with_template("{spinner:.green} {msg}")
            .unwrap()
            .tick_strings(&["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    );
    spinner.set_message(message.to_string());
    spinner.enable_steady_tick(Duration::from_millis(80));
    
    let result = f();
    
    spinner.finish_with_message(format!("✓ {}", message));
    result
}
```

#### Interactive Mode
```rust
use dialoguer::{theme::ColorfulTheme, Confirm, Select, Input, MultiSelect};
use console::style;

pub struct InteractiveMode;

impl InteractiveMode {
    pub fn confirm_overwrite(path: &Path) -> anyhow::Result<bool> {
        Confirm::with_theme(&ColorfulTheme::default())
            .with_prompt(format!(
                "File {} already exists. Overwrite?",
                style(path.display()).yellow()
            ))
            .default(false)
            .interact()
            .map_err(Into::into)
    }
    
    pub fn select_copy_mode() -> anyhow::Result<CopyMode> {
        let modes = vec![
            ("Auto (recommended)", CopyMode::Auto),
            ("Standard", CopyMode::Standard),
            ("Memory-mapped", CopyMode::Mmap),
            ("Zero-copy (Linux)", CopyMode::ZeroCopy),
        ];
        
        let selection = Select::with_theme(&ColorfulTheme::default())
            .with_prompt("Select copy mode")
            .items(&modes.iter().map(|(name, _)| name).collect::<Vec<_>>())
            .default(0)
            .interact()?;
        
        Ok(modes[selection].1.clone())
    }
    
    pub fn get_destination() -> anyhow::Result<PathBuf> {
        Input::with_theme(&ColorfulTheme::default())
            .with_prompt("Enter destination path")
            .validate_with(|input: &String| -> Result<(), &str> {
                if input.is_empty() {
                    Err("Path cannot be empty")
                } else {
                    Ok(())
                }
            })
            .interact_text()
            .map(PathBuf::from)
            .map_err(Into::into)
    }
    
    pub fn select_files(files: &[PathBuf]) -> anyhow::Result<Vec<PathBuf>> {
        let display_names: Vec<String> = files
            .iter()
            .map(|p| p.display().to_string())
            .collect();
        
        let selections = MultiSelect::with_theme(&ColorfulTheme::default())
            .with_prompt("Select files to copy")
            .items(&display_names)
            .interact()?;
        
        Ok(selections.into_iter()
            .map(|i| files[i].clone())
            .collect())
    }
}
```

### 4. Configuration Management

```rust
use serde::{Deserialize, Serialize};
use directories::ProjectDirs;

#[derive(Debug, Serialize, Deserialize)]
#[serde(default)]
pub struct Config {
    pub default_mode: CopyMode,
    pub preserve_attributes: bool,
    pub follow_symlinks: bool,
    pub parallel_operations: usize,
    pub buffer_size: usize,
    pub show_progress: bool,
    pub aliases: HashMap<String, String>,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            default_mode: CopyMode::Auto,
            preserve_attributes: true,
            follow_symlinks: false,
            parallel_operations: num_cpus::get(),
            buffer_size: 64 * 1024,
            show_progress: true,
            aliases: HashMap::new(),
        }
    }
}

impl Config {
    pub fn load() -> anyhow::Result<Self> {
        let config_path = Self::config_path()?;
        
        if config_path.exists() {
            let contents = std::fs::read_to_string(&config_path)?;
            let config: Config = toml::from_str(&contents)?;
            Ok(config)
        } else {
            Ok(Config::default())
        }
    }
    
    pub fn save(&self) -> anyhow::Result<()> {
        let config_path = Self::config_path()?;
        
        if let Some(parent) = config_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        
        let contents = toml::to_string_pretty(self)?;
        std::fs::write(config_path, contents)?;
        
        Ok(())
    }
    
    fn config_path() -> anyhow::Result<PathBuf> {
        let proj_dirs = ProjectDirs::from("com", "rustcopy", "rustcopy")
            .ok_or_else(|| anyhow::anyhow!("Unable to determine config directory"))?;
        
        Ok(proj_dirs.config_dir().join("config.toml"))
    }
    
    pub fn merge_with_args(&mut self, args: &CopyArgs) {
        if args.preserve {
            self.preserve_attributes = true;
        }
        if args.dereference {
            self.follow_symlinks = true;
        }
        if args.progress {
            self.show_progress = true;
        }
    }
}

// Environment variable support
pub fn load_from_env(config: &mut Config) {
    if let Ok(mode) = std::env::var("RUSTCOPY_MODE") {
        if let Ok(parsed) = mode.parse::<CopyMode>() {
            config.default_mode = parsed;
        }
    }
    
    if let Ok(parallel) = std::env::var("RUSTCOPY_PARALLEL") {
        if let Ok(num) = parallel.parse::<usize>() {
            config.parallel_operations = num;
        }
    }
}
```

### 5. Shell Completions

```rust
use clap_complete::{generate, Shell};
use std::io;

pub fn generate_completions(shell: Shell) {
    let mut cmd = Cli::command();
    let name = cmd.get_name().to_string();
    
    generate(shell, &mut cmd, name, &mut io::stdout());
}

// In main.rs
match cli.command {
    Commands::Completions { shell } => {
        generate_completions(shell);
    }
    // ... other commands
}

// Installation instructions
pub fn print_completion_instructions(shell: Shell) {
    let instructions = match shell {
        Shell::Bash => {
            "# Add to ~/.bashrc:\n\
             eval \"$(rustcopy completions bash)\""
        }
        Shell::Zsh => {
            "# Add to ~/.zshrc:\n\
             eval \"$(rustcopy completions zsh)\""
        }
        Shell::Fish => {
            "# Add to ~/.config/fish/config.fish:\n\
             rustcopy completions fish | source"
        }
        Shell::PowerShell => {
            "# Add to $PROFILE:\n\
             rustcopy completions powershell | Out-String | Invoke-Expression"
        }
        _ => "Shell not supported",
    };
    
    println!("{}", instructions);
}
```

### 6. Output Formatting

```rust
use colored::*;
use std::fmt;

pub struct OutputFormatter {
    verbose: bool,
    quiet: bool,
    color: bool,
}

impl OutputFormatter {
    pub fn new(verbose: bool, quiet: bool) -> Self {
        Self {
            verbose,
            quiet,
            color: atty::is(atty::Stream::Stdout),
        }
    }
    
    pub fn success(&self, message: &str) {
        if !self.quiet {
            if self.color {
                println!("{} {}", "✓".green(), message);
            } else {
                println!("✓ {}", message);
            }
        }
    }
    
    pub fn error(&self, message: &str) {
        if self.color {
            eprintln!("{} {}", "✗".red(), message.red());
        } else {
            eprintln!("✗ {}", message);
        }
    }
    
    pub fn warning(&self, message: &str) {
        if !self.quiet {
            if self.color {
                eprintln!("{} {}", "⚠".yellow(), message.yellow());
            } else {
                eprintln!("⚠ {}", message);
            }
        }
    }
    
    pub fn info(&self, message: &str) {
        if !self.quiet {
            if self.color {
                println!("{} {}", "ℹ".blue(), message);
            } else {
                println!("ℹ {}", message);
            }
        }
    }
    
    pub fn verbose(&self, message: &str) {
        if self.verbose && !self.quiet {
            if self.color {
                println!("{} {}", "→".dimmed(), message.dimmed());
            } else {
                println!("→ {}", message);
            }
        }
    }
}

// Pretty-print file sizes
pub fn format_bytes(bytes: u64) -> String {
    const UNITS: &[&str] = &["B", "KB", "MB", "GB", "TB"];
    let mut size = bytes as f64;
    let mut unit_index = 0;
    
    while size >= 1024.0 && unit_index < UNITS.len() - 1 {
        size /= 1024.0;
        unit_index += 1;
    }
    
    if unit_index == 0 {
        format!("{} {}", size as u64, UNITS[unit_index])
    } else {
        format!("{:.2} {}", size, UNITS[unit_index])
    }
}

// Table output
use comfy_table::{Table, ContentArrangement};

pub fn print_file_table(files: &[(PathBuf, u64, SystemTime)]) {
    let mut table = Table::new();
    table
        .set_content_arrangement(ContentArrangement::Dynamic)
        .set_header(vec!["File", "Size", "Modified"]);
    
    for (path, size, modified) in files {
        let modified_str = humantime::format_duration(
            SystemTime::now()
                .duration_since(*modified)
                .unwrap_or_default()
        );
        
        table.add_row(vec![
            path.display().to_string(),
            format_bytes(*size),
            format!("{} ago", modified_str),
        ]);
    }
    
    println!("{}", table);
}
```

### 7. Logging and Debugging

```rust
use log::{debug, error, info, trace, warn};
use env_logger::Builder;
use std::io::Write;

pub fn init_logging(verbose: bool) {
    let mut builder = Builder::from_default_env();
    
    builder
        .format(|buf, record| {
            let level_style = match record.level() {
                log::Level::Error => "ERROR".red(),
                log::Level::Warn => "WARN".yellow(),
                log::Level::Info => "INFO".green(),
                log::Level::Debug => "DEBUG".blue(),
                log::Level::Trace => "TRACE".purple(),
            };
            
            writeln!(
                buf,
                "[{} {}] {}",
                chrono::Local::now().format("%Y-%m-%d %H:%M:%S"),
                level_style,
                record.args()
            )
        })
        .filter(None, if verbose {
            log::LevelFilter::Debug
        } else {
            log::LevelFilter::Info
        });
    
    if std::env::var("RUST_LOG").is_err() {
        builder.init();
    } else {
        // Respect RUST_LOG if set
        env_logger::init();
    }
}

// Structured logging
#[derive(Debug)]
pub struct CopyOperation {
    pub id: uuid::Uuid,
    pub source: PathBuf,
    pub destination: PathBuf,
    pub start_time: Instant,
    pub bytes_copied: u64,
}

impl CopyOperation {
    pub fn log_start(&self) {
        info!(
            "Starting copy operation {} from {} to {}",
            self.id,
            self.source.display(),
            self.destination.display()
        );
        
        debug!(
            "Operation {}: mode={:?}, preserve={}, follow_symlinks={}",
            self.id,
            "auto",
            true,
            false
        );
    }
    
    pub fn log_progress(&self, current: u64, total: u64) {
        trace!(
            "Operation {}: progress {}/{}",
            self.id,
            format_bytes(current),
            format_bytes(total)
        );
    }
    
    pub fn log_complete(&self) {
        let duration = self.start_time.elapsed();
        let throughput = self.bytes_copied as f64 / duration.as_secs_f64();
        
        info!(
            "Operation {} complete: {} in {:.2}s ({}/s)",
            self.id,
            format_bytes(self.bytes_copied),
            duration.as_secs_f64(),
            format_bytes(throughput as u64)
        );
    }
}
```

### 8. Main Application Structure

```rust
use anyhow::{Context, Result};

#[tokio::main]
async fn main() -> Result<()> {
    // Parse CLI arguments
    let cli = Cli::parse();
    
    // Initialize logging
    init_logging(cli.verbose);
    
    // Load configuration
    let mut config = Config::load()
        .context("Failed to load configuration")?;
    load_from_env(&mut config);
    
    // Create output formatter
    let output = OutputFormatter::new(cli.verbose, cli.quiet);
    
    // Handle commands
    match cli.command {
        Commands::Copy(args) => {
            config.merge_with_args(&args);
            
            let operation = CopyOperation {
                id: uuid::Uuid::new_v4(),
                source: args.source.clone(),
                destination: args.destination.clone(),
                start_time: Instant::now(),
                bytes_copied: 0,
            };
            
            operation.log_start();
            
            match execute_copy(&args, &config, &output).await {
                Ok(bytes) => {
                    output.success(&format!(
                        "Copied {} from {} to {}",
                        format_bytes(bytes),
                        args.source.display(),
                        args.destination.display()
                    ));
                }
                Err(e) => {
                    output.error(&format!("Copy failed: {}", e));
                    std::process::exit(1);
                }
            }
        }
        
        Commands::Completions { shell } => {
            generate_completions(shell);
        }
        
        // ... other commands
    }
    
    Ok(())
}
```

### 9. Testing CLI Applications

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use assert_cmd::Command;
    use predicates::prelude::*;
    use tempfile::TempDir;
    
    #[test]
    fn test_cli_copy_command() {
        let temp_dir = TempDir::new().unwrap();
        let src = temp_dir.path().join("source.txt");
        let dst = temp_dir.path().join("dest.txt");
        
        std::fs::write(&src, "test content").unwrap();
        
        Command::cargo_bin("rustcopy")
            .unwrap()
            .arg("copy")
            .arg(&src)
            .arg(&dst)
            .assert()
            .success()
            .stdout(predicate::str::contains("Copied"));
        
        assert_eq!(
            std::fs::read_to_string(dst).unwrap(),
            "test content"
        );
    }
    
    #[test]
    fn test_cli_help() {
        Command::cargo_bin("rustcopy")
            .unwrap()
            .arg("--help")
            .assert()
            .success()
            .stdout(predicate::str::contains("A fast and reliable file copy utility"));
    }
    
    #[test]
    fn test_cli_version() {
        Command::cargo_bin("rustcopy")
            .unwrap()
            .arg("--version")
            .assert()
            .success()
            .stdout(predicate::str::contains(env!("CARGO_PKG_VERSION")));
    }
}
```

### 10. Distribution and Packaging

```rust
// Cargo.toml additions for distribution
[package]
name = "rustcopy"
version = "1.0.0"
authors = ["Your Name <email@example.com>"]
edition = "2021"
description = "A fast and reliable file copy utility"
readme = "README.md"
homepage = "https://github.com/yourusername/rustcopy"
repository = "https://github.com/yourusername/rustcopy"
license = "MIT OR Apache-2.0"
keywords = ["cli", "file", "copy", "utility", "tool"]
categories = ["command-line-utilities", "filesystem"]

[profile.release]
lto = true
codegen-units = 1
strip = true
opt-level = 3
```

Build script for releases:
```bash
#!/bin/bash
# scripts/release.sh

set -e

VERSION=$(cargo metadata --no-deps --format-version 1 | jq -r '.packages[0].version')

# Build for multiple platforms
TARGETS=(
    "x86_64-unknown-linux-gnu"
    "x86_64-unknown-linux-musl"
    "x86_64-apple-darwin"
    "aarch64-apple-darwin"
    "x86_64-pc-windows-gnu"
)

for target in "${TARGETS[@]}"; do
    echo "Building for $target..."
    cargo build --release --target "$target"
    
    # Package
    if [[ "$target" == *"windows"* ]]; then
        zip "rustcopy-v${VERSION}-${target}.zip" \
            "target/${target}/release/rustcopy.exe"
    else
        tar czf "rustcopy-v${VERSION}-${target}.tar.gz" \
            -C "target/${target}/release" rustcopy
    fi
done

# Generate checksums
shasum -a 256 rustcopy-v*.{tar.gz,zip} > checksums.txt
```

## Generate CLI Design Report

```markdown
# CLI Design Report

## Architecture Summary
- **Framework**: Clap v4 with derive macros
- **Async Runtime**: Tokio (multi-threaded)
- **Configuration**: TOML with env override
- **Output**: Colored, progress bars, tables

## Features Implemented

### Core CLI
- [x] Subcommands with nested arguments
- [x] Global and local flags
- [x] Value validation and enums
- [x] Auto-generated help
- [x] Version management

### User Experience
- [x] Progress bars with ETA
- [x] Interactive prompts
- [x] Colored output
- [x] Shell completions
- [x] Configuration files

### Developer Experience
- [x] Structured logging
- [x] Debug mode
- [x] Comprehensive testing
- [x] Cross-platform builds

## Usage Examples

```bash
# Basic copy
rustcopy copy source.txt dest.txt

# Advanced copy with options
rustcopy copy -Ppf --mode zero-copy /large/file /backup/

# Interactive mode
rustcopy copy -i ~/Downloads/* ~/Documents/

# With configuration
rustcopy -c custom.toml sync ~/project /backup/project

# Generate completions
rustcopy completions bash > ~/.local/share/bash-completion/completions/rustcopy
```

## Performance Characteristics

- Startup time: <5ms
- Memory usage: 2-4MB baseline
- Async operations: Non-blocking
- Progress updates: 60fps max
```

## Related Commands

- `/rust-error-design` - Design error handling
- `/rust-async` - Async patterns for CLI
- `/test-harness` - Generate CLI tests
- `/docker-optimize` - Package CLI in containers