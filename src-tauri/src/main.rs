// Disable windows subsystem for debugging to prevent STATUS_ENTRYPOINT_NOT_FOUND
// Re-enable for production builds
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::path::PathBuf;
use std::process::{Child, Command};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;
use tauri::{AppHandle, Emitter, Manager, State};
use std::fs;

// Embed the backend executable as bytes from dist directory
#[cfg(target_os = "windows")]
static BACKEND_EXE: &[u8] = include_bytes!("../../dist/yt-transcriptor-backend.exe");

#[cfg(not(target_os = "windows"))]
static BACKEND_EXE: &[u8] = include_bytes!("../../dist/yt-transcriptor-backend");


// Application state to manage the backend process
#[derive(Clone)]
struct AppState {
    backend_process: Arc<Mutex<Option<Child>>>,
    temp_backend_path: Arc<Mutex<Option<PathBuf>>>,
}

impl AppState {
    fn new() -> Self {
        AppState {
            backend_process: Arc::new(Mutex::new(None)),
            temp_backend_path: Arc::new(Mutex::new(None)),
        }
    }

    fn cleanup_existing_backend_processes() -> Result<(), String> {
        println!("Checking for existing backend processes...");

        #[cfg(target_os = "windows")]
        {
            // On Windows, kill any existing yt-transcriptor-backend.exe processes
            let output = Command::new("tasklist")
                .args(&["/FI", "IMAGENAME eq yt-transcriptor-backend.exe", "/FO", "CSV"])
                .output()
                .map_err(|e| format!("Failed to list processes: {}", e))?;

            let output_str = String::from_utf8_lossy(&output.stdout);
            if output_str.contains("yt-transcriptor-backend.exe") {
                println!("Found existing backend processes, terminating them...");

                let kill_output = Command::new("taskkill")
                    .args(&["/F", "/IM", "yt-transcriptor-backend.exe"])
                    .output()
                    .map_err(|e| format!("Failed to kill processes: {}", e))?;

                if kill_output.status.success() {
                    println!("Successfully terminated existing backend processes");
                } else {
                    println!("Warning: Failed to terminate some processes: {}",
                        String::from_utf8_lossy(&kill_output.stderr));
                }
            }
        }

        #[cfg(not(target_os = "windows"))]
        {
            // On Unix systems, kill any existing yt-transcriptor-backend processes
            let output = Command::new("pgrep")
                .arg("-f")
                .arg("yt-transcriptor-backend")
                .output();

            if let Ok(output) = output {
                if !output.stdout.is_empty() {
                    let pids = String::from_utf8_lossy(&output.stdout)
                        .lines()
                        .filter_map(|line| line.trim().parse().ok())
                        .collect::<Vec<_>>();

                    for pid in pids {
                        println!("Terminating backend process with PID: {}", pid);
                        let _ = Command::new("kill")
                            .arg("-9")
                            .arg(pid.to_string())
                            .output();
                    }
                }
            }
        }

        // Wait a moment for processes to terminate
        thread::sleep(Duration::from_millis(500));
        Ok(())
    }

