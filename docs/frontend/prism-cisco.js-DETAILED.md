# prism-cisco.js - Detaljeret Dokumentation

## Overordnet Formål
`prism-cisco.js` definerer Cisco IOS syntax highlighting for Prism.js. Den:
- Registrerer custom language (`cisco`) i Prism
- Definerer token patterns (regex) for Cisco commands
- Highlighter prompts, interfaces, IP addresses, MAC addresses
- Color-codes good/bad keywords (permit/deny, up/down)
- Detekterer security-kritiske linjer (passwords, secrets)

**Fil størrelse**: 130 linjer
**Dependencies**: Prism.js (must load before this)
**Pattern**: Prism language definition object
**Usage**: Automatically applied when code block has `language-cisco` class

---

## Prism.js Integration

### Language Registration (Linje 4-129)
```javascript
Prism.languages.cisco = {
    // Token definitions
};
```
- **Extends Prism.languages** - Global object from Prism.js
- **Key**: `'cisco'` - Language identifier
- **Value**: Object with token patterns

### How Prism Uses This
```html
<pre><code class="language-cisco">
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
</code></pre>
```
→ Prism.highlightElement() → Finds `language-cisco` → Uses `Prism.languages.cisco` → Applies regex patterns → Wraps matches in `<span class="token ...">` → CSS colors tokens

---

## Token Pattern Structure

### Standard Format
```javascript
'token-name': {
    pattern: /regex/,
    greedy: true,
    alias: 'prism-token-class'
}
```

#### pattern
- **Regex** - Matches text to highlight
- **Examples**: `/\b(?:permit|deny)\b/i`

#### greedy
- **true** - Match as much as possible
- **Prevents**: Token overlap conflicts
- **Example**: `192.168.1.1` matches as one IP, not multiple numbers

#### alias
- **Maps to CSS class** - Reuses existing Prism themes
- **Examples**:
  - `'inserted'` → Green (usually for git diffs)
  - `'deleted'` → Red
  - `'credential'` → Purple/orange (sensitive data)

---

## Token Definitions (By Priority)

### 1. comment (Linje 5-8)

```javascript
'comment': {
    pattern: /(?:!.*|remark\s+.*)/,
    greedy: true
}
```

#### Regex: `/(?:!.*|remark\s+.*)/`
- **`(?:...)`** - Non-capturing group
- **`!.*`** - Exclamation mark + any text to end of line
  - Example: `! This is a comment`
- **`|`** - OR
- **`remark\s+.*`** - `remark` + space + any text
  - Example: `access-list 1 remark Block internal traffic`

#### CSS Theme
- **Default**: Gray, italicized
- **From**: Prism's `.token.comment` class

#### Use Case
```cisco
! Uplink to core switch
interface GigabitEthernet0/1
 description Uplink to Core-SW1
 access-list 10 remark Management subnet only
```

---

### 2. prompt-enable (Linje 9-12)

```javascript
'prompt-enable': {
    pattern: /^[\w.-]+#(?:\s|$)/m,
    greedy: true
}
```

#### Regex: `/^[\w.-]+#(?:\s|$)/m`
- **`^`** - Start of line (multiline mode with `m` flag)
- **`[\w.-]+`** - Hostname: alphanumeric, underscore, dot, hyphen
  - Examples: `Router1`, `SW-CORE-01`, `ASA.example.com`
- **`#`** - Hash symbol (privileged exec mode indicator)
- **`(?:\s|$)`** - Followed by space or end of line
- **`m` flag** - Multiline mode (^ matches line start, not just string start)

#### Meaning in Cisco IOS
- **`#` prompt** - Privileged EXEC mode (enable mode)
- **Full control** - Can modify configuration
- **Security**: User ran `enable` command

#### CSS Theme
- **Custom**: Could style uniquely via `.token.prompt-enable`
- **Default**: Likely same as keywords (bold)

#### Example
```cisco
Router1# show ip interface brief
                ↑ Highlighted in privileged mode color
```

---

### 3. prompt-user (Linje 13-16)

```javascript
'prompt-user': {
    pattern: /^[\w.-]+>(?:\s|$)/m,
    greedy: true
}
```

