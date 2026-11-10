from tools.recon import (
    check_port_status,
    get_local_interfaces,
    scan_network,
    sniff_traffic_summary,
    lookup_dns,
    audit_listening_sockets,
    audit_auth_logs,
    audit_suid_binaries,
    generate_firewall_rule,
    decode_payload
)

TOOL_REGISTRY = {
    "check_port_status": {
        "function": check_port_status,
        "description": "Checks whether a specific TCP port is open or closed on a target host.",
        "parameters": {"host": "string", "port": "integer"}
    },
    "get_local_interfaces": {
        "function": get_local_interfaces,
        "description": "Lists local network interfaces and assigned IPv4 addresses.",
        "parameters": {}
    },
    "scan_network": {
        "function": scan_network,
        "description": "Scans a local subnet (e.g., 10.209.71.0/24) via ARP broadcast to discover active IP and MAC addresses.",
        "parameters": {"target_subnet": "string", "interface": "string"}
    },
    "sniff_traffic_summary": {
        "function": sniff_traffic_summary,
        "description": "Passively captures a small burst of live packets to report active protocols and endpoints.",
        "parameters": {"interface": "string", "count": "integer"}
    },
    "lookup_dns": {
        "function": lookup_dns,
        "description": "Resolves domain names to IP addresses or performs reverse PTR lookups on an IP.",
        "parameters": {"target": "string"}
    },
    "audit_listening_sockets": {
        "function": audit_listening_sockets,
        "description": "Audits all TCP/UDP listeners on the system to inspect open ports and daemon exposure.",
        "parameters": {}
    },
    "audit_auth_logs": {
        "function": audit_auth_logs,
        "description": "Parses /var/log/auth.log for failed SSH or sudo login attempts and brute-force indicators.",
        "parameters": {"max_entries": "integer"}
    },
    "audit_suid_binaries": {
        "function": audit_suid_binaries,
        "description": "Lists system binaries with the SUID bit set to evaluate privilege escalation exposure.",
        "parameters": {}
    },
    "generate_firewall_rule": {
        "function": generate_firewall_rule,
        "description": "Generates defensive iptables and ufw commands to block malicious or unauthorized IP addresses.",
        "parameters": {"ip_address": "string", "action": "string"}
    },
    "decode_payload": {
        "function": decode_payload,
        "description": "Decodes Base64/Hex strings and computes MD5, SHA-1, and SHA-256 hashes.",
        "parameters": {"data": "string"}
    }
}

def get_registered_tools() -> dict:
    return {name: meta["description"] for name, meta in TOOL_REGISTRY.items()}

def get_tool_descriptions() -> str:
    descriptions = []
    for name, meta in TOOL_REGISTRY.items():
        descriptions.append(f"- {name}: {meta['description']} (Parameters: {meta['parameters']})")
    return "\n".join(descriptions)

def execute_tool(tool_name: str, **kwargs):
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Tool '{tool_name}' is not registered."}
    try:
        func = TOOL_REGISTRY[tool_name]["function"]
        return func(**kwargs)
    except Exception as e:
        return {"error": f"Execution failure in '{tool_name}': {str(e)}"}
