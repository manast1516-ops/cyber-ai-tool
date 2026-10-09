import json
from tools.recon import check_port_status, get_local_interfaces

TOOL_DEFINITIONS = {
    "check_port_status": {
        "func": check_port_status,
        "description": "Checks if a TCP port is open. Parameters: host (str), port (int)."
    },
    "get_local_interfaces": {
        "func": get_local_interfaces,
        "description": "Retrieves local network interfaces and their IPv4 addresses. No arguments needed."
    }
}

def get_tool_descriptions() -> str:
    """Returns formatted tool descriptions for system prompting."""
    descriptions = []
    for name, meta in TOOL_DEFINITIONS.items():
        descriptions.append(f"- {name}: {meta['description']}")
    return "\n".join(descriptions)

def execute_tool(tool_name: str, **kwargs):
    """Executes a registered tool by name with arguments."""
    if tool_name not in TOOL_DEFINITIONS:
        return {"error": f"Tool '{tool_name}' not found."}
    return TOOL_DEFINITIONS[tool_name]["func"](**kwargs)