#### Regex: `/^[\w.-]+>(?:\s|$)/m`
- **Same as prompt-enable** but with `>` instead of `#`

#### Meaning in Cisco IOS
- **`>` prompt** - User EXEC mode
- **Limited access** - Can only view, not configure
- **No enable password** entered yet

#### Example
```cisco
Router1> show version
                ↑ Highlighted in user mode color (different from #)
```

---

### 4. interface (Linje 17-20)

```javascript
'interface': {
    pattern: /\b(?:Embedded-Service-Engine|GigabitEthernet|FastEthernet|TenGigabitEthernet|Ethernet|Serial|Tunnel|Loopback|Port-channel|Vlan|Multilink|Null|Nvi|vfc|Te|Gi|Fa|Eth?|Po)\d+(?:[\/.:]\d+)*[*]?\b/i,
    greedy: true
}
```

#### Regex Breakdown
- **`\b`** - Word boundary
- **Interface Types** (alternation):
  - `Embedded-Service-Engine` - Router blade module
  - `GigabitEthernet`, `FastEthernet`, `TenGigabitEthernet` - Physical Ethernet
  - `Serial` - WAN serial links
  - `Tunnel` - VPN tunnels
  - `Loopback` - Virtual loopback interfaces
  - `Port-channel` - EtherChannel bundles
  - `Vlan` - VLAN interfaces (L3 SVI)
  - `Multilink` - PPP multilink
  - `Null` - Null interface (blackhole)
  - `Nvi` - NAT Virtual Interface
  - `vfc` - Virtual Fibre Channel
  - **Abbreviations**: `Te`, `Gi`, `Fa`, `Eth?`, `Po`
    - `Eth?` - `Eth` or `Et` (optional 'h')

- **`\d+`** - Slot/module number
  - Example: `GigabitEthernet0`

- **`(?:[\/.:]\d+)*`** - Port/subinterface numbers (repeating)
  - **Separators**: `/` (slash), `.` (dot), `:` (colon)
  - Examples:
    - `GigabitEthernet0/1` - Slot 0, port 1
    - `GigabitEthernet0/0/1` - Module 0, slot 0, port 1
    - `Ethernet2/1.100` - Port 2/1, subinterface 100 (VLAN tagging)
    - `Serial1/0:1` - Channel 1 on Serial1/0

- **`[*]?`** - Optional asterisk (active interface in `show ip interface brief`)
  - Example: `GigabitEthernet0/1*` - Currently active

- **`/i`** - Case insensitive
  - `gigabitethernet0/1` also matches

#### Examples
```cisco
interface GigabitEthernet0/1         ← Full name
interface Gi0/1                      ← Abbreviation
interface Vlan10                     ← VLAN interface
interface Tunnel0                    ← VPN tunnel
interface Port-channel1              ← EtherChannel
interface GigabitEthernet0/0/1.100   ← Subinterface (dot1q encap)
```

---

### 5. wwn (Linje 21-25)

```javascript
'wwn': {
    pattern: /\b(?:wwn|pwwn|(?:[a-f0-9]{2}:){7}[a-f0-9]{2})\b/i,
    greedy: true,
    alias: 'credential'
}
```

#### Purpose
- **World Wide Name** - Fibre Channel unique identifier
- **Like MAC** but for SAN (Storage Area Network)

#### Regex: `/\b(?:wwn|pwwn|(?:[a-f0-9]{2}:){7}[a-f0-9]{2})\b/i`
- **`wwn`** - Keyword "wwn"
- **`pwwn`** - Port WWN (specific port identifier)
- **`(?:[a-f0-9]{2}:){7}[a-f0-9]{2}`** - 8 hex octets with colons
  - Example: `20:00:00:25:b5:00:00:00`
  - Format: `XX:XX:XX:XX:XX:XX:XX:XX`

#### Alias: 'credential'
- **Treated as sensitive** - Purple/orange color
- **Security relevance** - Unique device identifier

#### Example
```cisco
switchport trunk allowed san pwwn 20:00:00:25:b5:00:00:00
                                  ↑ Highlighted as credential
```

---

### 6. ip-address (Linje 26-30)

```javascript
'ip-address': {
    pattern: /\b(?:\d{1,3}\.){3}\d{1,3}(?:\/\d{1,2})?(?::\d{1,5})?\b/,
    greedy: true,
    alias: 'number'
}
```

