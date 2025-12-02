// Theme definitions and management

const themes = {
    vscode: {
        '--bg-darkest': '#1e1e1e',
        '--bg-dark': '#252526',
        '--bg-medium': '#2d2d30',
        '--border-color': '#3e3e42',
        '--text-primary': '#cccccc',
        '--text-secondary': '#6a6a6a',
        '--accent-primary': '#4ec9b0',
        '--accent-secondary': '#ce9178',
        '--button-primary': '#0e639c',
        '--button-primary-hover': '#1177bb',
        '--button-secondary': '#4ec9b0',
        '--scrollbar-thumb': '#424242',
        '--scrollbar-thumb-hover': '#4e4e4e',
        prismTheme: 'tomorrow'
    },
    monokai: {
        '--bg-darkest': '#1e1e1e',
        '--bg-dark': '#272822',
        '--bg-medium': '#3e3d32',
        '--border-color': '#49483e',
        '--text-primary': '#f8f8f2',
        '--text-secondary': '#75715e',
        '--accent-primary': '#a6e22e',
        '--accent-secondary': '#f92672',
        '--button-primary': '#ae81ff',
        '--button-primary-hover': '#c49dff',
        '--button-secondary': '#a6e22e',
        '--scrollbar-thumb': '#49483e',
        '--scrollbar-thumb-hover': '#5a5950',
        prismTheme: 'okaidia'
    },
    dracula: {
        '--bg-darkest': '#21222c',
        '--bg-dark': '#282a36',
        '--bg-medium': '#343746',
        '--border-color': '#44475a',
        '--text-primary': '#f8f8f2',
        '--text-secondary': '#6272a4',
        '--accent-primary': '#8be9fd',
        '--accent-secondary': '#ff79c6',
        '--button-primary': '#bd93f9',
        '--button-primary-hover': '#caa7ff',
        '--button-secondary': '#50fa7b',
        '--scrollbar-thumb': '#44475a',
        '--scrollbar-thumb-hover': '#565869',
        prismTheme: 'okaidia'
    },
    nord: {
        '--bg-darkest': '#2e3440',
        '--bg-dark': '#3b4252',
        '--bg-medium': '#434c5e',
        '--border-color': '#4c566a',
        '--text-primary': '#eceff4',
        '--text-secondary': '#616e88',
        '--accent-primary': '#88c0d0',
        '--accent-secondary': '#d08770',
        '--button-primary': '#5e81ac',
        '--button-primary-hover': '#81a1c1',
        '--button-secondary': '#a3be8c',
        '--scrollbar-thumb': '#4c566a',
        '--scrollbar-thumb-hover': '#5a6680',
        prismTheme: 'twilight'
    },
    solarized: {
        '--bg-darkest': '#002b36',
        '--bg-dark': '#073642',
        '--bg-medium': '#094656',
        '--border-color': '#0d5766',
        '--text-primary': '#839496',
        '--text-secondary': '#586e75',
        '--accent-primary': '#2aa198',
        '--accent-secondary': '#cb4b16',
        '--button-primary': '#268bd2',
        '--button-primary-hover': '#3a9ce3',
        '--button-secondary': '#859900',
        '--scrollbar-thumb': '#0d5766',
        '--scrollbar-thumb-hover': '#11697a',
        prismTheme: 'solarizedlight'
    },
    github: {
        '--bg-darkest': '#0d1117',
        '--bg-dark': '#161b22',
        '--bg-medium': '#21262d',
        '--border-color': '#30363d',
        '--text-primary': '#c9d1d9',
        '--text-secondary': '#8b949e',
        '--accent-primary': '#58a6ff',
        '--accent-secondary': '#f85149',
        '--button-primary': '#238636',
        '--button-primary-hover': '#2ea043',
        '--button-secondary': '#58a6ff',
        '--scrollbar-thumb': '#30363d',
        '--scrollbar-thumb-hover': '#484f58',
        prismTheme: 'tomorrow'
    },
    cisco: {
        '--bg-darkest': '#505050',
        '--bg-dark': '#505050',
        '--bg-medium': '#585858',
        '--border-color': '#707070',
        '--text-primary': '#00ffff',
        '--text-secondary': '#00d7ff',
        '--accent-primary': '#00ffff',
        '--accent-secondary': '#00d7ff',
        '--button-primary': '#006b7a',
        '--button-primary-hover': '#008a9c',
        '--button-secondary': '#00ffff',
        '--scrollbar-thumb': '#707070',
        '--scrollbar-thumb-hover': '#808080',
        prismTheme: 'tomorrow'
    },
    light: {
        '--bg-darkest': '#ffffff',
        '--bg-dark': '#f5f5f5',
        '--bg-medium': '#e8e8e8',
        '--border-color': '#d0d0d0',
        '--text-primary': '#2c3e50',
        '--text-secondary': '#7f8c8d',
        '--accent-primary': '#3498db',
        '--accent-secondary': '#e74c3c',
        '--button-primary': '#3498db',
        '--button-primary-hover': '#2980b9',
        '--button-secondary': '#2ecc71',
        '--scrollbar-thumb': '#bdc3c7',
        '--scrollbar-thumb-hover': '#95a5a6',
        prismTheme: 'solarizedlight',
        lightTheme: true
    },
    'light-quiet': {
        '--bg-darkest': '#f5f0f5',
        '--bg-dark': '#f0e8f0',
        '--bg-medium': '#e8dce8',
        '--border-color': '#c8b8c8',
        '--text-primary': '#4a3a4a',
        '--text-secondary': '#8b7b9b',
        '--accent-primary': '#b08bc0',
        '--accent-secondary': '#d88ba8',
        '--button-primary': '#b8a8c8',
        '--button-primary-hover': '#9b8bab',
        '--button-secondary': '#c8a8d8',
        '--scrollbar-thumb': '#b4a4c4',
        '--scrollbar-thumb-hover': '#9688a6',
        prismTheme: 'quietlight',
        lightTheme: true
    }
};

