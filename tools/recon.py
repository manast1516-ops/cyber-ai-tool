import socket
import psutil

def check_port_status(host: str, port: int) -> dict:
    """Checks whether a specific TCP port is listening on a host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            result = sock.connect_ex((host, int(port)))
            return {
                "host": host,
                "port": int(port),
                "status": "open" if result == 0 else "closed"
            }
    except Exception as e:
        return {"host": host, "port": int(port), "error": str(e)}

def get_local_interfaces() -> dict:
    """Lists local network interfaces and assigned IP addresses."""
    interfaces = {}
    for iface_name, addrs in psutil.net_if_addrs().items():
        interfaces[iface_name] = [
            addr.address for addr in addrs if addr.family == socket.AF_INET
        ]
    return interfaces