#### Regex: `/\b(?:\d{1,3}\.){3}\d{1,3}(?:\/\d{1,2})?(?::\d{1,5})?\b/`
- **`(?:\d{1,3}\.){3}`** - Three octets with dots
  - `192.168.1.`
  - Each octet: 1-3 digits

- **`\d{1,3}`** - Fourth octet
  - `192.168.1.1`

- **`(?:\/\d{1,2})?`** - Optional CIDR prefix
  - `/24`, `/32`, `/8`
  - Example: `192.168.1.0/24`

- **`(?::\d{1,5})?`** - Optional port number
  - `:80`, `:443`, `:22`
  - Example: `192.168.1.1:8080`

#### Alias: 'number'
- **Blue color** (typical for numbers in themes)

#### Note: No Validation
- **Accepts invalid IPs** like `999.999.999.999`
- **Regex limitation** - Full validation would be complex
- **Good enough** - Real configs have valid IPs

#### Examples
```cisco
ip address 192.168.1.1 255.255.255.0
ip route 0.0.0.0 0.0.0.0 10.0.0.1
ntp server 10.0.0.50
access-list 1 permit 172.16.0.0 0.0.255.255
ip nat inside source static tcp 192.168.1.100:80 203.0.113.1:8080
```

---

### 7. mac-address (Linje 31-35)

```javascript
'mac-address': {
    pattern: /\b(?:[0-9a-f]{4}\.){2}[0-9a-f]{4}\b|\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b/i,
    greedy: true,
    alias: 'builtin'
}
```

#### Regex: Two formats (alternation)

##### Cisco Format: `(?:[0-9a-f]{4}\.){2}[0-9a-f]{4}`
- **Format**: `xxxx.xxxx.xxxx`
- **Example**: `0050.56c0.0001`
- **Used by**: Cisco devices (native format)

##### Standard Format: `(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}`
- **Format**: `xx:xx:xx:xx:xx:xx` or `xx-xx-xx-xx-xx-xx`
- **Example**: `00:50:56:c0:00:01`
- **Used by**: Most other vendors, Linux, Windows

#### Alias: 'builtin'
- **Cyan/teal color** (typical for built-in functions)

#### Examples
```cisco
mac address-table static 0050.56c0.0001 vlan 10 interface Gi0/1
arp 192.168.1.1 0050.56c0.0001 ARPA
show mac address-table address 00:50:56:c0:00:01
```

---

### 8. ios-version (Linje 36-40)

```javascript
'ios-version': {
    pattern: /\b\d+\.\d+(?:\.\d+)?(?:\([^)]+\))?[^\s,]*\b/,
    greedy: true,
    alias: 'version'
}
```

#### Regex: `/\b\d+\.\d+(?:\.\d+)?(?:\([^)]+\))?[^\s,]*\b/`
- **`\d+\.\d+`** - Major.minor version
  - `15.2`, `12.4`

- **`(?:\.\d+)?`** - Optional patch version
  - `15.2.4`

- **`(?:\([^)]+\))?`** - Optional build/feature code in parentheses
  - `(M1)`, `(EX)`, `(3)a`
  - Captures any text within `( )`

- **`[^\s,]*`** - Additional characters until space or comma
  - Build suffixes: `a`, `b`, `T`, `XE3`

#### Alias: 'version'
- **Custom class** - Could style uniquely

#### Examples
```cisco
Cisco IOS Software, Version 15.2(4)M1
Version 12.4(15)T
IOS-XE Version 16.9.3
Version 15.0(1)M4
```

---

### 9. serial-number (Linje 41-45)

```javascript
'serial-number': {
    pattern: /\b[A-Z]{2,3}\d{4}[A-Z0-9]{4}\b/i,
    greedy: true,
    alias: 'version'
}
```

#### Regex: `/\b[A-Z]{2,3}\d{4}[A-Z0-9]{4}\b/i`
- **`[A-Z]{2,3}`** - 2-3 letter prefix
  - Manufacturer code
  - Examples: `FDO`, `FOC`, `SAL`

- **`\d{4}`** - 4 digits (year/week code)
  - `2145` - Week 45 of 2021

