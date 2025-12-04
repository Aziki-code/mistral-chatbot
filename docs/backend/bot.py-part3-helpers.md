# bot.py - Part 3: Helper Functions and Utilities

## Overview
This document details all helper functions and utility code in the main.py file. These functions provide essential services for database operations, language detection, user management, and configuration.

---

## Table of Contents
1. [Database Helper Functions](#database-helper-functions)
2. [Language Detection Utility](#language-detection-utility)
3. [User Management Functions](#user-management-functions)
4. [Configuration and Initialization](#configuration-and-initialization)

---

## Database Helper Functions

### 1. get_db_connection()

**Location:** Lines 108-112

```python
def get_db_connection():
    """Create a new database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
```

#### Purpose
Creates and returns a new SQLite database connection for storing and retrieving chat history messages.

#### Parameters
None

#### Returns
- `sqlite3.Connection`: A connection object to the SQLite database with Row factory enabled

#### Line-by-Line Explanation

**Line 108-109:** Function definition with docstring
- Function takes no parameters and is designed to be called whenever database access is needed

**Line 110:** `conn = sqlite3.connect(db_path)`
- Creates a connection to the SQLite database file specified by `db_path`
- `db_path` is defined globally as: `os.path.join(os.path.dirname(__file__), "chat_history.db")`
- If the database file doesn't exist, SQLite will create it automatically
- Opens database in read-write mode by default

**Line 111:** `conn.row_factory = sqlite3.Row`
- Sets the row factory to `sqlite3.Row` class
- This allows accessing columns by name instead of just by index
- Example: `row['content']` instead of `row[1]`
- Makes code more readable and less prone to errors from column reordering

**Line 112:** `return conn`
- Returns the configured connection object to the caller
- Caller is responsible for closing the connection when done

#### Usage Pattern
```python
# Typical usage
conn = get_db_connection()
try:
    cursor = conn.cursor()
    # ... perform database operations
    conn.commit()
finally:
    conn.close()
```

#### Error Handling
- If database file cannot be accessed, `sqlite3.connect()` will raise `sqlite3.OperationalError`
- No explicit error handling in this function - errors propagate to caller
- Connection must be manually closed by caller to prevent resource leaks

#### Dependencies
- `sqlite3` module (standard library)
- `db_path` global variable
- File system access to the database location

---

### 2. init_db()

**Location:** Lines 114-129

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

#### Purpose
Creates the database schema if it doesn't already exist. Called once at application startup to ensure the messages table is available.

#### Parameters
None

#### Returns
None

#### Line-by-Line Explanation

**Line 114-115:** Function definition with docstring
- No parameters needed as it operates on the global database

**Line 116:** `conn = get_db_connection()`
- Obtains a database connection using the helper function
- This connection will be used to create the schema

**Line 117:** `try:`
- Begins try-finally block to ensure connection is always closed
- Using finally ensures cleanup even if an exception occurs

**Line 118:** `cursor = conn.cursor()`
- Creates a cursor object for executing SQL commands
- Cursor is used to execute queries and fetch results

**Line 119-126:** SQL CREATE TABLE statement
- **Line 120:** `CREATE TABLE IF NOT EXISTS messages`
  - Creates table only if it doesn't already exist
  - Safe to call multiple times without errors
  - Table name is "messages"

- **Line 121:** `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - Primary key column that auto-increments
  - Unique identifier for each message
  - SQLite automatically creates an index on primary keys

- **Line 122:** `role TEXT NOT NULL`
  - Stores the message role (e.g., "user", "assistant", "system")
  - TEXT type for variable-length strings
  - NOT NULL constraint ensures every message has a role

- **Line 123:** `content TEXT NOT NULL`
  - Stores the actual message content
  - TEXT type can store large strings (up to 1GB in SQLite)
  - NOT NULL ensures no empty messages are stored

- **Line 124:** `timestamp DATETIME DEFAULT CURRENT_TIMESTAMP`
  - Automatically records when the message was created
  - DEFAULT CURRENT_TIMESTAMP means SQLite fills this in automatically
  - No need to explicitly set timestamp when inserting

**Line 127:** `conn.commit()`
- Commits the transaction to save the schema changes
- Without commit, changes would be lost when connection closes

**Line 128-129:** Finally block
- Ensures the connection is closed regardless of success or failure
- Releases database lock and frees resources

#### Database Schema Details

The `messages` table structure:
- **id**: Auto-incrementing integer, unique identifier
- **role**: Text field for message sender ("user", "assistant", "system")
- **content**: Text field for message content (supports large text)
- **timestamp**: Automatically set to current time on insert

#### Usage
Called once at application startup:
```python
# Initialize database on startup
init_db()
```

#### Error Handling
- If table creation fails, exception propagates to caller
- Connection is always closed via finally block
- CREATE TABLE IF NOT EXISTS prevents errors if table already exists

#### Dependencies
- `get_db_connection()` function
- SQLite3 module
- Writable filesystem for database file

---

## Language Detection Utility

### 3. detect_language()

**Location:** Lines 134-157

```python
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

#### Purpose
Analyzes code snippets to automatically determine the programming language. Used for syntax highlighting by adding appropriate language tags to code blocks.

#### Parameters
- **code** (str): The code content to analyze

#### Returns
- **str**: Language identifier string such as:
  - 'python' - Python code
  - 'html' - HTML markup
  - 'javascript' - JavaScript code
  - 'java' - Java code
  - 'css' - CSS stylesheets
  - 'sql' - SQL queries
  - 'plaintext' - Unknown or plain text

#### Line-by-Line Explanation

**Line 134-142:** Function signature and docstring
- Type hints indicate string input and string output
- Comprehensive docstring explains parameters and return value

**Line 143:** `code_lower = code.lower()`
- Converts entire code string to lowercase
- Makes pattern matching case-insensitive
- Original code is preserved, only the comparison copy is lowercased

**Line 145-151:** Language pattern dictionary
- Dictionary mapping language names to their identifying patterns
- Each language has a list of characteristic strings to look for

**Line 146:** `'html': ['<html', '<!doctype', '<div', '<script>']`
- HTML patterns: common tags and declarations
- Looking for markup structure indicators
- Most HTML documents contain at least one of these

**Line 147:** `'python': ['def ', 'import ', 'print(', 'class ', '__init__']`
- Python patterns: function definitions, imports, print statements, classes
- Trailing spaces prevent false matches (e.g., "define" vs "def ")
- `__init__` is unique to Python class constructors

**Line 148:** `'javascript': ['function', 'const ', 'let ', 'var ', '=>']`
- JavaScript patterns: function keyword, variable declarations, arrow functions
- Covers both ES5 (function, var) and ES6+ (const, let, arrow functions)

**Line 149:** `'java': ['public class', 'private ', 'void main']`
- Java patterns: access modifiers and main method
- These are distinctive to Java syntax
- "public class" is very common in Java files

**Line 150:** `'css': ['{', '}', 'color:', 'background:']`
- CSS patterns: curly braces and common properties
- Note: curly braces alone aren't definitive (many languages use them)
- CSS properties like 'color:' and 'background:' are more specific

**Line 151:** `'sql': ['select ', 'from ', 'where ', 'insert into']`
- SQL patterns: common query keywords
- Covers both read (SELECT) and write (INSERT) operations
- Case-insensitive matching catches SELECT, select, Select, etc.

**Line 153-155:** Pattern matching loop
```python
for lang, patterns in language_patterns.items():
    if any(pattern in code_lower for pattern in patterns):
        return lang
```

**Line 153:** `for lang, patterns in language_patterns.items():`
- Iterates through each language and its patterns
- `lang` is the language name (string)
- `patterns` is the list of identifying strings for that language

**Line 154:** `if any(pattern in code_lower for pattern in patterns):`
- `any()` returns True if at least one pattern matches
- Generator expression checks each pattern in the code
- `pattern in code_lower` performs substring search
- Short-circuits on first match for efficiency

**Line 155:** `return lang`
- Returns the language name immediately upon first match
- Order matters: HTML is checked before JavaScript (since JS can be in HTML)

**Line 157:** `return 'plaintext'`
- Default fallback if no patterns match
- Ensures function always returns a valid language string
- 'plaintext' is safe for syntax highlighting (no highlighting applied)

#### Algorithm Logic

1. Convert code to lowercase for case-insensitive matching
2. Define pattern dictionary with language signatures
3. Iterate through languages in order
4. For each language, check if ANY pattern appears in the code
5. Return first matching language
6. If no match, return 'plaintext'

#### Usage Example
```python
# In the chat route, when auto-wrapping code
code_snippet = "def hello():\n    print('Hello')"
language = detect_language(code_snippet)
# Returns: 'python'

# Wrapping in markdown code block
result = f"```{language}\n{code_snippet}\n```"
```

#### Limitations and Considerations

1. **Ambiguity**: Some code might match multiple languages
   - Order in dictionary matters (first match wins)
   - HTML checked before CSS/JavaScript to avoid confusion

2. **False Positives**: 
   - Curly braces in CSS also match many C-style languages
   - Common words might appear in comments

3. **False Negatives**:
   - Code snippets without characteristic keywords might be missed
   - Unusual or minimal code might not contain any patterns

4. **Performance**:
   - Simple substring search is very fast
   - O(n*m) where n is code length, m is total pattern count
   - Short-circuits on first match

5. **Enhancement Opportunities**:
   - Could add more languages (Ruby, Go, Rust, etc.)
   - Could use regex for more sophisticated patterns
   - Could weight patterns by reliability
   - Could check file extensions if available

#### Error Handling
- No explicit error handling needed
- Function always returns a valid string
- `str.lower()` and `in` operator won't raise exceptions on valid strings
- Default return value prevents None returns

#### Dependencies
- No external dependencies
- Uses only built-in Python string operations
- Pure function with no side effects

---

## User Management Functions

### 4. User Class

**Location:** Lines 85-94

```python
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

#### Purpose
Represents an authenticated user in the application. Integrates with Flask-Login to manage user sessions and authentication state.

#### Class Inheritance
- **UserMixin**: Provided by Flask-Login
- Provides default implementations for:
  - `is_authenticated` (returns True)
  - `is_active` (returns True)
  - `is_anonymous` (returns False)

#### Constructor: `__init__(self, dn, username, data)`

**Parameters:**
- **dn** (str): Distinguished Name from LDAP (unique identifier)
- **username** (str): User's login username
- **data** (dict): Additional user data from LDAP

**Line-by-Line Explanation:**

**Line 86:** `def __init__(self, dn, username, data):`
- Constructor method called when creating new User instance
- Takes three required parameters beyond self

**Line 87:** `self.dn = dn`
- Stores the Distinguished Name (DN) from LDAP
- Format example: "CN=john.doe,CN=Users,DC=Area51,DC=local"
- DN uniquely identifies the user in the LDAP directory
- Used as the user ID for Flask-Login

**Line 88:** `self.username = username`
- Stores the username (typically the sAMAccountName)
- Human-readable identifier
- Used for display and logging purposes
- Example: "john.doe"

**Line 89:** `self.data = data`
- Stores additional LDAP attributes
- Dictionary containing user information like:
  - Email address
  - Full name
  - Department
  - Group memberships
- Can be empty if using simple authentication

#### Method: `__repr__(self)`

**Location:** Lines 91-92

```python
def __repr__(self):
    return self.dn
```

**Purpose:**
- Provides string representation of User object
- Used when printing or logging User instances

**Returns:**
- The user's Distinguished Name (DN)

**Usage Example:**
```python
user = User("CN=john,CN=Users,DC=example,DC=com", "john", {})
print(user)  # Output: CN=john,CN=Users,DC=example,DC=com
```

#### Method: `get_id(self)`

**Location:** Lines 94-95

```python
def get_id(self):
    return self.dn
```

**Purpose:**
- Required by Flask-Login to identify users
- Returns unique identifier stored in session
- Called by Flask-Login to load user from session

**Returns:**
- The user's Distinguished Name (DN) as a string

**Why DN as ID:**
- DN is guaranteed unique in LDAP
- Persists across sessions
- Can be used to reload user data from LDAP if needed

#### Integration with Flask-Login

The User class works with these Flask-Login components:

1. **Session Management:**
   - Flask-Login calls `get_id()` to store user identifier in session
   - Session cookie contains encrypted user ID

2. **User Loading:**
   - `@login_manager.user_loader` uses the ID to recreate User object
   - Called on each request to load current_user

3. **Authentication State:**
   - Inherited methods from UserMixin provide authentication checks
   - `@login_required` decorator uses these methods

#### Usage Examples

**Creating a user after LDAP authentication:**
```python
# In login route
user = User(user_dn, username, {})
login_user(user)
```

**Accessing current user in routes:**
```python
@app.route("/profile")
@login_required
def profile():
    print(f"Current user: {current_user.username}")
    print(f"User DN: {current_user.dn}")
    return render_template("profile.html", user=current_user)
```

**Logging user actions:**
```python
logger.info(f"User {current_user.username} performed action")
```

#### Security Considerations

1. **DN in Session:**
   - Session is encrypted by Flask using SECRET_KEY
   - DN is safe to store as long as SECRET_KEY is secure

2. **No Password Storage:**
   - User object never stores passwords
   - Authentication handled by LDAP
   - Sessions expire requiring re-authentication

3. **Minimal Data:**
   - Only essential data stored
   - Additional data can be fetched from LDAP when needed

---

### 5. load_user()

**Location:** Lines 96-98

```python
@login_manager.user_loader
def load_user(user_id):
    # Return a user object based on the user_id (DN)
    return User(user_id, user_id.split(',')[0].split('=')[1], {})
```

#### Purpose
Callback function for Flask-Login to reload a user object from the session. Called on every request when a user is logged in.

#### Decorator
- **@login_manager.user_loader**: Registers this function as the user loader callback
- Flask-Login calls this function to convert user ID to User object

#### Parameters
- **user_id** (str): The user's Distinguished Name (DN) retrieved from session

#### Returns
- **User**: New User object with the given DN

#### Line-by-Line Explanation

**Line 96:** `@login_manager.user_loader`
- Decorator that registers this function with Flask-Login
- Must be applied to exactly one function in the application
- Flask-Login will call this function on each request for authenticated users

**Line 97:** `def load_user(user_id):`
- Function name can be anything, but `load_user` is conventional
- Takes user_id parameter which is the return value from User.get_id()
- User_id is retrieved from the encrypted session cookie

**Line 98:** `return User(user_id, user_id.split(',')[0].split('=')[1], {})`
- Creates and returns a new User object
- Let's break down the username extraction:

**Username Extraction Logic:**
```python
user_id.split(',')[0].split('=')[1]
```

1. **`user_id.split(',')`**:
   - Splits DN by commas
   - DN format: "CN=john.doe,CN=Users,DC=Area51,DC=local"
   - Result: ['CN=john.doe', 'CN=Users', 'DC=Area51', 'DC=local']

2. **`[0]`**:
   - Gets first component
   - Result: 'CN=john.doe'

3. **`.split('=')`**:
   - Splits by equals sign
   - Result: ['CN', 'john.doe']

4. **`[1]`**:
   - Gets the value part (after =)
   - Result: 'john.doe'

**Full Example:**
```python
user_id = "CN=john.doe,CN=Users,DC=Area51,DC=local"
username = user_id.split(',')[0].split('=')[1]
# username = "john.doe"
```

**Empty Data Dictionary:**
- Third parameter is empty dict `{}`
- User data not stored in session
- Additional data can be fetched from LDAP if needed
- Keeps session size small

#### Request Flow

1. **User logs in:**
   ```python
   user = User(dn, username, data)
   login_user(user)  # Flask-Login calls user.get_id() and stores in session
   ```

2. **Subsequent requests:**
   ```python
   # Flask-Login automatically:
   # 1. Reads user_id from session
   # 2. Calls load_user(user_id)
   # 3. Sets result as current_user
   ```

3. **Accessing current user:**
   ```python
   @app.route("/dashboard")
   @login_required
   def dashboard():
       # current_user is the User object returned by load_user
       return f"Welcome {current_user.username}"
   ```

#### Performance Considerations

- Called on **every request** with authenticated user
- Very lightweight - no database or LDAP queries
- Just string parsing and object creation
- Minimal memory footprint

#### Error Handling

**Potential Issues:**
1. **Malformed DN:**
   - If DN doesn't contain comma or equals sign, will raise IndexError
   - Should never happen with valid LDAP DNs
   - Session tampering would be caught by encryption check first

2. **Invalid Session:**
   - If session is invalid, Flask-Login sets current_user to AnonymousUser
   - No error raised - graceful degradation

**Improvement Opportunity:**
```python
@login_manager.user_loader
def load_user(user_id):
    try:
        username = user_id.split(',')[0].split('=')[1]
        return User(user_id, username, {})
    except (IndexError, AttributeError):
        # Invalid user_id format
        return None  # Flask-Login treats as logged out
```

#### Security Considerations

1. **Session Security:**
   - User_id in session is encrypted by Flask's SECRET_KEY
   - Can't be tampered without secret key
   - Session expires after configured timeout

2. **No Password in Session:**
   - Only DN stored, never passwords
   - Authentication state managed by session
   - Re-authentication required after session expires

3. **Minimal Data Exposure:**
   - Only DN and derived username in User object
   - Additional sensitive data not cached
   - Can be fetched from LDAP on-demand if needed

#### Alternative Implementation

For applications needing more user data:
```python
@login_manager.user_loader
def load_user(user_id):
    # Fetch from database
    user_data = db.query(User).filter_by(dn=user_id).first()
    if user_data:
        return User(user_data.dn, user_data.username, user_data.attributes)
    return None
```

---

### 6. save_user()

**Location:** Lines 100-102

```python
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    # Create and return user object after successful LDAP authentication
    return User(dn, username, data)
```

#### Purpose
Callback function for Flask-LDAP3-Login to create a User object after successful LDAP authentication. Converts LDAP authentication data into application User object.

#### Decorator
- **@ldap_manager.save_user**: Registers this function with Flask-LDAP3-Login
- Called automatically after successful LDAP bind
- Required callback for LDAP integration

#### Parameters

- **dn** (str): Distinguished Name of authenticated user
  - Example: "CN=john.doe,CN=Users,DC=Area51,DC=local"
  - Unique identifier in LDAP directory

- **username** (str): Username that was used to authenticate
  - Example: "john.doe"
  - Typically the sAMAccountName attribute

- **data** (dict): LDAP attributes retrieved for the user
  - Contains user information from LDAP directory
  - May include: email, full name, department, etc.
  - Structure depends on LDAP schema and query

- **memberships** (list): LDAP groups the user belongs to
  - List of group DNs
  - Example: ["CN=Admins,CN=Groups,DC=Area51,DC=local"]
  - Can be used for role-based access control

#### Returns
- **User**: New User object representing the authenticated user

#### Line-by-Line Explanation

**Line 100:** `@ldap_manager.save_user`
- Decorator provided by Flask-LDAP3-Login
- Registers this function as the user factory callback
- Called after LDAP bind succeeds but before login_user()

**Line 101:** `def save_user(dn, username, data, memberships):`
- Function name can be anything
- Four parameters passed by Flask-LDAP3-Login
- Parameters populated from LDAP authentication response

**Line 102:** `return User(dn, username, data)`
- Creates new User instance with LDAP data
- Note: `memberships` parameter not passed to User constructor
- Could be included in `data` dict if needed for RBAC
- Returned User object is then passed to `login_user()`

#### Authentication Flow

1. **User submits credentials:**
   ```
   POST /login
   username: john.doe
   password: ********
   ```

2. **LDAP authentication:**
   ```python
   # Flask-LDAP3-Login internally:
   # 1. Builds user DN
   # 2. Attempts LDAP bind with DN and password
   # 3. If successful, queries user attributes
   ```

3. **save_user() called:**
   ```python
   # Flask-LDAP3-Login calls:
   user = save_user(
       dn="CN=john.doe,CN=Users,DC=Area51,DC=local",
       username="john.doe",
       data={"mail": "john@example.com", "displayName": "John Doe"},
       memberships=["CN=Admins,CN=Groups,DC=Area51,DC=local"]
   )
   ```

4. **User logged in:**
   ```python
   # Flask-LDAP3-Login then calls:
   login_user(user)
   ```

#### Current Implementation Note

**This function is defined but not actively used** in the current implementation. The application uses manual LDAP authentication in the `/login` route instead:

```python
# In /login route (lines 195-227):
# Manual LDAP authentication
conn = Connection(server, user=user_dn, password=password, auto_bind=True)
conn.unbind()

# Manual user creation (not using save_user)
user = User(user_dn, username, {})
login_user(user)
```

#### Why Manual Authentication?

The code switched to manual LDAP authentication for:
1. **Direct control** over the authentication process
2. **Better error handling** for connection issues
3. **Custom SSL/TLS configuration** (CERT_NONE)
4. **Simpler debugging** of LDAP issues

#### If Using Flask-LDAP3-Login

If the application used Flask-LDAP3-Login's built-in authentication:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LDAPLoginForm()
    
    if form.validate_on_submit():
        # Flask-LDAP3-Login handles authentication
        # save_user() is called automatically
        # User is logged in automatically
        return redirect(url_for('index'))
    
    return render_template("login.html", form=form)
```

#### Enhanced Implementation Example

For applications needing group-based access control:

```python
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    # Check if user is in required group
    required_group = "CN=ChatbotUsers,CN=Groups,DC=Area51,DC=local"
    
    if required_group not in memberships:
        logger.warning(f"User {username} not in required group")
        return None  # Deny access
    
    # Determine role from group membership
    role = 'user'
    if "CN=Admins,CN=Groups,DC=Area51,DC=local" in memberships:
        role = 'admin'
    
    # Include role and groups in user object
    user_data = {
        **data,  # Spread LDAP attributes
        'role': role,
        'groups': memberships
    }
    
    return User(dn, username, user_data)
```

#### Accessing User Data

If LDAP data was stored in User object:

```python
@app.route("/profile")
@login_required
def profile():
    email = current_user.data.get('mail', 'No email')
    full_name = current_user.data.get('displayName', current_user.username)
    role = current_user.data.get('role', 'user')
    
    return render_template("profile.html", 
                         email=email, 
                         name=full_name,
                         role=role)
```

#### Security Considerations

1. **Group Membership Validation:**
   - Can enforce access control based on LDAP groups
   - Return None to deny authentication
   - Log unauthorized access attempts

2. **Data Storage:**
   - Be careful what LDAP data is stored in session
   - Large data increases session size
   - Sensitive data should not be cached

3. **Re-authentication:**
   - LDAP data in User object is only fetched at login
   - Changes in LDAP (like group membership) require re-login
   - Consider token expiration for security-sensitive applications

#### Dependencies
- Flask-LDAP3-Login library
- User class
- LDAP configuration in app.config

---

## Configuration and Initialization

### 7. Application Bootstrap and Configuration

**Location:** Lines 1-131

This section covers the initialization sequence and configuration of the Flask application.

#### Environment Variables Loading

**Lines 1-14:**
```python
#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_ldap3_login import LDAP3LoginManager
from flask_ldap3_login.forms import LDAPLoginForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import sqlite3
import logging

# --- Load .env FIRST before any other imports that need environment variables ---
load_dotenv()
```

**Line 1:** `#!/usr/bin/env python3`
- Shebang line for Unix systems
- Allows script to be executed directly
- Specifies Python 3 interpreter

**Lines 2-11:** Import statements
- **Flask core**: Web framework components
- **Flask-Login**: User session management
- **Flask-LDAP3-Login**: LDAP authentication integration
- **Flask-Limiter**: Rate limiting to prevent abuse
- **dotenv**: Environment variable loading from .env file
- **os, sqlite3, logging**: Standard library utilities

**Line 14:** `load_dotenv()`
- **Critical**: Must be called before importing modules that use env vars
- Loads variables from `.env` file into `os.environ`
- Variables loaded: LDAP_HOST, MISTRAL_API_KEY, SECRET_KEY, etc.
- If .env doesn't exist, no error raised - continues with system env vars

**Why Load Early:**
```python
# WRONG - bot_manager tries to use env vars before they're loaded:
from bot_manager import get_bot_manager
load_dotenv()

# CORRECT - load env vars first:
load_dotenv()
from bot_manager import get_bot_manager
```

#### Bot Manager Initialization

**Lines 16-18:**
```python
# Import Bot Manager AFTER loading .env
from bot_manager import get_bot_manager
```

**Purpose:**
- Imports the bot manager after environment variables are loaded
- Bot manager needs API keys from environment
- Comment emphasizes the ordering requirement

**Lines 35-40:**
```python
try:
    bot_manager = get_bot_manager()
    logger.info("Bot manager initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize bot manager: {e}")
    raise
```

**Line 35:** `try:`
- Begin exception handling for bot manager initialization
- Critical step - app can't function without bots

**Line 36:** `bot_manager = get_bot_manager()`
- Gets singleton instance of BotManager
- BotManager loads all configured AI bots (Mistral, GitHub Copilot)
- Reads API keys from environment variables
- Initializes API clients

**Line 37:** `logger.info("Bot manager initialized successfully")`
- Logs successful initialization
- Important for debugging startup issues
- Confirms at least one bot is available

**Lines 38-40:** Exception handling
- Catches any initialization errors
- Logs as CRITICAL level (highest severity)
- Re-raises exception to stop app startup
- Better to fail fast than run with broken bots

#### Logging Configuration

**Lines 20-31:**
```python
# --- Configure Logging ---
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'azikiai.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
```

**Line 21:** `log_dir = os.path.join(os.path.dirname(__file__), 'logs')`
- Gets directory where main.py is located: `os.path.dirname(__file__)`
- Joins with 'logs' subdirectory
- Result: `/home/kasperadm/projects/AzikiAI-codingbot/logs`

**Line 22:** `os.makedirs(log_dir, exist_ok=True)`
- Creates logs directory if it doesn't exist
- `exist_ok=True` prevents error if directory already exists
- Ensures log file can be written

**Lines 24-30:** `logging.basicConfig(...)`
- Configures root logger for entire application

**Line 25:** `level=logging.INFO`
- Sets minimum log level to INFO
- Levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
- INFO and above will be logged, DEBUG filtered out

**Line 26:** Format string breakdown:
```python
'%(asctime)s [%(levelname)s] %(name)s: %(message)s'
```
- `%(asctime)s`: Timestamp (e.g., "2025-12-03 14:30:45,123")
- `[%(levelname)s]`: Log level (e.g., "[INFO]", "[ERROR]")
- `%(name)s`: Logger name (e.g., "__main__", "bot_manager")
- `%(message)s`: The actual log message

Example output:
```
2025-12-03 14:30:45,123 [INFO] __main__: Bot manager initialized successfully
2025-12-03 14:30:46,456 [WARNING] __main__: User attempted to use unavailable bot: mistral
```

**Lines 27-30:** Handlers (output destinations)
1. **FileHandler**: Writes to `logs/azikiai.log`
   - Persistent logging for debugging and auditing
   - File appended to (not overwritten) on each run
   
2. **StreamHandler**: Writes to console (stdout)
   - Real-time monitoring during development
   - Captured by systemd when running as service

**Line 31:** `logger = logging.getLogger(__name__)`
- Creates logger instance for this module
- `__name__` is "__main__" when script run directly
- Used throughout the file for logging

#### Flask Application Setup

**Lines 42-44:**
```python
# --- Flask app ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')
```

**Line 43:** `app = Flask(__name__)`
- Creates Flask application instance
- `__name__` tells Flask the root path for templates/static files

**Line 44:** Secret key configuration
- `os.getenv('SECRET_KEY', '...')`: Get from environment or use default
- **SECRET_KEY**: Used for session encryption and CSRF protection
- Default value is for development only - insecure for production
- Should be set in .env file for production deployment

**Security Note:**
```python
# In .env file:
SECRET_KEY=randomly-generated-64-character-string-for-production
```

#### Rate Limiting Configuration

**Lines 46-51:**
```python
# --- Rate Limiting ---
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
```

**Line 47:** `limiter = Limiter(...)`
- Creates rate limiter instance
- Prevents API abuse and DoS attacks

**Line 48:** `app=app`
- Associates limiter with Flask application
- Required parameter

**Line 49:** `key_func=get_remote_address`
- Function to identify users for rate limiting
- Uses client IP address from request
- Same IP = same user for rate limit purposes

**Line 50:** `default_limits=["200 per day", "50 per hour"]`
- Default limits applied to all routes
- Per IP address:
  - Maximum 200 requests per day
  - Maximum 50 requests per hour
- More strict limits applied per route (e.g., 30/min for chat)

**Line 51:** `storage_uri="memory://"`
- Stores rate limit counters in memory
- Fast but resets on application restart
- For production, consider Redis: `storage_uri="redis://localhost:6379"`

**Usage in Routes:**
```python
@app.route("/chat", methods=["POST"])
@login_required
@limiter.limit("30 per minute")  # Override default with stricter limit
def chat():
    # ...
```

#### LDAP Configuration

**Lines 53-76:**
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
app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True  # Enable direct credential binding
app.config['LDAP_BIND_DIRECT_SUFFIX'] = ''  # Will use full DN
app.config['LDAP_BIND_DIRECT_GET_USER_INFO'] = True

# SSL/TLS Configuration - Don't validate certificate for internal AD
import ssl
from ldap3 import Tls
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
app.config['LDAP_TLS_CONFIG'] = tls_configuration
```

**Line 54:** `app.config['LDAP_HOST'] = os.getenv('LDAP_HOST')`
- LDAP server hostname or IP
- Example: 'ad.area51.local' or '192.168.1.10'
- Must be set in .env file

**Line 55:** `app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN')`
- Base Distinguished Name for LDAP directory
- Example: 'DC=Area51,DC=local'
- Root of LDAP tree structure

**Line 56:** `app.config['LDAP_USER_DN']`
- Where to search for user accounts
- Default: 'CN=Users,DC=Area51,DC=local'
- Fallback provided if env var not set

**Line 57:** `app.config['LDAP_GROUP_DN'] = ''`
- Empty string = group search disabled
- Could be set to 'CN=Groups,DC=Area51,DC=local' for group queries

**Line 58:** `app.config['LDAP_USER_RDN_ATTR'] = 'cn'`
- Relative Distinguished Name attribute
- 'cn' = Common Name
- Comment indicates changed from 'sAMAccountName'

**Line 59:** `app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'`
- Attribute used for login username
- sAMAccountName is Windows username
- Example: 'john.doe' (not full email)

**Lines 60-61:** Direct bind configuration
- `LDAP_BIND_USER_DN = None`: No service account used
- `LDAP_BIND_USER_PASSWORD = None`: No service account password
- Users authenticate with their own credentials directly

**Line 62:** `app.config['LDAP_USE_SSL'] = True`
- Enable SSL/TLS encryption
- Protects credentials in transit
- Required for secure LDAP (LDAPS on port 636)

**Lines 63-65:** Direct credential binding
- `LDAP_BIND_DIRECT_CREDENTIALS = True`: Authenticate users directly
- `LDAP_BIND_DIRECT_SUFFIX = ''`: No suffix appended to username
- `LDAP_BIND_DIRECT_GET_USER_INFO = True`: Fetch user attributes after auth

**Lines 67-72:** SSL/TLS Configuration
```python
import ssl
from ldap3 import Tls
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
app.config['LDAP_TLS_CONFIG'] = tls_configuration
```

**Line 71:** `Tls(validate=ssl.CERT_NONE, ...)`
- **validate=ssl.CERT_NONE**: Don't verify SSL certificate
- **WARNING**: Security risk - vulnerable to MITM attacks
- Used because internal AD uses self-signed certificate
- **Production**: Should use valid certificates and CERT_REQUIRED

**Line 71:** `version=ssl.PROTOCOL_TLSv1_2`
- Use TLS 1.2 protocol
- More secure than older versions (SSLv3, TLS 1.0)
- Widely supported by Active Directory

#### Flask-Login Setup

**Lines 78-80:**
```python
# --- Flask-Login Setup ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ldap_manager = LDAP3LoginManager(app)
```

**Line 79:** `login_manager = LoginManager(app)`
- Initializes Flask-Login extension
- Manages user sessions and authentication state
- Provides @login_required decorator

**Line 80:** `login_manager.login_view = 'login'`
- Sets the route name for login page
- When @login_required fails, redirects to this route
- 'login' refers to the function decorated with @app.route('/login')

**Line 81:** `ldap_manager = LDAP3LoginManager(app)`
- Initializes Flask-LDAP3-Login extension
- Provides LDAP authentication callbacks
- Note: Currently not actively used (manual LDAP auth in use)

#### Database Initialization

**Lines 104-129:**
```python
# --- SQLite setup ---
db_path = os.path.join(os.path.dirname(__file__), "chat_history.db")

def get_db_connection():
    # ... (documented above)

def init_db():
    # ... (documented above)

# Initialize database on startup
init_db()
```

**Line 105:** `db_path = os.path.join(...)`
- Constructs path to SQLite database file
- Placed in same directory as main.py
- Full path: `/home/kasperadm/projects/AzikiAI-codingbot/chat_history.db`

**Line 131:** `init_db()`
- Called immediately at module load
- Creates database schema if needed
- Safe to call multiple times (CREATE TABLE IF NOT EXISTS)
- Ensures database ready before first request

#### Upload Folder Setup

**Lines 159-161:**
```python
# --- Upload folder ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
```

**Line 160:** Upload folder path
- Images uploaded via /upload endpoint saved here
- Path: `/home/kasperadm/projects/AzikiAI-codingbot/static/uploads`
- In static folder so can be served by Flask

**Line 161:** `os.makedirs(UPLOAD_FOLDER, exist_ok=True)`
- Creates upload directory on startup
- `exist_ok=True` prevents error if already exists
- Ensures uploads won't fail due to missing directory

#### Initialization Summary

**Startup Sequence:**
1. Load environment variables (.env file)
2. Configure logging (file + console)
3. Import bot manager after env vars loaded
4. Initialize bot manager (loads AI bot clients)
5. Create Flask application
6. Configure secret key for session encryption
7. Setup rate limiting
8. Configure LDAP authentication
9. Initialize Flask-Login
10. Create database schema
11. Create upload directory

**Critical Dependencies:**
- Environment variables must be loaded first
- Bot manager initialization must succeed
- Database schema must be created
- Directories must exist (logs, uploads)

**Error Handling:**
- Bot manager failure stops application (raise exception)
- Missing directories created automatically
- Missing .env falls back to defaults (dev mode)
- LDAP errors handled per-request in login route

---

## Summary

This document covered all helper functions and utility code in main.py:

### Database Functions
1. **get_db_connection()** - Creates SQLite connections with Row factory
2. **init_db()** - Initializes database schema on startup

### Utility Functions
3. **detect_language()** - Auto-detects programming language from code snippets

### User Management
4. **User class** - Represents authenticated users with Flask-Login integration
5. **load_user()** - Reloads user from session on each request
6. **save_user()** - Creates user after LDAP authentication (currently unused)

### Configuration & Initialization
7. **Application bootstrap** - Environment loading, logging, LDAP config, database setup

### Key Takeaways

**Database Operations:**
- Simple SQLite with no ORM for lightweight deployment
- Connection must be manually closed in try-finally blocks
- Row factory enables dict-like access to results

**Language Detection:**
- Pattern-based matching with fallback to plaintext
- Fast and simple but limited accuracy
- Used for automatic syntax highlighting

**User Management:**
- Minimal user data stored in session
- DN used as unique identifier
- Manual LDAP authentication for better control

**Configuration:**
- Environment-first approach with .env file
- Proper initialization ordering critical
- Fail-fast on critical component failure

**Security Considerations:**
- SSL certificate validation disabled (CERT_NONE) - should fix for production
- Rate limiting prevents abuse
- Sessions encrypted with SECRET_KEY
- No passwords stored anywhere

---

*Documentation complete. Total: 6 main functions/classes documented with comprehensive line-by-line explanations.*
