#!/usr/bin/env python3
from ldap3 import Server, Connection, ALL, NTLM, Tls
import ssl

# LDAP Configuration
ldap_host = "192.168.0.82"
ldap_port = 636
base_dn = "DC=Area51,DC=local"
bind_user = "CN=svc_mistralbot,CN=Users,DC=Area51,DC=local"
bind_password = 'H"MPt=_3zq\'lZMq%zE+Q'

print(f"Testing LDAP connection to {ldap_host}:{ldap_port}")
print(f"Base DN: {base_dn}")
print(f"Bind User: {bind_user}")

try:
    # Create TLS object that doesn't validate cert (for testing)
    tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    
    # Create server object
    server = Server(ldap_host, port=ldap_port, use_ssl=True, tls=tls, get_info=ALL)
    print(f"\n✓ Server object created")
    print(f"Server info: {server}")
    
    # Try to connect and bind
    conn = Connection(server, user=bind_user, password=bind_password, auto_bind=True)
    print(f"\n✓ LDAP Bind successful!")
    print(f"Connection: {conn}")
    
    # Try to search for a user
    test_username = "kasper"
    search_filter = f"(sAMAccountName={test_username})"
    search_base = "CN=Users,DC=Area51,DC=local"
    
    print(f"\nSearching for user: {test_username}")
    print(f"Search base: {search_base}")
    print(f"Filter: {search_filter}")
    
    conn.search(search_base, search_filter, attributes=['*'])
    
    if conn.entries:
        print(f"\n✓ User found!")
        for entry in conn.entries:
            print(f"DN: {entry.entry_dn}")
            print(f"Attributes: {entry.entry_attributes_as_dict}")
    else:
        print(f"\n✗ User not found")
    
    conn.unbind()
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