- **`[A-Z0-9]{4}`** - 4 alphanumeric characters
  - Unique unit identifier

#### Examples
```cisco
Processor board ID FDO21451ABC
System serial number: FOC1234ABCD
S/N: SAL12345678
```

---

### 10. important (Linje 46-49)

```javascript
'important': {
    pattern: /\b(?:erase|remove|delete|Building|configuration|reload|\[confirm\]|\(yes\/no\):?|--more--)\b/i,
    greedy: true
}
```

#### Keywords
- **Destructive commands**:
  - `erase` - Delete files/configs
  - `remove` - Remove files
  - `delete` - Delete command
  - `reload` - Reboot device

- **Interactive prompts**:
  - `[confirm]` - Press Enter to confirm
  - `(yes/no):` - Type yes or no
  - `--more--` - Pagination (press Space)

- **Status**:
  - `Building` - Building configuration (boot process)
  - `configuration` - Configuration keyword

#### CSS Theme
- **Bold, red** - Draws attention to critical actions
- **From**: Prism's `.token.important` class

#### Examples
```cisco
erase startup-config       ← Destructive!
reload                     ← Reboots device
[confirm]                  ← User must press Enter
System configuration has been modified. Save? (yes/no): yes
--more--                   ← Press Space to continue
Building configuration...  ← Building config file
```

---

### 11. good-keyword (Linje 50-54)

```javascript
'good-keyword': {
    pattern: /\b(?:yes|permit|clear|\[OK\]|on|Full-duplex|cir|police|mgmt|Management|inside|1000000|1000Mb\/s|enabled|down->up|running|SUCCESS|success|up|passed|kasper|PASS|Active|Complete|GRE|ipsec)\b/i,
    greedy: true,
    alias: 'inserted'
}
```

#### Purpose
- **Positive indicators** - Green highlighting
- **Good status** - up, success, permit

#### Keywords (Categories)

##### Affirmative
- `yes` - Confirmation
- `permit` - Allow traffic (ACL)
- `[OK]` - Success indicator

##### Status Up
- `up` - Interface up
- `down->up` - Transitioning to up
- `running` - Active/running
- `Active` - Active state
- `enabled` - Feature enabled

##### Performance Good
- `Full-duplex` - Good performance (vs half-duplex)
- `1000Mb/s`, `1000000` - Gigabit speed (good)

##### Success
- `SUCCESS`, `success` - Operation succeeded
- `PASS`, `passed` - Test passed
- `Complete` - Operation complete

##### Security/Features
- `GRE`, `ipsec` - VPN protocols (good encryption)
- `inside` - Inside interface (trusted)
- `mgmt`, `Management` - Management interface

##### Misc
- `kasper` - Username (specific to this system)

#### Alias: 'inserted'
- **Green color** - Positive/safe actions
- **From**: Git diff inserted lines (usually green)

#### Examples
```cisco
access-list 10 permit 192.168.1.0 0.0.0.255
                ↑ Green

GigabitEthernet0/1 is up, line protocol is up
                       ↑ Green          ↑ Green

Configuration accepted [OK]
                       ↑ Green

crypto ipsec transform-set MYSET esp-aes esp-sha-hmac
       ↑ Green
```

---

### 12. bad-keyword (Linje 55-59)

```javascript
'bad-keyword': {
    pattern: /\b(?:no|administratively|shutdown?|never|deny|down|fail|invalid|reload|not|initializing|Off|1024|768|half-duplex|100Mb\/s|100000|des56?|telnet|err-disabled|disabled|up->down|trunk|exceeded|inhibit|_ERR:)\b/i,
    greedy: true,
    alias: 'deleted'
}
```

#### Purpose
- **Negative indicators** - Red highlighting
- **Problems/risks** - down, deny, shutdown

#### Keywords (Categories)

##### Negative Commands
- `no` - Negate command (disable feature)
- `shutdown` - Disable interface
- `administratively` - Admin shutdown (manual disable)

##### Status Down
- `down` - Interface down
- `up->down` - Transitioning to down
- `fail`, `invalid` - Failure state
- `err-disabled` - Error disabled (security violation)
- `disabled` - Disabled state

