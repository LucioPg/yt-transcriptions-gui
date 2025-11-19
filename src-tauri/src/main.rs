// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Stdio};
use std::sync::Mutex;
use std::thread;
use std::time::Duration;

// Backend process management
struct PythonBackend {
    port: u16,
    child: Option<std::process::Child>,
    restart_attempts: u32,
    max_restart_attempts: u32,
}

impl PythonBackend {
    fn new() -> Self {
        Self {
            port: 8031,
            child: None,
            restart_attempts: 0,
            max_restart_attempts: 5,
        }
    }

    fn start(&mut self) -> Result<String, String> {
        if self.child.is_some() {
            return Ok(format!("http://127.0.0.1:{}", self.port));
        }

        // Use fixed port 8031
        self.port = 8031;

        // Check if port is available
        if !self.is_port_available(self.port) {
            return Err("Port 8031 is not available".to_string());
        }

        // Start the Python backend on port 8031
        let child = self.start_backend_process()
            .map_err(|e| format!("Failed to start Python backend: {}", e))?;

        self.child = Some(child);

        // Wait for backend to be ready
        let backend_url = format!("http://127.0.0.1:{}", self.port);
        self.wait_for_backend(&backend_url)?;

        Ok(backend_url)
    }

    fn start_backend_process(&self) -> Result<std::process::Child, String> {
        Command::new("python")
            .arg("-c")
            .arg(&format!(
                r#"
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import uvicorn
from web_app import app

# Run on specific port 8031
uvicorn.run(app, host="127.0.0.1", port=8031, log_level="warning")
"#
            ))
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| format!("Failed to start Python backend: {}", e))
    }

    fn is_port_available(&self, port: u16) -> bool {
        // Simple check by trying to bind to the port
        use std::net::TcpListener;
        let addr = format!("127.0.0.1:{}", port);
        TcpListener::bind(addr).is_ok()
    }

    
    fn restart_backend(&mut self) -> Result<String, String> {
        if self.restart_attempts >= self.max_restart_attempts {
            return Err("Maximum restart attempts reached".to_string());
        }

        self.restart_attempts += 1;

        // Kill existing child if exists
        if let Some(mut child) = self.child.take() {
            let _ = child.kill();
        }

        // Wait a bit before restarting
        thread::sleep(Duration::from_secs(2));

        // Start new backend
        self.start()
    }

    fn wait_for_backend(&self, backend_url: &str) -> Result<(), String> {
        let client = reqwest::blocking::Client::new();
        let health_url = format!("{}/health", backend_url);

        // Try to connect for up to 10 seconds
        for _ in 0..20 {
            thread::sleep(Duration::from_millis(500));
            if let Ok(response) = client.get(&health_url).send() {
                if response.status().is_success() {
                    return Ok(());
                }
            }
        }

        Err("Backend failed to start within timeout".to_string())
    }
}

impl Drop for PythonBackend {
    fn drop(&mut self) {
        if let Some(mut child) = self.child.take() {
            let _ = child.kill();
        }
    }
}

#[tauri::command]
async fn get_backend_url(backend: tauri::State<'_, Mutex<PythonBackend>>) -> Result<String, String> {
    let mut backend = backend.lock().map_err(|e| format!("Failed to lock backend: {}", e))?;
    backend.start()
}

#[tauri::command]
async fn restart_backend(backend: tauri::State<'_, Mutex<PythonBackend>>) -> Result<String, String> {
    let mut backend = backend.lock().map_err(|e| format!("Failed to lock backend: {}", e))?;
    backend.restart_backend()
}

#[tauri::command]
async fn check_backend_status(url: String) -> Result<bool, String> {
    let client = reqwest::Client::new();
    match client.get(&format!("{}/health", url)).send().await {
        Ok(response) => Ok(response.status().is_success()),
        Err(_) => Ok(false),
    }
}

fn main() {
    let python_backend = PythonBackend::new();

    tauri::Builder::default()
        .manage(Mutex::new(python_backend))
        .setup(|_app| {
            // Backend will be started when the frontend requests it
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![get_backend_url, restart_backend, check_backend_status])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}