function applyTheme(themeName) {
    const theme = themes[themeName];
    if (!theme) return;
    
    const root = document.documentElement;
    Object.keys(theme).forEach(key => {
        if (key !== 'prismTheme' && key !== 'lightTheme') {
            root.style.setProperty(key, theme[key]);
        }
    });
    
    // Add theme class to body for special styling
    document.body.className = themeName;
    
    // Handle Kali watermark filter for light theme
    const watermark = document.querySelector('body::before') || document.body;
    if (theme.lightTheme) {
        // Light theme: dark gray dragon on white background
        document.body.setAttribute('data-light-theme', 'true');
    } else {
        // Dark theme: keep original filter
        document.body.removeAttribute('data-light-theme');
    }
    
    // Update browser theme color for all browsers (Chrome, Edge, Firefox, Safari)
    // Remove old meta tags and create new ones (some browsers don't respect setAttribute)
    const oldMetaTags = document.querySelectorAll('meta[name="theme-color"], meta[name="msapplication-navbutton-color"]');
    oldMetaTags.forEach(tag => tag.remove());
    
    const themeColor = theme['--bg-darkest'];
    
    // Add fresh meta tags
    const head = document.querySelector('head');
    
    // Standard theme-color
    const metaThemeColor = document.createElement('meta');
    metaThemeColor.name = 'theme-color';
    metaThemeColor.content = themeColor;
    head.appendChild(metaThemeColor);
    
    // MS Edge/IE
    const metaMsNav = document.createElement('meta');
    metaMsNav.name = 'msapplication-navbutton-color';
    metaMsNav.content = themeColor;
    head.appendChild(metaMsNav);
    
    // Update body background and html background for full browser integration
    document.body.style.backgroundColor = themeColor;
    document.documentElement.style.backgroundColor = themeColor;
    
    // Update Prism theme or enable custom Cisco theme
    const prismLink = document.querySelector('link[href*="prism"]');
    const ciscoTheme = document.getElementById('cisco-prism-theme');
    const quietLightTheme = document.getElementById('quiet-light-prism-theme');
    
    if (themeName === 'cisco' && ciscoTheme) {
        // Enable custom Cisco theme
        if (prismLink) prismLink.disabled = true;
        if (ciscoTheme) ciscoTheme.disabled = false;
        if (quietLightTheme) quietLightTheme.disabled = true;
    } else if (themeName === 'light-quiet' && quietLightTheme) {
        // Enable custom Quiet Light theme
        if (prismLink) prismLink.disabled = true;
        if (ciscoTheme) ciscoTheme.disabled = true;
        if (quietLightTheme) quietLightTheme.disabled = false;
    } else {
        // Use standard Prism theme
        if (ciscoTheme) ciscoTheme.disabled = true;
        if (quietLightTheme) quietLightTheme.disabled = true;
        if (prismLink) {
            prismLink.disabled = false;
            prismLink.href = `https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-${theme.prismTheme}.min.css`;
        }
    }
    
    // Re-highlight all code blocks
    setTimeout(() => {
        if (typeof Prism !== 'undefined') {
            document.querySelectorAll('pre code').forEach(block => {
                // Remove existing highlighting
                block.removeAttribute('class');
                block.className = block.parentElement.className.replace('line-numbers', '').trim();
                
                // Re-highlight
                if (Prism.highlightElement) {
                    Prism.highlightElement(block);
                }
            });
        }
    }, 150);
    
    // Save preference
    localStorage.setItem('chatbot-theme', themeName);
}

function initThemes() {
    const themeDropdown = document.getElementById('theme-dropdown');
    
    // Always reset to Cisco theme on page load (ignore saved theme)
    const defaultTheme = 'cisco';
    themeDropdown.value = defaultTheme;
    applyTheme(defaultTheme);

    // Theme change event
    themeDropdown.addEventListener('change', (e) => {
        applyTheme(e.target.value);
    });
}
