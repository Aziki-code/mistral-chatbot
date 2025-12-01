// Message parsing utilities

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
}

function parseMessage(text) {
    // State-machine parser that only treats fences at line start as delimiters
    const blocks = [];
    const src = normalizeNewlines(text);
    const lines = src.split('\n');
    let inCode = false;
    let lang = 'plaintext';
    let codeLines = [];
    let textBuffer = [];

    function flushText() {
        if (textBuffer.length) {
            const t = textBuffer.join('\n').trim();
            if (t) blocks.push({type: 'text', content: t});
            textBuffer = [];
        }
    }

    function flushCode() {
        if (codeLines.length) {
            blocks.push({type: 'code', language: lang || 'plaintext', content: codeLines.join('\n')});
            codeLines = [];
            lang = 'plaintext';
        }
    }

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const fenceMatch = line.match(/^\s*```\s*(.*)$/); // only consider fences at line start
        if (fenceMatch) {
            if (!inCode) {
                // opening fence
                flushText();
                lang = (fenceMatch[1] || '').trim();
                inCode = true;
            } else {
                // closing fence
                flushCode();
                inCode = false;
            }
            continue;
        }
        if (inCode) {
            codeLines.push(line);
        } else {
            textBuffer.push(line);
        }
    }

    // Flush any remaining content
    if (inCode) {
        // Unclosed code fence: treat remaining as code
        flushCode();
    } else {
        flushText();
    }

    return blocks;
}
