# 🏗️ Modular Architecture Documentation

## New File Structure

```
AzikiAI-codingbot/
├── 🌐 main.py                    # Flask web server (LDAP + routes)
├── 🎯 bot_manager.py             # Bot Manager orchestrator
├── 📦 base_bot.py                # Abstract base class for all bots
├── 🤖 mistral_bot.py             # Mistral AI specific implementation
├── 💻 github_copilot_bot.py      # GitHub Copilot specific implementation
├── 🧪 bot.py                     # Test script
└── 📋 github_copilot_client.py  # (DEPRECATED - no longer used)
```

---

## 📚 Module Descriptions

### **bot_manager.py** - Central Orchestrator
**Responsibility:** Initializes and manages all AI bots

```python
# Singleton pattern - one global bot manager
bot_manager = get_bot_manager()

# BotManager class:
# - initialize_all()          → Starts all bots
# - get_bot(bot_id)          → Get specific bot
# - get_default_bot()        → Get default bot
# - is_bot_available(bot_id) → Check availability
# - chat(bot_id, messages)   → Send chat request
```

**Key Features:**
- ✅ Singleton pattern for global access
- ✅ Automatic initialization on import
- ✅ Can run standalone for testing: `python main.py`
- ✅ Centralized bot management

---

### **base_bot.py** - Abstract Interface
**Responsibility:** Defines common contract for all bots

```python
class BaseBot(ABC):
    @abstractmethod
    def initialize() -> bool:
        """Initialize bot with API credentials"""
        
    @abstractmethod
    def chat_complete(messages, model) -> str:
        """Send chat completion request"""
        
    @property
    def is_available() -> bool:
        """Check if bot is ready"""
```

**Design Pattern:** Template Method Pattern
- All bots MUST implement these methods
- Uniform interface = polymorphism = easy to add new bots

---

### **mistral_bot.py** - Mistral AI Implementation
**Responsibility:** Mistral AI logic only

```python
class MistralBot(BaseBot):
    def __init__(self, api_key=None):
        # Read MISTRAL_API_KEY from env if not provided
        
    def initialize(self) -> bool:
        # Import mistralai library
        # Create Mistral client
        # Return success/failure
        
    def chat_complete(self, messages, model) -> str:
        # Call Mistral API
        # Return response text
```

**Isolation:** 
- No dependencies on GitHub code
- Only Mistral-specific logic
- Error handling isolated

---

### **github_copilot_bot.py** - GitHub Copilot Implementation
**Responsibility:** GitHub Copilot logic only

```python
class GitHubCopilotBot(BaseBot):
    def __init__(self, github_token=None):
        # Read GITHUB_TOKEN from env if not provided
        
    def initialize(self) -> bool:
        # Validate GitHub token
        # Setup HTTP headers
        # Return success/failure
        
    def chat_complete(self, messages, model) -> str:
        # Map model names (mistral → gpt-4o)
        # Try primary GitHub endpoint
        # Fallback to Azure endpoint
        # Return response text
```

**Features:**
- ✅ Model name mapping
- ✅ Multi-endpoint fallback
- ✅ Detailed error messages

---

### **main.py** - Flask Web Server
**Responsibility:** Web interface, LDAP auth, routing

```python
# INITIALIZATION
bot_manager = get_bot_manager()  # Get singleton

# ROUTES
@app.route("/")
def index():
    # Pass bot availability to template
    return render_template(
        mistral_available=bot_manager.is_bot_available("mistral"),
        github_available=bot_manager.is_bot_available("github-copilot")
    )

@app.route("/chat")
def chat():
    ai_model = request.json["ai_model"]  # "mistral" or "github-copilot"
    
    # Get response via bot manager
    response = bot_manager.chat(
        bot_id=ai_model,
        messages=history
    )
```

**Changes from before:**
- ❌ No direct client initialization
- ❌ No if/else for bot selection
- ✅ Uses bot_manager for everything
- ✅ Much simpler code

---

## 🔄 Execution Flow

### Startup Sequence:
```
1. Flask starts main.py
2. Import bot_manager.py
3. get_bot_manager() called first time
4. BotManager.__init__()
5. BotManager.initialize_all()
   ├─ Load .env
   ├─ MistralBot() → initialize()
   └─ GitHubCopilotBot() → initialize()
6. Flask routes are ready
```

