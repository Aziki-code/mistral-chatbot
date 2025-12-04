# main.py - Part 1: Imports, Globals, and Helper Functions

## File Overview

**File Path:** `/home/kasperadm/projects/AzikiAI-codingbot/main.py`

**Purpose:** This is the main Flask web application that powers the AzikiAI chatbot system. It provides a secure, multi-AI chatbot interface with LDAP authentication, rate limiting, conversation history storage, and file upload capabilities.

**Main Responsibilities:**
- Initialize and configure the Flask web application
- Handle LDAP authentication for enterprise user access
- Manage multiple AI bot providers (Mistral, GitHub Copilot, etc.)
- Store and retrieve chat conversation history in SQLite
- Process file uploads and chat messages
- Implement rate limiting and security measures
- Provide web routes for login, chat, history, and file management

**Type:** Flask web application (main entry point)

**Note:** This document covers PART 1 only - imports, global configurations, and helper functions. Flask routes are documented separately.

---

## Line-by-Line Documentation

### Line 1: Shebang Declaration

```python
#!/usr/bin/env python3
```

**Purpose:** Specifies the interpreter for executing this script.

**Detailed Explanation:**
- `#!` - Shebang characters that must be at the beginning of the file
- `/usr/bin/env` - Uses the `env` program to locate Python in the system PATH
- `python3` - Specifies Python 3 interpreter (required for modern Python features)

**Why this approach?**
Using `/usr/bin/env python3` makes the script portable across different systems where Python might be installed in different locations (e.g., `/usr/bin/python3`, `/usr/local/bin/python3`, or in virtual environments).

**Usage:** Allows direct execution as `./main.py` instead of `python3 main.py`.

---

## Import Statements (Lines 2-11)

### Line 2: Flask Core Imports

```python
from flask import Flask, request, jsonify, render_template, redirect, url_for
```

**Purpose:** Imports essential Flask components for building the web application.

**Detailed Explanation of Each Import:**

- **`Flask`**: The main application class that creates the Flask app instance
  - Used to initialize the web application
  - Handles routing, configuration, and request processing

- **`request`**: Provides access to incoming HTTP request data
  - Used to access form data (`request.form`)
  - Access JSON payloads (`request.json`)
  - Access uploaded files (`request.files`)
  - Get request method (`request.method`)

- **`jsonify`**: Converts Python dictionaries to JSON responses
  - Automatically sets the correct `Content-Type: application/json` header
  - Used for API endpoints that return JSON data
  - Example: `jsonify({"status": "success", "data": result})`

- **`render_template`**: Renders Jinja2 HTML templates
  - Loads templates from the `templates/` directory
  - Allows passing variables to templates
  - Example: `render_template('index.html', username=user)`

- **`redirect`**: Creates HTTP redirect responses
  - Returns a 302 redirect status code
  - Example: `redirect(url_for('login'))`

- **`url_for`**: Generates URLs for Flask routes
  - Builds URLs dynamically based on route names
  - Handles URL construction properly even if routes change
  - Example: `url_for('index')` generates the URL for the index route

---