##### Security Risks
- `deny` - Block traffic (ACL - shows blocked traffic)
- `des56`, `des` - Weak encryption (DES is insecure)
- `telnet` - Insecure protocol (use SSH)

##### Performance Bad
- `half-duplex` - Poor performance (duplex mismatch)
- `100Mb/s`, `100000` - Only 100Mbps (should be gigabit)
- `1024`, `768` - Low resolution/bandwidth

##### Error States
- `_ERR:` - Error prefix
- `exceeded` - Threshold exceeded
- `inhibit` - Inhibited (blocked)
- `Off` - Turned off
- `never` - Never occurred

##### Other
- `reload` - Reboot (disruptive)
- `trunk` - Trunk port (can be security risk if misconfigured)

#### Alias: 'deleted'
- **Red color** - Negative/danger
- **From**: Git diff deleted lines (usually red)

#### Examples
```cisco
access-list 10 deny 192.168.1.0 0.0.0.255
                ↑ Red

no ip routing
↑ Red (disabling routing)

GigabitEthernet0/1 is administratively down
                      ↑ Red

switchport mode trunk
                ↑ Red (security awareness)

Half-duplex, 100Mb/s
↑ Red         ↑ Red (performance issues)
```

---

### 13. security (Linje 60-64)

```javascript
'security': {
    pattern: /\b(?:username|password|key|enable\s+secret)\b.*$/m,
    greedy: true,
    alias: 'credential'
}
```

#### Regex: `/\b(?:username|password|key|enable\s+secret)\b.*$/m`
- **Keywords**: `username`, `password`, `key`, `enable secret`
- **`.*$`** - Match entire rest of line
  - **Why?** Highlight actual password/secret
- **`m` flag** - Multiline mode

#### Alias: 'credential'
- **Purple/orange** - Sensitive data warning
- **Indicates**: Line contains credentials

#### Security Note
- **Passwords visible** - Cisco configs often show plaintext passwords
- **Type 7 passwords** - Weakly encrypted (easily decoded)
- **Type 5 passwords** - MD5 hash (stronger, not plaintext)
- **enable secret** - Always hashed

#### Examples
```cisco
username admin password cisco123
         ↑ Entire line highlighted (credential)

enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
       ↑ Entire line highlighted (credential)

crypto isakmp key MyVPNKey address 10.0.0.1
       ↑ Entire line highlighted (credential)
```

---

### 14. acl (Linje 65-68)

```javascript
'acl': {
    pattern: /\b(?:access-(?:list|class|group)|use-acl|prefix-list|time-range|object-group|route-map)\b/i,
    greedy: true
}
```

#### Keywords
- **Access Lists**:
  - `access-list` - Standard ACL command
  - `access-class` - Apply ACL to line (VTY)
  - `access-group` - Apply ACL to interface

- **Advanced Filtering**:
  - `prefix-list` - BGP/OSPF route filtering
  - `route-map` - Complex policy routing
  - `object-group` - Group objects (IPs, ports)
  - `time-range` - Time-based ACLs

- **Other**:
  - `use-acl` - Apply existing ACL

#### Examples
```cisco
access-list 10 permit 192.168.1.0 0.0.0.255
↑ Highlighted

ip access-group 10 in
   ↑ Highlighted

route-map POLICY permit 10
↑ Highlighted

ip prefix-list LOOPBACKS permit 10.0.0.0/24
   ↑ Highlighted
```

---

### 15. hitcount-zero (Linje 69-72)

```javascript
'hitcount-zero': {
    pattern: /\(hitcnt=0\)/,
    greedy: true
}
```

#### Purpose
- **ACL hit counter** - Shows rule never matched
- **Troubleshooting**: Unused rule (maybe typo?)

#### Format
- `(hitcnt=0)` - Zero hits
- **Literal match** - No regex complexity

#### Example
```cisco
access-list 10 permit 192.168.1.0 0.0.0.255 (hitcnt=0)
                                            ↑ Highlighted (zero hits)
```

---

### 16. hitcount-active (Linje 73-77)

```javascript
'hitcount-active': {
    pattern: /\(hitcnt=[1-9]\d*\)/,
    greedy: true,
    alias: 'credential'
}
```