### Chat Request Flow:
```
User → Frontend JS
    ↓ fetch('/chat', {ai_model: "mistral"})
Flask Route Handler
    ↓ bot_manager.chat("mistral", messages)
BotManager
    ↓ self.bots["mistral"]
MistralBot
    ↓ chat_complete(messages)
Mistral API
    ↓ response text
← Back to user
```

---

## 🎯 Design Patterns Used

| Pattern | Where | Purpose |
|---------|-------|---------|
| **Singleton** | `BotManager` in main.py | One global bot manager instance |
| **Abstract Base Class** | `BaseBot` | Define common interface |
| **Template Method** | `BaseBot` methods | Subclasses implement details |
| **Factory** | `get_bot_manager()` | Encapsulate complex initialization |
| **Strategy** | Runtime bot selection | Choose algorithm dynamically |
| **Dependency Injection** | Flask → BotManager | Loose coupling |

---

## ✅ Advantages of New Structure

### 1. **Separation of Concerns**
```
base_bot.py         → Interface definition
mistral_bot.py      → Mistral implementation
github_copilot_bot.py → GitHub implementation
bot_manager.py      → Orchestration
main.py             → Web layer
```

### 2. **Easy to Extend**
Add new AI provider (e.g., Claude):
```python
# 1. Create claude_bot.py
class ClaudeBot(BaseBot):
    def initialize(self): ...
    def chat_complete(self): ...

# 2. Add in bot_manager.py
claude = ClaudeBot()
if claude.is_available:
    self.bots["claude"] = claude

# 3. Add in frontend dropdown
<option value="claude">🤖 Claude AI</option>

# DONE! ✓
```

### 3. **Better Testing**
```python
# Mock a bot without affecting others
def test_mistral():
    bot = MistralBot(api_key="test_key")
    assert bot.initialize() == True
    
# Test bot manager in isolation
def test_manager():
    manager = BotManager()
    assert len(manager.bots) >= 1
```

### 4. **Error Isolation**
```python
# If Mistral fails, GitHub still works
try:
    mistral = MistralBot()
except:
    pass  # Ignore - GitHub is still available

# If NO bots start
if not self.bots:
    raise RuntimeError("No bots available")
```

### 5. **Code Reuse**
```python
# Common logic in BaseBot
class BaseBot:
    def get_display_name(self):
        return f"{self.icon} {self.name}"

# All subclasses inherit automatically
mistral.get_display_name()  # "🤖 Mistral AI"
github.get_display_name()   # "💻 GitHub Copilot"
```

---

## 🚀 How to Run

### Test Bots Individually:
```bash
# Test bot manager
python bot_manager.py

# Test in web context
python bot.py

# Start web server
python main.py
```

### Output Example:
```
============================================================
Initializing AI Chatbots...
============================================================
✓ Mistral AI initialized successfully
✓ GitHub Copilot initialized successfully
============================================================
✓ 2 bot(s) initialized
  Available: 🤖 Mistral AI, 💻 GitHub Copilot
  Default: 🤖 Mistral AI
============================================================
```

---

## 📊 Before vs. After

### BEFORE (Monolithic):
```python
# main.py had EVERYTHING:
- Mistral initialization
- GitHub initialization
- if/else bot selection
- Error handling for each bot
- Model mapping
- HTTP requests

# 308 lines, mixed responsibilities
```

### AFTER (Modular):
```python
# main.py:
bot_manager = get_bot_manager()
response = bot_manager.chat(bot_id, messages)

# 40 lines, one responsibility (web routing)

# Logic spread across 5 modules:
base_bot.py           - 65 lines
mistral_bot.py        - 110 lines  
github_copilot_bot.py - 180 lines
bot_manager.py        - 210 lines
main.py               - Web routing
```

**Total:** More code, but each file has ONE responsibility! 🎯

---

## 🎓 Conclusion

New structure follows **SOLID principles:**
- ✅ **S**ingle Responsibility - Each module has one job
- ✅ **O**pen/Closed - Open for new bots, closed for changes
- ✅ **L**iskov Substitution - All bots are interchangeable
- ✅ **I**nterface Segregation - Minimal interface in BaseBot
- ✅ **D**ependency Inversion - Flask depends on abstraction

This makes the code:
- 📖 Easier to read
- 🧪 Easier to test
- 🔧 Easier to maintain
- 🚀 Easier to extend