### Line 3: Flask-Login Imports

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
```

**Purpose:** Imports Flask-Login components for user session management and authentication.

**Detailed Explanation of Each Import:**

- **`LoginManager`**: Main class that manages user sessions
  - Handles session cookies
  - Manages user authentication state
  - Configures login view and messages

- **`UserMixin`**: Mixin class that provides default implementations for user objects
  - Provides `is_authenticated` property (always True for logged-in users)
  - Provides `is_active` property (True if account is active)
  - Provides `is_anonymous` property (False for real users)
  - Provides `get_id()` method to return unique user identifier

- **`login_user`**: Function to log a user in
  - Creates a session for the user
  - Sets session cookies
  - Example: `login_user(user_object, remember=True)`

- **`logout_user`**: Function to log the current user out
  - Clears the user's session
  - Removes session cookies
  - Example: `logout_user()`

- **`login_required`**: Decorator to protect routes
  - Ensures only authenticated users can access a route
  - Redirects unauthenticated users to login page
  - Example: `@app.route('/protected') @login_required def protected(): ...`

- **`current_user`**: Proxy object representing the current logged-in user
  - Accessible from any request context
  - Returns the actual user object if authenticated
  - Returns anonymous user object if not authenticated
  - Example: `current_user.username`

---

### Line 4: Flask-LDAP3-Login Imports

```python
from flask_ldap3_login import LDAP3LoginManager
```

**Purpose:** Imports the LDAP3 login manager for enterprise authentication.

**Detailed Explanation:**

- **`LDAP3LoginManager`**: Manages LDAP (Lightweight Directory Access Protocol) authentication
  - Connects to Active Directory or other LDAP servers
  - Authenticates users against corporate directory services
  - Validates usernames and passwords
  - Retrieves user information from LDAP
  - Integrates with Flask-Login for session management

**Use Case:** In enterprise environments, users authenticate with their corporate credentials stored in Active Directory rather than maintaining a separate user database.

---

### Line 5: Flask-LDAP3-Login Forms Import

```python
from flask_ldap3_login.forms import LDAPLoginForm
```

**Purpose:** Imports a pre-built login form for LDAP authentication.

**Detailed Explanation:**

- **`LDAPLoginForm`**: WTForms-based form for LDAP login
  - Provides username and password fields
  - Includes CSRF protection
  - Handles form validation
  - Can be customized or extended

**Note:** This import is available but may not be used if custom login forms are implemented.

---

### Line 6: Flask-Limiter Imports

```python
from flask_limiter import Limiter
```

**Purpose:** Imports the rate limiting extension for Flask.

**Detailed Explanation:**

- **`Limiter`**: Main class for implementing rate limiting
  - Prevents abuse by limiting request rates
  - Can set global limits (e.g., "200 per day")
  - Can set per-route limits
  - Stores rate limit data in memory or Redis
  - Returns 429 (Too Many Requests) when limit exceeded

**Why Rate Limiting?**
- Prevents brute-force login attempts
- Protects against denial-of-service attacks
- Prevents API abuse
- Controls resource consumption

---

### Line 7: Flask-Limiter Utility Import

```python
from flask_limiter.util import get_remote_address
```

**Purpose:** Imports utility function to identify clients for rate limiting.

**Detailed Explanation:**

- **`get_remote_address`**: Function that extracts the client's IP address
  - Used as the "key" to track requests per client
  - Handles proxy headers (X-Forwarded-For)
  - Returns the remote IP address of the requester
  - Each unique IP gets its own rate limit counter

**Alternative approaches:** Rate limiting can also be based on user ID, session ID, or API keys depending on requirements.

---

### Line 8: Dotenv Import

```python
from dotenv import load_dotenv
```

**Purpose:** Imports function to load environment variables from `.env` file.

**Detailed Explanation:**

- **`load_dotenv`**: Function that reads `.env` file and loads variables into `os.environ`
  - Keeps sensitive configuration (API keys, passwords) out of source code
  - Allows different configurations per environment (dev, staging, production)
  - Reads key=value pairs from `.env` file
  - Makes variables accessible via `os.getenv('VARIABLE_NAME')`

**Example `.env` file:**
```
MISTRAL_API_KEY=abc123
LDAP_HOST=ldap://ad.company.com
SECRET_KEY=my-secret-key
```

---

### Line 9: OS Module Import

```python
import os
```

**Purpose:** Imports Python's operating system interface module.

**Detailed Explanation:**

- **`os`**: Provides operating system dependent functionality
  - **`os.getenv()`**: Get environment variables
  - **`os.path.join()`**: Join path components correctly for the OS
  - **`os.path.dirname()`**: Get directory name from path
  - **`os.makedirs()`**: Create directories (including parents)
  - **`os.path.exists()`**: Check if path exists

**Common uses in this application:**
- Reading environment variables
- Building file paths
- Creating directories for logs and uploads
- Getting the application directory

---

### Line 10: SQLite3 Import

```python
import sqlite3
```

**Purpose:** Imports Python's built-in SQLite database interface.

**Detailed Explanation:**

- **`sqlite3`**: Provides DB-API 2.0 interface for SQLite databases
  - SQLite is a serverless, file-based database
  - No separate database server required
  - Perfect for small to medium applications
  - Stores data in a single file (`chat_history.db`)

**Key sqlite3 features used:**
- **`sqlite3.connect()`**: Create database connection
- **`conn.cursor()`**: Create cursor for executing SQL
- **`cursor.execute()`**: Execute SQL statements
- **`conn.commit()`**: Save changes to database
- **`conn.row_factory`**: Configure how rows are returned

---

### Line 11: Logging Import

```python
import logging
```

**Purpose:** Imports Python's built-in logging framework.

**Detailed Explanation:**

- **`logging`**: Provides flexible event logging system
  - Logs messages at different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - Can output to multiple destinations (file, console, network)
  - Supports formatted log messages with timestamps
  - Thread-safe for concurrent applications

**Why logging?**
- Track application behavior and errors
- Debug issues in production
- Monitor system health
- Audit user actions
- Performance troubleshooting

---

## Configuration Section 1: Environment Loading (Lines 13-16)

### Lines 13-14: Load Environment Variables

```python
# --- Load .env FIRST before any other imports that need environment variables ---
load_dotenv()
```

**Purpose:** Load environment variables from `.env` file before importing modules that depend on them.

**Detailed Explanation:**

- **Comment**: Emphasizes the critical ordering - `.env` MUST be loaded BEFORE importing bot_manager
- **`load_dotenv()`**: Reads `.env` file and populates `os.environ` dictionary

**Why this order matters:**
1. `bot_manager` module needs API keys from environment variables
2. If we import `bot_manager` before calling `load_dotenv()`, the API keys won't be available
3. This causes initialization errors or missing credentials
4. Loading `.env` first ensures all environment variables are ready

**Critical Sequence:**
```
1. Import load_dotenv
2. Call load_dotenv()        ← Must happen here
3. Import bot_manager        ← Now this can access environment variables
```

---

### Lines 16-17: Import Bot Manager

```python
# Import Bot Manager AFTER loading .env
from bot_manager import get_bot_manager
```

**Purpose:** Import the bot manager factory function after environment variables are loaded.

**Detailed Explanation:**

- **`get_bot_manager`**: Factory function that returns a singleton BotManager instance
  - Manages multiple AI bot providers (Mistral, GitHub Copilot, etc.)
  - Handles bot initialization and configuration
  - Provides bot selection and availability checking
  - Requires API keys from environment variables

**Why import this module separately?**
- It's a local module (not a third-party package)
- It needs environment variables to initialize bots
- Must be imported AFTER `load_dotenv()` to work correctly

---

## Configuration Section 2: Logging Setup (Lines 19-30)

### Lines 19-20: Create Log Directory

```python
# --- Configure Logging ---
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
```

**Purpose:** Create a `logs/` directory in the same location as the main.py file.

**Detailed Explanation:**

- **`os.path.dirname(__file__)`**: Gets the directory containing main.py
  - `__file__` is a special variable containing the path to the current script
  - `dirname()` extracts just the directory part
  
- **`os.path.join()`**: Combines directory path with 'logs' subdirectory
  - Handles path separators correctly for the OS (/ on Linux/Mac, \ on Windows)
  - Example result: `/home/user/projects/AzikiAI-codingbot/logs`

- **`os.makedirs(log_dir, exist_ok=True)`**: Creates the directory
  - Creates parent directories if needed (like `mkdir -p`)
  - `exist_ok=True` prevents error if directory already exists
  - Without this, the logging would fail if the directory doesn't exist

---

### Lines 22-29: Configure Logging System

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'azikiai.log')),
        logging.StreamHandler()
    ]
)
```

**Purpose:** Configure the Python logging system with file and console output.

**Detailed Explanation:**

- **`logging.basicConfig()`**: Performs basic configuration of the logging system
  - Sets up root logger configuration
  - Must be called once at application startup
  - All subsequent loggers inherit these settings

**Configuration Parameters:**

1. **`level=logging.INFO`**:
   - Sets minimum severity level to log
   - Hierarchy: DEBUG < INFO < WARNING < ERROR < CRITICAL
   - INFO and above will be logged (INFO, WARNING, ERROR, CRITICAL)
   - DEBUG messages will be ignored
   - Use DEBUG level for detailed troubleshooting

