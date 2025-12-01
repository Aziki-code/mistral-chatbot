// UI event handlers and initialization

function initializeUI() {
    // Initialize DOM elements
    chat = document.getElementById("chat");
    codeOutput = document.getElementById("code-output");
    pastedCodeOutput = document.getElementById("pasted-code-output");
    input = document.getElementById("input");
    const send = document.getElementById("send");
    const upload = document.getElementById("upload");
    const uploadBtn = document.getElementById("uploadBtn");

    // Initialize themes
    initThemes();

    // Send button click
    send.onclick = sendMessage;

    // Enter key to send (Shift+Enter for newline)
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Upload button
    uploadBtn.onclick = () => {
        if (upload.files.length) uploadScreenshotFile(upload.files[0]);
    };

    // Input listener for pasted code detection
    input.addEventListener('input', e => {
        const value = e.target.value.trim();
        if (value.length > 20) { // Only show if more than 20 chars
            const detectedLang = detectLanguage(value);
            
            // Only show pasted code panel if actual code was detected
            if (detectedLang) {
                pastedCodeOutput.innerHTML = '';
                pastedCodeCounter = 1;
                addPastedCode(value, detectedLang, pastedCodeCounter);
                document.getElementById('input-panel').classList.add('visible');
            } else {
                // Not code, hide panel
                pastedCodeOutput.innerHTML = '';
                document.getElementById('input-panel').classList.remove('visible');
            }
        } else if (value.length === 0) {
            pastedCodeOutput.innerHTML = '';
            document.getElementById('input-panel').classList.remove('visible');
        }
    });

    // Paste from clipboard (images)
    document.addEventListener('paste', e => {
        const items = e.clipboardData.items;
        for (let item of items) {
            if (item.type.indexOf('image') !== -1) {
                const file = item.getAsFile();
                uploadScreenshotFile(file);
            }
        }
    });

    // Focus input on load
    input.focus();

    // Update code block heights when window resizes
    window.addEventListener('resize', () => {
        const chatHeight = chat.offsetHeight;
        document.querySelectorAll('.codeblock').forEach(block => {
            block.style.maxHeight = `${chatHeight}px`;
            const pre = block.querySelector('pre');
            if (pre) {
                pre.style.maxHeight = `${chatHeight - 40}px`;
            }
        });
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUI);
} else {
    initializeUI();
}
