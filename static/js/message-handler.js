// Message handling - append, send, display

// Global state
let codeBlockCounter = 0;
let pastedCodeCounter = 0;

// DOM elements (initialized in ui-handlers.js)
let chat, codeOutput, pastedCodeOutput, input;

function appendMessage(role, text, isImage = false) {
    if (!text || text.trim() === '') return;

    const blocks = isImage ? [{type: 'image', content: text}] : parseMessage(text);

    blocks.forEach(block => {
        if (block.type === 'text') {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.innerHTML = escapeHtml(block.content).replace(/\n/g, '<br>');
            chat.appendChild(div);
        } else if (block.type === 'code') {
            // NEVER show code in chat - only show indicator
            codeBlockCounter++;
            
            const indicator = document.createElement('div');
            indicator.className = 'message assistant';
            const codeTag = document.createElement('span');
            codeTag.className = 'code-indicator';
            codeTag.textContent = `📝 Code #${codeBlockCounter}`;
            codeTag.onclick = () => {
                document.getElementById(`code-block-${codeBlockCounter}`).scrollIntoView({behavior: 'smooth'});
            };
            indicator.appendChild(document.createTextNode('Code output → '));
            indicator.appendChild(codeTag);
            chat.appendChild(indicator);

            // Add code block to right panel
            const wrapper = document.createElement('div');
            wrapper.className = 'codeblock';
            wrapper.id = `code-block-${codeBlockCounter}`;
            
            // Set max-height based on chat window height
            const chatHeight = chat.offsetHeight;
            wrapper.style.maxHeight = `${chatHeight}px`;

            const pre = document.createElement('pre');
            pre.style.maxHeight = `${chatHeight - 40}px`;
            const code = document.createElement('code');

            // Auto-detect Cisco if not specified or if plaintext
            let detectedLang = block.language || '';
            
            // Try Cisco detection even if bash/plaintext/text is specified (AI often uses wrong language)
            if (!detectedLang || detectedLang === 'plaintext' || detectedLang === 'text' || detectedLang === '' || detectedLang === 'bash' || detectedLang === 'shell') {
                const ciscoDetected = detectCiscoInContent(block.content);
                if (ciscoDetected) {
                    detectedLang = ciscoDetected;
                } else {
                    // Keep original language if no Cisco patterns found
                    detectedLang = detectedLang || 'plaintext';
                }
            }

            const prismLang = getPrismLanguage(detectedLang);
            
            pre.className = `language-${prismLang}`;
            code.className = `language-${prismLang}`;

            const safeContent = block.content.replace(/```/g, '``\\`');
            code.textContent = safeContent;

            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.textContent = 'Copy';

            const feedback = document.createElement('div');
            feedback.className = 'copy-feedback';
            feedback.textContent = 'Copied!';

            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(block.content)
                    .then(() => {
                        feedback.classList.add('show');
                        setTimeout(() => feedback.classList.remove('show'), 2000);
                    });
            });

            pre.appendChild(copyBtn);
            pre.appendChild(feedback);
            pre.appendChild(code);
            wrapper.appendChild(pre);
            codeOutput.appendChild(wrapper);
            document.getElementById('right-panel').classList.add('visible');

            if (typeof Prism !== 'undefined' && Prism.highlightElement) {
                requestAnimationFrame(() => {
                    try {
                        Prism.highlightElement(code);
                    } catch(e) { /* ignore */ }
                });
            }
        } else if (block.type === 'image') {
            const img = document.createElement('img');
            img.className = 'screenshot';
            img.src = block.content;
            chat.appendChild(img);
        }
    });

    // Scroll to bottom after adding new message
    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    // Check if message contains code block with backticks
    const hasCodeBlock = msg.includes('```');
    
    // Also check if it's Cisco config without backticks (auto-detect)
    const lowerMsg = msg.toLowerCase();
    const isCiscoConfig = (msg.match(/^[\w.-]+[#>]/m) || 
                          lowerMsg.includes('interface ') || 
                          lowerMsg.includes('switchport ') ||
                          lowerMsg.includes('ip address') ||
                          (lowerMsg.includes('vlan') && msg.includes('!'))) &&
                          msg.split('\n').length > 3; // Multiple lines
    
    if (hasCodeBlock || isCiscoConfig) {
        // Code already shown in left panel by input listener
        // Add indicator to chat
        appendMessage('user', '← Code Input');
    } else {
        // Normal text message
        appendMessage('user', msg);
    }
    input.value = '';

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: msg})
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        const data = await res.json();
        appendMessage('assistant', data.response);
    } catch(err) {
        appendMessage('assistant', 'Error connecting to server: ' + err.message);
    }
}

async function uploadScreenshotFile(file) {
    const formData = new FormData();
    formData.append('screendump', file);

    appendMessage('user', '[Uploaded screenshot]');

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        const data = await res.json();
        appendMessage('assistant', data.response);

        const blobUrl = URL.createObjectURL(file);
        appendMessage('assistant', blobUrl, true);
    } catch(err) {
        appendMessage('assistant', 'Upload error: ' + err.message);
    }
}

function addPastedCode(content, language, counter) {
    const wrapper = document.createElement('div');
    wrapper.className = 'codeblock';
    wrapper.id = `pasted-code-${counter}`;
    wrapper.style.marginBottom = '15px';
    
    // Set max-height based on chat window height
    const chatHeight = chat.offsetHeight;
    wrapper.style.maxHeight = `${chatHeight}px`;

    const header = document.createElement('div');
    header.style.fontSize = '11px';
    header.style.color = '#666';
    header.style.marginBottom = '5px';
    header.textContent = `#${counter} (${language || 'plaintext'})`;

    const pre = document.createElement('pre');
    pre.style.maxHeight = `${chatHeight - 40}px`;
    const code = document.createElement('code');

    const prismLang = getPrismLanguage(language || '');
    pre.className = `language-${prismLang}`;
    code.className = `language-${prismLang}`;
    code.textContent = content;

    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'Copy';

    const feedback = document.createElement('div');
    feedback.className = 'copy-feedback';
    feedback.textContent = 'Copied!';

    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(content)
            .then(() => {
                feedback.classList.add('show');
                setTimeout(() => feedback.classList.remove('show'), 2000);
            });
    });

    pre.appendChild(copyBtn);
    pre.appendChild(feedback);
    pre.appendChild(code);
    wrapper.appendChild(header);
    wrapper.appendChild(pre);
    pastedCodeOutput.appendChild(wrapper);

    // Use same highlighting method as right panel for consistency
    if (typeof Prism !== 'undefined' && Prism.highlightElement) {
        requestAnimationFrame(() => {
            try {
                Prism.highlightElement(code);
            } catch(e) { /* ignore */ }
        });
    }

    pastedCodeOutput.scrollTop = pastedCodeOutput.scrollHeight;
}