2. **`format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'`**:
   - Defines the format of log messages
   - **`%(asctime)s`**: Timestamp (e.g., "2025-12-03 10:30:15,123")
   - **`[%(levelname)s]`**: Severity level in brackets (e.g., "[INFO]", "[ERROR]")
   - **`%(name)s`**: Logger name (usually module name)
   - **`: %(message)s`**: The actual log message
   - Example output: `2025-12-03 10:30:15,123 [INFO] __main__: Bot manager initialized`

3. **`handlers=[...]`**: List of output destinations:

   a. **`logging.FileHandler(os.path.join(log_dir, 'azikiai.log'))`**:
      - Writes logs to file: `logs/azikiai.log`
      - Persists logs for later review
      - Grows over time (consider log rotation in production)
      - Useful for debugging issues that occurred when you weren't watching

   b. **`logging.StreamHandler()`**:
      - Writes logs to console (stdout/stderr)
      - Allows real-time monitoring during development
      - Visible when running `python3 main.py`
      - Captured by systemd/Docker in production

**Result:** All log messages will appear both in the console AND in the log file.

---

### Line 30: Create Module Logger

```python
logger = logging.getLogger(__name__)
```

**Purpose:** Create a logger instance specific to this module.

**Detailed Explanation:**

- **`logging.getLogger(__name__)`**: Creates or retrieves a logger
  - `__name__` is a special variable containing the module name
  - When main.py runs as script: `__name__ == "__main__"`
  - When imported: `__name__ == "main"`
  - Using `__name__` creates a properly named logger

**Why use module-specific loggers?**
- Identifies which module generated each log message
- Allows per-module log level configuration
- Makes debugging easier in large applications
- Example: `[INFO] __main__: Bot manager initialized` - we know this came from main.py

**Usage examples:**
```python
logger.debug("Detailed debugging information")
logger.info("General information about program execution")
logger.warning("Something unexpected happened")
logger.error("An error occurred but app continues")
logger.critical("Serious error, program may not continue")
```

---

## Configuration Section 3: Bot Manager Initialization (Lines 32-38)

### Lines 32-38: Initialize Bot Manager

```python
# --- Initialize Bot Manager (handles all AI bots) ---
try:
    bot_manager = get_bot_manager()
    logger.info("Bot manager initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize bot manager: {e}")
    raise
```

**Purpose:** Initialize the bot manager system and handle initialization failures gracefully.

**Detailed Explanation:**

**`try-except` block**: Wraps initialization to catch any errors
- If initialization succeeds, execution continues
- If initialization fails, error is logged and re-raised

**Inside the `try` block:**

1. **`bot_manager = get_bot_manager()`**:
   - Calls factory function to get BotManager singleton instance
   - BotManager initializes all available AI bots:
     - Mistral AI (if API key provided)
     - GitHub Copilot (if API key provided)
     - Other bots as configured
   - Verifies API credentials
   - Sets up bot configurations

2. **`logger.info("Bot manager initialized successfully")`**:
   - Logs successful initialization
   - Appears in both console and log file
   - Helps confirm system startup is proceeding correctly

**Inside the `except` block:**

1. **`except Exception as e`**:
   - Catches ANY exception that occurs during initialization
   - `e` contains the exception object with error details

2. **`logger.critical(f"Failed to initialize bot manager: {e}")`**:
   - Logs at CRITICAL level (highest severity)
   - Indicates a fatal error that prevents app from running
   - Includes the actual error message in the log
   - Example: "Failed to initialize bot manager: MISTRAL_API_KEY not found"

3. **`raise`**:
   - Re-raises the caught exception
   - Stops application startup
   - Prevents app from running in broken state
   - Without this, app might continue without working bots

**Why this approach?**
- Fail fast: If bots can't initialize, app shouldn't start
- Clear logging: Error is logged before crash
- Debugging: Developers know exactly what failed
- Production safety: Prevents running non-functional application

---

## Configuration Section 4: Flask Application Setup (Lines 40-42)

### Lines 40-42: Initialize Flask App

```python
# --- Flask app ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')
```

**Purpose:** Create the Flask application instance and configure the secret key.

**Detailed Explanation:**

1. **`app = Flask(__name__)`**:
   - Creates the main Flask application object
   - `__name__` helps Flask determine the root path for the application
   - Flask uses this to locate templates and static files
   - The `app` object is used to:
     - Define routes (@app.route)
     - Configure application settings
     - Register extensions
     - Handle requests

2. **`app.config['SECRET_KEY'] = ...`**:
   - Sets the secret key for cryptographic signing
   - **What does the secret key protect?**
     - Session cookies (prevents tampering)
     - CSRF tokens (prevents cross-site request forgery)
     - Flash messages
     - Any signed data

3. **`os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')`**:
   - Attempts to read SECRET_KEY from environment variables
   - If SECRET_KEY exists in environment: uses that value
   - If SECRET_KEY doesn't exist: uses the default value
   - **Default value**: 'change-this-secret-key-in-production'
     - This is intentionally obvious to remind developers
     - Should NEVER be used in production
     - Should be a long, random string in production

**Security Implications:**
- ⚠️ **Using default key in production is a CRITICAL security vulnerability**
- Attackers can forge session cookies
- Users can be impersonated
- Cross-site attacks become possible

**Production Best Practice:**
```bash
# Generate a secure random key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Add to .env file
SECRET_KEY=a1b2c3d4e5f6...
```

---

## Configuration Section 5: Rate Limiting Setup (Lines 44-50)

### Lines 44-50: Configure Rate Limiter

```python
# --- Rate Limiting ---
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
```

**Purpose:** Configure rate limiting to prevent abuse and protect server resources.

**Detailed Explanation:**

**`limiter = Limiter(...)`**: Creates a rate limiter instance

**Configuration Parameters:**

1. **`app=app`**:
   - Attaches the limiter to the Flask application
   - Limiter will intercept requests before they reach routes
   - Automatically handles rate limit enforcement

