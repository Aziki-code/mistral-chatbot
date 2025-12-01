#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL, Tls
import ssl

# Test user authentication (not service account)
ldap_host = "192.168.0.82"
ldap_port = 636
base_dn = "DC=Area51,DC=local"

# Try to authenticate as the actual user (kasper)
test_username = "kasper"
test_password = input(f"Enter password for {test_username}: ")

print(f"\nTesting user authentication to {ldap_host}:{ldap_port}")

try:
    # Create TLS object
    tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    server = Server(ldap_host, port=ldap_port, use_ssl=True, tls=tls, get_info=ALL)
    
    # Try different authentication methods
    
    # Method 1: Full DN
    user_dn = f"CN={test_username},CN=Users,DC=Area51,DC=local"
    print(f"\n--- Method 1: Full DN ---")
    print(f"User DN: {user_dn}")
    try:
        conn = Connection(server, user=user_dn, password=test_password, auto_bind=True)
        print(f"✓ SUCCESS with full DN!")
        conn.unbind()
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 2: sAMAccountName
    print(f"\n--- Method 2: sAMAccountName ---")
    print(f"Username: {test_username}")
    try:
        conn = Connection(server, user=test_username, password=test_password, auto_bind=True)
        print(f"✓ SUCCESS with sAMAccountName!")
        conn.unbind()
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 3: UPN format
    upn = f"{test_username}@Area51.local"
    print(f"\n--- Method 3: UPN format ---")
    print(f"UPN: {upn}")
    try:
        conn = Connection(server, user=upn, password=test_password, auto_bind=True)
        print(f"✓ SUCCESS with UPN!")
        conn.unbind()
    except Exception as e:
        print(f"✗ Failed: {e}")
    
    # Method 4: Domain\username format
    domain_user = f"AREA51\\{test_username}"
    print(f"\n--- Method 4: Domain\\Username ---")
    print(f"User: {domain_user}")
    try:
        conn = Connection(server, user=domain_user, password=test_password, auto_bind=True)
        print(f"✓ SUCCESS with Domain\\Username!")
        conn.unbind()
    except Exception as e:
        print(f"✗ Failed: {e}")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
