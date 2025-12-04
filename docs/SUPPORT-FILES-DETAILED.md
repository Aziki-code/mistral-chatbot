# Support Files - Detaljeret Dokumentation

Dokumentation for supportfiler der ikke er del af hovedapplikationen: startup scripts og test scripts.

---

## start.sh - Portable Startup Script

### Fil Information
- **Type**: Bash shell script
- **Størrelse**: 31 linjer
- **Formål**: Automatisk setup og launch af Flask chatbot
- **Platform**: Linux/macOS (bruger bash)

---

## Shebang (Linje 1)

```bash
#!/bin/bash
```
- **#!/bin/bash** - Shebang (specifies interpreter)
- **Why bash?** Universal on Linux/macOS, supports modern scripting
- **Execution**: Makes file executable (`chmod +x start.sh`)

---

## Header Comment (Linje 2)

```bash
# Portable startup script for Mistral Chatbot
```
- **"Portable"** - Runs on any Linux/macOS without modification
- **"Mistral Chatbot"** - Legacy name (now AzikiAI with Mistral Vision)

---

## Script Directory Detection (Linje 4-5)

```bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
```

### Line 4: Get Script Location
```bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
```

#### Breakdown
1. **${BASH_SOURCE[0]}** - Path to current script
   - Example: `/home/kasperadm/projects/AzikiAI-codingbot/start.sh`
2. **dirname** - Extract directory
   - Result: `/home/kasperadm/projects/AzikiAI-codingbot`
3. **cd** - Change to that directory
4. **pwd** - Print working directory (absolute path)
5. **$( ... )** - Command substitution (capture output)
6. **SCRIPT_DIR=** - Store in variable

#### Why This Pattern?
- **Portable** - Works if script called from any directory
- **Absolute path** - Avoids relative path issues
- **Standard idiom** - Common bash pattern

### Line 5: Change to Script Directory
```bash
cd "$SCRIPT_DIR"
```
- **cd** - Change directory
- **"$SCRIPT_DIR"** - Quoted (handles spaces in path)
- **Why?** Ensures all subsequent commands run in correct directory

---

## Virtual Environment Check (Linje 7-11)

```bash
# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
```

### Line 8: Test Condition
```bash
if [ ! -d "venv" ]; then
```
- **[ ... ]** - Test command (condition)
- **!** - Logical NOT
- **-d "venv"** - Test if "venv" is a directory
- **Translation**: "If venv directory does NOT exist..."

### Line 9: User Feedback
```bash
echo "Creating virtual environment..."
```
- **echo** - Print to terminal
- **Why?** Lets user know what's happening (slow operation)

### Line 10: Create venv
```bash
python3 -m venv venv
```
- **python3** - Python 3 interpreter
- **-m venv** - Run venv module
- **venv** - Directory name for virtual environment

#### What This Does
1. Creates `venv/` directory
2. Installs Python interpreter copy
3. Creates `bin/activate` script
4. Creates `lib/` for packages
5. Creates `pip` and `setuptools`

---

## Virtual Environment Activation (Linje 13-14)

```bash
# Activate venv
source venv/bin/activate
```

### source Command
- **source** - Execute script in current shell (not subshell)
- **venv/bin/activate** - Bash script that modifies environment

### What activate Does
1. **Modifies PATH** - Prepends `venv/bin/` to PATH
2. **Sets VIRTUAL_ENV** - Environment variable
3. **Changes prompt** - Shows `(venv)` in terminal
4. **Isolates packages** - `pip install` goes to venv, not system

### After Activation
```bash
$ which python
/home/kasperadm/projects/AzikiAI-codingbot/venv/bin/python

$ echo $VIRTUAL_ENV
/home/kasperadm/projects/AzikiAI-codingbot/venv
```

---

## Dependency Installation (Linje 16-20)

```bash
# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install flask python-dotenv mistralai
fi
```