2. **`key_func=get_remote_address`**:
   - Function that identifies unique clients
   - Returns the IP address of the requesting client
   - Each IP address gets its own rate limit counter
   - Example: IP 192.168.1.100 has separate limits from 192.168.1.101

3. **`default_limits=["200 per day", "50 per hour"]`**:
   - Sets global rate limits for all routes (unless overridden)
   - **"200 per day"**: Maximum 200 requests per IP address per 24-hour period
   - **"50 per hour"**: Maximum 50 requests per IP address per 60-minute period
   - Both limits are enforced simultaneously
   - Uses sliding window algorithm

   **How it works:**
   - Request at 10:00 AM counts toward both daily and hourly limits
   - Hourly limit resets on a sliding window (not at clock hour boundaries)
   - If you make 50 requests in one hour, you must wait for the oldest request to age out

4. **`storage_uri="memory://"`**:
   - Stores rate limit counters in application memory (RAM)
   - Fast and simple for single-server deployments
   - **Limitation**: Counters reset when application restarts
   - **Limitation**: Won't work with multiple server instances (use Redis instead)

**Alternative storage options:**
```python
# For production with multiple servers
storage_uri="redis://localhost:6379"

# For persistence across restarts
storage_uri="redis://localhost:6379/0"
```

**What happens when limit is exceeded?**
- Client receives HTTP 429 (Too Many Requests) response
- Response includes headers:
  - `X-RateLimit-Limit`: The limit value
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: When the limit resets
- Client should wait before retrying

**Per-route overrides:**
```python
@app.route("/expensive-operation")
@limiter.limit("10 per hour")  # Stricter limit for expensive routes
def expensive_operation():
    pass
```

---

## Configuration Section 6: LDAP Configuration (Lines 52-72)

### Lines 52-61: Basic LDAP Settings

```python
# --- LDAP Configuration ---
app.config['LDAP_HOST'] = os.getenv('LDAP_HOST')
app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN')
app.config['LDAP_USER_DN'] = os.getenv('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=Area51,DC=local')
app.config['LDAP_GROUP_DN'] = ''
app.config['LDAP_USER_RDN_ATTR'] = 'cn'  # Changed from sAMAccountName to cn
app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'
app.config['LDAP_BIND_USER_DN'] = None  # Use direct bind instead of service account
app.config['LDAP_BIND_USER_PASSWORD'] = None
app.config['LDAP_USE_SSL'] = True
```

**Purpose:** Configure LDAP/Active Directory authentication settings.

**Detailed Explanation:**

**What is LDAP?**
- Lightweight Directory Access Protocol
- Used by Active Directory and other directory services
- Stores user accounts, groups, and organizational information
- Allows centralized authentication

1. **`app.config['LDAP_HOST'] = os.getenv('LDAP_HOST')`**:
   - LDAP server hostname or IP address
   - Example: `'ldap://ad.company.com'` or `'ldaps://192.168.1.10'`
   - Read from environment variable for security and flexibility
   - `ldap://` for non-SSL, `ldaps://` for SSL

2. **`app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN')`**:
   - Base Distinguished Name - the root of the LDAP directory tree
   - Example: `'DC=company,DC=com'`
   - All searches start from this point
   - DC = Domain Component

3. **`app.config['LDAP_USER_DN'] = os.getenv('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=Area51,DC=local')`**:
   - Where to search for user accounts in the directory
   - CN = Common Name (container name)
   - Default: `'CN=Users,DC=Area51,DC=local'`
   - Example full user DN: `CN=jsmith,CN=Users,DC=Area51,DC=local`

4. **`app.config['LDAP_GROUP_DN'] = ''`**:
   - Where to search for groups
   - Empty string = not checking group membership
   - Could be set to enforce access based on AD group membership
   - Example: `'CN=ChatbotUsers,CN=Groups,DC=Area51,DC=local'`

5. **`app.config['LDAP_USER_RDN_ATTR'] = 'cn'`**:
   - RDN = Relative Distinguished Name attribute
   - `'cn'` = Common Name attribute
   - Used to construct the user's full DN
   - Comment notes this changed from `sAMAccountName` to `cn`
   - This affects how user DNs are built

6. **`app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'`**:
   - Attribute used for login/username
   - `sAMAccountName` is the Windows username (e.g., "jsmith")
   - Users enter this in the login form
   - Example: User types "jsmith" - this is matched against sAMAccountName

7. **`app.config['LDAP_BIND_USER_DN'] = None`**:
   - Service account DN for LDAP queries
   - `None` = not using a service account
   - Comment: "Use direct bind instead of service account"
   - Direct bind means user credentials are used directly

8. **`app.config['LDAP_BIND_USER_PASSWORD'] = None`**:
   - Password for the service account
   - `None` because not using service account
   - If using service account, would contain password

9. **`app.config['LDAP_USE_SSL'] = True`**:
   - Enable SSL/TLS encryption for LDAP connection
   - `True` = use LDAPS (LDAP over SSL) on port 636
   - `False` = use unencrypted LDAP on port 389
   - Should always be `True` in production for security

---

### Lines 62-64: Advanced LDAP Binding Configuration

```python
app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True  # Enable direct credential binding
app.config['LDAP_BIND_DIRECT_SUFFIX'] = ''  # Will use full DN
app.config['LDAP_BIND_DIRECT_GET_USER_INFO'] = True
```

**Purpose:** Configure how LDAP authentication binds (authenticates) users.

**Detailed Explanation:**

1. **`app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True`**:
   - Enables direct credential binding
   - User's entered credentials are used to authenticate directly with LDAP
   - No service account needed
   - **How it works:**
     1. User enters username and password in login form
     2. Application constructs full DN from username
     3. Application attempts LDAP bind with that DN and password
     4. If LDAP bind succeeds, user is authenticated
   - More secure: Application never stores or uses a service account password

2. **`app.config['LDAP_BIND_DIRECT_SUFFIX'] = ''`**:
   - Suffix added to username when constructing DN
   - Empty string = use full DN construction
   - Alternative: Could be `'@domain.com'` for UPN-style authentication
   - Example with suffix `@company.com`: username "jsmith" becomes "jsmith@company.com"

