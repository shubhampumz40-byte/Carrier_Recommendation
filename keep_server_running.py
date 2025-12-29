#!/usr/bin/env python3
"""
Career Compass - Server Keep-Alive Script
This script ensures your Career Compass server stays running 24/7
"""

import subprocess
import time
import sys
import os
import requests
from datetime import datetime

class ServerKeepAlive:
    def __init__(self):
        self.flask_process = None
        self.tunnel_process = None
        self.local_url = "http://localhost:5000"
        self.check_interval = 30  # Check every 30 seconds
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def start_flask_server(self):
        """Start the Flask server"""
        try:
            if self.flask_process is None or self.flask_process.poll() is not None:
                self.log("Starting Flask server...")
                self.flask_process = subprocess.Popen(
                    [sys.executable, "run.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(5)  # Give Flask time to start
                self.log("Flask server started successfully")
            return True
        except Exception as e:
            self.log(f"Error starting Flask server: {e}")
            return False
            
    def start_tunnel(self):
        """Start the Cloudflare tunnel"""
        try:
            if self.tunnel_process is None or self.tunnel_process.poll() is not None:
                self.log("Starting Cloudflare tunnel...")
                self.tunnel_process = subprocess.Popen(
                    ["./cloudflared.exe", "tunnel", "--url", "http://localhost:5000"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                time.sleep(10)  # Give tunnel time to establish
                self.log("Cloudflare tunnel started successfully")
            return True
        except Exception as e:
            self.log(f"Error starting tunnel: {e}")
            return False
            
    def check_server_health(self):
        """Check if the server is responding"""
        try:
            response = requests.get(self.local_url, timeout=10)
            return response.status_code == 200
        except:
            return False
            
    def restart_services(self):
        """Restart both Flask and tunnel services"""
        self.log("Restarting services...")
        
        # Stop existing processes
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process = None
            
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_process = None
            
        time.sleep(5)
        
        # Restart services
        self.start_flask_server()
        self.start_tunnel()
        
    def run(self):
        """Main keep-alive loop"""
        self.log("🚀 Career Compass Keep-Alive Service Started")
        self.log("=" * 50)
        
        # Initial startup
        self.start_flask_server()
        self.start_tunnel()
        
        consecutive_failures = 0
        
        while True:
            try:
                # Check server health
                if self.check_server_health():
                    if consecutive_failures > 0:
                        self.log("✅ Server is back online!")
                        consecutive_failures = 0
                    else:
                        self.log("✅ Server is healthy")
                else:
                    consecutive_failures += 1
                    self.log(f"❌ Server health check failed (attempt {consecutive_failures})")
                    
                    # Restart after 3 consecutive failures
                    if consecutive_failures >= 3:
                        self.log("🔄 Restarting services due to health check failures...")
                        self.restart_services()
                        consecutive_failures = 0
                        
                # Check if processes are still running
                if self.flask_process and self.flask_process.poll() is not None:
                    self.log("🔄 Flask process died, restarting...")
                    self.start_flask_server()
                    
                if self.tunnel_process and self.tunnel_process.poll() is not None:
                    self.log("🔄 Tunnel process died, restarting...")
                    self.start_tunnel()
                    
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("🛑 Shutting down keep-alive service...")
                if self.flask_process:
                    self.flask_process.terminate()
                if self.tunnel_process:
                    self.tunnel_process.terminate()
                break
            except Exception as e:
                self.log(f"❌ Unexpected error: {e}")
                time.sleep(self.check_interval)

if __name__ == "__main__":
    print("🧭 Career Compass - Server Keep-Alive Service")
    print("This will keep your server running 24/7 for public access")
    print("Press Ctrl+C to stop")
    print()
    
    keeper = ServerKeepAlive()
    keeper.run()