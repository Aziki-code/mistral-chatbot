# chatbot_sql.py - DETAILED DOCUMENTATION

## File Overview
**Note:** There is no separate `chatbot_sql.py` file. All SQL/database functionality is embedded within `main.py`. This document provides comprehensive documentation of all SQL-related code in the AzikiAI Chatbot application.

**Purpose:** Database operations for storing and retrieving chat conversation history using SQLite3.

**Location:** SQL code is located in `/home/kasperadm/projects/AzikiAI-codingbot/main.py`

**Database File:** `chat_history.db` (SQLite database stored in application root directory)

---

## Imports Related to Database

### Line 10: `import sqlite3`
```python
import sqlite3
```
**Purpose:** Imports Python's built-in SQLite3 module for database operations.
- **SQLite3:** Lightweight, serverless, self-contained SQL database engine
- **Why used:** No external database server required, perfect for small-to-medium chat history storage
- **Thread-safety:** Each connection is created per-request to avoid threading issues

---

## Database Configuration

### Lines 101-102: Database Path Setup
```python
# --- SQLite setup ---
db_path = os.path.join(os.path.dirname(__file__), "chat_history.db")
```

**Line-by-line breakdown:**
1. **`os.path.dirname(__file__)`** - Gets the directory where `main.py` is located
   - `__file__` is the absolute path to the current Python file
   - `os.path.dirname()` extracts just the directory portion
   