3. **`app.config['LDAP_BIND_DIRECT_GET_USER_INFO'] = True`**:
   - After successful authentication, retrieve user information from LDAP
   - Gets attributes like email, full name, department, etc.
   - User info can be used in the application (display name, email notifications, etc.)

**Authentication Flow with Direct Bind:**
```
1. User enters: username="jsmith", password="secret123"
2. App constructs DN: "CN=jsmith,CN=Users,DC=Area51,DC=local"
3. App attempts LDAP bind with DN and password
4. LDAP server verifies credentials
5. If valid: bind succeeds, user authenticated
6. App retrieves user info from LDAP
7. User session created
```

---

### Lines 66-69: SSL/TLS Configuration

```python
# SSL/TLS Configuration - Don't validate certificate for internal AD
import ssl
from ldap3 import Tls
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
```

**Purpose:** Configure SSL/TLS settings for secure LDAP connections.

**Detailed Explanation:**

1. **`import ssl`**:
   - Python's SSL/TLS module
   - Provides SSL constants and configuration options
   - Defines certificate validation options

2. **`from ldap3 import Tls`**:
   - LDAP3 library's TLS configuration class
   - Handles SSL/TLS settings for LDAP connections
   - Wraps Python's SSL configuration for LDAP use

3. **`tls_configuration = Tls(...)`**:
   - Creates TLS configuration object for LDAP

   **Parameters:**
   
   a. **`validate=ssl.CERT_NONE`**:
      - **Does NOT validate SSL certificates**
      - Comment explains: "Don't validate certificate for internal AD"
      - ⚠️ **Security Warning**: This disables certificate validation
      - **Why used here:**
        - Internal Active Directory servers often use self-signed certificates
        - Certificate hostname might not match LDAP server hostname
        - In controlled internal networks, risk is acceptable
      - **Production recommendation:** Use proper certificates and `ssl.CERT_REQUIRED`
      - **Alternative values:**
        - `ssl.CERT_REQUIRED`: Verify certificate (most secure)
        - `ssl.CERT_OPTIONAL`: Verify if provided

   b. **`version=ssl.PROTOCOL_TLSv1_2`**:
      - Forces TLS version 1.2
      - TLS 1.2 is secure and widely supported
      - Prevents downgrade to older, vulnerable versions (SSL 2.0, SSL 3.0, TLS 1.0)
      - TLS 1.3 is newer but may not be supported by older AD servers

**Security Implications:**
- ✅ Encrypted connection (TLS 1.2)
- ⚠️ No certificate validation (vulnerable to man-in-the-middle attacks)
- ✅ Acceptable for internal networks with controlled infrastructure
- ❌ Not recommended for internet-facing or untrusted networks

---

### Line 70: Apply TLS Configuration

```python
app.config['LDAP_TLS_CONFIG'] = tls_configuration
```

**Purpose:** Apply the TLS configuration to Flask-LDAP3-Login.

**Detailed Explanation:**
- Assigns the TLS configuration object to Flask app config
- Flask-LDAP3-Login will use these TLS settings for all LDAP connections
- Ensures SSL/TLS is used with the specified validation and protocol version

---

## Configuration Section 7: Flask-Login Setup (Lines 72-76)

### Lines 72-76: Initialize Authentication Managers

```python
# --- Flask-Login Setup ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ldap_manager = LDAP3LoginManager(app)
```

**Purpose:** Initialize Flask-Login and LDAP authentication systems.

**Detailed Explanation:**

1. **`login_manager = LoginManager(app)`**:
   - Creates Flask-Login manager instance
   - Attaches to Flask application
   - Manages user sessions and authentication state
   - **Responsibilities:**
     - Track logged-in users
     - Manage session cookies
     - Protect routes with @login_required decorator
     - Handle user loading and authentication

2. **`login_manager.login_view = 'login'`**:
   - Sets the login route name
   - When unauthenticated user accesses @login_required route:
     - User is redirected to this view
     - URL becomes: `/login?next=/protected-page`
     - After login, user is redirected back to original page
   - `'login'` refers to the function name, not the URL path

3. **`ldap_manager = LDAP3LoginManager(app)`**:
   - Creates LDAP authentication manager
   - Integrates with Flask-Login
   - Handles LDAP authentication logic
   - Uses LDAP configuration from app.config
   - **Responsibilities:**
     - Connect to LDAP server
     - Authenticate user credentials
     - Retrieve user information
     - Create user objects after successful authentication

**How Flask-Login and LDAP work together:**
```
1. User submits login form (username + password)
2. LDAP manager authenticates against Active Directory
3. If successful, LDAP manager creates User object
4. Flask-Login creates session for User object
5. Session cookie sent to user's browser
6. Subsequent requests include session cookie
7. Flask-Login loads User from session
8. User can access @login_required routes
```

---

## Configuration Section 8: User Class Definition (Lines 78-86)

### Lines 78-86: User Model for Authentication

```python
# User class for Flask-Login
class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn
```

**Purpose:** Define a User class that Flask-Login can use to represent authenticated users.

**Detailed Explanation:**

**`class User(UserMixin):`**:
- Inherits from `UserMixin` to get default Flask-Login methods
- Represents an authenticated user in the system

**Methods and Attributes:**

1. **`def __init__(self, dn, username, data):`**:
   - Constructor called when creating a User object
   - **Parameters:**
     - `dn`: Distinguished Name from LDAP (unique identifier)
       - Example: "CN=John Smith,CN=Users,DC=Area51,DC=local"
     - `username`: The login username (sAMAccountName)
       - Example: "jsmith"
     - `data`: Dictionary of additional LDAP attributes
       - Could contain: email, full name, department, phone, etc.
   
2. **`self.dn = dn`**:
   - Stores the LDAP Distinguished Name
   - Used as the unique identifier for this user
   - Required by Flask-Login to identify user across requests

3. **`self.username = username`**:
   - Stores the short username
   - Used for display purposes
   - Example: Show "Welcome, jsmith" in UI

4. **`self.data = data`**:
   - Stores additional user information from LDAP
   - Could be accessed like: `user.data.get('mail')` for email
   - Flexible storage for any LDAP attributes

