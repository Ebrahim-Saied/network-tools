#!/usr/bin/env python3
"""
Network Monitoring Tool
Monitors network connectivity and interface health
"""

import subprocess
import platform
import socket
import psutil
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.system = platform.system()
        
    def check_connectivity(self, host='8.8.8.8'):
        """Check internet connectivity"""
        try:
            socket.gethostbyaddr(host)
            return True, "Connected"
        except socket.error:
            return False, "No connectivity"
    
    def get_network_interfaces(self):
        """Get all network interfaces and their status"""
        interfaces = {}
        for interface, stats in psutil.net_if_stats().items():
            interfaces[interface] = {
                'up': stats.isup,
                'speed': stats.speed,
                'mtu': stats.mtu
            }
        return interfaces
    
    def ping_host(self, host):
        """Ping a specific host"""
        try:
            output = subprocess.check_output(
                ['ping', '-c' if self.system == 'Darwin' else '-n', '1', host],
                stderr=subprocess.STDOUT,
                timeout=5
            )
            return True, f"Host {host} is reachable"
        except subprocess.CalledProcessError:
            return False, f"Host {host} is unreachable"
    
    def get_dns_config(self):
        """Get DNS configuration"""
        try:
            with open('/etc/resolv.conf', 'r') as f:
                dns_servers = [line.split()[1] for line in f if 'nameserver' in line]
                return dns_servers
        except:
            return ["Unable to retrieve DNS config"]
    
    def generate_report(self):
        """Generate network health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'connectivity': self.check_connectivity(),
            'interfaces': self.get_network_interfaces(),
            'dns_servers': self.get_dns_config()
        }
        return report

if __name__ == "__main__":
    monitor = NetworkMonitor()
    report = monitor.generate_report()
    print("Network Health Report")
    print("=" * 50)
    for key, value in report.items():
        print(f"{key}: {value}")