### Line 17: Check if Flask Installed
```bash
if ! python -c "import flask" 2>/dev/null; then
```

#### Breakdown
1. **python -c "import flask"** - Run Python command (import flask)
   - **Success**: Exit code 0 (Flask installed)
   - **Failure**: Exit code 1 + error message (Flask not found)
2. **2>/dev/null** - Redirect stderr to /dev/null (discard error messages)
   - **2** - File descriptor for stderr
   - **>** - Redirect
   - **/dev/null** - Black hole (discards everything)
3. **!** - Logical NOT (inverts exit code)
4. **if** - Execute block if condition true

#### Translation
"If Flask is NOT installed (import fails)..."

### Line 18: User Feedback
```bash
echo "Installing dependencies..."
```
- **Why?** pip install is slow, user needs to know what's happening

### Line 19: Install Packages
```bash
pip install flask python-dotenv mistralai
```

#### Packages
1. **flask** - Web framework
   - **Creates**: Flask app, routes, templates
   - **Version**: Latest (could pin with `flask==2.3.0`)
2. **python-dotenv** - Environment variable loader
   - **Loads**: .env file variables
   - **Why?** Keeps API keys out of code
3. **mistralai** - Mistral AI API client
   - **Provides**: API wrapper for Mistral models
   - **Used in**: bot.py for vision/chat

#### Why This List?
- **Minimal** - Only core dependencies
- **No extras** - ldap3, requests, etc. not listed (manual install)
- **Quick install** - ~30 seconds

---

## .env File Check (Linje 22-27)

```bash
# Check for .env file
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env with: MISTRAL_API_KEY=your_key_here"
    exit 1
fi
```

### Line 23: Test Condition
```bash
if [ ! -f ".env" ]; then
```
- **[ ! -f ".env" ]** - Test if .env is NOT a regular file
- **-f** - File exists and is regular file (not directory)

### Line 24-25: Error Message
```bash
echo "ERROR: .env file not found!"
echo "Please create .env with: MISTRAL_API_KEY=your_key_here"
```
- **ERROR:** - Prefix makes it obvious something's wrong
- **Instructions** - Tells user exactly what to do

### Line 26: Exit with Error Code
```bash
exit 1
```
- **exit** - Terminate script
- **1** - Non-zero exit code (indicates error)
  - **0** - Success
  - **1-255** - Various error codes
- **Effect**: Script stops, app won't start (prevents API errors)

---

## Application Launch (Linje 29-31)

### Line 29-30: User Feedback
```bash
echo "Starting Mistral Chatbot..."
echo "Access at: https://localhost:5000"
```
- **Starting...** - Indicates launch in progress
- **URL** - Tells user where to open browser
- **https** - Incorrect (should be http, no SSL cert)
  - **Bug**: Flask runs on http:// by default, not https://

### Line 31: Start Flask App
```bash
python main.py
```
- **python** - Uses venv's Python (from PATH)
- **main.py** - ⚠️ **BUG**: Should be `bot.py`
  - **Error**: main.py doesn't exist
  - **Correct**: `python bot.py`

#### What Should Happen
```bash
python bot.py
# Output:
# * Running on http://0.0.0.0:5000 (Press CTRL+C to quit)
# * Restarting with stat
# * Debugger is active!
```

---

## Issues & Bugs

### 1. Incorrect Filename (Line 31)
```bash
# Current (WRONG):
python main.py

# Should be:
python bot.py
```
- **Impact**: Script fails with "main.py not found"
- **Fix**: Rename to `bot.py`

### 2. Incorrect URL Scheme (Line 30)
```bash
# Current (WRONG):
echo "Access at: https://localhost:5000"

# Should be:
echo "Access at: http://localhost:5000"
```
- **Impact**: Browser security warning (no SSL cert)
- **Fix**: Change to `http://`