5. **`def __repr__(self):`**:
   - Returns string representation of User object
   - Used for debugging and logging
   - Returns the DN
   - Example: `print(user)` outputs "CN=jsmith,CN=Users,DC=Area51,DC=local"

6. **`def get_id(self):`**:
   - **Required by Flask-Login**
   - Returns unique identifier for the user
   - Must return a string (unicode in Python 3)
   - Used to:
     - Store user ID in session cookie
     - Load user from session via `load_user()` callback
   - Returns `self.dn` (the Distinguished Name)

**Methods inherited from UserMixin:**
- `is_authenticated`: Always True for logged-in users
- `is_active`: True (can be overridden for account deactivation)
- `is_anonymous`: Always False for real users
- `get_id()`: We override this to return DN

**Why use DN as user ID?**
- Guaranteed unique in LDAP/Active Directory
- Remains stable even if username changes
- Contains full path to user object in directory

---

## Configuration Section 9: Flask-Login Callbacks (Lines 88-101)

### Lines 92-94: User Loader Callback

```python
@login_manager.user_loader
def load_user(user_id):
    # Return a user object based on the user_id (DN)
    return User(user_id, user_id.split(',')[0].split('=')[1], {})
```

**Purpose:** Flask-Login callback that loads a user from their ID stored in the session.

**Detailed Explanation:**

**`@login_manager.user_loader` decorator:**
- Registers this function with Flask-Login
- Called automatically on every request from logged-in users
- Purpose: Reconstruct User object from session data

**Function signature: `def load_user(user_id):`**
- `user_id`: The value returned by `User.get_id()` (the DN)
- Retrieved from the user's session cookie
- Example: "CN=jsmith,CN=Users,DC=Area51,DC=local"

**Return statement breakdown:**
```python
return User(user_id, user_id.split(',')[0].split('=')[1], {})
```

Let's trace this with example: `user_id = "CN=jsmith,CN=Users,DC=Area51,DC=local"`

1. **`user_id`**: The full DN
   - Value: "CN=jsmith,CN=Users,DC=Area51,DC=local"

2. **`user_id.split(',')[0]`**: Get first component of DN
   - Split by comma: ["CN=jsmith", "CN=Users", "DC=Area51", "DC=local"]
   - Take first element: "CN=jsmith"

3. **`user_id.split(',')[0].split('=')[1]`**: Extract username
   - Split "CN=jsmith" by equals: ["CN", "jsmith"]
   - Take second element: "jsmith"

4. **`User(...)`**: Create User object with:
   - `dn`: The full DN
   - `username`: "jsmith" (extracted from DN)
   - `data`: Empty dictionary `{}`

**Why empty data dictionary?**
- This is a simplified user loader
- Only basic info needed for session management
- Full user data was retrieved during login
- For richer user data, could query LDAP here (but adds overhead)

**When is this called?**
- On every request from authenticated user
- Flask-Login checks session cookie
- Extracts user_id from session
- Calls `load_user(user_id)` to get User object
- Makes User available as `current_user` in routes

---

### Lines 96-99: Save User Callback

```python
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    # Create and return user object after successful LDAP authentication
    return User(dn, username, data)
```

**Purpose:** Flask-LDAP3-Login callback that creates a User object after successful LDAP authentication.

**Detailed Explanation:**

**`@ldap_manager.save_user` decorator:**
- Registers this function with Flask-LDAP3-Login
- Called after LDAP authentication succeeds
- Purpose: Convert LDAP data into User object for Flask-Login

**Function signature:**
```python
def save_user(dn, username, data, memberships):
```

**Parameters provided by LDAP manager:**

1. **`dn`**: Distinguished Name from LDAP
   - Full path to user in directory
   - Example: "CN=jsmith,CN=Users,DC=Area51,DC=local"

2. **`username`**: The login username
   - Value of sAMAccountName attribute
   - Example: "jsmith"

3. **`data`**: Dictionary of LDAP attributes
   - Retrieved from LDAP after authentication
   - May contain:
     - `mail`: Email address
     - `givenName`: First name
     - `sn`: Surname
     - `displayName`: Full display name
     - `memberOf`: Group memberships
     - Any other LDAP attributes configured

4. **`memberships`**: List of LDAP groups user belongs to
   - Example: ["CN=ChatbotUsers,CN=Groups,...", "CN=Admins,CN=Groups,..."]
   - Used for authorization/access control
   - Not used in this simple implementation

**Return statement:**
```python
return User(dn, username, data)
```
- Creates User object with LDAP data
- This User object is then passed to Flask-Login
- Flask-Login creates session for this user
- Session persists across requests

**Authentication flow:**
```
1. User submits login form
2. LDAP manager authenticates credentials
3. LDAP manager retrieves user data
4. save_user() is called with LDAP data
5. save_user() returns User object
6. Flask-Login creates session
7. User is logged in
```

---

## Configuration Section 10: Database Setup (Lines 101-130)

### Line 103: Database Path Configuration

```python
# --- SQLite setup ---
db_path = os.path.join(os.path.dirname(__file__), "chat_history.db")
```

**Purpose:** Define the file path for the SQLite database.

**Detailed Explanation:**

- **`os.path.dirname(__file__)`**: Gets directory containing main.py
  - `__file__`: Path to current script
  - `dirname()`: Extracts directory component
  - Example: "/home/user/projects/AzikiAI-codingbot"

- **`os.path.join(..., "chat_history.db")`**: Builds complete database path
  - Joins directory with database filename
  - Example result: "/home/user/projects/AzikiAI-codingbot/chat_history.db"
  - Uses OS-appropriate path separator

- **Why this location?**
  - Database stored alongside application code
  - Easy to find and back up
  - Relative path makes deployment portable
  - For production, might use `/var/lib/azikiai/` or similar

---

### Lines 105-108: Database Connection Function

```python
def get_db_connection():
    """Create a new database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
```

**Purpose:** Create a new SQLite database connection with proper configuration.

**Detailed Explanation:**

**Function signature: `def get_db_connection():`**
- Returns a new database connection
- Should be called for each database operation
- Connection should be closed after use

**`conn = sqlite3.connect(db_path)`**:
- Opens connection to SQLite database file
- If file doesn't exist, it will be created
- Returns connection object

