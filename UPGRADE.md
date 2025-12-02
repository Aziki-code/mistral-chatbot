# Upgrade Guide - v1.x to v2.0

This guide helps you upgrade from version 1.x to 2.0 with minimal downtime.

## Prerequisites

- Access to your server via SSH
- Sudo privileges
- Backup of your `.env` file

## Step-by-Step Upgrade

### 1. Backup Current Installation

```bash
cd /home/kasperadm/projects/AzikiAI-codingbot
cp .env .env.backup
sudo systemctl stop azikiai-chatbot
```

### 2. Pull Latest Code

```bash
git pull origin main
```

### 3. Update Environment File

Add these new variables to your `.env` file:

```bash
# Add to existing .env
LDAP_PORT=636
LDAP_VALIDATE_SSL=false
SESSION_TIMEOUT_MINUTES=10
```

Your existing `LDAP_HOST` and `LDAP_BASE_DN` will now be used automatically (no more hardcoded values).

### 4. Update Python Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

This installs:
- `flask-limiter` for rate limiting
- Updated dependencies

### 5. Create Logs Directory

```bash
mkdir -p logs
```

### 6. Update Systemd Service

```bash
# Copy new service file
sudo cp azikiai-chatbot.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Start service with new configuration
sudo systemctl start azikiai-chatbot
```

### 7. Verify Installation

```bash
# Check service status
sudo systemctl status azikiai-chatbot

# Check logs
tail -f logs/azikiai.log

# Test web access
curl -k https://localhost:5000
```

## What Changed?

### Security Enhancements
- LDAP credentials moved from code to `.env`
- Rate limiting added (30 req/min per user)
- SSL validation now configurable
- Better error handling

### Performance Improvements
- Gunicorn replaces Flask dev server
- Database connection pooling
- Multi-worker support

### New Features
- Structured logging to files
- Better error messages
- Health monitoring with systemd watchdog

## Rollback Procedure

If something goes wrong:

```bash
# Stop new version
sudo systemctl stop azikiai-chatbot

# Restore old files
git checkout HEAD~1
cp .env.backup .env

# Reinstall old dependencies
pip install flask python-dotenv requests mistralai flask-login flask-ldap3-login ldap3

# Restart with old config
sudo systemctl start azikiai-chatbot
```

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u azikiai-chatbot -n 50

# Verify .env variables
cat .env | grep LDAP
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Rate limiting too strict
Edit `main.py` line ~46:
```python
@limiter.limit("60 per minute")  # Increase from 30
```

## Support

Check logs in:
- `logs/azikiai.log` - Application logs
- `logs/gunicorn-access.log` - HTTP access logs
- `logs/gunicorn-error.log` - Server errors
- `sudo journalctl -u azikiai-chatbot` - Systemd logs
