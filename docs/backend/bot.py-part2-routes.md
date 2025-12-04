# bot.py - Part 2: Flask Routes Documentation

## Overview
This document provides an exhaustive line-by-line explanation of all Flask routes in `main.py` (formerly referred to as bot.py in the project structure). The application implements a secure AI chatbot interface with LDAP authentication, rate limiting, and multi-model AI support.

---

## Table of Contents
1. [Route: `/` (Index/Home)](#route--indexhome)
2. [Route: `/debug` (Debug Page)](#route-debug-debug-page)
3. [Route: `/login` (Login Handler)](#route-login-login-handler)
4. [Route: `/logout` (Logout Handler)](#route-logout-logout-handler)
5. [Route: `/chat` (Chat Endpoint)](#route-chat-chat-endpoint)
6. [Route: `/upload` (File Upload)](#route-upload-file-upload)
7. [Route: `/history` (Chat History)](#route-history-chat-history)

---

## Route: `/` (Index/Home)

### Route Definition
```python
@app.route("/")
@login_required
def index():
    # Pass available AI bots info to template
    return render_template("index.html", 
                         mistral_available=bot_manager.is_bot_available("mistral"),
                         github_available=bot_manager.is_bot_available("github-copilot"),
                         default_provider=bot_manager.get_default_bot().name)
```

**Location in file**: Lines 164-170

### Purpose
Serves the main chatbot interface page. This is the primary landing page after successful authentication.

### HTTP Methods
- **GET**: Default method, returns the main HTML page

### Authentication/Authorization
- **@login_required**: Decorator ensures only authenticated users can access this route
- Unauthenticated requests are automatically redirected to `/login` (configured in `login_manager.login_view`)

### Request Handling
No request parameters or body data are expected. This is a simple GET request.

### Response Generation

#### Line-by-line Analysis:

**Line 164**: `@app.route("/")`
- Registers this function as the handler for the root URL path "/"
- Only accepts GET requests by default (no methods parameter specified)

**Line 165**: `@login_required`
- Flask-Login decorator that enforces authentication
- If user is not authenticated, redirects to login page automatically
- Sets `current_user` context for authenticated sessions

**Line 166**: `def index():`
- Function definition for the route handler
- No parameters needed since it doesn't process any request data

**Line 167**: `# Pass available AI bots info to template`
- Comment explaining that we're passing bot availability status to the frontend

**Line 168**: `return render_template("index.html",`
- Calls Flask's `render_template()` to render the Jinja2 template `templates/index.html`
- Returns the rendered HTML as the HTTP response

**Line 169**: `mistral_available=bot_manager.is_bot_available("mistral"),`
- Queries the bot manager to check if Mistral AI bot is properly configured
- `is_bot_available()` returns True if the bot's API key is set and valid
- This boolean is passed to the template as `mistral_available` variable
- Frontend can use this to show/hide Mistral AI selection option

**Line 170**: `github_available=bot_manager.is_bot_available("github-copilot"),`
- Checks if GitHub Copilot bot is available
- Similar to mistral_available, determines if GitHub Models API is configured
- Passed to template as `github_available` for conditional rendering

**Line 171**: `default_provider=bot_manager.get_default_bot().name)`
- Gets the default bot instance from bot manager
- Accesses the `.name` property to get the bot's identifier (e.g., "mistral" or "github-copilot")
- Frontend uses this to pre-select the default AI model in the UI
- The default is determined by which bot is available (Mistral has priority)

### Error Handling
No explicit error handling in this route. If bot_manager fails:
- The application would have already crashed during initialization
- Bot manager is initialized globally before route registration

### Database Operations
None. This route only reads from the in-memory bot_manager state.

---

## Route: `/debug` (Debug Page)

### Route Definition
```python
@app.route("/debug")
@login_required
def debug():
    return render_template("debug.html")
```

**Location in file**: Lines 172-175

### Purpose
Serves a debug/diagnostics page for troubleshooting. This is a protected route for testing purposes.

### HTTP Methods
- **GET**: Returns the debug HTML page

### Authentication/Authorization
- **@login_required**: Only authenticated users can access
- No additional role-based authorization checks

### Request Handling
No request parameters needed. Simple GET request handler.

### Response Generation

#### Line-by-line Analysis:

**Line 172**: `@app.route("/debug")`
- Registers handler for `/debug` URL path
- GET method only (default)

**Line 173**: `@login_required`
- Requires user authentication to access debug page
- Prevents unauthorized access to potentially sensitive debug information

**Line 174**: `def debug():`
- Function definition for debug route handler

**Line 175**: `return render_template("debug.html")`
- Renders and returns `templates/debug.html`
- Debug template likely contains system information, bot status, or diagnostic tools

### Error Handling
No explicit error handling. Template rendering errors would be caught by Flask's default error handler.

### Database Operations
None.

---

## Route: `/login` (Login Handler)

### Route Definition
```python
@app.route("/login", methods=["GET", "POST"])
def login():
```

**Location in file**: Lines 177-233

### Purpose
Handles user authentication via LDAP (Active Directory). Supports both displaying the login form (GET) and processing login credentials (POST).

### HTTP Methods
- **GET**: Displays the login form
- **POST**: Processes login credentials and authenticates against LDAP

### Authentication/Authorization
- No `@login_required` decorator (would create infinite redirect loop)
- This route IS the authentication mechanism
- Uses LDAP/Active Directory for credential verification

### Request Handling

#### GET Request:
Returns login form HTML page.

#### POST Request:
Expects form data:
- `username`: User's Active Directory username (CN)
- `password`: User's password

### Line-by-line Analysis:

**Line 177**: `@app.route("/login", methods=["GET", "POST"])`
- Registers route for `/login` path
- Accepts both GET (show form) and POST (process login) methods

**Line 178**: `def login():`
- Route handler function definition

**Line 179**: `if request.method == "POST":`
- Checks if this is a login submission (POST) vs form display (GET)
- Only processes authentication logic for POST requests

**Line 180**: `username = request.form.get("username")`
- Extracts username from form data
- `request.form` contains POST form data (not JSON)
- `.get()` returns None if key doesn't exist (safe access)

**Line 181**: `password = request.form.get("password")`
- Extracts password from form data
- Password is transmitted in plaintext in POST body (protected by HTTPS)

**Line 183**: `# Manual LDAP authentication using ldap3 directly`
- Comment indicating manual LDAP implementation
- Not using Flask-LDAP3-Login's built-in authentication (more control)

**Line 184**: `try:`
- Begin exception handling block for LDAP operations
- LDAP connections can fail for multiple reasons (network, credentials, config)

**Line 185**: `from ldap3 import Server, Connection, ALL, Tls`
- Imports LDAP3 library components
- `Server`: Represents LDAP server configuration
- `Connection`: Handles LDAP connections and operations
- `ALL`: Constant to retrieve all server information
- `Tls`: TLS/SSL configuration object

**Line 186**: `from ldap3.core.exceptions import LDAPException, LDAPBindError`
- Imports specific LDAP exception types
- `LDAPException`: Base exception for all LDAP errors
- `LDAPBindError`: Specific exception for authentication failures

**Line 187**: `import ssl`
- Imports Python's SSL module for certificate handling

**Line 189**: `# LDAP server configuration from environment`
- Comment indicating configuration comes from .env file

**Line 190**: `ldap_host = os.getenv('LDAP_HOST')`
- Reads LDAP server hostname from environment variable
- Example: "ad.area51.local" or "192.168.1.10"

**Line 191**: `ldap_port = int(os.getenv('LDAP_PORT', 636))`
- Reads LDAP port, defaults to 636 (LDAPS - LDAP over SSL)
- Port 389 would be plain LDAP, 636 is secure LDAP
- Converts string environment variable to integer

**Line 192**: `base_dn = os.getenv('LDAP_BASE_DN')`
- Reads base Distinguished Name for LDAP queries
- Example: "DC=Area51,DC=local"
- Defines the root of the directory tree to search

**Line 193**: `validate_ssl = os.getenv('LDAP_VALIDATE_SSL', 'false').lower() == 'true'`
- Reads SSL certificate validation setting
- Defaults to 'false' (no validation) for internal self-signed certificates
- Converts string to boolean by comparing lowercase value to 'true'

**Line 195**: `# Create TLS configuration`
- Comment for TLS setup section

**Line 196**: `ssl_validation = ssl.CERT_REQUIRED if validate_ssl else ssl.CERT_NONE`
- Sets SSL validation mode based on configuration
- `ssl.CERT_REQUIRED`: Validates server certificate against trusted CAs
- `ssl.CERT_NONE`: Accepts any certificate (for internal/self-signed certs)

**Line 197**: `tls = Tls(validate=ssl_validation, version=ssl.PROTOCOL_TLSv1_2)`
- Creates TLS configuration object for LDAP connection
- Uses TLS 1.2 protocol (secure, widely supported)
- `validate` parameter controls certificate verification

**Line 198**: `server = Server(ldap_host, port=ldap_port, use_ssl=True, tls=tls, get_info=ALL)`
- Creates LDAP Server object with configuration
- `use_ssl=True`: Enables SSL/TLS encryption
- `tls=tls`: Uses the TLS configuration created above
- `get_info=ALL`: Retrieves full server schema and info

**Line 200**: `# Try to authenticate user with full DN`
- Comment explaining authentication approach

**Line 201**: `user_dn = f"CN={username},CN=Users,{base_dn}"`
- Constructs full Distinguished Name for user
- Format: "CN=username,CN=Users,DC=Area51,DC=local"
- CN = Common Name (the username)
- Assumes users are in the "Users" container (typical for AD)

**Line 203**: `try:`
- Inner try block specifically for bind attempt
- Separates bind failures from other LDAP errors

**Line 204**: `# Attempt to bind with user credentials`
- Comment explaining bind operation

**Line 205**: `conn = Connection(server, user=user_dn, password=password, auto_bind=True)`
- Creates LDAP connection and attempts to authenticate
- `user=user_dn`: Full DN of user attempting to log in
- `password=password`: User's password
- `auto_bind=True`: Immediately attempts connection and authentication
- If credentials are invalid, raises `LDAPBindError`

**Line 207**: `# If we got here, authentication succeeded`
- Comment confirming successful authentication

**Line 208**: `conn.unbind()`
- Closes the LDAP connection gracefully
- Releases server resources
- Connection is only needed for authentication, not ongoing session

**Line 210**: `# Create user object and log them in`
- Comment for user session creation

**Line 211**: `user = User(user_dn, username, {})`
- Creates Flask-Login User object
- Parameters: (DN, username, user data dictionary)
- User class defined earlier in the file (lines 84-95)

**Line 212**: `login_user(user)`
- Flask-Login function that starts the user's session
- Sets session cookie in response
- Makes `current_user` available in subsequent requests

**Line 213**: `logger.info(f"User {username} logged in successfully")`
- Logs successful authentication event
- INFO level logging for audit trail
- Records username for security monitoring

**Line 214**: `return redirect(url_for('index'))`
- Redirects user to main page after successful login
- `url_for('index')` generates URL for the index() route
- Returns HTTP 302 redirect response

**Line 216**: `except LDAPBindError:`
- Catches authentication failure exceptions
- Raised when username/password is incorrect

**Line 217**: `# Authentication failed`
- Comment confirming credential failure

**Line 218**: `logger.warning(f"Failed login attempt for user {username}")`
- Logs failed authentication attempt
- WARNING level for security monitoring
- Helps detect brute force attacks

**Line 219**: `error_msg = "Invalid username or password"`
- Generic error message for security (doesn't reveal which field is wrong)
- Prevents username enumeration attacks

**Line 220**: `return render_template("login.html", error=error_msg)`
- Re-renders login form with error message
- User stays on login page with feedback
- `error` variable available in template to display message

**Line 222**: `except LDAPException as e:`
- Catches other LDAP-related errors (connection failures, etc.)
- Broader exception than LDAPBindError

**Line 223**: `logger.error(f"LDAP connection error: {e}")`
- Logs LDAP infrastructure errors
- ERROR level indicates system problem, not user error

**Line 224**: `return render_template("login.html", error=f"LDAP Connection Error: {str(e)}")`
- Shows technical error to user
- Helpful for diagnosing LDAP server issues
- May expose more information than desired in production

**Line 225**: `except ValueError as e:`
- Catches configuration errors (e.g., invalid port number)

**Line 226**: `logger.error(f"Configuration error in login: {e}")`
- Logs configuration problems
- ERROR level indicates setup issue

**Line 227**: `return render_template("login.html", error=f"Configuration Error: {str(e)}")`
- Displays configuration error to user
- Indicates application misconfiguration

**Line 229**: `return render_template("login.html")`
- Handles GET requests (outside the POST if-block)
- Displays empty login form
- No error message for initial page load

### Database Operations
None. Authentication is handled entirely by LDAP server.

### Error Handling

**Authentication Failures** (`LDAPBindError`):
- Logs failed attempt
- Returns form with generic error message
- User can retry

**LDAP Connection Errors** (`LDAPException`):
- Logs technical error
- Shows error details to user
- Indicates infrastructure problem

**Configuration Errors** (`ValueError`):
- Logs configuration issue
- Shows error to user
- Indicates application setup problem

### Security Considerations
- Uses LDAPS (LDAP over SSL) for encrypted credential transmission
- Generic error message prevents username enumeration
- Failed attempts are logged for audit trail
- Session management handled by Flask-Login
- HTTPS required for secure password transmission (configured in app.run)

---

## Route: `/logout` (Logout Handler)

### Route Definition
```python
@app.route("/logout")
@login_required
def logout():
    logger.info(f"User {current_user.username if hasattr(current_user, 'username') else 'unknown'} logged out")
    logout_user()
    return redirect(url_for('login'))
```

**Location in file**: Lines 231-236

### Purpose
Terminates the user's session and redirects to the login page.

### HTTP Methods
- **GET**: Default method, performs logout operation

### Authentication/Authorization
- **@login_required**: User must be logged in to log out
- Prevents unnecessary requests to logout endpoint

### Request Handling
No parameters required. Simple GET request.

### Line-by-line Analysis:

**Line 231**: `@app.route("/logout")`
- Registers route for `/logout` path
- GET method only (default behavior)

**Line 232**: `@login_required`
- Ensures only authenticated users can access
- Prevents errors from logout_user() being called on non-logged-in users

**Line 233**: `def logout():`
- Route handler function definition

**Line 234**: `logger.info(f"User {current_user.username if hasattr(current_user, 'username') else 'unknown'} logged out")`
- Logs logout event for audit trail
- `current_user`: Flask-Login proxy object for authenticated user
- `hasattr(current_user, 'username')`: Safely checks if username attribute exists
- Falls back to 'unknown' if username attribute is missing
- Conditional is defensive programming in case User object lacks username

**Line 235**: `logout_user()`
- Flask-Login function that terminates the session
- Removes session cookie
- Clears current_user context
- User is no longer authenticated after this call

**Line 236**: `return redirect(url_for('login'))`
- Redirects user to login page
- Standard practice after logout
- `url_for('login')` generates URL for login() route

### Database Operations
None. Session management is handled by Flask-Login.

### Error Handling
No explicit error handling. Flask-Login handles edge cases internally.

---

## Route: `/chat` (Chat Endpoint)

### Route Definition
```python
@app.route("/chat", methods=["POST"])
@login_required
@limiter.limit("30 per minute")
def chat():
```

**Location in file**: Lines 238-377

### Purpose
Main AI chat endpoint. Processes user messages, queries selected AI bot, auto-detects and formats code blocks, and stores conversation history in SQLite database.

### HTTP Methods
- **POST**: Accepts JSON payload with user message and AI model selection

### Authentication/Authorization
- **@login_required**: User must be authenticated
- **@limiter.limit("30 per minute")**: Rate limiting prevents abuse
- 30 messages per minute per IP address
- Prevents API quota exhaustion and abuse

### Request Handling

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "message": "User's chat message",
  "ai_model": "mistral"  // or "github-copilot"
}
```

### Line-by-line Analysis:

**Line 238**: `@app.route("/chat", methods=["POST"])`
- Registers route for `/chat` path
- POST method only (chat submissions)

**Line 239**: `@login_required`
- Requires authentication to use chat
- Prevents unauthorized API access

**Line 240**: `@limiter.limit("30 per minute")`
- Rate limiting decorator from Flask-Limiter
- Allows 30 chat requests per minute per IP address
- Returns HTTP 429 (Too Many Requests) if exceeded
- Protects against abuse and excessive API costs

**Line 241**: `def chat():`
- Route handler function definition

**Line 242**: `data = request.get_json()`
- Parses JSON request body into Python dictionary
- Returns None if request is not JSON or is invalid

**Line 243**: `user_msg = data.get("message", "")`
- Extracts user message from JSON data
- Defaults to empty string if "message" key is missing
- Safe access using `.get()` instead of `[]`

**Line 244**: `ai_model = data.get("ai_model", "mistral")`
- Extracts selected AI model identifier
- Defaults to "mistral" if not specified
- Can be "mistral" or "github-copilot"

**Line 246**: `if not user_msg:`
- Checks if message is empty or None
- Empty strings evaluate to False in Python

**Line 247**: `return jsonify({"response": "No message sent."})`
- Returns JSON error response
- `jsonify()` creates JSON response with correct Content-Type header
- Returns HTTP 200 with error message (could be improved to HTTP 400)

**Line 249**: `# Check if selected bot is available`
- Comment explaining bot availability check

**Line 250**: `if not bot_manager.is_bot_available(ai_model):`
- Queries bot manager to verify bot is configured
- Returns False if API key is missing or invalid

**Line 251**: `bot_names = {"mistral": "Mistral AI", "github-copilot": "GitHub Copilot"}`
- Maps bot IDs to display names
- Used for user-friendly error messages

**Line 252**: `bot_name = bot_names.get(ai_model, ai_model)`
- Gets display name for selected bot
- Falls back to bot ID if not in mapping

**Line 253**: `logger.warning(f"User attempted to use unavailable bot: {ai_model}")`
- Logs attempted use of unconfigured bot
- WARNING level indicates potential configuration issue

**Line 254-256**: `return jsonify({ "response": f"⚠️ {bot_name} is not configured. ..." })`
- Returns error message to user
- Unicode warning symbol (⚠️) for visual indication
- Suggests checking .env configuration

**Line 258**: `# Get the selected bot`
- Comment for bot retrieval section

**Line 259**: `selected_bot = bot_manager.get_bot(ai_model)`
- Retrieves bot instance from bot manager
- Returns bot object with `chat_complete()` and other methods

**Line 260**: `ai_provider = selected_bot.name`
- Gets the bot's name property
- Used in system prompt and logging

**Line 262-263**: `if not user_msg: return jsonify({"response": "No message sent."})`
- Duplicate check for empty message (redundant, already checked at line 246)
- Could be removed as it's unreachable code

**Line 265**: `# Warn if message is very long but allow up to 100k chars`
- Comment explaining message length handling

**Line 266**: `truncated = False`
- Initializes flag to track if message was truncated
- Used later to warn user

**Line 267**: `if len(user_msg) > 100000:`
- Checks if message exceeds 100,000 character limit
- Mistral can handle ~32k tokens (roughly 100k chars)

**Line 268**: `user_msg = user_msg[:100000]`
- Truncates message to first 100,000 characters
- Prevents API errors from excessive input length

**Line 269**: `truncated = True`
- Sets flag to indicate truncation occurred
- Will trigger warning in response

**Line 271**: `# Save user message WITHOUT HTML-escaping`
- Comment emphasizing raw storage
- HTML escaping handled by frontend during display

**Line 272**: `conn = get_db_connection()`
- Creates new SQLite database connection
- Function defined earlier (line 105)
- Each request gets its own connection

**Line 273**: `try:`
- Begin database operation with exception handling
- Ensures connection is closed even if error occurs

**Line 274**: `cursor = conn.cursor()`
- Creates cursor for executing SQL queries
- Cursor is required for all database operations

**Line 275**: `cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))`
- Inserts user message into database
- Uses parameterized query (?) to prevent SQL injection
- `role`: "user" indicates this is from the user (vs "assistant")
- `content`: The actual message text
- Timestamp is auto-generated by database (DEFAULT CURRENT_TIMESTAMP)

**Line 276**: `conn.commit()`
- Commits the transaction to database
- Makes the insert permanent
- Required for data to be saved

**Line 278**: `# Limit history based on AI model`
- Comment explaining history size limits

**Line 279**: `# GitHub Models has smaller context window`
- Explains why different limits are needed

**Line 280-281**: `if ai_model == "github-copilot": history_limit = 6`
- Sets history limit to 6 messages for GitHub Copilot
- 6 messages = last 3 exchanges (3 user + 3 assistant)
- GitHub Models has smaller context window than Mistral

**Line 282-283**: `else: history_limit = 20`
- Default limit of 20 messages for Mistral
- 20 messages = last 10 exchanges
- Mistral supports larger context (32k tokens)

**Line 285**: `cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (history_limit,))`
- Queries last N messages from database
- `ORDER BY id DESC`: Gets most recent messages first
- `LIMIT ?`: Uses parameterized limit value
- Returns list of (role, content) tuples

**Line 286**: `history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]`
- Fetches all results and converts to list of dictionaries
- `cursor.fetchall()`: Gets all rows from query result
- `reversed()`: Reverses order (oldest first for API)
- List comprehension creates proper message format for AI API

**Line 287**: `finally:`
- Ensures cleanup code runs regardless of exceptions

**Line 288**: `conn.close()`
- Closes database connection
- Releases database file lock
- Important for preventing connection leaks

**Line 290**: `# Add system prompt to ensure proper code formatting`
- Comment explaining system prompt injection

**Line 291**: `if not history or history[0].get("role") != "system":`
- Checks if history is empty OR first message isn't system prompt
- System prompt should always be first in message list

**Line 292**: `history.insert(0, {`
- Inserts system prompt at beginning of history
- Index 0 = first position in list

**Line 293**: `"role": "system",`
- System role instructs AI on behavior
- Different from "user" and "assistant" roles

**Line 294**: `"content": f"You are {ai_provider}, a helpful coding assistant. When showing code, you MUST ALWAYS use fenced code blocks with triple backticks (\`\`\`) and the language name. Example:\n\`\`\`python\nprint('hello')\n\`\`\`"`
- System prompt content
- Identifies AI provider name
- Emphasizes code formatting requirements
- Provides example of expected format
- Helps ensure consistent code block formatting

**Line 297**: `# Use bot manager to get response`
- Comment for AI API call section

**Line 298**: `try:`
- Exception handling for API calls
- API calls can fail for various reasons

**Line 299**: `logger.info(f"Chat request using {ai_model} - message length: {len(user_msg)}")`
- Logs each chat request
- INFO level for monitoring usage
- Records model and message length for debugging

**Line 300-304**: `bot_msg = bot_manager.chat(...)`
- Calls bot manager's chat method
- `bot_id=ai_model`: Specifies which bot to use
- `messages=history`: Passes conversation history
- `model="mistral-small-latest"`: Specifies Mistral model variant (only used for Mistral bot)
- Returns AI's response as string

**Line 305**: `except Exception as e:`
- Catches any exception from API call
- Network errors, API errors, timeout, etc.

**Line 306**: `logger.error(f"Error in chat with {ai_model}: {e}")`
- Logs API errors
- ERROR level indicates failed operation

**Line 307**: `bot_msg = f"❌ Error: {str(e)}"`
- Creates user-friendly error message
- Includes error details for debugging
- Unicode X emoji for visual indication

**Line 309**: `# Add truncation warning if message was cut`
- Comment for truncation warning section

**Line 310**: `if truncated:`
- Checks if message was truncated earlier

**Line 311**: `bot_msg = "⚠️ Your message was truncated to 100,000 characters due to length limits.\n\n" + bot_msg`
- Prepends warning to AI response
- Informs user their message was cut off
- Double newline for spacing

**Line 313**: `# Auto-detect and wrap code blocks if not already wrapped`
- Comment explaining code detection logic

**Line 314**: `# Look for common code patterns (indented blocks, function definitions, etc.)`
- Explains what patterns are detected

**Line 315**: `import re`
- Imports regex module for pattern matching
- Local import (only needed in this function)

**Line 317**: `# If response doesn't contain triple-backticks but has code-like content`
- Comment explaining when auto-wrapping applies

**Line 318**: `if '```' not in bot_msg:`
- Only auto-wrap if AI didn't already format code
- Prevents double-wrapping
- String contains check for triple backticks

**Line 319**: `# Pattern: Multiple lines starting with common code keywords or significant indentation`
- Comment explaining detection strategy

**Line 320**: `lines = bot_msg.split('\n')`
- Splits response into individual lines
- Allows line-by-line analysis

**Line 321**: `in_code_block = False`
- Flag to track if currently in a code block
- State machine approach

**Line 322**: `result_lines = []`
- Accumulator for processed lines
- Will contain final result with code blocks

**Line 323**: `code_buffer = []`
- Temporary buffer for accumulating code lines
- Flushed when code block ends

**Line 325**: `for i, line in enumerate(lines):`
- Iterates through each line with index
- Index available for contextual analysis

**Line 326**: `# Detect code: starts with 4+ spaces, HTML tags, regex patterns, or has code keywords at start`
- Comment explaining code detection logic

**Line 327**: `stripped = line.strip()`
- Removes leading/trailing whitespace
- Used for keyword detection

**Line 328-334**: `is_code_line = (...)`
- Complex boolean expression determining if line is code
- Multiple conditions OR'ed together

**Line 329**: `line.startswith('    ') or`
- Detects 4-space indentation (Python convention)

**Line 330**: `line.startswith('\t') or`
- Detects tab indentation

**Line 331**: `re.match(r'^\s*<[^>]+>', line) or`
- Regex matches HTML tags
- `^\s*`: Optional leading whitespace
- `<[^>]+>`: HTML tag structure

**Line 332**: `(stripped and ('regex' in stripped.lower() or '=/.*/' in stripped or r'\n' in stripped or r'\s' in stripped)) or`
- Detects regex pattern indicators
- Checks for keyword "regex" or regex pattern syntax

**Line 333**: `re.match(r'^\s*(def|class|function|const|let|var|if|for|while|import|from|#include|public|private)\s', line) or`
- Matches common programming language keywords
- Covers Python, JavaScript, C++, Java
- `\s` at end ensures keyword is followed by space

**Line 334**: `(stripped and re.match(r'^[a-zA-Z_]\w*\s*[=\(]', stripped))`
- Matches variable assignment or function call patterns
- `[a-zA-Z_]\w*`: Valid identifier
- `\s*[=\(]`: Followed by = or (

**Line 336**: `if is_code_line and not in_code_block:`
- Entering new code block
- Code line detected, not currently in block

**Line 337**: `# Start code block`
- Comment for state transition

**Line 338**: `in_code_block = True`
- Update state flag

**Line 339**: `code_buffer = [line]`
- Initialize buffer with first code line

**Line 340**: `elif is_code_line and in_code_block:`
- Already in code block, code continues

**Line 341**: `# Continue code block`
- Comment for accumulation

**Line 342**: `code_buffer.append(line)`
- Add line to code buffer

**Line 343**: `elif not is_code_line and in_code_block:`
- Non-code line detected, end of code block

**Line 344**: `# End code block if we have 3+ lines of code`
- Comment explaining minimum threshold

**Line 345**: `if len(code_buffer) >= 3:`
- Only wrap blocks with 3+ lines
- Prevents over-wrapping of inline code

**Line 346**: `# Detect language using helper function`
- Comment for language detection

**Line 347**: `lang = detect_language('\n'.join(code_buffer))`
- Calls helper function (defined at line 133)
- Joins buffer into single string for analysis
- Returns language identifier

**Line 348**: `result_lines.append(f'```{lang}')`
- Adds opening code fence with language

**Line 349**: `result_lines.extend(code_buffer)`
- Adds all code lines to result

**Line 350**: `result_lines.append('```')`
- Adds closing code fence

**Line 351-353**: `else: ... result_lines.extend(code_buffer)`
- Buffer too short (< 3 lines)
- Keep as regular text without wrapping

**Line 355**: `code_buffer = []`
- Clear buffer for next code block

**Line 356**: `in_code_block = False`
- Reset state flag

**Line 357**: `result_lines.append(line)`
- Add current (non-code) line to result

**Line 358**: `else:`
- Line is not code, not in code block

**Line 359**: `# Regular text line`
- Comment for normal text

**Line 360**: `result_lines.append(line)`
- Add line to result as-is

**Line 362**: `# Handle any remaining code at end`
- Comment for cleanup

**Line 363**: `if in_code_block and len(code_buffer) >= 3:`
- Code block at end of message
- Has minimum 3 lines

**Line 364**: `lang = detect_language('\n'.join(code_buffer))`
- Detect language of final code block

**Line 365**: `result_lines.append(f'```{lang}')`
- Add opening fence

**Line 366**: `result_lines.extend(code_buffer)`
- Add code lines

**Line 367**: `result_lines.append('```')`
- Add closing fence

**Line 368**: `elif code_buffer:`
- Code buffer exists but < 3 lines

**Line 369**: `result_lines.extend(code_buffer)`
- Add as regular text (no wrapping)

**Line 371**: `bot_msg = '\n'.join(result_lines)`
- Reconstruct message from processed lines
- Joins with newlines to restore structure

**Line 373**: `# Save bot response`
- Comment for database save

**Line 374**: `conn = get_db_connection()`
- Opens new database connection

**Line 375**: `try:`
- Exception handling for save operation

**Line 376**: `cursor = conn.cursor()`
- Creates cursor for query

**Line 377**: `cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))`
- Inserts AI response into database
- `role`: "assistant" indicates bot response
- `content`: Processed response with code blocks

**Line 378**: `conn.commit()`
- Commits transaction

**Line 379**: `finally:`
- Cleanup block

**Line 380**: `conn.close()`
- Closes connection

**Line 382**: `return jsonify({"response": bot_msg})`
- Returns JSON response to frontend
- Contains processed AI response with formatted code blocks

### Database Operations

**INSERT User Message**:
- Table: `messages`
- Columns: `role`, `content`, `timestamp` (auto)
- Purpose: Store user's message for history

**SELECT History**:
- Table: `messages`
- Query: Last N messages (6-20 depending on model)
- Purpose: Build conversation context for AI

**INSERT Bot Response**:
- Table: `messages`
- Columns: `role`, `content`, `timestamp` (auto)
- Purpose: Store AI's response for history

### Error Handling

**Empty Message**:
- Returns: JSON error message
- Status: 200 (should be 400)

**Bot Not Available**:
- Logs: Warning
- Returns: Configuration error message

**API Call Failure**:
- Logs: Error with details
- Returns: Error message to user

**Database Errors**:
- Connection closed in `finally` block
- Errors propagate to Flask error handler

### Rate Limiting

- **Limit**: 30 requests per minute per IP
- **Exceeded**: Returns HTTP 429
- **Purpose**: Prevent abuse and API cost overruns
- **Storage**: In-memory (resets on restart)

---

## Route: `/upload` (File Upload)

### Route Definition
```python
@app.route("/upload", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def upload():
```

**Location in file**: Lines 384-419

### Purpose
Handles file uploads (primarily screenshots) and analyzes them using Mistral Vision API. Stores uploaded files and analysis results in database.

### HTTP Methods
- **POST**: Accepts multipart/form-data with file attachment

### Authentication/Authorization
- **@login_required**: User must be authenticated
- **@limiter.limit("10 per minute")**: Rate limiting (10 uploads per minute per IP)
- More restrictive than chat endpoint due to larger data transfer

### Request Handling

**Content-Type**: `multipart/form-data`

**Form Fields**:
- `screendump`: File field containing uploaded image

### Line-by-line Analysis:

**Line 384**: `@app.route("/upload", methods=["POST"])`
- Registers route for `/upload` path
- POST method only (file uploads)

**Line 385**: `@login_required`
- Requires authentication
- Prevents unauthorized file uploads

**Line 386**: `@limiter.limit("10 per minute")`
- Rate limiting: 10 uploads per minute per IP
- Prevents abuse and excessive storage usage
- More restrictive than chat (30/min)

**Line 387**: `def upload():`
- Route handler function definition

**Line 388**: `if "screendump" not in request.files:`
- Checks if file field exists in request
- `request.files`: MultiDict containing uploaded files
- "screendump" is the expected form field name

**Line 389**: `return jsonify({"response": "No file uploaded."})`
- Returns error if no file field present
- JSON format for consistency with chat endpoint

**Line 391**: `file = request.files["screendump"]`
- Retrieves file object from request
- FileStorage object with filename, save() method, etc.

**Line 392**: `if file.filename == "":`
- Checks if filename is empty string
- Happens when form submitted without file selected
- Different from field not existing (line 388)

**Line 393**: `return jsonify({"response": "No file selected."})`
- Returns error for empty filename
- User-friendly error message

**Line 395**: `# Save file`
- Comment for file saving section

**Line 396**: `file_path = os.path.join(UPLOAD_FOLDER, file.filename)`
- Constructs full path for saved file
- `UPLOAD_FOLDER`: "static/uploads" (defined at line 162)
- `file.filename`: Original filename from client
- **Security Note**: No sanitization of filename (potential vulnerability)

**Line 397**: `file.save(file_path)`
- Saves uploaded file to disk
- Writes file content to specified path
- **Security Note**: Should validate file type and sanitize filename

**Line 399**: `# Analyze image with Mistral Vision`
- Comment for vision analysis section

**Line 400**: `try:`
- Exception handling for vision API call

**Line 401**: `bot = bot_manager.get_bot('mistral')`
- Gets Mistral bot instance
- Only Mistral supports vision API (not GitHub Copilot)

**Line 402**: `if bot and bot.is_available:`
- Checks if Mistral bot is configured and available
- Two conditions: bot exists AND is properly configured

**Line 403-406**: `response_text = bot.analyze_image(...)`
- Calls Mistral Vision API
- `file_path`: Path to saved image
- `prompt`: Instructions for image analysis
- Analyzes screenshot content, identifies text, UI elements, code

**Line 407**: `else:`
- Mistral bot not available

**Line 408**: `response_text = f"Screenshot '{file.filename}' received and saved (vision analysis not available)."`
- Fallback message when vision unavailable
- Still confirms file was saved
- User knows analysis didn't happen

**Line 409**: `except Exception as e:`
- Catches vision API errors
- Network errors, API errors, invalid image format

**Line 410**: `logger.error(f"Error analyzing image: {str(e)}")`
- Logs error for debugging
- ERROR level indicates failed operation

**Line 411**: `response_text = f"Screenshot '{file.filename}' received and saved, but analysis failed: {str(e)}"`
- Error message includes filename and error details
- User informed of partial success (file saved)

**Line 413**: `# Save message to database`
- Comment for database operations

**Line 414**: `conn = get_db_connection()`
- Opens database connection

**Line 415**: `try:`
- Exception handling for database operations

**Line 416**: `cursor = conn.cursor()`
- Creates cursor for queries

**Line 417**: `cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))`
- Inserts user message indicating upload
- `role`: "user"
- `content`: Placeholder with filename
- Square brackets indicate system-generated message

**Line 418**: `cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))`
- Inserts analysis result as assistant message
- Contains vision API's analysis or error message
- Maintains conversation continuity

**Line 419**: `conn.commit()`
- Commits both messages to database

**Line 420**: `finally:`
- Cleanup block

**Line 421**: `conn.close()`
- Closes database connection

**Line 423**: `return jsonify({"response": response_text})`
- Returns analysis result to frontend
- Same format as chat endpoint for consistency

### Database Operations

**INSERT User Upload Notification**:
- Table: `messages`
- Content: "[Uploaded screenshot: filename]"
- Purpose: Record upload event in conversation

**INSERT Vision Analysis**:
- Table: `messages`
- Content: Analysis result or error message
- Purpose: Store AI's interpretation of image

### Error Handling

**No File Field**:
- Returns: "No file uploaded" error
- Status: 200 (should be 400)

**Empty Filename**:
- Returns: "No file selected" error

**Vision API Error**:
- Logs: Error with details
- Returns: Error message with filename
- File still saved despite analysis failure

**Database Errors**:
- Connection closed in `finally` block
- Errors propagate to Flask error handler

### Security Considerations

**Vulnerabilities**:
1. **Filename Injection**: No sanitization of `file.filename`
   - Could contain path traversal (../)
   - Could overwrite existing files
   
2. **File Type Validation**: No checking of file type
   - User could upload malicious files
   - Should validate MIME type and extension

3. **File Size Limits**: No size limit enforcement
   - Could fill disk with large files
   - Flask has default limit, but should be explicit

**Recommendations**:
- Use `secure_filename()` from `werkzeug.utils`
- Validate file extension against whitelist
- Check MIME type using `magic` library
- Enforce file size limit
- Generate unique filenames to prevent overwrites

### Rate Limiting
- **Limit**: 10 uploads per minute per IP
- **Rationale**: Files larger than text, vision API costs
- **Exceeded**: Returns HTTP 429

---

## Route: `/history` (Chat History)

### Route Definition
```python
@app.route("/history", methods=["GET"])
@login_required
def history():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
        history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
        return jsonify({"history": history})
    finally:
        conn.close()
```

**Location in file**: Lines 421-429

### Purpose
Retrieves recent chat history from database. Used for loading conversation history when page refreshes or user logs back in.

### HTTP Methods
- **GET**: Returns conversation history as JSON

### Authentication/Authorization
- **@login_required**: User must be authenticated
- History is global (not per-user) - all users see same history
- **Privacy Issue**: Should filter by user

### Request Handling
No parameters required. Simple GET request.

### Line-by-line Analysis:

**Line 421**: `@app.route("/history", methods=["GET"])`
- Registers route for `/history` path
- GET method for retrieving data

**Line 422**: `@login_required`
- Requires authentication to view history
- Prevents unauthorized access

**Line 423**: `def history():`
- Route handler function definition

**Line 424**: `conn = get_db_connection()`
- Opens database connection
- Function defined at line 105

**Line 425**: `try:`
- Exception handling for database operation

**Line 426**: `cursor = conn.cursor()`
- Creates cursor for query

**Line 427**: `cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")`
- Queries last 50 messages from database
- `SELECT role, content`: Gets message metadata
- `ORDER BY id DESC`: Most recent first
- `LIMIT 50`: Caps at 50 messages to prevent large responses
- **Note**: No timestamp selected, but could be useful

**Line 428**: `history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]`
- Fetches all results and converts to list of dictionaries
- `cursor.fetchall()`: Returns all 50 rows
- `reversed()`: Reverses order (oldest first for display)
- List comprehension creates JSON-serializable format
- Result: `[{"role": "user", "content": "..."}, ...]`

**Line 429**: `return jsonify({"history": history})`
- Returns history as JSON object
- Wrapped in "history" key
- Frontend can iterate and display messages

**Line 430**: `finally:`
- Cleanup block

**Line 431**: `conn.close()`
- Closes database connection
- Runs even if exception occurs

### Database Operations

**SELECT Recent Messages**:
- Table: `messages`
- Columns: `role`, `content`
- Limit: 50 messages
- Order: Most recent first (reversed for client)

### Error Handling
No explicit error handling. Database errors propagate to Flask's error handler.

### Response Format
```json
{
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    ...
  ]
}
```

### Privacy and Security Issues

**Major Issue**: History is global, not per-user
- All authenticated users see same conversation history
- User A can see User B's messages
- Violates privacy expectations

**Recommended Fix**:
1. Add `user_id` column to `messages` table
2. Store current user's ID with each message
3. Filter query: `WHERE user_id = ?`
4. Requires user ID to be part of User object

**Current Workaround**:
- If only one user, not a problem
- For multi-user deployment, requires database schema change

---

## Application Entry Point

### Code
```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))
```

**Location in file**: Lines 431-432

### Line-by-line Analysis:

**Line 431**: `if __name__ == "__main__":`
- Checks if script is run directly (not imported)
- Standard Python idiom for executable scripts

**Line 432**: `app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))`
- Starts Flask development server
- `host="0.0.0.0"`: Listens on all network interfaces (not just localhost)
- `port=5000`: HTTP port (actually HTTPS with SSL context)
- `debug=False`: Disables debug mode (production-ready)
- `ssl_context=('cert.pem','key.pem')`: Enables HTTPS
  - `cert.pem`: SSL certificate file
  - `key.pem`: Private key file
  - Files must exist in project root

### Purpose
- Enables HTTPS for secure password transmission
- Makes app accessible from other machines on network
- Development server (production should use Gunicorn)

### Security Notes
- HTTPS required for LDAP authentication (passwords in transit)
- Debug mode OFF prevents information leakage
- Certificate should be valid (not self-signed) in production

---

## Summary

### Total Routes: 7

1. **`/`** - Main chat interface page
2. **`/debug`** - Debug/diagnostics page
3. **`/login`** - LDAP authentication handler
4. **`/logout`** - Session termination
5. **`/chat`** - AI chat processing endpoint
6. **`/upload`** - File upload and vision analysis
7. **`/history`** - Conversation history retrieval

### Key Features

**Authentication**:
- LDAP/Active Directory integration
- Flask-Login session management
- HTTPS for secure transmission

**Rate Limiting**:
- Chat: 30 requests/minute
- Upload: 10 requests/minute
- Global limits: 200/day, 50/hour

**Multi-Model AI Support**:
- Mistral AI (including vision)
- GitHub Copilot
- Dynamic bot selection

**Code Formatting**:
- Auto-detection of code blocks
- Language identification
- Automatic syntax highlighting

**Data Persistence**:
- SQLite database for history
- File storage for uploads
- Conversation continuity

### Security Considerations

**Strengths**:
- LDAP authentication
- HTTPS encryption
- Rate limiting
- Session management

**Weaknesses**:
- No filename sanitization in uploads
- No file type validation
- Global chat history (privacy issue)
- Error messages expose technical details
- No CSRF protection

### Architecture Patterns

**Separation of Concerns**:
- Bot logic in `bot_manager.py`
- Routes in `main.py`
- Templates in `templates/`
- Database abstraction with connection helper

**Error Handling**:
- Try-finally for resource cleanup
- Logging at appropriate levels
- User-friendly error messages

**Scalability Limitations**:
- In-memory rate limiting (doesn't scale across processes)
- SQLite database (single-writer limitation)
- Development server (not production-ready)

---

## Recommendations

### High Priority

1. **User Isolation**: Add per-user chat history
2. **File Security**: Sanitize filenames and validate file types
3. **Production Server**: Use Gunicorn instead of Flask dev server
4. **CSRF Protection**: Add Flask-WTF CSRF tokens
5. **Error Messages**: Don't expose technical details to users

### Medium Priority

6. **Persistent Rate Limiting**: Use Redis for rate limit storage
7. **Database Migration**: Consider PostgreSQL for production
8. **Logging**: Add request ID tracking for debugging
9. **Monitoring**: Add metrics for API usage and errors
10. **Input Validation**: Add request schema validation

### Low Priority

11. **API Documentation**: Add OpenAPI/Swagger docs
12. **Testing**: Add unit and integration tests
13. **Caching**: Cache bot availability checks
14. **Pagination**: Add pagination to history endpoint
15. **WebSocket**: Consider WebSocket for real-time chat

---

**Documentation Created**: December 3, 2025
**Source File**: `/home/kasperadm/projects/AzikiAI-codingbot/main.py`
**Total Lines Documented**: 439 lines analyzed
**Routes Documented**: 7 routes with complete line-by-line analysis