**`conn.row_factory = sqlite3.Row`**:
- **Critical configuration line**
- Changes how database rows are returned
- **Default behavior**: Rows returned as tuples
  ```python
  # Default (tuple)
  row = cursor.fetchone()
  print(row[0], row[1])  # Access by index
  ```
- **With sqlite3.Row**: Rows returned as dict-like objects
  ```python
  # With sqlite3.Row
  row = cursor.fetchone()
  print(row['id'], row['username'])  # Access by column name
  ```

**Benefits of sqlite3.Row:**
- More readable code (column names instead of indices)
- Less error-prone (no need to remember column order)
- Self-documenting (clear what data is being accessed)
- Can still access by index if needed: `row[0]`

**`return conn`**:
- Returns the configured connection
- Caller is responsible for closing connection

**Usage pattern:**
```python
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    for row in rows:
        print(row['content'])  # Access by name!
finally:
    conn.close()  # Always close connection
```

---

### Lines 110-125: Database Initialization Function

```python
def init_db():
    """Initialize database schema"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
    finally:
        conn.close()
```

**Purpose:** Create the database schema (tables) if they don't exist.

**Detailed Explanation:**

**Function signature: `def init_db():`**
- Called once at application startup
- Ensures database schema exists
- Safe to call multiple times (CREATE TABLE IF NOT EXISTS)

**`conn = get_db_connection()`**:
- Get database connection
- Database file created if it doesn't exist

**`try-finally` block**:
- Ensures connection is always closed
- Even if an error occurs, `finally` block runs

**Inside `try` block:**

1. **`cursor = conn.cursor()`**:
   - Creates cursor object for executing SQL
   - Required for all SQL operations

2. **`cursor.execute("...")`**:
   - Executes SQL statement
   - Creates the messages table

**SQL Statement Breakdown:**

```sql
CREATE TABLE IF NOT EXISTS messages (
```
- **CREATE TABLE**: Creates a new table
- **IF NOT EXISTS**: Only create if table doesn't exist
  - Prevents error if table already exists
  - Makes function idempotent (safe to call multiple times)
- **messages**: Table name

**Column Definitions:**

1. **`id INTEGER PRIMARY KEY AUTOINCREMENT`**:
   - **`id`**: Column name
   - **`INTEGER`**: Data type (whole numbers)
   - **`PRIMARY KEY`**: Unique identifier for each row
   - **`AUTOINCREMENT`**: Automatically assigns next available number
   - First message gets id=1, second gets id=2, etc.
   - Never reuses IDs even after deletion

2. **`role TEXT NOT NULL`**:
   - **`role`**: Column name (stores message sender)
   - **`TEXT`**: Data type (string/text)
   - **`NOT NULL`**: Must have a value (cannot be NULL)
   - Values: "user", "assistant", or "system"
   - Identifies who sent the message

3. **`content TEXT NOT NULL`**:
   - **`content`**: Column name (stores message text)
   - **`TEXT`**: Data type (can store large text)
   - **`NOT NULL`**: Message must have content
   - Stores the actual message text

4. **`timestamp DATETIME DEFAULT CURRENT_TIMESTAMP`**:
   - **`timestamp`**: Column name (when message was created)
   - **`DATETIME`**: Data type (date and time)
   - **`DEFAULT CURRENT_TIMESTAMP`**: Automatically set to current time
   - If not specified, SQLite inserts current date/time
   - Format: "2025-12-03 10:30:45"

**`conn.commit()`**:
- Saves changes to database
- Without commit, changes are not persisted
- Required for CREATE, INSERT, UPDATE, DELETE

**`finally: conn.close()`**:
- Closes database connection
- Runs even if error occurs
- Frees database resources

**Why this schema?**
- Simple and efficient for chat history
- Timestamps for chronological ordering
- Role distinguishes user vs. AI messages
- Can query recent messages, search content, etc.

---

### Lines 127-128: Initialize Database on Startup

```python
# Initialize database on startup
init_db()
```

**Purpose:** Call the database initialization function when the application starts.

**Detailed Explanation:**

- Executes at module load time (when main.py is imported)
- Creates database schema if needed
- Ensures database is ready before handling requests
- Safe to run on every startup (IF NOT EXISTS protection)

**Application startup sequence:**
1. Import modules
2. Load environment variables
3. Initialize bot manager
4. Create Flask app
5. Configure authentication
6. **Initialize database** ← This line
7. Define routes
8. Start server

---

## Helper Functions Section (Lines 130-159)

### Lines 132-156: Language Detection Function

```python
# --- Helper Functions ---
def detect_language(code: str) -> str:
    """
    Detect programming language from code content
    
    Args:
        code: Code string to analyze
        
    Returns:
        str: Language identifier (e.g., 'python', 'html', 'javascript')
    """
    code_lower = code.lower()
    
    language_patterns = {
        'html': ['<html', '<!doctype', '<div', '<script>'],
        'python': ['def ', 'import ', 'print(', 'class ', '__init__'],
        'javascript': ['function', 'const ', 'let ', 'var ', '=>'],
        'java': ['public class', 'private ', 'void main'],
        'css': ['{', '}', 'color:', 'background:'],
        'sql': ['select ', 'from ', 'where ', 'insert into'],
    }
    
    for lang, patterns in language_patterns.items():
        if any(pattern in code_lower for pattern in patterns):
            return lang
    
    return 'plaintext'
```

**Purpose:** Automatically detect the programming language of code snippets for proper syntax highlighting.

**Detailed Explanation:**

**Function signature:**
```python
def detect_language(code: str) -> str:
```
- **`code: str`**: Type hint indicating parameter is a string
- **`-> str`**: Type hint indicating return value is a string
- Takes code as input, returns language identifier

**Docstring:**
- Documents function purpose
- Lists parameters and their types
- Describes return value
- Provides example return values

**`code_lower = code.lower()`**:
- Converts code to lowercase
- Makes pattern matching case-insensitive
- "DEF " and "def " both match python patterns

**`language_patterns` dictionary:**
```python
language_patterns = {
    'html': ['<html', '<!doctype', '<div', '<script>'],
    ...
}
```
- Maps language names to pattern lists
- Each pattern is a distinctive keyword/syntax for that language

