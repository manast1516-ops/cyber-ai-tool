import socket
import subprocess
import json
import base64
import hashlib
import binascii
import psutil
from datetime import datetime
from scapy.all import ARP, Ether, srp, sniff, IP, TCP, UDP, ICMP, DNS

def check_port_status(host: str, port: int) -> dict:
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
    interfaces = {}
    for iface_name, addrs in psutil.net_if_addrs().items():
        interfaces[iface_name] = [
            addr.address for addr in addrs if addr.family == socket.AF_INET
        ]
    return interfaces

def scan_network(target_subnet: str = "10.209.71.0/24", interface: str = "wlx306893b54f95") -> dict:
    try:
        arp = ARP(pdst=target_subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, iface=interface, timeout=2.5, verbose=False)[0]

        devices = [{"ip": r.psrc, "mac": r.hwsrc} for _, r in result]
        return {
            "status": "success",
            "subnet": target_subnet,
            "device_count": len(devices),
            "devices": devices
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def sniff_traffic_summary(interface: str = "wlx306893b54f95", count: int = 30) -> dict:
    try:
        packets = sniff(iface=interface, count=int(count), timeout=6)
        protocols = {"TCP": 0, "UDP": 0, "ICMP": 0, "DNS": 0, "Other": 0}
        endpoints = set()

        for pkt in packets:
            if IP in pkt:
                endpoints.add(f"{pkt[IP].src} -> {pkt[IP].dst}")
                if DNS in pkt:
                    protocols["DNS"] += 1
                elif TCP in pkt:
                    protocols["TCP"] += 1
                elif UDP in pkt:
                    protocols["UDP"] += 1
                elif ICMP in pkt:
                    protocols["ICMP"] += 1
                else:
                    protocols["Other"] += 1

        return {
            "status": "success",
            "packets_captured": len(packets),
            "protocols": protocols,
            "sample_conversations": list(endpoints)[:10]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def lookup_dns(target: str) -> dict:
    try:
        target = target.strip()
        if all(part.isdigit() for part in target.split(".") if len(target.split(".")) == 4):
            host, _, _ = socket.gethostbyaddr(target)
            return {"target": target, "type": "reverse_ptr", "hostname": host}
        ip = socket.gethostbyname(target)
        return {"target": target, "type": "forward_a", "resolved_ip": ip}
    except Exception as e:
        return {"target": target, "status": "error", "message": str(e)}

def audit_listening_sockets() -> dict:
    try:
        output = subprocess.check_output(["ss", "-tuln"], text=True)
        listeners = []
        for line in output.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 5:
                listeners.append({"proto": parts[0], "local_address": parts[4]})
        return {"status": "success", "total_listeners": len(listeners), "listeners": listeners}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def audit_auth_logs(max_entries: int = 20) -> dict:
    log_path = "/var/log/auth.log"
    failed_attempts = []
    try:
        with open(log_path, "r", errors="ignore") as f:
            lines = f.readlines()[-300:]
        for line in lines:
            if "Failed password" in line or "authentication failure" in line:
                failed_attempts.append(line.strip())
        return {
            "status": "success",
            "total_failed_detected": len(failed_attempts),
            "recent_events": failed_attempts[-int(max_entries):]
        }
    except FileNotFoundError:
        return {"status": "error", "message": f"{log_path} not found on host."}
    except PermissionError:
        return {"status": "error", "message": "Permission denied reading auth.log. Grant read access."}

def audit_suid_binaries() -> dict:
    try:
        cmd = ["find", "/usr/bin", "/bin", "/usr/sbin", "-perm", "-4000", "-type", "f"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        suid_files = [f.strip() for f in output.strip().split("\n") if f.strip()]
        return {
            "status": "success",
            "suid_count": len(suid_files),
            "binaries": suid_files[:25]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_firewall_rule(ip_address: str, action: str = "DROP") -> dict:
    ip = ip_address.strip()
    action = action.upper()
    if action not in ("DROP", "REJECT", "ACCEPT"):
        action = "DROP"
    iptables_cmd = f"sudo iptables -A INPUT -s {ip} -j {action}"
    ufw_cmd = f"sudo ufw deny from {ip}"
    return {
        "status": "generated",
        "target_ip": ip,
        "action": action,
        "iptables_command": iptables_cmd,
        "ufw_command": ufw_cmd,
        "note": "Execute manually or copy to terminal with root privileges to enforce."
    }

def decode_payload(data: str) -> dict:
    raw = data.strip()
    result = {"input": raw}
    try:
        b64_decoded = base64.b64decode(raw, validate=True).decode("utf-8", errors="ignore")
        result["base64_decoded"] = b64_decoded
    except Exception:
        result["base64_decoded"] = None

    try:
        hex_clean = raw.replace("0x", "").replace(" ", "")
        hex_decoded = binascii.unhexlify(hex_clean).decode("utf-8", errors="ignore")
        result["hex_decoded"] = hex_decoded
    except Exception:
        result["hex_decoded"] = None

    result["hashes"] = {
        "md5": hashlib.md5(raw.encode()).hexdigest(),
        "sha1": hashlib.sha1(raw.encode()).hexdigest(),
        "sha256": hashlib.sha256(raw.encode()).hexdigest()
    }
    return result
