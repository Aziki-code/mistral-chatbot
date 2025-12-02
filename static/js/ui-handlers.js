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
    
    // Scroll chat to bottom on load - multiple attempts to ensure it works
    const scrollToBottom = () => {
        if (chat) {
            chat.scrollTop = chat.scrollHeight;
        }
    };
    
    // Immediate scroll
    scrollToBottom();
    
    // Delayed scrolls to handle async content
    setTimeout(scrollToBottom, 50);
    setTimeout(scrollToBottom, 200);
    setTimeout(scrollToBottom, 500);

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

    // Input listener for pasted code detection - only for preview
    let lastPreviewedCode = '';
    input.addEventListener('input', e => {
        const value = e.target.value.trim();
        if (value.length > 20) { // Only show if more than 20 chars
            const detectedLang = detectLanguage(value);
            
            // Only show pasted code panel if actual code was detected
            if (detectedLang && value !== lastPreviewedCode) {
                // Show live preview of what will be pasted (doesn't affect counter)
                lastPreviewedCode = value;
                document.getElementById('input-panel').classList.add('visible');
            } else if (!detectedLang) {
                // Not code
                lastPreviewedCode = '';
                if (pastedCodeCounter === 0) {
                    document.getElementById('input-panel').classList.remove('visible');
                }
            }
        } else if (value.length === 0) {
            lastPreviewedCode = '';
            if (pastedCodeCounter === 0) {
                document.getElementById('input-panel').classList.remove('visible');
            }
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