    #[cfg_attr(debug_assertions, allow(unused_variables))]
    fn start_backend(&self, _app_handle: &AppHandle) -> Result<String, String> {
        // First check if backend is already responding
        if let Ok(client) = reqwest::blocking::Client::builder()
            .timeout(std::time::Duration::from_secs(2))
            .build() {
            if let Ok(response) = client.get("http://127.0.0.1:8031/health").send() {
                if response.status().is_success() {
                    println!("Backend is already running and responding");
                    return Ok("http://127.0.0.1:8031".to_string());
                }
            }
        }

        // Check if process is already running
        if let Ok(mut process_guard) = self.backend_process.lock() {
            if let Some(child) = process_guard.as_mut() {
                if let Ok(None) = child.try_wait() {
                    // Process is still running
                    return Ok("http://127.0.0.1:8031".to_string());
                }
            }
        }

        // Clean up existing processes
        Self::cleanup_existing_backend_processes()?;

        #[cfg(debug_assertions)]
        {
            // In development mode, start backend using uv
            println!("Starting Python backend in development mode");

            // Get the project root directory (two levels up from src-tauri)
            let current_dir = std::env::current_dir()
                .map_err(|e| format!("Failed to get current directory: {}", e))?;
            let project_root = current_dir
                .parent()
                .and_then(|p| p.parent())
                .ok_or("Failed to find project root")?;

            println!("Project root: {:?}", project_root);

            Command::new("uv")
                .arg("run")
                .arg("python")
                .arg("-m")
                .arg("uvicorn")
                .arg("src.web_app:app")
                .args(&[
                    "--host", "127.0.0.1",
                    "--port", "8031"
                ])
                .current_dir(project_root)
                .spawn()
                .map_err(|e| format!("Failed to start Python backend: {}", e))?;
        }

        #[cfg(not(debug_assertions))]
        {
            // In production mode, extract and run embedded backend
            println!("Starting embedded Python backend");

            let temp_dir = std::env::temp_dir();
            let backend_filename = if cfg!(target_os = "windows") {
                "yt-transcriptor-backend.exe"
            } else {
                "yt-transcriptor-backend"
            };

            let temp_backend_path = temp_dir.join(backend_filename);

            // Store temp path for cleanup
            if let Ok(mut path_guard) = self.temp_backend_path.lock() {
                *path_guard = Some(temp_backend_path.clone());
            }

            println!("Extracting embedded backend to: {:?}", temp_backend_path);

            // Write embedded backend to temp file
            std::fs::write(&temp_backend_path, BACKEND_EXE)
                .map_err(|e| format!("Failed to extract backend executable: {}", e))?;

            // Make it executable on Unix systems
            #[cfg(not(target_os = "windows"))]
            {
                use std::os::unix::fs::PermissionsExt;
                let mut perms = std::fs::metadata(&temp_backend_path)
                    .map_err(|e| format!("Failed to get backend metadata: {}", e))?
                    .permissions();
                perms.set_mode(0o755);
                std::fs::set_permissions(&temp_backend_path, perms)
                    .map_err(|e| format!("Failed to set executable permissions: {}", e))?;
            }

            println!("Starting embedded backend from: {:?}", temp_backend_path);
            println!("Backend file size: {} bytes", BACKEND_EXE.len());

            if !temp_backend_path.exists() {
                return Err(format!(
                    "Backend executable not found at {:?}",
                    temp_backend_path
                ));
            }

            println!("Attempting to start embedded backend process...");
            let mut cmd = Command::new(&temp_backend_path);

            // Hide console window on Windows
            #[cfg(target_os = "windows")]
            {
                use std::os::windows::process::CommandExt;
                cmd.creation_flags(0x08000000); // CREATE_NO_WINDOW
            }

            let child = cmd.spawn()
                .map_err(|e| format!("Failed to start embedded backend: {}", e))?;

            // Store the process handle
            if let Ok(mut process_guard) = self.backend_process.lock() {
                *process_guard = Some(child);
            }

            println!("Embedded backend process started successfully");
        }

        // Wait for backend to be ready
        self.wait_for_backend_ready()
    }

    fn wait_for_backend_ready(&self) -> Result<String, String> {
        let client = reqwest::blocking::Client::new();
        let health_url = "http://127.0.0.1:8031/health";

        // Try to connect for up to 10 seconds
        for _ in 0..20 {
            thread::sleep(Duration::from_millis(500));
            if let Ok(response) = client.get(health_url).send() {
                if response.status().is_success() {
                    return Ok("http://127.0.0.1:8031".to_string());
                }
            }
        }

        Err("Backend failed to start within timeout".to_string())
    }