#### Regex: `/\(hitcnt=[1-9]\d*\)/`
- **`[1-9]`** - First digit 1-9 (not zero)
- **`\d*`** - Additional digits (0-9)
- **Matches**: `(hitcnt=1)`, `(hitcnt=42)`, `(hitcnt=9999)`
- **Doesn't match**: `(hitcnt=0)` (handled by hitcount-zero)

#### Alias: 'credential'
- **Purple/orange** - Active rule (important)
- **Different from zero** - Shows rule is working

#### Example
```cisco
access-list 10 permit 192.168.1.0 0.0.0.255 (hitcnt=42)
                                            ↑ Highlighted (active)
```

---

### 17. property (Linje 78-81)

```javascript
'property': {
    pattern: /\b(?:class|policy|service|parameter|match|version|PN|SN|S\/N|ID|PID|VID|NAME|DESCR|Device|Local|Intrfce|Holdtme|Capability|Platform|Port|Address|Interface|Hold|Uptime|SRTT|RTO|Seq|Neighbor|AS|MsgRcvd|MsgSent|TblVer|InQ|OutQ|Up\/Down|State|IP-Address|Method|OK\?|Status|Protocol|aaa|vlan|MTU|BW|DLY|bits\/sec|packets\/sec)[:,]?\b/i,
    greedy: true
}
```

#### Purpose
- **Table headers** - `show` command output
- **Property names** - Configuration properties

#### Keywords (Categories)

##### General
- `class`, `policy`, `service`, `parameter`, `match`
- `version`, `ID`, `NAME`, `DESCR`

##### Serial/Part Numbers
- `PN` - Part Number
- `SN`, `S/N` - Serial Number
- `PID` - Product ID
- `VID` - Version ID

##### Show Output Headers
- `Device`, `Local`, `Platform`, `Port`
- `Interface`, `Intrfce` (abbreviated)
- `Address`, `IP-Address`
- `Neighbor`, `AS` (BGP Autonomous System)
- `State`, `Status`, `Protocol`
- `Up/Down`, `Uptime`, `Hold`, `Holdtme`

##### Routing Protocol
- `SRTT` - Smooth Round Trip Time (EIGRP)
- `RTO` - Retransmission Timeout
- `Seq` - Sequence number
- `MsgRcvd`, `MsgSent` - BGP messages
- `TblVer` - Table version
- `InQ`, `OutQ` - Input/output queue

##### Performance
- `MTU` - Maximum Transmission Unit
- `BW` - Bandwidth
- `DLY` - Delay
- `bits/sec`, `packets/sec` - Throughput

##### Other
- `aaa` - Authentication, Authorization, Accounting
- `vlan` - VLAN
- `OK?` - Status column (question mark in header)
- `Method` - Auth method
- `Capability` - CDP/LLDP capability

#### Optional Colon/Comma (Linje 78)
- **`[:,]?`** - Optional `:` or `,` after property
- **Example**: `Interface:` or `Port,`

#### Examples
```cisco
Interface              IP-Address      OK? Method Status                Protocol
                       ↑ Highlighted   ↑   ↑      ↑                     ↑

Device ID: SW-CORE-01
↑ Highlighted

Platform: cisco WS-C3750, Capabilities: Router Switch
↑ Highlighted             ↑ Highlighted

Neighbor        AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
↑ Highlighted   ↑  ↑ Highlighted (all table headers)
```

---

### 18. keyword (Linje 82-85)

```javascript
'keyword': {
    pattern: /\b(?:interface|ip|ipv6|address|description|switchport|mode|access|trunk|encapsulation|dot1q|native|vlan|speed|duplex|spanning-tree|portfast|bpduguard|router|bgp|eigrp|ospf|route|static|default|gateway|line|vty|console|con|aux|enable|secret|password|service|hostname|banner|motd|aaa|authentication|authorization|accounting|snmp-server|ntp|clock|timezone|logging|permit|deny|any|host|established|log)\b/i,
    greedy: true
}
```

#### Purpose
- **Common Cisco commands** - Blue highlighting
- **Catch-all** for main keywords

#### Keywords (Categories)

