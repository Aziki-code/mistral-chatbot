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
            const currentBlockNumber = codeBlockCounter; // Capture the current value
            
            const indicator = document.createElement('div');
            indicator.className = 'message assistant';
            const codeTag = document.createElement('span');
            codeTag.className = 'code-indicator';
            codeTag.textContent = `📝 Code #${currentBlockNumber}`;
            codeTag.dataset.targetId = `code-block-${currentBlockNumber}`;
            codeTag.onclick = () => {
                const targetBlock = document.getElementById(`code-block-${currentBlockNumber}`);
                if (targetBlock) {
                    // Scroll to the code block in the right panel
                    const codeOutput = document.getElementById('code-output');
                    const blockOffset = targetBlock.offsetTop - codeOutput.offsetTop;
                    codeOutput.scrollTo({
                        top: blockOffset,
                        behavior: 'smooth'
                    });
                    
                    // Add ripple effect
                    targetBlock.classList.add('highlight');
                    setTimeout(() => {
                        targetBlock.classList.remove('highlight');
                    }, 1000);
                }
            };
            indicator.appendChild(document.createTextNode('Code output → '));
            indicator.appendChild(codeTag);
            chat.appendChild(indicator);

            // Add code block to right panel
            const wrapper = document.createElement('div');
            wrapper.className = 'codeblock';
            wrapper.id = `code-block-${currentBlockNumber}`;
            
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

            // Create header with language label and copy button
            const header = document.createElement('div');
            header.className = 'code-header';

            const langLabel = document.createElement('span');
            langLabel.className = 'code-language';
            langLabel.textContent = detectedLang.toUpperCase();

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

            header.appendChild(langLabel);
            header.appendChild(copyBtn);
            
            wrapper.appendChild(header);
            wrapper.appendChild(feedback);
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
    setTimeout(() => {
        chat.scrollTop = chat.scrollHeight;
    }, 50);
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
        // Increment counter and add code permanently to left panel
        pastedCodeCounter++;
        const detectedLang = detectLanguage(msg);
        addPastedCode(msg, detectedLang, pastedCodeCounter);
        document.getElementById('input-panel').classList.add('visible');
        
        const currentPastedNumber = pastedCodeCounter; // Capture the current value
        
        // Add indicator in chat with clickable reference
        const indicator = document.createElement('div');
        indicator.className = 'message user';
        
        const codeTag = document.createElement('span');
        codeTag.className = 'code-indicator';
        codeTag.textContent = `📝 Code #${currentPastedNumber}`;
        codeTag.dataset.targetId = `pasted-code-${currentPastedNumber}`;
        codeTag.onclick = () => {
            const targetBlock = document.getElementById(`pasted-code-${currentPastedNumber}`);
            if (targetBlock) {
                // Scroll to the code block in the left panel
                const pastedOutput = document.getElementById('pasted-code-output');
                const blockOffset = targetBlock.offsetTop - pastedOutput.offsetTop;
                pastedOutput.scrollTo({
                    top: blockOffset,
                    behavior: 'smooth'
                });
                
                // Add ripple effect
                targetBlock.classList.add('highlight');
                setTimeout(() => {
                    targetBlock.classList.remove('highlight');
                }, 1000);
            }
        };
        
        indicator.appendChild(document.createTextNode('Code input ← '));
        indicator.appendChild(codeTag);
        chat.appendChild(indicator);
    } else {
        // Normal text message
        appendMessage('user', msg);
    }
    input.value = '';

    // Get selected AI model
    const aiModelDropdown = document.getElementById('ai-model-dropdown');
    const selectedModel = aiModelDropdown ? aiModelDropdown.value : 'mistral';

    try {
        // Create abort controller for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minute timeout

        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: msg,
                ai_model: selectedModel
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`HTTP ${res.status}: ${errorText || res.statusText}`);
        }

        const data = await res.json();
        appendMessage('assistant', data.response);
    } catch(err) {
        if (err.name === 'AbortError') {
            appendMessage('assistant', '⏱️ Request timeout - The AI is taking too long to respond. Please try again with a shorter message.');
        } else {
            appendMessage('assistant', `❌ Error: ${err.message || 'Failed to connect to server'}`);
        }
    }
}

async function uploadScreenshotFile(file) {
    const formData = new FormData();
    formData.append('screendump', file);

    appendMessage('user', '[Uploaded screenshot]');

    // Add timeout for upload
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutes

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`HTTP ${res.status}: ${errorText || res.statusText}`);
        }

        const data = await res.json();
        appendMessage('assistant', data.response);

        const blobUrl = URL.createObjectURL(file);
        appendMessage('assistant', blobUrl, true);
    } catch(err) {
        clearTimeout(timeoutId);
        if (err.name === 'AbortError') {
            appendMessage('assistant', 'Upload timed out after 2 minutes. Please try again.');
        } else {
            appendMessage('assistant', 'Upload error: ' + err.message);
        }
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

    // Create header with language label and copy button
    const header = document.createElement('div');
    header.className = 'code-header';

    const langLabel = document.createElement('span');
    langLabel.className = 'code-language';
    langLabel.textContent = `#${counter} ${(language || 'plaintext').toUpperCase()}`;

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

    header.appendChild(langLabel);
    header.appendChild(copyBtn);

    const pre = document.createElement('pre');
    pre.style.maxHeight = `${chatHeight - 40}px`;
    const code = document.createElement('code');

    const prismLang = getPrismLanguage(language || '');
    pre.className = `language-${prismLang}`;
    code.className = `language-${prismLang}`;
    code.textContent = content;

    pre.appendChild(code);
    wrapper.appendChild(header);
    wrapper.appendChild(feedback);
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
