#!/usr/bin/env python3
"""
RDS Configuration Checker
This script helps identify common RDS configuration issues
"""

import socket
import sys

def check_dns_resolution():
    """Check if the RDS endpoint resolves"""
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    print("=== DNS Resolution Test ===")
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolution successful: {host} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def check_port_connectivity():
    """Check if port 3306 is accessible"""
    host = 'pmc6-devbd.c63wim4ayano.us-east-1.rds.amazonaws.com'
    port = 3306
    print(f"\n=== Port Connectivity Test ===")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is accessible on {host}")
            return True
        else:
            print(f"❌ Port {port} is not accessible on {host}")
            return False
    except Exception as e:
        print(f"❌ Port connectivity test failed: {e}")
        return False

def get_public_ip():
    """Get your current public IP address"""
    print(f"\n=== Your Public IP Address ===")
    try:
        import urllib.request
        response = urllib.request.urlopen('https://api.ipify.org')
        ip = response.read().decode('utf-8')
        print(f"Your public IP: {ip}")
        print(f"Make sure this IP is allowed in your RDS security group!")
        return ip
    except Exception as e:
        print(f"❌ Could not determine public IP: {e}")
        return None

def print_troubleshooting_steps():
    """Print troubleshooting steps"""
    print(f"\n=== Troubleshooting Steps ===")
    print("1. **Check RDS Security Group:**")
    print("   - Go to AWS Console -> RDS -> Your Instance -> Connectivity & Security")
    print("   - Check the Security Groups")
    print("   - Ensure port 3306 is open for your IP address")
    print()
    print("2. **Check RDS Public Accessibility:**")
    print("   - Go to AWS Console -> RDS -> Your Instance -> Connectivity & Security")
    print("   - Ensure 'Publicly accessible' is set to 'Yes'")
    print()
    print("3. **Check VPC and Subnet:**")
    print("   - Ensure your RDS is in a public subnet if you want external access")
    print("   - Check route tables and internet gateway configuration")
    print()
    print("4. **Verify Credentials:**")
    print("   - Double-check the master username and password")
    print("   - Try resetting the password if needed")
    print()
    print("5. **Check RDS Status:**")
    print("   - Ensure the RDS instance status is 'Available'")
    print("   - Check for any maintenance windows or backups in progress")

if __name__ == '__main__':
    print("=== RDS Configuration Checker ===\n")
    
    dns_ok = check_dns_resolution()
    port_ok = check_port_connectivity()
    get_public_ip()
    
    if not dns_ok or not port_ok:
        print_troubleshooting_steps()
    else:
        print("\n✅ Basic connectivity looks good!")
        print("If you're still getting access denied errors, it's likely a credentials or security group issue.")