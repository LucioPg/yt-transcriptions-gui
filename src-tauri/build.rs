use std::env;
use std::fs;
use std::path::Path;
use std::process::Command;

fn main() {
    // Run tauri_build to embed icon and other resources (uses default manifest)
    tauri_build::build();

    println!("cargo:rerun-if-changed=../src");
    println!("cargo:rerun-if-changed=../pyproject.toml");
    println!("cargo:rerun-if-changed=../requirements.txt");

    // Only build backend in release mode
    let profile = env::var("PROFILE").unwrap_or_else(|_| "debug".to_string());
    if profile != "release" {
        println!("Skipping backend build in debug mode (backend will be started with uv)");
        return;
    }

    println!("Building Python backend for release mode...");

    // Get the project root directory
    let project_root = env::var("CARGO_MANIFEST_DIR").unwrap();
    let project_root = Path::new(&project_root).parent().unwrap_or_else(|| Path::new("."));

    // Create dist directory if it doesn't exist
    let dist_dir = project_root.join("dist");
    if !dist_dir.exists() {
        fs::create_dir_all(&dist_dir).expect("Failed to create dist directory");
    }

    // Determine the output filename based on the target OS
    let target_os = env::var("CARGO_CFG_TARGET_OS").unwrap_or_else(|_| "unknown".to_string());
    let output_filename = if target_os == "windows" {
        "yt-transcriptor-backend.exe"
    } else {
        "yt-transcriptor-backend"
    };

    let output_path = dist_dir.join(output_filename);

    // Check if we need to rebuild (simple timestamp check)
    let mut should_rebuild = true;
    if output_path.exists() {
        // Check if any Python files are newer than the executable
        let output_time = fs::metadata(&output_path)
            .and_then(|m| m.modified())
            .unwrap_or(std::time::SystemTime::UNIX_EPOCH);

        let src_dir = project_root.join("src");
        if let Ok(mut should_rebuild_local) = check_python_files_newer(&src_dir, output_time) {
            // Also check pyproject.toml and requirements.txt
            for config_file in &["pyproject.toml", "requirements.txt"] {
                let config_path = project_root.join(config_file);
                if config_path.exists() {
                    if let Ok(config_time) = fs::metadata(&config_path).and_then(|m| m.modified()) {
                        if config_time > output_time {
                            should_rebuild_local = true;
                            break;
                        }
                    }
                }
            }
            should_rebuild = should_rebuild_local;
        }
    }

    if should_rebuild {
        println!("Building Python backend executable...");

        // Use PyInstaller to create the executable
        let output = Command::new("uv")
            .args(&[
                "run",
                "pyinstaller",
                "--onefile",
                "--name",
                &output_filename.strip_suffix(".exe").unwrap_or(&output_filename),
                "--distpath",
                dist_dir.to_str().expect("Invalid dist path"),
                "--workpath",
                project_root.join("build").to_str().expect("Invalid build path"),
                "--specpath",
                project_root.join("build").to_str().expect("Invalid build path"),
                "--noconfirm",
                "--clean",
                "src/web_app.py"
            ])
            .current_dir(project_root)
            .output()
            .expect("Failed to execute PyInstaller command");

        if !output.status.success() {
            eprintln!("PyInstaller failed:");
            eprintln!("stdout: {}", String::from_utf8_lossy(&output.stdout));
            eprintln!("stderr: {}", String::from_utf8_lossy(&output.stderr));
            panic!("Failed to build Python backend");
        }

        println!("Python backend built successfully: {:?}", output_path);
    } else {
        println!("Python backend is up to date: {:?}", output_path);
    }

    // Set rerun triggers
    println!("cargo:rerun-if-changed=../src");
    println!("cargo:rerun-if-changed=../pyproject.toml");
    println!("cargo:rerun-if-changed=../requirements.txt");
}

fn check_python_files_newer(src_dir: &Path, reference_time: std::time::SystemTime) -> std::io::Result<bool> {
    if src_dir.is_dir() {
        for entry in fs::read_dir(src_dir)? {
            let entry = entry?;
            let path = entry.path();

            if path.is_dir() {
                if check_python_files_newer(&path, reference_time)? {
                    return Ok(true);
                }
            } else if let Some(ext) = path.extension() {
                if ext == "py" {
                    if let Ok(file_time) = fs::metadata(&path).and_then(|m| m.modified()) {
                        if file_time > reference_time {
                            return Ok(true);
                        }
                    }
                }
            }
        }
    }
    Ok(false)
}