##### Interface Config
- `interface`, `description`
- `switchport`, `mode`, `access`, `trunk`
- `encapsulation`, `dot1q` (VLAN tagging)
- `native`, `vlan`
- `speed`, `duplex`
- `spanning-tree`, `portfast`, `bpduguard`

##### IP Config
- `ip`, `ipv6`, `address`
- `route`, `static`, `default`, `gateway`

##### Routing Protocols
- `router`, `bgp`, `eigrp`, `ospf`

##### Line Config
- `line`, `vty` (SSH/Telnet), `console`, `con`, `aux`
- `enable`, `secret`, `password`

##### System
- `service`, `hostname`
- `banner`, `motd` (Message of the Day)
- `clock`, `timezone`, `ntp`
- `logging`

##### AAA
- `aaa`, `authentication`, `authorization`, `accounting`
- `snmp-server`

##### ACL
- `permit`, `deny`, `any`, `host`, `established`, `log`

#### Examples
```cisco
interface GigabitEthernet0/1
↑ Blue

 description Uplink to Core
 ↑ Blue

 switchport mode access
 ↑ Blue     ↑ Blue

 ip address 192.168.1.1 255.255.255.0
 ↑  ↑ Blue

router bgp 65000
↑ Blue ↑ Blue
```

---

### 19. string (Linje 86-89)

```javascript
'string': {
    pattern: /(["'])(?:\\.|(?!\1)[^\\\r\n])*\1/,
    greedy: true
}
```

#### Regex: `/(["'])(?:\\.|(?!\1)[^\\\r\n])*\1/`
Complex regex for quoted strings.

