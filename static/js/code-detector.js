// Code language detection utilities

function normalizeNewlines(src) {
    return src.replace(/\r\n?/g, "\n");
}

function getPrismLanguage(lang) {
    const map = {
        html: 'markup',
        xml: 'markup',
        js: 'javascript',
        py: 'python',
        python: 'python',
        cpp: 'cpp',
        c: 'c',
        java: 'java',
        css: 'css',
        json: 'json',
        bash: 'bash',
        sh: 'bash',
        shell: 'bash',
        sql: 'sql',
        cisco: 'cisco',
        ios: 'cisco',
        plaintext: 'plaintext',
        text: 'plaintext',
        '': 'plaintext'
    };
    return map[lang.toLowerCase()] || 'plaintext';
}

function detectCiscoConfig(value) {
    // Check for Cisco IOS config - ONLY if it looks like actual config (not description)
    // Must have prompt at start of line AND config commands
    const hasPrompt = value.match(/^[\w-]+[#>]\s/m);
    const hasConfigCommands = value.match(/^(interface|switchport|ip address|router|crypto|access-list|!\s)/m);
    
    return hasPrompt && hasConfigCommands;
}

function detectLanguage(value) {
    // Auto-detect language from content
    let detectedLang = null; // null = not code, just text
    
    // Check for ACTUAL code fences at line start, not just backticks anywhere
    const hasCodeFence = /^\s*```/m.test(value);
    
    if (hasCodeFence) {
        // If it has code fences, parse and use the language
        const blocks = parseMessage(value);
        if (blocks.length > 0 && blocks[0].type === 'code') {
            detectedLang = blocks[0].language || 'javascript';
        }
    } else {
        // Better language detection - check in order (most specific first)
        const lowerValue = value.toLowerCase();
        
        if (detectCiscoConfig(value)) {
            detectedLang = 'cisco';
        }
        // Check HTML first - very specific tags
        else if (lowerValue.includes('<!doctype') || lowerValue.includes('<html') || lowerValue.includes('<head') || lowerValue.includes('</html>')) {
            detectedLang = 'html';
        } else if (value.match(/[#\.]\w+\s*\{/) || (value.includes('{') && value.includes('}') && value.includes(':') && value.includes(';') && value.split('\n').length > 2)) {
            detectedLang = 'css';
        } else if ((value.includes('def ') && value.includes(':')) || (value.includes('import ') && !value.includes('import {')) || value.includes('print(') || value.includes('self.')) {
            detectedLang = 'python';
        } else if (value.includes('SELECT ') || value.includes('INSERT INTO') || value.includes('CREATE TABLE')) {
            detectedLang = 'sql';
        }
    }
    
    return detectedLang;
}

function detectCiscoInContent(content) {
    // Auto-detect Cisco if not specified or if plaintext
    // Try Cisco detection even if bash/plaintext/text is specified (AI often uses wrong language)
    const lowerContent = content.toLowerCase();
    
    // Force Cisco detection if content matches Cisco patterns
    if (lowerContent.match(/^[\w.-]+[#>]/m) || 
        lowerContent.includes('interface ') || 
        lowerContent.includes('switchport ') ||
        lowerContent.includes('ip address') ||
        lowerContent.includes('gigabitethernet') ||
        lowerContent.includes('fastethernet') ||
        lowerContent.includes('ethernet') ||
        (lowerContent.includes('vlan') && content.includes('!'))) {
        return 'cisco';
    }
    
    return null;
}