    fn stop_backend(&self) -> Result<(), String> {
        if let Ok(mut process_guard) = self.backend_process.lock() {
            if let Some(mut child) = process_guard.take() {
                println!("Stopping Python backend gracefully...");

                // First attempt: request graceful shutdown via HTTP
                println!("Sending graceful shutdown request...");
                match reqwest::blocking::Client::new()
                    .post("http://127.0.0.1:8031/shutdown")
                    .timeout(Duration::from_secs(2))
                    .send()
                {
                    Ok(_) => {
                        println!("Graceful shutdown request sent, waiting for backend to exit...");
                        // Wait up to 5 seconds for graceful shutdown
                        for i in 1..=10 {
                            thread::sleep(Duration::from_millis(500));
                            if let Ok(Some(_status)) = child.try_wait() {
                                println!("Backend gracefully stopped after {}s", i as f32 * 0.5);
                                return Ok(());
                            }
                        }
                    }
                    Err(e) => {
                        println!("Failed to send graceful shutdown request: {}, forcing termination", e);
                    }
                }

                // Second attempt: force termination
                #[cfg(target_os = "windows")]
                {
                    let pid = child.id();
                    println!("Force killing backend process tree...");
                    let kill_result = Command::new("taskkill")
                        .args(&["/F", "/T", "/PID", &pid.to_string()])
                        .output();

                    match kill_result {
                        Ok(output) => {
                            if output.status.success() {
                                println!("Backend process tree force terminated successfully");
                            } else {
                                println!("Warning: Force kill failed: {}",
                                    String::from_utf8_lossy(&output.stderr));
                            }
                        }
                        Err(e) => println!("Error during force kill: {}", e),
                    }
                }

                #[cfg(not(target_os = "windows"))]
                {
                    println!("Sending SIGKILL to backend process...");
                    match child.kill() {
                        Ok(_) => println!("SIGKILL sent to backend process"),
                        Err(e) => println!("Failed to send SIGKILL: {}", e),
                    }
                }

                // Final wait for process exit
                match child.wait() {
                    Ok(status) => println!("Backend process exited with status: {}", status),
                    Err(e) => println!("Backend process exit error: {}", e),
                }
            }
        }

        // Clean up temporary backend file
        if let Ok(mut path_guard) = self.temp_backend_path.lock() {
            if let Some(temp_path) = path_guard.take() {
                if temp_path.exists() {
                    println!("Cleaning up temporary backend file: {:?}", temp_path);
                    if let Err(e) = std::fs::remove_file(&temp_path) {
                        println!("Warning: Failed to cleanup temporary file: {}", e);
                    } else {
                        println!("Temporary backend file cleaned up successfully");
                    }
                }
            }
        }

        Ok(())
    }
}

fn check_backend_status_sync() -> bool {
    match reqwest::blocking::Client::new()
        .get("http://127.0.0.1:8031/health")
        .timeout(Duration::from_secs(2))
        .send()
    {
        Ok(response) => response.status().is_success(),
        Err(_) => false,
    }
}

#[tauri::command]
async fn check_backend_status() -> bool {
    check_backend_status_sync()
}

#[tauri::command]
async fn get_backend_url(state: State<'_, AppState>, app_handle: AppHandle) -> Result<String, String> {
    state.start_backend(&app_handle)
}

#[tauri::command]
async fn restart_backend(state: State<'_, AppState>, app_handle: AppHandle) -> Result<String, String> {
    state.stop_backend()?;
    thread::sleep(Duration::from_millis(500));
    state.start_backend(&app_handle)
}

#[tauri::command]
async fn stop_backend_for_update(state: State<'_, AppState>) -> Result<(), String> {
    state.stop_backend()
}

#[tauri::command]
async fn save_file(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content)
        .map_err(|e| format!("Failed to save file: {}", e))
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_single_instance::init(|_app, argv, cwd| {
            println!("Single instance triggered: argv={:?}, cwd={:?}", argv, cwd);
        }))
        .setup(|app| {
            let app_state = AppState::new();

            // Start the backend
            app_state.start_backend(app.handle())?;

            // Start health monitoring
            let app_handle = app.handle().clone();
            let app_state_clone = app_state.clone();
            thread::spawn(move || {
                thread::sleep(Duration::from_secs(2)); // Wait for initial backend startup

                loop {
                    thread::sleep(Duration::from_secs(10));

                    if !check_backend_status_sync() {
                        println!("Backend health check failed, attempting restart...");

                        match app_state_clone.stop_backend() {
                            Ok(_) => println!("Backend stopped successfully"),
                            Err(e) => println!("Error stopping backend: {}", e),
                        }

                        thread::sleep(Duration::from_millis(500));

                        match app_state_clone.start_backend(&app_handle) {
                            Ok(_) => {
                                println!("Backend restarted successfully");
                                // Emit event to frontend
                                let _ = app_handle.emit("backend-status", "restarted");
                            }
                            Err(e) => {
                                println!("Failed to restart backend: {}", e);
                                let _ = app_handle.emit("backend-status", "failed");
                            }
                        }
                    }
                }
            });

            app.manage(app_state);

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            check_backend_status,
            get_backend_url,
            restart_backend,
            stop_backend_for_update,
            save_file
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
