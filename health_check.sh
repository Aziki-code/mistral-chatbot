#!/bin/bash
# Quick health check script for AzikiAI Chatbot

echo "=================================="
echo "AzikiAI Chatbot Health Check"
echo "=================================="
echo ""

# Check service status
echo "1. Systemd Service Status:"
sudo systemctl is-active azikiai-chatbot > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Service is running"
else
    echo "   ✗ Service is NOT running"
fi
echo ""

# Check if port is listening
echo "2. Port Status:"
sudo ss -tlnp | grep :5000 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Port 5000 is listening"
else
    echo "   ✗ Port 5000 is NOT listening"
fi
echo ""

# Check log files
echo "3. Log Files:"
if [ -f "logs/azikiai.log" ]; then
    lines=$(wc -l < logs/azikiai.log)
    echo "   ✓ Application log exists ($lines lines)"
else
    echo "   ✗ Application log missing"
fi

if [ -f "logs/gunicorn-access.log" ]; then
    lines=$(wc -l < logs/gunicorn-access.log)
    echo "   ✓ Gunicorn access log exists ($lines lines)"
else
    echo "   ⚠ Gunicorn access log missing (normal on first run)"
fi
echo ""

# Check environment file
echo "4. Configuration:"
if [ -f ".env" ]; then
    echo "   ✓ .env file exists"
    
    # Check for required variables
    required_vars=("LDAP_HOST" "LDAP_BASE_DN" "SECRET_KEY")
    for var in "${required_vars[@]}"; do
        if grep -q "^$var=" .env; then
            echo "   ✓ $var is configured"
        else
            echo "   ✗ $var is missing"
        fi
    done
else
    echo "   ✗ .env file missing"
fi
echo ""

# Check Python dependencies
echo "5. Dependencies:"
if [ -d "venv" ]; then
    source venv/bin/activate
    python3 -c "import flask_limiter" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ Flask-Limiter installed"
    else
        echo "   ✗ Flask-Limiter missing"
    fi
    
    python3 -c "import gunicorn" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ Gunicorn installed"
    else
        echo "   ✗ Gunicorn missing"
    fi
    deactivate
else
    echo "   ✗ Virtual environment missing"
fi
echo ""

# Recent errors in logs
echo "6. Recent Errors (last 5):"
if [ -f "logs/azikiai.log" ]; then
    errors=$(grep -i "error\|critical" logs/azikiai.log | tail -5)
    if [ -z "$errors" ]; then
        echo "   ✓ No recent errors"
    else
        echo "$errors"
    fi
else
    echo "   ⚠ No log file to check"
fi
echo ""

echo "=================================="
echo "Health Check Complete"
echo "=================================="