```
AzikiAI-codingbot/
├── 🌐 main.py                    # Flask web server (LDAP + routes)
├── 🎯 bot_manager.py             # Bot Manager orchestrator
├── 📦 base_bot.py                # Abstract base class for alle bots
├── 🤖 mistral_bot.py             # Mistral AI specifik implementation
├── 💻 github_copilot_bot.py      # GitHub Copilot specifik implementation
├── 🧪 bot.py                     # Test script
└── 📋 github_copilot_client.py  # (DEPRECATED - ikke længere brugt)
```

---

## 📚 Modul Beskrivelser

### **bot_manager.py** - Central Orchestrator
**Ansvar:** Initialiserer og håndterer alle AI bots

```python
# Singleton pattern - én global bot manager
bot_manager = get_bot_manager()

# BotManager class:
# - initialize_all()          → Starter alle bots
# - get_bot(bot_id)          → Hent specifik bot
# - get_default_bot()        → Hent default bot
# - is_bot_available(bot_id) → Tjek tilgængelighed
# - chat(bot_id, messages)   → Send chat request
```

**Nøgle Features:**
- ✅ Singleton pattern for global adgang
- ✅ Automatisk initialization ved import
- ✅ Kan køres standalone for test: `python main.py`
- ✅ Centraliseret bot management

---

### **base_bot.py** - Abstract Interface
**Ansvar:** Definerer fælles contract for alle bots

```python
class BaseBot(ABC):
    @abstractmethod
    def initialize() -> bool:
        """Initialize bot med API credentials"""
        
    @abstractmethod
    def chat_complete(messages, model) -> str:
        """Send chat completion request"""
        
    @property
    def is_available() -> bool:
        """Check if bot er klar"""
```

**Design Pattern:** Template Method Pattern
- Alle bots SKAL implementere disse metoder
- Ensartet interface = polymorfi = nemt at tilføje nye bots

---

### **mistral_bot.py** - Mistral AI Implementation
**Ansvar:** Kun Mistral AI logik

```python
class MistralBot(BaseBot):
    def __init__(self, api_key=None):
        # Læs MISTRAL_API_KEY fra env hvis ikke givet
        
    def initialize(self) -> bool:
        # Import mistralai library
        # Opret Mistral client
        # Return success/failure
        
    def chat_complete(self, messages, model) -> str:
        # Call Mistral API
        # Return response text
```

**Isolation:** 
- Ingen afhængigheder til GitHub kode
- Kun Mistral-specifik logik
- Error handling isoleret

---

### **github_copilot_bot.py** - GitHub Copilot Implementation
**Ansvar:** Kun GitHub Copilot logik

```python
class GitHubCopilotBot(BaseBot):
    def __init__(self, github_token=None):
        # Læs GITHUB_TOKEN fra env hvis ikke givet
        
    def initialize(self) -> bool:
        # Validate GitHub token
        # Setup HTTP headers
        # Return success/failure
        
    def chat_complete(self, messages, model) -> str:
        # Map model names (mistral → gpt-4o)
        # Try primary GitHub endpoint
        # Fallback til Azure endpoint
        # Return response text
```

**Features:**
- ✅ Model name mapping
- ✅ Multi-endpoint fallback
- ✅ Detailed error messages

---

### **main.py** - Flask Web Server
**Ansvar:** Web interface, LDAP auth, routing

```python
# INITIALIZATION
bot_manager = get_bot_manager()  # Få singleton

# ROUTES
@app.route("/")
def index():
    # Pass bot availability til template
    return render_template(
        mistral_available=bot_manager.is_bot_available("mistral"),
        github_available=bot_manager.is_bot_available("github-copilot")
    )

@app.route("/chat")
def chat():
    ai_model = request.json["ai_model"]  # "mistral" eller "github-copilot"
    
    # Get response via bot manager
    response = bot_manager.chat(
        bot_id=ai_model,
        messages=history
    )
```

**Ændringer fra før:**
- ❌ Ingen direkte client initialization
- ❌ Ingen if/else for bot selection
- ✅ Bruger bot_manager for alt
- ✅ Meget simplere kode

---

## 🔄 Execution Flow

### Startup Sequence:
```
1. Flask starter main.py
2. Import bot_manager.py
3. get_bot_manager() kaldes første gang
4. BotManager.__init__()
5. BotManager.initialize_all()
   ├─ Load .env
   ├─ MistralBot() → initialize()
   └─ GitHubCopilotBot() → initialize()
6. Flask routes er klar
```

### Chat Request Flow:
```
User → Frontend JS
    ↓ fetch('/chat', {ai_model: "mistral"})
Flask Route Handler
    ↓ bot_manager.chat("mistral", messages)
BotManager
    ↓ self.bots["mistral"]
MistralBot
    ↓ chat_complete(messages)
Mistral API
    ↓ response text
← Tilbage til user
```