2. **`os.path.join(..., "chat_history.db")`** - Constructs full database file path
   - Joins directory path with database filename
   - Creates: `/home/kasperadm/projects/AzikiAI-codingbot/chat_history.db`
   - Uses `os.path.join()` for cross-platform compatibility (handles `/` vs `\`)

3. **`db_path`** - Module-level variable storing the database location
   - Accessible throughout the entire application
   - Used by all database functions to locate the SQLite file

---

## Database Functions

### Function 1: `get_db_connection()`

**Lines 104-108:**
```python
def get_db_connection():
    """Create a new database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
```

#### Function Signature
```python
get_db_connection() -> sqlite3.Connection
```

#### Purpose
Creates and configures a new SQLite database connection for each request. This function is called whenever the application needs to interact with the database.

#### Parameters
**None** - Uses the module-level `db_path` variable

#### Return Value
- **Type:** `sqlite3.Connection` object
- **Description:** Active database connection with row factory configured
- **Usage:** Must be closed after use (typically in a `try/finally` block)

#### Line-by-Line Explanation

**Line 106: `conn = sqlite3.connect(db_path)`**
- **Purpose:** Opens/creates SQLite database connection
- **Behavior:**
  - If `chat_history.db` exists: Opens existing database
  - If `chat_history.db` doesn't exist: Creates new database file
- **Connection properties:**
  - Each call creates a **new, independent** connection
  - Connection is not shared between threads (thread-safe design)
  - Autocommit is OFF by default (requires explicit `conn.commit()`)

**Line 107: `conn.row_factory = sqlite3.Row`**
- **Purpose:** Configures how rows are returned from queries
- **Without this setting:** Rows returned as plain tuples: `(1, 'user', 'Hello', '2025-12-03 10:30:00')`
- **With this setting:** Rows returned as `sqlite3.Row` objects that act like dictionaries
- **Benefits:**
  - Access columns by name: `row['role']` instead of `row[1]`
  - More readable and maintainable code
  - Reduces errors from column position changes
- **Example:**
  ```python
  row = cursor.fetchone()
  # Without row_factory:
  role = row[1]  # Must remember position
  
  # With row_factory:
  role = row['role']  # Clear and self-documenting
  ```

**Line 108: `return conn`**
- Returns the configured connection object
- Caller is responsible for closing the connection
- Connection remains open until explicitly closed or program exits

#### Error Handling
- **No explicit error handling in this function**
- Errors propagate to caller (typically caught in route handlers)
- Common errors:
  - `sqlite3.OperationalError`: Database is locked
  - `PermissionError`: No write access to directory
  - `sqlite3.DatabaseError`: Database file corrupted

#### Usage Pattern
```python
conn = get_db_connection()
try:
    cursor = conn.cursor()
    # ... database operations ...
    conn.commit()
finally:
    conn.close()  # Always close connection
```

---

### Function 2: `init_db()`

**Lines 110-125:**
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

#### Function Signature
```python
init_db() -> None
```

#### Purpose
Initializes the database schema by creating the `messages` table if it doesn't exist. This function is idempotent (safe to run multiple times).

#### Parameters
**None**

#### Return Value
**None** - Side effect: Creates database table

#### Line-by-Line Explanation

**Line 112: `conn = get_db_connection()`**
- Calls the connection function to get a database connection
- If database file doesn't exist, it's created now

**Lines 113-124: Try/Finally Block**
- **Purpose:** Ensures connection is closed even if error occurs
- **Try block:** Contains database operations
- **Finally block:** Cleanup (connection close) always executes

**Line 114: `cursor = conn.cursor()`**
- **Purpose:** Creates a cursor object for executing SQL commands
- **Cursor:** Database pointer that tracks position in result set
- **Why needed:** SQLite requires cursor to execute SQL statements
- **Properties:**
  - Maintains state for queries
  - Can execute multiple SQL statements
  - Iterates through result sets

**Lines 115-123: CREATE TABLE SQL Statement**
```sql
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

**SQL Breakdown:**

**`CREATE TABLE IF NOT EXISTS messages`**
- **`CREATE TABLE`**: SQL command to create new table
- **`IF NOT EXISTS`**: Prevents error if table already exists
  - If table exists: Statement does nothing (no error)
  - If table doesn't exist: Creates table with specified schema
- **`messages`**: Table name (stores chat messages)

**Column 1: `id INTEGER PRIMARY KEY AUTOINCREMENT`**
- **`id`**: Column name - unique identifier for each message
- **`INTEGER`**: Data type - whole number
- **`PRIMARY KEY`**: Constraints:
  - Uniquely identifies each row
  - Cannot be NULL
  - Creates automatic index for fast lookups
  - Only one primary key per table
- **`AUTOINCREMENT`**: Behavior:
  - SQLite automatically assigns next available integer
  - Starts at 1, increments by 1 for each insert
  - Never reuses IDs even after deletion
  - Guarantees ID values always increase
- **Usage:** `id` tracks message order and provides unique reference

**Column 2: `role TEXT NOT NULL`**
- **`role`**: Column name - identifies message sender
- **`TEXT`**: Data type - variable-length string
  - Can store strings of any length (up to SQLite limits)
  - No length restriction needed
- **`NOT NULL`**: Constraint:
  - Column must have a value
  - Cannot insert/update with NULL or missing value
  - Enforces data integrity
- **Values stored:** 
  - `"user"` - Message from human user
  - `"assistant"` - Message from AI bot
  - `"system"` - System prompt/instructions

**Column 3: `content TEXT NOT NULL`**
- **`content`**: Column name - the actual message text
- **`TEXT`**: Data type - variable-length string
  - Stores full message content
  - Can handle very long messages (up to ~2GB in SQLite)
- **`NOT NULL`**: Required field
  - Empty messages not allowed
  - Ensures every message has content
- **Storage:** 
  - User questions
  - AI responses (including code blocks)
  - System prompts
  - Special messages (upload notifications)

**Column 4: `timestamp DATETIME DEFAULT CURRENT_TIMESTAMP`**
- **`timestamp`**: Column name - when message was created
- **`DATETIME`**: Data type - date and time value
  - Format: 'YYYY-MM-DD HH:MM:SS'
  - Example: '2025-12-03 14:30:45'
  - SQLite stores as TEXT internally
- **`DEFAULT CURRENT_TIMESTAMP`**: Default value behavior:
  - If no timestamp provided on INSERT, uses current time
  - `CURRENT_TIMESTAMP` is SQLite built-in function
  - Automatically set by database, not application
  - Always uses UTC time
- **Nullable:** Column can be NULL (no NOT NULL constraint)
  - Though default ensures value is always set
- **Usage:** Track conversation chronology, debugging, audit trail

**Line 123: `conn.commit()`**
- **Purpose:** Saves all pending changes to database file
- **How it works:**
  - SQLite uses transactions (changes held in memory)
  - `commit()` writes transaction to disk
  - Makes changes permanent and visible to other connections
- **Without commit:**
  - Changes exist only in memory
  - Lost when connection closes
  - Not visible to other connections
- **Atomicity:** Either all changes commit or none (ACID properties)

**Lines 124-125: Finally Block**
```python
finally:
    conn.close()
```
- **Purpose:** Release database connection resources
- **Why in finally:**
  - Executes even if error occurs in try block
  - Prevents connection leaks
  - Releases file locks on database
- **Effect of close:**
  - Commits any uncommitted changes (auto-commit on close)
  - Releases locks
  - Frees memory
  - Connection object becomes unusable

#### Error Handling
- **Implicit:** Errors propagate to startup routine
- **Possible Errors:**
  - `sqlite3.OperationalError`: File permissions, disk full
  - `sqlite3.DatabaseError`: Corrupt database file
- **Recovery:** Application logs error and may fail to start

#### Usage
**Line 127-128: Startup Initialization**
```python
# Initialize database on startup
init_db()
```
- Called once when application starts
- Ensures database and table exist before handling requests
- Safe to call multiple times (idempotent due to `IF NOT EXISTS`)

---

## Database Operations in Routes

### Operation 1: INSERT User Message

**Location:** `/chat` route, Lines 273-275

```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
conn.commit()
```

#### Context
This code runs when a user sends a chat message to the AI bot.

#### Line-by-Line Explanation

**Line 274: SQL INSERT Statement**
```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
```

**SQL Breakdown:**
- **`INSERT INTO messages`**: Insert new row into `messages` table
- **`(role, content)`**: Columns to populate (omits `id` and `timestamp`)
  - `id`: Auto-generated by AUTOINCREMENT
  - `timestamp`: Auto-set by DEFAULT CURRENT_TIMESTAMP
  - Only need to provide `role` and `content`
- **`VALUES (?, ?)`**: Placeholder syntax for parameterized query
  - **`?`**: Positional parameter placeholders
  - Prevents SQL injection attacks
  - Values bound at execution time
- **`("user", user_msg)`**: Tuple of parameter values
  - First `?` replaced with `"user"` (role is always "user" for user messages)
  - Second `?` replaced with `user_msg` (actual message content from JSON request)

**Why Parameterized Queries?**
```python
# UNSAFE (vulnerable to SQL injection):
cursor.execute(f"INSERT INTO messages VALUES ('{role}', '{content}')")

# SAFE (parameterized query):
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
```
- **Security:** Prevents SQL injection attacks
- **Automatic escaping:** SQLite handles special characters (quotes, etc.)
- **Type safety:** Proper data type conversion
- **Performance:** Query plan can be cached

**Example with real data:**
```python
user_msg = "How do I use Python's sqlite3 module?"
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
# Results in: INSERT INTO messages (role, content) VALUES ('user', 'How do I use Python''s sqlite3 module?')
```

**Line 275: Commit Transaction**
```python
conn.commit()
```
- Writes the INSERT to disk
- Makes user message permanent
- Must commit before querying to ensure data is visible

#### Error Handling
Wrapped in try/finally block (lines 271-280) ensuring connection closes

---

### Operation 2: SELECT Chat History

**Location:** `/chat` route, Lines 278-285

```python
# Limit history based on AI model
# GitHub Models has smaller context window
if ai_model == "github-copilot":
    history_limit = 6  # Only last 3 exchanges (6 messages)
else:
    history_limit = 20  # Mistral can handle more

cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (history_limit,))
history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
```

#### Purpose
Retrieves recent conversation history to provide context to the AI model.

#### Context Window Management

**Lines 278-282: Dynamic History Limit**
```python
if ai_model == "github-copilot":
    history_limit = 6  # Only last 3 exchanges (6 messages)
else:
    history_limit = 20  # Mistral can handle more
```

**Rationale:**
- Different AI models have different context window sizes
- **GitHub Copilot (via GitHub Models API):**
  - Smaller context window
  - Limit to 6 messages = 3 exchanges (user + assistant, user + assistant, user + assistant)
  - Prevents exceeding token limits
- **Mistral AI:**
  - Larger context window (~32k tokens)
  - Can handle 20 messages = 10 exchanges
  - Provides more conversation context for better responses

**Lines 284-285: History Query**
```python
cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (history_limit,))
history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
```

**SQL Query Breakdown:**

**Line 284: `SELECT role, content FROM messages ORDER BY id DESC LIMIT ?`**

- **`SELECT role, content`**: Retrieve only these two columns
  - Don't need `id` or `timestamp` for AI context
  - Reduces data transfer and memory usage
  
- **`FROM messages`**: Query the messages table
  
- **`ORDER BY id DESC`**: Sort by ID in descending order
  - **`id`**: Primary key (chronological order due to AUTOINCREMENT)
  - **`DESC`**: Descending order (newest first)
  - Result: Most recent messages come first in result set
  
- **`LIMIT ?`**: Restrict number of rows returned
  - **`?`**: Parameterized limit value
  - Bound to `history_limit` variable (6 or 20)
  - More efficient than fetching all and slicing in Python

**Query Example:**
```sql
-- If history_limit = 6:
SELECT role, content FROM messages ORDER BY id DESC LIMIT 6

-- Returns (example):
-- ('assistant', 'Here is the code...')   -- id: 105 (newest)
-- ('user', 'Show me Python code')        -- id: 104
-- ('assistant', 'Let me explain...')     -- id: 103
-- ('user', 'What is SQLite?')            -- id: 102
-- ('assistant', 'Hello! How can I...')   -- id: 101
-- ('user', 'Hi')                          -- id: 100 (oldest in result)
```

**Line 285: Process Results**
```python
history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
```

**Breakdown:**

1. **`cursor.fetchall()`**: Retrieves all rows from last query
   - Returns list of `sqlite3.Row` objects (due to `row_factory`)
   - In newest-first order (because of `ORDER BY id DESC`)
   - Example: `[Row('assistant', 'response'), Row('user', 'question'), ...]`

2. **`reversed(...)`**: Reverses the order
   - Changes from newest-first to oldest-first
   - AI models expect chronological order (oldest to newest)
   - Now: `[Row('user', 'Hi'), Row('assistant', 'Hello!'), ...]`

3. **`for role, content in ...`**: Unpacks each Row object
   - Tuple unpacking: `role, content = row`
   - Extracts the two column values
   - Works because we selected exactly 2 columns

4. **`{"role": role, "content": content}`**: Creates dictionary
   - Converts Row object to plain dictionary
   - Format required by AI model APIs
   - Structure: `{"role": "user", "content": "message text"}`

5. **List comprehension `[... for ...]`**: Builds list
   - Creates list of dictionaries
   - One dictionary per message
   - Final result stored in `history` variable

**Result Example:**
```python
history = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I help?"},
    {"role": "user", "content": "What is SQLite?"},
    {"role": "assistant", "content": "SQLite is a database..."},
    {"role": "user", "content": "Show me Python code"},
    {"role": "assistant", "content": "Here is the code..."}
]
```

#### Why Reverse Order?

**Database Storage:** Messages stored with auto-incrementing IDs
```
id: 100 - "Hi"                      (oldest)
id: 101 - "Hello!"
id: 102 - "What is SQLite?"
id: 103 - "SQLite is..."
id: 104 - "Show me Python code"
id: 105 - "Here is the code..."     (newest)
```

**Query Returns:** Newest first (DESC order)
```
id: 105 - "Here is the code..."     (first in result)
id: 104 - "Show me Python code"
...
id: 100 - "Hi"                      (last in result)
```

**AI Needs:** Oldest first (chronological context)
```
id: 100 - "Hi"                      (first in context)
id: 101 - "Hello!"
...
id: 105 - "Here is the code..."     (last in context)
```

**Solution:** `reversed()` flips the newest-first to oldest-first

#### Performance Considerations

**Why ORDER BY + LIMIT + reversed() instead of ORDER BY ASC?**

```python
# Current approach (efficient):
# 1. Get N newest with DESC + LIMIT (fast - uses index)
# 2. Reverse in Python (negligible cost for small lists)

# Alternative (less efficient):
# 1. Get all messages ordered ASC
# 2. Slice last N in Python (scans entire table)
```

- **Index usage:** `ORDER BY id DESC LIMIT N` uses primary key index efficiently
- **Database efficiency:** LIMIT reduces rows transferred from database
- **Memory efficiency:** Only N rows loaded into memory, not entire table
- **Python reverse:** O(N) operation on small list (6-20 items) is negligible

---

### Operation 3: INSERT Assistant Response

**Location:** `/chat` route, Lines 376-377

```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
conn.commit()
```

#### Purpose
Saves the AI bot's response to the database after generating it.

#### Line-by-Line Explanation

**Line 377: INSERT Statement**
```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
```

**Differences from User Message Insert:**
- **Role value:** `"assistant"` instead of `"user"`
  - Identifies message as AI-generated response
  - Used when retrieving history to format conversation
- **Content value:** `bot_msg` - AI's complete response
  - May contain markdown formatting
  - Can include code blocks with triple backticks
  - Can be very long (multiple paragraphs, code examples)

**Example:**
```python
bot_msg = """Here's how to use SQLite in Python:

```python
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
```

This creates a database connection."""

cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
```

**Storage:** Entire formatted response (including markdown and code blocks) stored as-is

**Line 378: Commit**
```python
conn.commit()
```
- Makes assistant's response permanent
- Completes the conversation turn
- Next request will see this message in history

#### Context Block

**Lines 374-379: Full Context**
```python
# Save bot response
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
    conn.commit()
finally:
    conn.close()
```

**Flow:**
1. Get new database connection
2. Create cursor
3. Insert assistant message
4. Commit transaction
5. Close connection (in finally block)

**Error Handling:**
- Wrapped in try/finally
- Connection always closed
- Errors propagate to route handler

---

### Operation 4: INSERT Upload Notification

**Location:** `/upload` route, Lines 412-414

```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))
conn.commit()
```

#### Purpose
Records file upload events and AI analysis in conversation history.

#### Line-by-Line Explanation

**Line 413: User Upload Message**
```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))
```

- **Role:** `"user"` - upload initiated by user
- **Content:** Special formatted message indicating file upload
- **Format:** `[Uploaded screenshot: {file.filename}]`
  - Square brackets indicate system-generated message
  - Shows filename of uploaded image
  - Example: `[Uploaded screenshot: error_screen.png]`

**Line 414: Assistant Analysis Message**
```python
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))
```

- **Role:** `"assistant"` - AI's analysis of image
- **Content:** `response_text` - AI vision model's description
  - Describes what's in the screenshot
  - Identifies UI elements, code, text
  - Provides analysis of image content

**Line 415: Commit Both Messages**
```python
conn.commit()
```
- Single commit for both INSERT statements
- Transaction includes both messages (atomic)
- If commit fails, neither message is saved

#### Example Conversation Entry

```python
# Upload flow creates two messages:
1. {"role": "user", "content": "[Uploaded screenshot: code_error.png]"}
2. {"role": "assistant", "content": "I can see a Python error in your code. The error message shows..."}
```

#### Context Block

**Lines 410-417: Full Upload Context**
```python
# Save message to database
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))
    conn.commit()
finally:
    conn.close()
```

**Multi-statement Transaction:**
- Both INSERTs in same transaction
- Either both succeed or both fail (atomicity)
- Maintains conversation integrity

---

### Operation 5: SELECT History for Display

**Location:** `/history` route, Lines 425-430

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

#### Purpose
Retrieves conversation history for display in UI or API responses.

#### Function Details

**Line 422: Route Definition**
```python
@app.route("/history", methods=["GET"])
```
- **Endpoint:** `/history`
- **Method:** GET only
- **Purpose:** Retrieve conversation history
- **Authentication:** Required (see `@login_required` decorator)

**Line 423: Login Protection**
```python
@login_required
```
- Flask-Login decorator
- Redirects unauthenticated users to login page
- Ensures only logged-in users access history

**Line 428: History Query**
```python
cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
```

**SQL Breakdown:**

- **`SELECT role, content`**: Same columns as chat history query
  - Only data needed for display
  - Excludes `id` and `timestamp`

- **`FROM messages`**: Query messages table

- **`ORDER BY id DESC`**: Newest messages first
  - `DESC` = descending order
  - Higher IDs (newer messages) come first

- **`LIMIT 50`**: Return maximum 50 messages
  - **Why 50?** Balance between:
    - Showing enough context
    - Not overwhelming UI
    - Reasonable data transfer size
  - **Hard-coded:** Unlike chat history (6 or 20), this is fixed
  - **Coverage:** 50 messages = ~25 conversation exchanges

**Example Query Result:**
```
Row 1: role='assistant', content='Here is how to...'    (id: 150 - newest)
Row 2: role='user', content='Show me code'              (id: 149)
Row 3: role='assistant', content='SQLite is...'         (id: 148)
...
Row 50: role='user', content='Hello'                    (id: 101 - 50th newest)
```

**Line 429: Process and Format**
```python
history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
```

**Processing Steps:**

1. **`cursor.fetchall()`**: Get all 50 rows
   - Returns list of Row objects
   - Newest-first order (DESC)

2. **`reversed(...)`**: Flip to oldest-first
   - Chronological order for display
   - Matches conversation flow

3. **List comprehension**: Convert to dictionaries
   - Format: `{"role": "...", "content": "..."}`
   - JSON-serializable structure

4. **Result:** List of up to 50 message dictionaries

**Line 430: Return JSON Response**
```python
return jsonify({"history": history})
```

- **`jsonify()`**: Flask function to create JSON response
- **Response structure:**
  ```json
  {
    "history": [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi! How can I help?"},
      ...
    ]
  }
  ```
- **HTTP Status:** 200 OK (default)
- **Content-Type:** `application/json`

**Lines 431-432: Cleanup**
```python
finally:
    conn.close()
```
- Ensures connection closed even if error
- Prevents connection leaks

#### Use Cases

**Frontend Display:**
```javascript
// JavaScript code might call this endpoint
fetch('/history')
  .then(response => response.json())
  .then(data => {
    data.history.forEach(msg => {
      displayMessage(msg.role, msg.content);
    });
  });
```

**API Integration:**
```python
# External service retrieving conversation history
response = requests.get('https://azikiai.com/history')
history = response.json()['history']
```

#### Comparison: Chat History vs. Display History

| Aspect | Chat History (in `/chat`) | Display History (in `/history`) |
|--------|---------------------------|----------------------------------|
| **Limit** | 6 or 20 (dynamic) | 50 (fixed) |
| **Purpose** | AI context window | User viewing |
| **Order** | Oldest-first | Oldest-first |
| **Selection** | Model-specific | UI display |

---

## Database Connection Patterns

### Pattern 1: Standard Operation Pattern

**Used in:** Most database operations

```python
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("SQL QUERY", (params,))
    conn.commit()
finally:
    conn.close()
```

**Components:**

1. **`get_db_connection()`**: Obtain connection
2. **`try` block**: Database operations
3. **`cursor.cursor()`**: Create cursor
4. **`cursor.execute()`**: Run SQL
5. **`conn.commit()`**: Save changes
6. **`finally` block**: Always close connection

**Benefits:**
- Connection always closed (prevents leaks)
- Transactions explicit (must call commit)
- Error propagation to caller
- Resource cleanup guaranteed

### Pattern 2: Query-Only Pattern

**Used in:** `/history` route

```python
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("SELECT ...")
    results = cursor.fetchall()
    return process(results)
finally:
    conn.close()
```

**Differences:**
- **No `commit()`**: SELECT doesn't modify data
- **No transaction**: Read-only operation
- **Implicit rollback**: Any transaction auto-rolled back on close

### Pattern 3: Multi-Statement Transaction

**Used in:** `/upload` route

```python
conn = get_db_connection()
try:
    cursor = conn.cursor()
    cursor.execute("INSERT ...")
    cursor.execute("INSERT ...")
    conn.commit()  # Commits both INSERTs
finally:
    conn.close()
```

**Benefits:**
- **Atomicity:** Both statements succeed or both fail
- **Consistency:** Related data inserted together
- **Single commit:** More efficient than multiple commits

---

## Database Schema Details

### Table: `messages`

**Purpose:** Store all chat conversation messages

**Schema:**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Column Specifications

#### Column: `id`
- **Type:** INTEGER
- **Constraints:** PRIMARY KEY, AUTOINCREMENT
- **Purpose:** Unique identifier for each message
- **Values:** 1, 2, 3, ... (automatically assigned)
- **Index:** Automatic index on primary key
- **Behavior:**
  - Auto-assigned on INSERT
  - Never reused (even after DELETE)
  - Guarantees chronological order
  - Used for sorting and pagination

#### Column: `role`
- **Type:** TEXT
- **Constraints:** NOT NULL
- **Purpose:** Identifies message sender
- **Allowed Values:**
  - `"user"` - Human user's message
  - `"assistant"` - AI bot's response
  - `"system"` - System prompts (added in code, not stored)
- **Length:** Typically 4-9 characters
- **Indexing:** Not indexed (small cardinality)
- **Validation:** None in database (enforced in application)

#### Column: `content`
- **Type:** TEXT
- **Constraints:** NOT NULL
- **Purpose:** Actual message text
- **Content Types:**
  - Plain text questions
  - Markdown-formatted responses
  - Code blocks with syntax highlighting
  - Upload notifications
  - Error messages
- **Size:** Can be very large (up to SQLite limit)
- **Special Characters:** Handled by parameterized queries
- **Encoding:** UTF-8 (default SQLite)
- **Indexing:** Not indexed (full-text search not implemented)

#### Column: `timestamp`
- **Type:** DATETIME
- **Constraints:** None (nullable)
- **Default:** CURRENT_TIMESTAMP (auto-set)
- **Purpose:** Record when message was created
- **Format:** 'YYYY-MM-DD HH:MM:SS'
- **Timezone:** UTC (SQLite default)
- **Example:** '2025-12-03 14:30:45'
- **Uses:**
  - Debugging conversation flow
  - Audit trail
  - Future time-based queries
  - Currently not used in application logic

### Table Statistics

**Expected Size:**
- **Rows:** Grows continuously (all messages retained)
- **Size per row:** 
  - `id`: 4-8 bytes
  - `role`: 4-9 bytes + overhead
  - `content`: Variable (typically 100-5000 bytes)
  - `timestamp`: 20 bytes
  - Total: ~200-5000 bytes per message average
- **Growth rate:** Depends on usage
  - Active conversation: 20-100 messages/day
  - Database size: ~1MB per 5000 messages

### Data Integrity

**Enforced by Database:**
- `id` uniqueness (PRIMARY KEY)
- `role` required (NOT NULL)
- `content` required (NOT NULL)

**Not Enforced by Database:**
- `role` value validation (any string allowed)
- `content` format (no schema)
- Message ordering (relies on AUTOINCREMENT)
- User identity (no foreign key to users table)

**Application-Level Integrity:**
- Role values controlled in code ("user" or "assistant")
- Content sanitization (none - raw text stored)
- No message deletion (append-only pattern)

---

## Security Considerations

### SQL Injection Prevention

**Method:** Parameterized queries (prepared statements)

**All queries use `?` placeholders:**
```python
# SAFE - Parameterized
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (history_limit,))

# NEVER DONE - String formatting (vulnerable to SQL injection)
cursor.execute(f"INSERT INTO messages VALUES ('{role}', '{content}')")
```

**Protection:**
- SQLite automatically escapes special characters
- SQL structure separated from data
- Cannot inject SQL commands through user input

**Example Attack Prevented:**
```python
user_msg = "'; DROP TABLE messages; --"

# With parameterized query (SAFE):
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
# Results in: INSERT with content = "'; DROP TABLE messages; --" (harmless string)

# With string formatting (VULNERABLE):
cursor.execute(f"INSERT INTO messages (role, content) VALUES ('user', '{user_msg}')")
# Results in: INSERT INTO messages (role, content) VALUES ('user', ''); DROP TABLE messages; --')
# EXECUTES DROP TABLE! Database destroyed!
```

### Data Encryption

**Current State:** None

**Database File:** Stored unencrypted on disk
- Location: `/home/kasperadm/projects/AzikiAI-codingbot/chat_history.db`
- Permissions: Based on file system (typically 644 or 664)
- Anyone with file access can read all messages

**Content Storage:** Plain text
- Messages stored as-is
- No encryption of sensitive information
- API keys, passwords in messages are visible

**Recommendations for Production:**
- Encrypt database file with SQLCipher
- Encrypt sensitive content before storage
- Use environment variables for secrets (already done)
- Implement data retention policies

### Authentication & Authorization

**Current Implementation:**

**Authentication:**
```python
@login_required
def chat():
    ...
```
- All database operations behind `@login_required` decorator
- Must authenticate via LDAP before accessing data
- Flask-Login session management

**Authorization:**
- **No per-user isolation** - all users share same database
- Any authenticated user can see all messages
- No user column in messages table
- All users see same conversation history

**Implications:**
- Suitable for single-user or trusted team environment
- Not suitable for multi-tenant use case
- Need user_id column for true multi-user support

**Multi-User Support (Future Enhancement):**
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,  -- Add user identifier
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Rate Limiting

**Database Protection:**

```python
@limiter.limit("30 per minute")
def chat():
    ...
```

- Rate limiting prevents abuse
- Protects database from excessive writes
- INSERT operations limited by API rate limits

**Database-Level Limits:**
- No database-level rate limiting
- Relies on application-level protection
- SQLite handles concurrent access with file locking

---

## Session Management

### Session Isolation

**Connection Per Request:**
- Each route handler creates new connection
- No connection pooling
- Connections not shared between requests

**Benefits:**
- Thread-safe (no shared state)
- Simpler error handling
- Automatic cleanup

**Drawbacks:**
- Connection overhead per request
- No connection reuse
- File open/close per operation

### Transaction Management

**Explicit Transactions:**
```python
conn = get_db_connection()
# Transaction starts implicitly on first SQL statement
cursor.execute("INSERT ...")
# Changes held in memory (not visible to others)
conn.commit()
# Transaction committed (changes permanent and visible)
conn.close()
# Connection closed (auto-commits if not already committed)
```

**Transaction Behavior:**

**ACID Properties:**
- **Atomicity:** All SQL statements in transaction succeed or all fail
- **Consistency:** Database remains in valid state
- **Isolation:** Changes not visible until commit
- **Durability:** Committed changes survive crashes

**Isolation Level:**
- SQLite default: SERIALIZABLE
- Highest isolation level
- No dirty reads, non-repeatable reads, or phantoms

**Rollback:**
```python
conn = get_db_connection()
try:
    cursor.execute("INSERT ...")
    cursor.execute("INSERT ...")
    # If error occurs here, no commit
except Exception:
    conn.rollback()  # Explicitly rollback (or just don't commit)
finally:
    conn.close()  # Auto-rollback if not committed
```

### Concurrent Access

**SQLite Locking:**

**Write Lock:**
- Only one writer at a time
- Other connections wait (or timeout)
- Locks entire database file

**Read Lock:**
- Multiple readers allowed
- Readers don't block readers
- Readers block writers

**Implications:**
- High read concurrency: Good
- High write concurrency: Limited
- Suitable for low-to-medium write load

**Deadlock Prevention:**
- Short transactions (commit quickly)
- No cross-connection dependencies
- Timeout handling (default 5 seconds)

**Error Example:**
```python
# If two requests try to write simultaneously:
sqlite3.OperationalError: database is locked
```

---

## Error Handling

### Database Errors

**Common Errors:**

**1. Database Locked**
```python
sqlite3.OperationalError: database is locked
```
**Cause:** Another connection holding write lock
**Handling:** Propagates to Flask error handler (500 response)
**Prevention:** Keep transactions short, commit quickly

**2. Disk Full**
```python
sqlite3.OperationalError: database or disk is full
```
**Cause:** No space to write database changes
**Handling:** Propagates to Flask, user sees error
**Prevention:** Monitor disk space, implement cleanup

**3. Permission Denied**
```python
PermissionError: [Errno 13] Permission denied: 'chat_history.db'
```
**Cause:** Application lacks write permission to database file/directory
**Handling:** Application fails to start (init_db fails)
**Prevention:** Ensure correct file permissions on deployment

**4. Corrupt Database**
```python
sqlite3.DatabaseError: database disk image is malformed
```
**Cause:** Database file corrupted (crash during write, disk error)
**Handling:** Application may fail to start or on first query
**Recovery:** Restore from backup, or delete and recreate

### Application Error Handling

**Pattern in All Routes:**
```python
conn = get_db_connection()
try:
    # Database operations
    conn.commit()
finally:
    conn.close()  # Always executes
```

**Error Propagation:**
- No `except` blocks in database code
- Errors propagate to Flask route handler
- Flask converts exceptions to HTTP 500 responses
- Errors logged by Flask's default logging

**Cleanup Guarantee:**
- `finally` block always closes connection
- Even if error occurs in try block
- Prevents connection leaks

### Logging

**Database Operations:**
```python
logger.info(f"Chat request using {ai_model} - message length: {len(user_msg)}")
logger.warning(f"User attempted to use unavailable bot: {ai_model}")
logger.error(f"Error in chat with {ai_model}: {e}")
```

**What's Logged:**
- AI model selection
- Message lengths
- Errors during chat
- LDAP authentication events

**What's NOT Logged:**
- Database queries (no query logging)
- Message content (privacy consideration)
- Connection open/close events
- Transaction commits

**Log Location:**
- File: `/home/kasperadm/projects/AzikiAI-codingbot/logs/azikiai.log`
- Console: Standard output (systemd journal if running as service)

---

## Performance Considerations

### Indexing

**Current Indexes:**
- **PRIMARY KEY on `id`**: Automatic index
  - Used for: `ORDER BY id DESC`
  - Performance: O(log n) for sorted retrieval
  - Covers: All queries that sort by id

**Missing Indexes:**
- No index on `role` (not needed - low cardinality, small table)
- No index on `timestamp` (not queried currently)
- No full-text index on `content` (no search implemented)

**Query Performance:**

**Fast Queries:**
```sql
SELECT role, content FROM messages ORDER BY id DESC LIMIT 50
-- Uses PRIMARY KEY index, very fast (milliseconds even with millions of rows)
```

**Slow Queries (if implemented):**
```sql
SELECT * FROM messages WHERE timestamp > '2025-12-01'
-- Table scan (no index on timestamp), slow with large table
```

### Database Size Management

**Growth Pattern:**
- Append-only (no DELETE operations)
- Grows continuously
- No cleanup or archival

**Size Estimates:**
| Messages | Avg Size | DB Size |
|----------|----------|---------|
| 1,000 | 500 bytes | ~500 KB |
| 10,000 | 500 bytes | ~5 MB |
| 100,000 | 500 bytes | ~50 MB |
| 1,000,000 | 500 bytes | ~500 MB |

**Management Strategies (Not Implemented):**
1. **Periodic Cleanup:**
   ```sql
   DELETE FROM messages WHERE timestamp < date('now', '-30 days');
   ```

2. **Archival:**
   ```python
   # Export old messages to archive
   # Delete from active database
   ```

3. **VACUUM:**
   ```sql
   VACUUM;  -- Reclaim space from deleted rows
   ```

### Query Optimization

**Efficient Patterns Used:**

**1. Column Selection:**
```python
# GOOD - Only select needed columns
cursor.execute("SELECT role, content FROM messages ...")

# AVOID - Selecting unnecessary data
cursor.execute("SELECT * FROM messages ...")
```

**2. LIMIT Clauses:**
```python
# GOOD - Limit rows at database level
cursor.execute("... LIMIT ?", (50,))

# AVOID - Fetch all, limit in Python
cursor.execute("SELECT ...")
results = cursor.fetchall()[:50]
```

**3. Result Processing:**
```python
# GOOD - Process while iterating
for row in cursor.fetchall():
    process(row)

# ACCEPTABLE - Load all (small result sets)
results = cursor.fetchall()  # OK for 6-50 rows
```

---

## Code Quality Analysis

### Strengths

**1. SQL Injection Protection:**
- ✅ All queries use parameterized statements
- ✅ No string formatting in SQL
- ✅ Consistent pattern across all routes

**2. Connection Management:**
- ✅ try/finally ensures cleanup
- ✅ Connections closed in all code paths
- ✅ No connection leaks

**3. Transaction Consistency:**
- ✅ Explicit commit calls
- ✅ Multi-statement transactions grouped
- ✅ Rollback on errors (implicit via no-commit)

**4. Code Organization:**
- ✅ Database functions separated
- ✅ Consistent patterns
- ✅ Clear purpose for each function

### Areas for Improvement

**1. No User Isolation:**
```python
# Current: All users share same conversation
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", msg))

# Better: Associate messages with user
cursor.execute(
    "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)", 
    (current_user.id, "user", msg)
)
```

**2. No Error Handling:**
```python
# Current: Errors propagate
conn = get_db_connection()
cursor.execute("...")

# Better: Specific error handling
try:
    conn = get_db_connection()
    cursor.execute("...")
except sqlite3.OperationalError as e:
    logger.error(f"Database locked: {e}")
    return jsonify({"error": "Database busy, try again"}), 503
```

**3. No Data Validation:**
```python
# Current: Any role value accepted
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))

# Better: Validate before insert
if role not in ['user', 'assistant']:
    raise ValueError(f"Invalid role: {role}")
cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
```

**4. No Connection Pooling:**
- Each request creates new connection
- Could use connection pool for better performance
- Consider `sqlite3.connect()` with `check_same_thread=False` for pooling

**5. No Backup Strategy:**
- No automated backups
- No point-in-time recovery
- Single file vulnerability

**6. Missing Features:**
- No message deletion
- No search functionality
- No conversation sessions
- No message editing
- No data retention policy

---

## Summary

### Database Overview

**Technology:** SQLite3
**File:** `chat_history.db`
**Size:** Growing (append-only)
**Tables:** 1 (`messages`)

### Operations Summary

| Operation | Location | Purpose | Complexity |
|-----------|----------|---------|------------|
| `init_db()` | Lines 110-125 | Create schema | O(1) |
| INSERT user msg | Line 274 | Save user question | O(1) |
| SELECT history | Line 284 | Get conversation context | O(log n) |
| INSERT assistant msg | Line 377 | Save AI response | O(1) |
| INSERT upload msgs | Lines 413-414 | Record file upload | O(1) |
| SELECT display history | Line 428 | Show conversation | O(log n) |

### Functions Documented

1. **`get_db_connection()`** - Create database connection
2. **`init_db()`** - Initialize database schema

### Total Lines of SQL Code: ~50 lines
### Total Functions/Methods: 2 dedicated + 5 operations in routes

---

## File Metadata

**Documentation Created:** December 3, 2025
**Python Version:** 3.x (compatible with 3.7+)
**SQLite Version:** 3.x (system default)
**Application:** AzikiAI Chatbot
**Author:** [Original application author]
**Documentation by:** GitHub Copilot (Claude Sonnet 4.5)
