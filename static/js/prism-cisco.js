// Cisco IOS language definition for Prism.js
// Custom language for Cisco IOS syntax highlighting

Prism.languages.cisco = {
    'comment': {
        pattern: /(?:!.*|remark\s+.*)/,
        greedy: true
    },
    'prompt-enable': {
        pattern: /^[\w.-]+#(?:\s|$)/m,
        greedy: true
    },
    'prompt-user': {
        pattern: /^[\w.-]+>(?:\s|$)/m,
        greedy: true
    },
    'interface': {
        pattern: /\b(?:Embedded-Service-Engine|GigabitEthernet|FastEthernet|TenGigabitEthernet|Ethernet|Serial|Tunnel|Loopback|Port-channel|Vlan|Multilink|Null|Nvi|vfc|Te|Gi|Fa|Eth?|Po)\d+(?:[\/.:]\d+)*[*]?\b/i,
        greedy: true
    },
    'wwn': {
        pattern: /\b(?:wwn|pwwn|(?:[a-f0-9]{2}:){7}[a-f0-9]{2})\b/i,
        greedy: true,
        alias: 'credential'
    },
    'ip-address': {
        pattern: /\b(?:\d{1,3}\.){3}\d{1,3}(?:\/\d{1,2})?(?::\d{1,5})?\b/,
        greedy: true,
        alias: 'number'
    },
    'mac-address': {
        pattern: /\b(?:[0-9a-f]{4}\.){2}[0-9a-f]{4}\b|\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b/i,
        greedy: true,
        alias: 'builtin'
    },
    'ios-version': {
        pattern: /\b\d+\.\d+(?:\.\d+)?(?:\([^)]+\))?[^\s,]*\b/,
        greedy: true,
        alias: 'version'
    },
    'serial-number': {
        pattern: /\b[A-Z]{2,3}\d{4}[A-Z0-9]{4}\b/i,
        greedy: true,
        alias: 'version'
    },
    'important': {
        pattern: /\b(?:erase|remove|delete|Building|configuration|reload|\[confirm\]|\(yes\/no\):?|--more--)\b/i,
        greedy: true
    },
    'good-keyword': {
        pattern: /\b(?:yes|permit|clear|\[OK\]|on|Full-duplex|cir|police|mgmt|Management|inside|1000000|1000Mb\/s|enabled|down->up|running|SUCCESS|success|up|passed|kasper|PASS|Active|Complete|GRE|ipsec)\b/i,
        greedy: true,
        alias: 'inserted'
    },
    'bad-keyword': {
        pattern: /\b(?:no|administratively|shutdown?|never|deny|down|fail|invalid|reload|not|initializing|Off|1024|768|half-duplex|100Mb\/s|100000|des56?|telnet|err-disabled|disabled|up->down|trunk|exceeded|inhibit|_ERR:)\b/i,
        greedy: true,
        alias: 'deleted'
    },
    'security': {
        pattern: /\b(?:username|password|key|enable\s+secret)\b.*$/m,
        greedy: true,
        alias: 'credential'
    },
    'acl': {
        pattern: /\b(?:access-(?:list|class|group)|use-acl|prefix-list|time-range|object-group|route-map)\b/i,
        greedy: true
    },
    'hitcount-zero': {
        pattern: /\(hitcnt=0\)/,
        greedy: true
    },
    'hitcount-active': {
        pattern: /\(hitcnt=[1-9]\d*\)/,
        greedy: true,
        alias: 'credential'
    },
    'property': {
        pattern: /\b(?:class|policy|service|parameter|match|version|PN|SN|S\/N|ID|PID|VID|NAME|DESCR|Device|Local|Intrfce|Holdtme|Capability|Platform|Port|Address|Interface|Hold|Uptime|SRTT|RTO|Seq|Neighbor|AS|MsgRcvd|MsgSent|TblVer|InQ|OutQ|Up\/Down|State|IP-Address|Method|OK\?|Status|Protocol|aaa|vlan|MTU|BW|DLY|bits\/sec|packets\/sec)[:,]?\b/i,
        greedy: true
    },
    'keyword': {
        pattern: /\b(?:interface|ip|ipv6|address|description|switchport|mode|access|trunk|encapsulation|dot1q|native|vlan|speed|duplex|spanning-tree|portfast|bpduguard|router|bgp|eigrp|ospf|route|static|default|gateway|line|vty|console|con|aux|enable|secret|password|service|hostname|banner|motd|aaa|authentication|authorization|accounting|snmp-server|ntp|clock|timezone|logging|permit|deny|any|host|established|log)\b/i,
        greedy: true
    },
    'string': {
        pattern: /(["'])(?:\\.|(?!\1)[^\\\r\n])*\1/,
        greedy: true
    },
    'number': {
        pattern: /\b\d+\b/,
        greedy: true
    },
    'punctuation': /[{}[\];(),.:]/
};
