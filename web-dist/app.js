// YouTube Transcriptor Frontend Application

// Tauri API for backend management
const invoke = window.__TAURI__?.invoke;

// DOM elements
const mainForm = document.getElementById('mainForm');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const transcriptForm = document.getElementById('transcriptForm');
const newExtractionBtn = document.getElementById('newExtraction');

let API_BASE = '';
let backendMonitorInterval = null;
let isBackendHealthy = false;

// Initialize backend and get URL
async function initializeBackend() {
    try {
        if (invoke) {
            // Running in Tauri environment
            API_BASE = await invoke('get_backend_url');
            console.log('Backend started on:', API_BASE);
        } else {
            // Fallback for development - use port 8031
            API_BASE = 'http://127.0.0.1:8031';
            console.warn('Not running in Tauri, using fallback:', API_BASE);
        }

        // Start backend monitoring
        startBackendMonitoring();

    } catch (error) {
        console.error('Failed to initialize backend:', error);
        showError('Impossibile avviare il backend Python. Si prega di riavviare l\'applicazione.');
        return false;
    }
    return true;
}

// Backend monitoring and auto-recovery
function startBackendMonitoring() {
    if (backendMonitorInterval) {
        clearInterval(backendMonitorInterval);
    }

    backendMonitorInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/health`, {
                method: 'GET',
                timeout: 5000
            });

            if (response.ok) {
                if (!isBackendHealthy) {
                    isBackendHealthy = true;
                    showNotification('Backend ripristinato', 'success');
                }
            } else {
                throw new Error('Health check failed');
            }
        } catch (error) {
            if (isBackendHealthy) {
                isBackendHealthy = false;
                showNotification('Backend non raggiungibile. Tentativo di ripristino...', 'warning');
                attemptBackendRecovery();
            }
        }
    }, 10000); // Check every 10 seconds
}

// Attempt to recover backend
async function attemptBackendRecovery() {
    try {
        if (invoke) {
            // Try to restart backend in Tauri environment
            const newUrl = await invoke('restart_backend');
            API_BASE = newUrl;
            showNotification('Backend riavviato con successo', 'success');
            isBackendHealthy = true;
        } else {
            // In development mode, just show warning
            showNotification('Backend crash in development mode. Riavvia manualmente il backend.', 'error');
        }
    } catch (error) {
        console.error('Failed to restart backend:', error);
        showNotification('Impossibile ripristinare il backend automaticamente', 'error');
    }
}

// Show notification to user
function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotification = document.querySelector('.backend-notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `backend-notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 10 seconds for success/info, 30 seconds for warning/error
    const timeout = type === 'success' || type === 'info' ? 10000 : 30000;
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, timeout);
}

// Form submission
transcriptForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(transcriptForm);
    const data = Object.fromEntries(formData);

    showLoading();

    try {
        const formData = new FormData();
        formData.append('url', data.url);
        formData.append('format_type', data.format_type);
        if (data.language) {
            formData.append('language', data.language);
        }

        const response = await fetch(`${API_BASE}/api/transcript`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Format the result for display
            const resultHtml = `
                <div class="result-container">
                    <div class="video-info">
                        <h3>📹 ${result.video_title}</h3>
                        <div class="stats">
                            <div class="stat-item">
                                <strong>Formato</strong><br>
                                ${data.format_type.toUpperCase()}
                            </div>
                            <div class="stat-item">
                                <strong>File salvato</strong><br>
                                ${result.filename}
                            </div>
                        </div>
                    </div>
                    <h3>📝 Trascrizione</h3>
                    <div class="transcript-content">${result.transcript}</div>
                    <div class="download-section">
                        <button onclick="downloadTranscript('${result.filename}', '${result.transcript}', '${data.format_type}')" class="primary">
                            💾 Scarica ${data.format_type.toUpperCase()}
                        </button>
                        <a href="#" id="newExtraction" class="primary-link">← Nuova estrazione</a>
                    </div>
                </div>
            `;
            showResults(resultHtml, true);
        } else {
            showError(result.error || 'Errore del server: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Impossibile connettersi al backend. Assicurati che il backend sia in esecuzione.');
    }
});

// New extraction button
newExtractionBtn.addEventListener('click', (e) => {
    e.preventDefault();
    showMainForm();
});

function showLoading() {
    mainForm.style.display = 'none';
    results.style.display = 'none';
    loading.style.display = 'block';
}

function showMainForm() {
    mainForm.style.display = 'block';
    results.style.display = 'none';
    loading.style.display = 'none';
    transcriptForm.reset();
}

function showResults(content, success) {
    mainForm.style.display = 'none';
    loading.style.display = 'none';
    results.style.display = 'block';
    results.innerHTML = content;

    // Fix download links to use absolute URLs
    const downloadLinks = results.querySelectorAll('a[href^="/download/"]');
    downloadLinks.forEach(link => {
        link.href = API_BASE + link.getAttribute('href');
    });

    // Fix home links
    const homeLinks = results.querySelectorAll('a[href="/"]');
    homeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            showMainForm();
        });
    });
}

function downloadTranscript(filename, content, format) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function showError(message) {
    showResults(`
        <div class="error-message">
            <h3>❌ Si è verificato un errore</h3>
            <p><strong>Errore di connessione</strong></p>
            <p>${message}</p>
            <div style="margin-top: 1rem;">
                <button onclick="location.reload()" class="primary">
                    ↻ Riavvia Applicazione
                </button>
            </div>
        </div>
    `, false);
}

// Initialize application
document.addEventListener('DOMContentLoaded', async () => {
    const initialized = await initializeBackend();
    if (!initialized) {
        return; // Error already shown by initializeBackend
    }

    // Check backend status
    try {
        let isHealthy;
        if (invoke) {
            isHealthy = await invoke('check_backend_status', { url: API_BASE });
        } else {
            const response = await fetch(`${API_BASE}/health`);
            isHealthy = response.ok;
        }

        if (!isHealthy) {
            console.warn('Backend health check failed');
        }
    } catch (error) {
        console.warn('Backend not accessible:', error);
        // Show a warning but allow the user to continue
        const warning = document.createElement('div');
        warning.className = 'form-container';
        warning.style.borderColor = 'var(--del-border-color)';
        warning.innerHTML = `
            <h4>⚠️ Attenzione</h4>
            <p>Il backend Python non è attualmente accessibile.</p>
            <p><strong>Tentativo di connessione:</strong> ${API_BASE}</p>
        `;
        mainForm.insertBefore(warning, mainForm.firstChild);
    }
});