---

## 🎯 Design Patterns Brugt

| Pattern | Hvor | Formål |
|---------|------|--------|
| **Singleton** | `BotManager` i main.py | Én global bot manager instance |
| **Abstract Base Class** | `BaseBot` | Definer fælles interface |
| **Template Method** | `BaseBot` metoder | Subclasses implementerer detaljer |
| **Factory** | `get_bot_manager()` | Enkapsulér complex initialization |
| **Strategy** | Runtime bot valg | Vælg algoritme dynamisk |
| **Dependency Injection** | Flask → BotManager | Loose coupling |

---

## ✅ Fordele ved Ny Struktur

### 1. **Separation of Concerns**
```
base_bot.py         → Interface definition
mistral_bot.py      → Mistral implementation
github_copilot_bot.py → GitHub implementation
main.py             → Orchestration
chatbot_sql.py      → Web layer
```

### 2. **Nem at Udvide**
Tilføj ny AI provider (f.eks. Claude):
```python
# 1. Opret claude_bot.py
class ClaudeBot(BaseBot):
    def initialize(self): ...
    def chat_complete(self): ...

# 2. Tilføj i bot_manager.py
claude = ClaudeBot()
if claude.is_available:
    self.bots["claude"] = claude

# 3. Tilføj i frontend dropdown
<option value="claude">🤖 Claude AI</option>

# DONE! ✓
```

### 3. **Bedre Testing**
```python
# Mock en bot uden at påvirke andre
def test_mistral():
    bot = MistralBot(api_key="test_key")
    assert bot.initialize() == True
    
# Test bot manager isoleret
def test_manager():
    manager = BotManager()
    assert len(manager.bots) >= 1
```

### 4. **Fejl Isolation**
```python
# Hvis Mistral fejler, GitHub virker stadig
try:
    mistral = MistralBot()
except:
    pass  # Ignore - GitHub er stadig tilgængelig

# Hvis INGEN bots starter
if not self.bots:
    raise RuntimeError("No bots available")
```

### 5. **Kode Reuse**
```python
# Fælles logik i BaseBot
class BaseBot:
    def get_display_name(self):
        return f"{self.icon} {self.name}"

# Alle subclasses arver automatisk
mistral.get_display_name()  # "🤖 Mistral AI"
github.get_display_name()   # "💻 GitHub Copilot"
```

---

## 🚀 Hvordan Kører Det?

### Test Bots Individuelt:
```bash
# Test bot manager
python bot_manager.py

# Test i web context
python bot.py

# Start web server
python main.py
```

### Output Eksempel:
```
============================================================
Initializing AI Chatbots...
============================================================
✓ Mistral AI initialized successfully
✓ GitHub Copilot initialized successfully
============================================================
✓ 2 bot(s) initialized
  Available: 🤖 Mistral AI, 💻 GitHub Copilot
  Default: 🤖 Mistral AI
============================================================
```

---

## 📊 Før vs. Efter

### FØR (Monolitisk):
```python
# main.py (chatbot_sql.py) havde ALT:
- Mistral initialization
- GitHub initialization
- if/else bot selection
- Error handling for hver bot
- Model mapping
- HTTP requests

# 308 linjer, blandet ansvar
```

### EFTER (Modular):
```python
# main.py:
bot_manager = get_bot_manager()
response = bot_manager.chat(bot_id, messages)

# 40 linjer, ét ansvar (web routing)

# Logik spredt i 5 moduler:
base_bot.py           - 65 linjer
mistral_bot.py        - 110 linjer  
github_copilot_bot.py - 180 linjer
bot_manager.py        - 210 linjer
main.py               - Web routing
```

**Total:** Mere kode, men hver fil har ÉT ansvar! 🎯

---

## 🎓 Konklusion

Ny struktur følger **SOLID principper:**
- ✅ **S**ingle Responsibility - Hver modul har ét job
- ✅ **O**pen/Closed - Åben for nye bots, lukket for ændringer
- ✅ **L**iskov Substitution - Alle bots er udskiftelige
- ✅ **I**nterface Segregation - Minimal interface i BaseBot
- ✅ **D**ependency Inversion - Flask afhænger af abstraktion

Dette gør koden:
- 📖 Lettere at læse
- 🧪 Lettere at teste
- 🔧 Lettere at vedligeholde
- 🚀 Lettere at udvide
