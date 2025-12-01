// AI Model Selector - Initialize and manage AI model dropdown

(function() {
    'use strict';

    function initAISelector() {
        const dropdown = document.getElementById('ai-model-dropdown');
        if (!dropdown) return;

        // Update dropdown options based on availability
        const options = [];
        
        if (window.mistralAvailable) {
            options.push({value: 'mistral', text: '🤖 Mistral AI'});
        }
        
        if (window.githubAvailable) {
            options.push({value: 'github-copilot', text: '💻 GitHub Copilot'});
        }

        // Clear and populate dropdown
        dropdown.innerHTML = '';
        options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt.value;
            option.textContent = opt.text;
            dropdown.appendChild(option);
        });

        // Restore previous selection from localStorage, or default to Mistral AI
        const savedModel = localStorage.getItem('selectedAIModel');
        if (savedModel && dropdown.querySelector(`option[value="${savedModel}"]`)) {
            dropdown.value = savedModel;
        } else {
            // Default to Mistral AI if available
            dropdown.value = window.mistralAvailable ? 'mistral' : (options[0]?.value || 'mistral');
        }

        // If only one option, disable dropdown
        if (options.length === 1) {
            dropdown.disabled = true;
            dropdown.style.opacity = '0.7';
        }

        // Add visual feedback on change
        dropdown.addEventListener('change', function() {
            const modelName = this.options[this.selectedIndex].text;
            
            // Show brief notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 60px;
                right: 20px;
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 10px 20px;
                border-radius: 5px;
                z-index: 10000;
                font-family: monospace;
                animation: fadeInOut 2s ease-in-out;
            `;
            notification.textContent = `Switched to ${modelName}`;
            document.body.appendChild(notification);

            setTimeout(() => {
                notification.remove();
            }, 2000);
        });

        // Save selection to localStorage
        dropdown.addEventListener('change', function() {
            localStorage.setItem('selectedAIModel', this.value);
        });
    }

    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInOut {
            0% { opacity: 0; transform: translateY(-10px); }
            20% { opacity: 1; transform: translateY(0); }
            80% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-10px); }
        }
    `;
    document.head.appendChild(style);

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAISelector);
    } else {
        initAISelector();
    }
})();