### 3. Missing Dependency Check
```bash
# Only checks Flask:
if ! python -c "import flask" 2>/dev/null; then
```
- **Problem**: Doesn't check for `python-dotenv` or `mistralai`
- **Impact**: Might fail later if those missing
- **Better**:
  ```bash
  if ! python -c "import flask, dotenv, mistralai" 2>/dev/null; then
  ```

### 4. Hardcoded Package List
```bash
pip install flask python-dotenv mistralai
```
- **Problem**: Doesn't include all dependencies
  - **Missing**: ldap3, requests, Pillow, etc.
- **Better**: Use requirements.txt
  ```bash
  pip install -r requirements.txt
  ```

---

## Expected .env File Format

Based on line 25 instructions:
```bash
# .env file format
MISTRAL_API_KEY=your_api_key_here
```

### Minimal .env (Script Requirement)
```env
MISTRAL_API_KEY=fj3k4l5j6k7l8m9n0
```

### Full .env (Actual Application Needs)
```env
# Mistral AI API
MISTRAL_API_KEY=fj3k4l5j6k7l8m9n0

# Flask secret key
SECRET_KEY=random_secret_key_here

# LDAP Configuration
LDAP_SERVER=ldap://192.168.0.153
LDAP_USER_DN=CN=ldapuser,CN=Users,DC=domain,DC=local
LDAP_PASSWORD=ldap_password
LDAP_SEARCH_BASE=DC=domain,DC=local

# Admin credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=hashed_password_here
```

---

## Execution Flow Diagram

```
┌─────────────────────────────────┐
│ User runs: ./start.sh           │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ Detect script directory         │
│ cd to project root              │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ venv exists?                    │
│  NO -> Create venv              │
│  YES -> Skip                    │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ Activate venv                   │
│ (modifies PATH, env vars)       │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ Flask installed?                │
│  NO -> pip install packages     │
│  YES -> Skip                    │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ .env file exists?               │
│  NO -> Print error, exit 1      │
│  YES -> Continue                │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ Print "Starting..." message     │
│ Print URL (https://...)         │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ ⚠️ Run python main.py (BUG)     │
│ Should be: python bot.py        │
└────────────┬────────────────────┘
             │
             v
┌─────────────────────────────────┐
│ ERROR: main.py not found        │
│ Script fails                    │
└─────────────────────────────────┘
```

---

## Manual Execution (Alternative)

If script has bugs, run manually:

### Step 1: Create venv (if needed)
```bash
cd /home/kasperadm/projects/AzikiAI-codingbot
python3 -m venv venv
```

### Step 2: Activate venv
```bash
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install flask python-dotenv mistralai ldap3 requests Pillow
```

### Step 4: Create .env file
```bash
cat > .env << 'EOF'
MISTRAL_API_KEY=your_key_here
SECRET_KEY=random_secret_here
EOF
```

### Step 5: Run app
```bash
python bot.py
```

---

## Improved Version of start.sh

```bash
#!/bin/bash
# Portable startup script for AzikiAI Chatbot

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=== AzikiAI Chatbot Setup ==="

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment exists"
fi

# Activate venv
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import flask, dotenv, mistralai" 2>/dev/null; then
    echo "[3/4] Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        pip install flask python-dotenv mistralai ldap3 requests Pillow
    fi
else
    echo "[3/4] Dependencies already installed"
fi

# Check for .env file
echo "[4/4] Checking configuration..."
if [ ! -f ".env" ]; then
    echo ""
    echo "ERROR: .env file not found!"
    echo "Please create .env with required API keys:"
    echo ""
    echo "  MISTRAL_API_KEY=your_mistral_key_here"
    echo "  SECRET_KEY=your_flask_secret_here"
    echo ""
    exit 1
fi

# Start the chatbot
echo ""
echo "=== Starting AzikiAI Chatbot ==="
echo "Access at: http://192.168.0.80:5000"
echo "Press CTRL+C to stop"
echo ""
python bot.py
```

