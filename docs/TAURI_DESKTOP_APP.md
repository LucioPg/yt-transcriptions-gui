# Tauri Desktop Application

This document describes the Tauri desktop application that provides a complete, self-contained YouTube Transcriptor experience.

## Overview

The Tauri application is now the primary desktop interface for YouTube Transcriptor, automatically managing the Python backend internally while providing the exact same look and feel as the original web interface.

## Architecture

### Components

1. **Rust Frontend Wrapper** (`src-tauri/`)
   - Main application entry point
   - Manages the desktop window (1000x800, resizable)
   - Automatically starts and manages Python backend process
   - Finds available ports dynamically (18000-18999 range)
   - Handles system integration and lifecycle management

2. **Static Web Assets** (`web-dist/`)
   - Contains the HTML, CSS, and JavaScript interface
   - Communicates with dynamically assigned backend port
   - Provides fallback for development mode
   - Integrates with Tauri's invoke API for backend communication

3. **Python Backend** (integrated, managed by Rust)
   - FastAPI application automatically started by Rust wrapper
   - Runs on dynamically assigned port (not default 8000)
   - Handles YouTube transcript extraction and file downloads
   - Managed as subprocess of Tauri application

### Key Features

- **Self-Contained Application**: No external backend required - everything managed internally
- **Dynamic Port Management**: Automatically finds and uses available ports (18000-18999 range)
- **Automatic Backend Lifecycle**: Backend starts when needed, stops when app closes
- **Same UI**: Exact same appearance and functionality as the web version
- **Native Desktop Integration**: Proper window controls, system integration, and native feel
- **Cross-platform**: Works on Windows, macOS, and Linux with single binary
- **Small Bundle Size**: Lightweight compared to Electron alternatives
- **Development Fallback**: Can still run in development mode with external backend

## File Structure

```
src-tauri/
├── src/
│   ├── main.rs          # Main Rust application
│   └── lib.rs           # Library wrapper
├── Cargo.toml           # Rust dependencies
├── tauri.conf.json      # Tauri configuration
├── build.rs             # Build script
└── icons/               # Application icons

web-dist/
└── index.html           # Static web interface
```

## Configuration

### Tauri Configuration (`tauri.conf.json`)

- **Window Settings**: 1000x800 default size, resizable, minimum 800x600
- **Title**: "YouTube Transcriptor"
- **Static Frontend**: Uses `../web-dist` as frontend directory
- **No Dev Server**: Configured for static file serving

### Dependencies

- `tauri = "2.9.3"` - Main Tauri framework
- `serde` - JSON serialization
- `tokio` - Async runtime
- `reqwest` - HTTP client for backend communication

## Usage

### Development

To run the application in development mode:

```bash
# Run Tauri in development mode (will start backend automatically)
npm run tauri:dev
```

### Building

To build the application for distribution:

```bash
npm run tauri:build
```

The built application will be available in:
- Windows: `src-tauri/target/release/yt-transcriptor.exe`
- macOS: `src-tauri/target/release/bundle/macos/YouTube Transcriptor.app`
- Linux: `src-tauri/target/release/bundle/appimage/yt-transcriptor.AppImage`

### Running the Built Application

The Tauri application is completely self-contained:

1. Simply run the built executable (no external backend required)
2. The application will automatically:
   - Start the Python backend internally
   - Find an available port dynamically
   - Initialize the web interface
   - Handle all cleanup on exit

### Development Mode with External Backend (Optional)

For development purposes, you can still run with an external backend:

1. Start external backend:
   ```bash
   uv run python -m uvicorn src.web_app:app --host 127.0.0.1 --port 8000
   ```

2. Open `web-dist/index.html` in a browser (fallback mode)

The frontend will automatically detect if it's running in Tauri and use the appropriate backend management.

## Technical Details

### Frontend-Backend Communication

The static HTML/JavaScript frontend communicates with the Python backend using the standard `fetch()` API:

```javascript
// Example API call
const response = await fetch(`${API_BASE}/extract`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams(data)
});
```

### Error Handling

- Backend connectivity warnings are displayed on page load
- Network errors are gracefully handled with user-friendly messages
- Download links are automatically converted to absolute URLs

### Security Considerations

- Backend runs locally on `127.0.0.1:8000`
- No external network access required for the frontend
- Standard web security model applies

## Comparison with Web Version

| Feature | Web Version | Tauri Version |
|---------|-------------|----------------|
| UI/UX | Browser-based | Native desktop window |
| Backend | Same FastAPI server | Same FastAPI server |
| Functionality | Full transcript extraction | Full transcript extraction |
| Distribution | User opens browser | Standalone executable |
| Installation | None required | Single executable |
| Updates | Manual | Manual rebuild |

## Troubleshooting

### Common Issues

1. **Backend Not Running**: The app will show a warning if the Python backend is not accessible at `http://127.0.0.1:8000`

2. **Compilation Errors**: Ensure all Rust dependencies are properly installed and the Rust toolchain is up to date

3. **Window Size**: If the window appears too small, resize it or check the window configuration in `tauri.conf.json`

### Debugging

- Enable developer tools in Tauri for debugging the frontend
- Check console output for backend communication issues
- Verify the Python backend is running and accessible

## Future Improvements

Potential enhancements for the Tauri application:

1. **Integrated Backend**: Bundle the Python backend within the Tauri application
2. **Automatic Backend Management**: Start/stop the Python backend from the Rust code
3. **System Tray Integration**: Add system tray functionality
4. **Auto-updates**: Implement automatic update mechanism
5. **Offline Mode**: Cache commonly used transcripts

## Deployment

### Windows

- Build the executable using `npm run tauri:build`
- The resulting `.exe` file can be distributed directly
- Consider creating an installer for better user experience

### macOS

- Build produces a `.app` bundle
- Code signing is required for distribution outside the App Store
- Notarization needed for macOS Gatekeeper compliance

### Linux

- Produces an AppImage by default
- Can also create .deb or .rpm packages
- Consider distribution through package managers

## Resources

- [Tauri Documentation](https://tauri.app/)
- [Rust Book](https://doc.rust-lang.org/book/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)