import os
import http.server
import socketserver
import webbrowser
import threading
import json
import subprocess
import time
import signal
import sys
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv

# Set the port for serving the HTML page
HTML_PORT = 8000
# Set the port for the Streamlit app
STREAMLIT_PORT = 8501

# Load environment variables
load_dotenv()

def check_cohere_api_key():
    """Check if Cohere API key is set and valid"""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("\033[93m[WARNING] Cohere API key not set or invalid\033[0m")
        print("\033[93mPlease set your API key in the .env file\033[0m")
        new_key = input("Enter your Cohere API key (or press Enter to continue anyway): ")
        if new_key:
            with open('.env', 'w') as f:
                f.write(f"COHERE_API_KEY={new_key}")
            print("API key saved!")
            return True
        return False
    return True

def signal_handler(sig, frame):
    print("\n\033[94mStopping servers...\033[0m")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class ChatbotRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Customize logging format
        sys.stderr.write("\033[92m[WEB] %s - %s\033[0m\n" %
                         (self.address_string(),
                          format % args))

    def do_GET(self):
        # Serve the index.html file
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Handle API requests from the frontend
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Parse the request body
        try:
            request_data = json.loads(post_data.decode('utf-8'))
            response_data = {"status": "success", "message": "Received your message"}
            
            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            # Send an error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def start_html_server():
    """Start the HTTP server to serve the HTML interface"""
    try:
        handler = ChatbotRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", HTML_PORT), handler)
        print(f"\033[94m[INFO] Serving HTML interface at \033[4mhttp://localhost:{HTML_PORT}\033[0m")
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\033[91m[ERROR] Port {HTML_PORT} is already in use. Try a different port.\033[0m")
            sys.exit(1)
        else:
            raise

def start_streamlit_app():
    """Start the Streamlit app as a subprocess"""
    print("\033[94m[INFO] Starting Streamlit app...\033[0m")
    try:
        # Check if Streamlit is installed
        subprocess.run(["streamlit", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Start the Streamlit app
        process = subprocess.Popen(
            ["streamlit", "run", "app.py", "--server.port", str(STREAMLIT_PORT), "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor the process output for startup
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if "You can now view your Streamlit app in your browser" in line:
                print(f"\033[94m[INFO] Streamlit app running at \033[4mhttp://localhost:{STREAMLIT_PORT}\033[0m")
                break
            if "Error" in line or "Exception" in line:
                print(f"\033[91m[ERROR] Streamlit app failed to start: {line}\033[0m")
                break
    except subprocess.CalledProcessError:
        print("\033[91m[ERROR] Streamlit is not installed. Please install it with 'pip install streamlit'.\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\033[91m[ERROR] Failed to start Streamlit app: {e}\033[0m")
        sys.exit(1)

def open_browser():
    """Open the web browser to the HTML interface"""
    time.sleep(3)  # Wait for servers to start
    print("\033[94m[INFO] Opening web browser...\033[0m")
    webbrowser.open(f"http://localhost:{HTML_PORT}")

def print_banner():
    """Print a nice banner"""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║           Proactive Networking                ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print("\033[95m" + banner + "\033[0m")
    print("\033[94mStarting services...\033[0m")

if __name__ == "__main__":
    print_banner()
    
    # Check Cohere API key
    if not check_cohere_api_key():
        print("\033[93m[WARNING] Continuing without a valid Cohere API key. The chatbot may not function correctly.\033[0m")
    
    # Start the HTML server in a separate thread
    html_server_thread = threading.Thread(target=start_html_server)
    html_server_thread.daemon = True
    html_server_thread.start()
    
    # Start the Streamlit app in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit_app)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Open the browser
    open_browser()
    
    print("\033[94m[INFO] Press Ctrl+C to stop the servers\033[0m")
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\033[94m[INFO] Shutting down servers...\033[0m")
        sys.exit(0) 