**Pattern explanations:**

1. **'html'**: `['<html', '<!doctype', '<div', '<script>']`
   - HTML tags are distinctive
   - Opening tags indicate HTML code
   - `<!doctype` is HTML5 declaration

2. **'python'**: `['def ', 'import ', 'print(', 'class ', '__init__']`
   - `def ` defines functions (note space to avoid false matches)
   - `import ` for module imports
   - `print(` for print statements
   - `class ` for class definitions
   - `__init__` for Python constructors

3. **'javascript'**: `['function', 'const ', 'let ', 'var ', '=>']`
   - `function` keyword for function declarations
   - `const`, `let`, `var` for variable declarations
   - `=>` arrow function syntax (ES6)

4. **'java'**: `['public class', 'private ', 'void main']`
   - `public class` for class declarations
   - `private ` for access modifiers
   - `void main` for main method

5. **'css'**: `['{', '}', 'color:', 'background:']`
   - Curly braces for CSS rules
   - Property names with colons

6. **'sql'**: `['select ', 'from ', 'where ', 'insert into']`
   - SQL keywords (case-insensitive)
   - Common SQL operations

**Detection logic:**
```python
for lang, patterns in language_patterns.items():
    if any(pattern in code_lower for pattern in patterns):
        return lang
```
- Iterates through each language
- `any(...)`: Returns True if ANY pattern matches
- `pattern in code_lower`: Checks if pattern exists in code
- Returns first matching language
- **Order matters**: HTML checked before JavaScript (HTML can contain JS)

**Default return:**
```python
return 'plaintext'
```
- If no patterns match, return 'plaintext'
- Prevents errors in syntax highlighter
- Plain text has no special highlighting

**Limitations:**
- Simple pattern matching (not a full parser)
- Returns first match (HTML before CSS/JS)
- Can have false positives (word "def" in comments)
- Doesn't distinguish similar languages (Java vs. C++)

**Why this matters:**
- Proper syntax highlighting in web UI
- Better code readability
- Enhanced user experience
- Works with Prism.js or similar syntax highlighters

**Usage example:**
```python
code = """
def hello():
    print("Hello, world!")
"""
language = detect_language(code)  # Returns "python"
```

---

## Upload Folder Configuration (Lines 158-159)

### Lines 158-159: Setup Upload Directory

```python
# --- Upload folder ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

**Purpose:** Create a directory for storing uploaded files from users.

**Detailed Explanation:**

**`UPLOAD_FOLDER = os.path.join(...)`**:
- Builds path to uploads directory
- **`os.path.dirname(__file__)`**: Application directory
- **`"static"`**: Flask's static files directory
- **`"uploads"`**: Subdirectory for user uploads
- Example result: "/home/user/projects/AzikiAI-codingbot/static/uploads"

**Why in static/ folder?**
- Static files are served by Flask without routing
- Uploaded files accessible via URL
- Example: `/static/uploads/image.png`
- Separates user uploads from application static assets

**`os.makedirs(UPLOAD_FOLDER, exist_ok=True)`**:
- Creates the directory structure
- **`UPLOAD_FOLDER`**: Path to create
- **`exist_ok=True`**: Don't error if directory already exists
- Creates parent directories if needed (`static/` and `static/uploads/`)
- Equivalent to `mkdir -p static/uploads`

**Why create on startup?**
- Ensures directory exists before any uploads
- Prevents errors when users try to upload files
- Simplifies deployment (no manual directory creation)

**Global variable `UPLOAD_FOLDER`:**
- Uppercase indicates it's a constant
- Used by file upload routes
- Centralized configuration (easy to change location)

**Security considerations:**
- Should validate file types before saving
- Should sanitize filenames to prevent path traversal
- Should limit file sizes
- Should scan for malware in production
- Should set appropriate file permissions

**Typical usage in upload route:**
```python
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
```

---

## End of Part 1

This concludes the documentation of the first half of `main.py`, covering:

### What Was Documented:

1. **Shebang and Core Imports (Lines 1-11)**
   - Flask components for web framework
   - Flask-Login for session management
   - Flask-LDAP3-Login for LDAP authentication
   - Flask-Limiter for rate limiting
   - Dotenv for environment variable management
   - Standard library modules (os, sqlite3, logging)

2. **Environment and Module Loading (Lines 13-17)**
   - Loading .env file before other imports
   - Importing bot_manager after environment setup

3. **Logging Configuration (Lines 19-30)**
   - Log directory creation
   - Logging format and handlers
   - Module-specific logger creation

4. **Bot Manager Initialization (Lines 32-38)**
   - Bot manager initialization with error handling
   - Critical error logging on failure

5. **Flask Application Setup (Lines 40-50)**
   - Flask app creation
   - Secret key configuration
   - Rate limiter configuration with memory storage

6. **LDAP Configuration (Lines 52-70)**
   - LDAP host and base DN settings
   - User search and authentication configuration
   - SSL/TLS security settings
   - Direct credential binding setup

7. **Authentication Setup (Lines 72-101)**
   - Flask-Login and LDAP manager initialization
   - User class definition with UserMixin
   - User loader callback for session management
   - Save user callback for LDAP integration

8. **Database Setup (Lines 103-128)**
   - SQLite database path configuration
   - Database connection function with Row factory
   - Database schema initialization
   - Messages table creation

9. **Helper Functions (Lines 130-156)**
   - Language detection function for code syntax highlighting
   - Pattern-based language identification

10. **Upload Directory Setup (Lines 158-159)**
    - Upload folder path configuration
    - Directory creation with error handling

### What Was NOT Documented (Part 2 - Flask Routes):

- `@app.route("/")` - Index/home page
- `@app.route("/debug")` - Debug page
- `@app.route("/login")` - Login handling
- `@app.route("/logout")` - Logout handling
- `@app.route("/chat")` - Chat message processing
- `@app.route("/upload")` - File upload handling
- `@app.route("/history")` - Chat history retrieval
- Application startup code (`if __name__ == "__main__"`)

Flask routes and endpoints will be documented in Part 2.