##### Breakdown:
- **`(["'])`** - Capture quote type (" or ')
  - Group 1: `\1` references this later

- **`(?:\\.|(?!\1)[^\\\r\n])*`** - Content inside quotes (repeating)
  - **`\\.`** - Escaped character (e.g., `\"`, `\\`)
  - **`|`** - OR
  - **`(?!\1)[^\\\r\n]`** - Any character except:
    - `\1` (matching quote - lookahead prevents early close)
    - `\\` (backslash)
    - `\r\n` (newlines)

- **`\1`** - Closing quote (matches opening quote)

#### Why Complex?
- **Handles escapes**: `"He said \"Hello\""`
- **Matches quote type**: `"text"` or `'text'` (not mixed)

#### Examples
```cisco
banner motd "Welcome to Router1"
            ↑ String highlighted

description "Uplink to DC"
            ↑ String highlighted

snmp-server community 'MySecret123' RO
                      ↑ String highlighted
```

---

### 20. number (Linje 90-93)

```javascript
'number': {
    pattern: /\b\d+\b/,
    greedy: true
}
```

#### Regex: `/\b\d+\b/`
- **`\d+`** - One or more digits
- **`\b`** - Word boundaries (prevents partial matches)

#### Examples
```cisco
access-list 10 permit 192.168.1.0 0.0.0.255
            ↑ Number (but 192.168.1.0 matched as IP)

vlan 100
     ↑ Number

bandwidth 1000000
          ↑ Number
```

---

### 21. punctuation (Linje 94)

```javascript
'punctuation': /[{}[\];(),.:]/
```

#### Characters
- `{}` - Braces (rare in Cisco, but included)
- `[]` - Brackets (ACLs, optional parameters)
- `;` - Semicolon
- `()` - Parentheses (hitcnt, route-map, etc.)
- `,` - Comma
- `.` - Dot (interfaces, IPs, MACs)
- `:` - Colon (property headers, WWN)

#### Examples
```cisco
interface GigabitEthernet0/1
                        ↑ Punctuation (slash)

access-list 10 permit host 192.168.1.1 (hitcnt=42)
                                        ↑ Punctuation
```

---

## Token Priority (Order Matters!)

### Why Order is Critical
Prism.js processes tokens **in order defined**. First match wins.

### Example Conflict:
```javascript
// If 'number' came before 'ip-address':
'192.168.1.1' would match as:
  '192' (number), '.', '168' (number), '.', '1' (number), '.', '1' (number)

// With 'ip-address' first:
'192.168.1.1' matches as one token (ip-address)
```

### Current Priority (Good):
1. **Comments** - Highest (anything after `!` is comment, not other tokens)
2. **Prompts** - Before keywords (prevent `#` being punctuation)
3. **Interfaces** - Before keywords (GigabitEthernet is one token)
4. **IP/MAC addresses** - Before numbers (prevent digit splitting)
5. **Keywords** - Before strings/numbers (commands first)
6. **Strings** - After keywords (quoted text)
7. **Numbers** - Near end (catch remaining digits)
8. **Punctuation** - Last (lowest priority)

---

## Usage Example

### HTML
```html
<pre><code class="language-cisco">
! Core switch config
interface GigabitEthernet0/1
 description Uplink to CORE-SW1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
</code></pre>
```

### After Prism.js Processing
```html
<pre><code class="language-cisco">
<span class="token comment">! Core switch config</span>
<span class="token keyword">interface</span> <span class="token interface">GigabitEthernet0/1</span>
 <span class="token keyword">description</span> Uplink to CORE-SW1
 <span class="token keyword">ip</span> <span class="token keyword">address</span> <span class="token ip-address">192.168.1.1</span> <span class="token ip-address">255.255.255.0</span>
 <span class="token bad-keyword">no</span> <span class="token bad-keyword">shutdown</span>
</code></pre>
```

### CSS Applies Colors
```css
.token.comment { color: #6a9955; font-style: italic; }
.token.keyword { color: #569cd6; font-weight: bold; }
.token.interface { color: #4ec9b0; }
.token.ip-address { color: #b5cea8; }
.token.bad-keyword { color: #f44747; }
```

---

## Integration with Chatbot

### Flow:
```
1. AI returns: "```cisco\nshow ip int brief\n```"
   ↓
2. message-parser.js → {type:'code', language:'cisco', content:'...'}
   ↓
3. message-handler.js → Create <pre><code class="language-cisco">
   ↓
4. Prism.highlightElement() → Detects 'cisco' language
   ↓
5. Uses Prism.languages.cisco → Applies regex patterns
   ↓
6. Wraps tokens in <span class="token ...">
   ↓
7. Cisco theme CSS → Colors tokens
```

### Auto-Detection in code-detector.js
```javascript
function detectCiscoConfig(code) {
    const ciscoPatterns = [
        /^interface\s+(GigabitEthernet|FastEthernet|Ethernet)/m,
        /^router\s+(bgp|eigrp|ospf)\s+\d+/m,
        /^\s*ip\s+address\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/m
    ];
    return ciscoPatterns.some(p => p.test(code));
}
```
→ If detected, sets `language: 'cisco'` → Uses this file's definitions

---

## Performance

### Regex Complexity
- **Simple patterns** - Most are basic alternation
- **Complex patterns** - String, interface (nested groups)
- **greedy: true** - Prevents backtracking issues

### Execution Time
- **Per code block** - Runs once during `Prism.highlightElement()`
- **Client-side** - No backend load
- **Fast** - Even large configs (1000 lines) highlight in < 100ms

---

## Browser Compatibility

### Regex Features
- **Lookahead** - IE 5.5+, all modern browsers
- **Non-capturing groups** - IE 5.5+
- **Multiline mode** - IE 5.5+
- **Case insensitive** - IE 5.5+

### Prism.js Requirement
- **IE 9+** (with polyfills)
- **Chrome 4+**, **Firefox 2+**, **Safari 4+**
- **Universal support** in modern browsers

---

## Konklusion

`prism-cisco.js` provides comprehensive Cisco IOS syntax highlighting:
- **21 token types** - Comments, prompts, interfaces, IPs, MACs, security, ACLs, keywords
- **Smart patterns** - Regex handles Cisco-specific formats (wwn, hitcount, serial numbers)
- **Color semantics** - Green (good), red (bad), purple (security), blue (commands)
- **Order matters** - Token priority prevents conflicts
- **Extensible** - Easy to add new patterns

**Key design decisions:**
- Separate good/bad keywords (visual status indication)
- Highlight entire security lines (password visibility warning)
- Detect both MAC formats (Cisco `xxxx.xxxx.xxxx` and standard `xx:xx:xx:xx:xx:xx`)
- Table header detection (show command output readability)
- ACL hitcount zero vs active (troubleshooting aid)

**File size**: 130 lines defining Cisco-specific syntax for Prism.js.
