# GitHub Copilot Integration Guide

## How to Get Your GitHub Token

### Step 1: Go to GitHub Settings
1. Log in to [GitHub](https://github.com)
2. Click on your profile picture in the top right
3. Select **Settings**
4. Scroll down in the left sidebar and click on **Developer settings**
5. Click on **Personal access tokens** → **Tokens (classic)**

### Step 2: Create New Token
1. Click **Generate new token** → **Generate new token (classic)**
2. Give your token a descriptive name, e.g., "AzikiAI Chatbot"
3. Choose an expiration date (recommended: 90 days or No expiration for testing)
4. Select the following scopes:
   - ✅ `read:user` - Read user data
   - ✅ `copilot` - Access to GitHub Copilot (if available)
   
5. Click **Generate token** at the bottom

### Step 3: Copy Token
1. **IMPORTANT:** Copy the token NOW - you won't be able to see it again!
2. The token looks like this: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add to .env File
1. Open/create the `.env` file in the project root directory
2. Add the line:
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   (replace with your actual token)

### Alternative: GitHub Models API
If you don't have access to the Copilot API, you can also use GitHub Models:
- Same token works
- The chatbot will automatically select the correct endpoint
- Free access to GPT-4o and other models

### Troubleshooting
**Problem:** "GITHUB_TOKEN not found"
- Solution: Make sure the `.env` file is in the same directory as `main.py`

**Problem:** "Error communicating with GitHub API"
- Solution 1: Check that your token has the correct scopes
- Solution 2: Check that your token hasn't expired
- Solution 3: Use Mistral AI as fallback (add MISTRAL_API_KEY to .env)

## Advantages of GitHub Copilot
- ✅ Uses your existing GitHub credentials
- ✅ Powerful GPT-4 based AI
- ✅ Optimized for coding and programming
- ✅ Secure and enterprise-ready
- ✅ Automatic fallback to Mistral AI if GitHub is unavailable

## Security
- 🔒 NEVER save your token in git repositories
- 🔒 The `.env` file is already in `.gitignore`
- 🔒 Rotate tokens regularly (every 90 days)
- 🔒 Use only minimal scopes that are necessary
