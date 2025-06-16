import network
import socket
import time

# --- Wi-Fi Configuration ---
SSID = ''    # Replace with your Wi-Fi network name
PASSWORD = '' # Replace with your Wi-Fi password

# --- Web Server Configuration ---
PORT = 80 # Standard HTTP port

# HTML content to serve
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Pico W Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f0f0f0; }
        h1 { color: #333; }
        p { color: #666; }
        .container { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello from Raspberry Pi Pico W!</h1>
        <p>Hi dhanishka didi</p>
        <p>Current time (Pico's perspective): <span id="time">Loading...</span></p>
    </div>
    <script>
        function updateTime() {
            const now = new Date();
            document.getElementById('time').innerText = now.toLocaleString();
        }
        setInterval(updateTime, 1000); // Update time every second
        updateTime(); // Initial call
    </script>
</body>
</html>
"""

# --- Wi-Fi Connection Function ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connection
    max_attempts = 10
    for i in range(max_attempts):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        print(f"Waiting for Wi-Fi connection... ({i+1}/{max_attempts})")
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Wi-Fi connection failed!')
    else:
        status = wlan.ifconfig()
        print(f'Wi-Fi connected! IP address: {status[0]}')
        return status[0] # Return the IP address

# --- Main Web Server Loop ---
def start_web_server():
    try:
        ip_address = connect_wifi()
    except RuntimeError as e:
        print(e)
        print("Please check your SSID and PASSWORD.")
        return # Exit if Wi-Fi fails

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reusing the address
    s.bind(('', PORT))
    s.listen(5) # Listen for up to 5 incoming connections

    print(f"Web server listening on http://{ip_address}:{PORT}")

    while True:
        try:
            conn, addr = s.accept()
            print(f'Got a connection from {addr}')
            request = conn.recv(1024) # Read up to 1024 bytes of the request
            request_str = request.decode('utf-8')
            print(f'Request: {request_str.splitlines()[0]}') # Print first line of request

            # Simple check for GET request (we're not parsing full HTTP headers)
            if 'GET / HTTP/1.1' in request_str:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                response += f"Content-Length: {len(html_content)}\r\n"
                response += "Connection: close\r\n\r\n"
                response += html_content
                conn.sendall(response.encode('utf-8'))
            else:
                # For any other request, send a 404 Not Found
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found"
                conn.sendall(response.encode('utf-8'))

            conn.close()
            print('Connection closed.')

        except OSError as e:
            print(f'Error accepting connection or sending data: {e}')
            # Clean up socket if error (e.g., connection reset by peer)
            if e.args[0] == 104: # ECONNRESET
                conn.close()
            time.sleep(1) # Small delay before trying again
        except KeyboardInterrupt:
            print("Web server stopped.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    s.close() # Close the server socket when loop exits

# --- Start the server ---
start_web_server()