### Improvements
1. **Progress indicators** - `[1/4]`, `[2/4]`, etc.
2. **Better error checking** - Tests all imports
3. **Correct filename** - `python bot.py` (not main.py)
4. **Correct URL** - `http://` (not https://)
5. **requirements.txt support** - Falls back to manual install
6. **Better .env instructions** - Shows multiple required keys
7. **Visual sections** - `===` headers for clarity
8. **Correct IP** - 192.168.0.80 (not localhost)

---

## Test Scripts (Missing Files)

### test_ldap.py (NOT FOUND)
- **Expected**: Test LDAP connection to Active Directory
- **Status**: File doesn't exist (might be deleted or never created)
- **Purpose**: Would test LDAP authentication flow

#### Likely Content (Reconstruction)
```python
import ldap3
import os
from dotenv import load_dotenv

load_dotenv()

def test_ldap_connection():
    server = os.getenv('LDAP_SERVER')
    user_dn = os.getenv('LDAP_USER_DN')
    password = os.getenv('LDAP_PASSWORD')
    
    try:
        server_obj = ldap3.Server(server, get_info=ldap3.ALL)
        conn = ldap3.Connection(server_obj, user=user_dn, password=password)
        
        if conn.bind():
            print("✓ LDAP connection successful")
            print(f"  Server: {server}")
            print(f"  User: {user_dn}")
            conn.unbind()
            return True
        else:
            print("✗ LDAP bind failed")
            return False
    except Exception as e:
        print(f"✗ LDAP error: {e}")
        return False

if __name__ == '__main__':
    test_ldap_connection()
```

### test_user_auth.py (NOT FOUND)
- **Expected**: Test user authentication against database
- **Status**: File doesn't exist
- **Purpose**: Would test login flow with SQLite database

#### Likely Content (Reconstruction)
```python
import sqlite3
from werkzeug.security import check_password_hash

def test_user_auth(username, password):
    try:
        conn = sqlite3.connect('azikiai_users.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        
        if result and check_password_hash(result[0], password):
            print(f"✓ Authentication successful for {username}")
            return True
        else:
            print(f"✗ Authentication failed for {username}")
            return False
            
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    # Test with example credentials
    test_user_auth('admin', 'test_password')
```

---

## requirements.txt (Missing, Should Exist)

### Recommended Content
```txt
# Web framework
Flask==3.0.0

# Environment variables
python-dotenv==1.0.0

# AI API client
mistralai==0.1.8

# LDAP authentication
ldap3==2.9.1

# HTTP requests
requests==2.31.0

# Image processing (for Vision API)
Pillow==10.1.0

# Password hashing (usually included with Flask)
Werkzeug==3.0.1
```

### Usage
```bash
pip install -r requirements.txt
```

---

## Konklusion

### start.sh Analysis
- **Purpose**: Automated setup and launch script
- **Strengths**:
  - Portable (works on any Linux/macOS)
  - Auto-creates venv
  - Auto-installs dependencies
  - Checks for .env file
- **Bugs**:
  1. **Critical**: Runs `python main.py` (should be `bot.py`)
  2. **Minor**: URL says `https` (should be `http`)
  3. **Minor**: Only checks Flask import (should check all)
  4. **Minor**: Hardcoded package list (should use requirements.txt)

### Missing Test Files
- **test_ldap.py**: Missing (likely deleted)
- **test_user_auth.py**: Missing (likely deleted)
- **Impact**: No automated testing for authentication

### Missing Dependencies File
- **requirements.txt**: Should exist for proper dependency management
- **Current**: Hardcoded in start.sh (incomplete list)
- **Recommended**: Create requirements.txt with all packages

### Immediate Actions Needed
1. **Fix start.sh**: Change `main.py` to `bot.py`
2. **Fix URL**: Change `https` to `http`
3. **Create requirements.txt**: List all dependencies
4. **Optional**: Recreate test scripts for auth testing
