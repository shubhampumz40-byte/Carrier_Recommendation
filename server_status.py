#!/usr/bin/env python3
"""
Career Compass - Server Status Checker
Quick script to check if your server is running and accessible
"""

import requests
import subprocess
import json
from datetime import datetime

def check_local_server():
    """Check if local Flask server is running"""
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_network_server():
    """Check if network server is accessible"""
    try:
        response = requests.get("http://192.168.0.115:5000", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_running_processes():
    """Get list of running Python and tunnel processes"""
    processes = []
    try:
        # Check for Python processes
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        if 'python.exe' in result.stdout:
            processes.append("✅ Python process found")
        else:
            processes.append("❌ No Python process found")
            
        # Check for Cloudflare tunnel
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq cloudflared.exe'], 
                              capture_output=True, text=True)
        if 'cloudflared.exe' in result.stdout:
            processes.append("✅ Cloudflare tunnel found")
        else:
            processes.append("❌ No Cloudflare tunnel found")
            
    except Exception as e:
        processes.append(f"❌ Error checking processes: {e}")
        
    return processes

def main():
    print("🧭 Career Compass - Server Status Check")
    print("=" * 50)
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check servers
    print("🌐 Server Status:")
    local_status = check_local_server()
    network_status = check_network_server()
    
    print(f"   Local (localhost:5000): {'✅ Online' if local_status else '❌ Offline'}")
    print(f"   Network (192.168.0.115:5000): {'✅ Online' if network_status else '❌ Offline'}")
    print()
    
    # Check processes
    print("🔄 Running Processes:")
    processes = get_running_processes()
    for process in processes:
        print(f"   {process}")
    print()
    
    # Overall status
    if local_status and network_status:
        print("🎉 Status: All systems operational!")
        print("📱 Your Career Compass is ready for public access")
    elif local_status:
        print("⚠️  Status: Local server running, but network access may be limited")
    else:
        print("🚨 Status: Server appears to be down")
        print("💡 Try running: python keep_server_running.py")
    
    print()
    print("🔗 Access URLs:")
    print("   Local: http://localhost:5000")
    print("   Network: http://192.168.0.115:5000")
    print("   Public: Check Cloudflare tunnel output for public URL")

if __name__ == "__main__":
    main()