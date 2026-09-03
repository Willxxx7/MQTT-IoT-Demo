import os
import sys
import time
import subprocess
import webbrowser
import threading
import signal

# ============================================================
# THREE WAYS TO BUILD REAL-TIME SYSTEMS - WITH LIVE DEMOS
# Press ENTER to move through the lesson.
# ============================================================

# Fix for Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class _Dummy:
        RESET_ALL = ""
        CYAN = GREEN = YELLOW = MAGENTA = BLUE = RED = WHITE = ""
        BRIGHT = ""
    Fore = Style = _Dummy()

WIDTH = 78
DEMO_PROCESSES = []

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def wait_for_enter():
    input("\n" + Fore.YELLOW + ">>> Press ENTER to continue..." + Style.RESET_ALL)


def choose_interface():
    """Offer a fancy UI or a simpler plain terminal interface."""
    print(Fore.CYAN + "Choose your interface:" + Style.RESET_ALL)
    print("  1. Fancy interface (coloured dashboard + boxed sections)")
    print("  2. Plain interface (simple text menu)")
    print(Fore.YELLOW + "If you prefer a simpler experience, you can use the plain interface." + Style.RESET_ALL)
    choice = input(Fore.WHITE + "Select [1/2]: " + Style.RESET_ALL).strip().lower()

    if choice in ("2", "plain"):
        return "plain"
    return "fancy"


def prompt_choice(prompt, options):
    """Prompt the user to pick from a list of numbered options."""
    while True:
        print(Fore.CYAN + prompt + Style.RESET_ALL)
        for key, label in options.items():
            print(f"  {key}. {label}")

        choice = input(Fore.YELLOW + "Select an option: " + Style.RESET_ALL).strip().lower()
        if choice in options:
            return choice
        print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


def type_text(text, delay=0.012):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def box(title, lines, colour=Fore.CYAN):
    print(colour + "╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + title.center(WIDTH - 2) + "║")
    print("╠" + "═" * (WIDTH - 2) + "╣")
    for line in lines:
        print("║ " + line.ljust(WIDTH - 4) + " ║")
    print("╚" + "═" * (WIDTH - 2) + "╝" + Style.RESET_ALL)

def header():
    clear()
    print(Fore.CYAN + Style.BRIGHT)
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + "THREE WAYS TO BUILD REAL-TIME SYSTEMS".center(WIDTH - 2) + "║")
    print("║" + "With live demonstrations!".center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝")
    print(Style.RESET_ALL)

def write_file_with_unicode(filename, content):
    """Write a file with proper UTF-8 encoding to handle emojis"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def run_demo_safely(command):
    """Run a demo and handle KeyboardInterrupt gracefully"""
    try:
        # Use subprocess.run with proper signal handling
        if isinstance(command, str):
            command = command.split()
        result = subprocess.run(command, capture_output=False, text=True)
        return result
    except KeyboardInterrupt:
        # User pressed Ctrl+C to stop the demo - this is expected
        print(Fore.YELLOW + "\nDemo stopped by user.")
        return None
    except Exception as e:
        print(Fore.RED + f"Error running demo: {e}")
        return None


def start_background_process(command, label, url=None):
    """Launch a demo process in the background so earlier demos stay alive."""
    try:
        if os.name == "nt":
            proc = subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            proc = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if url:
            webbrowser.open(url)
            print(Fore.GREEN + f"✅ {label} is running in the background.")
            print(Fore.CYAN + f"Open: {url}")
        else:
            print(Fore.GREEN + f"✅ {label} is running in a separate console.")
        return proc
    except Exception as e:
        print(Fore.RED + f"Error starting {label}: {e}")
        return None


def terminate_process(proc):
    """Cleanly stop a background process if it is still running."""
    if proc is None:
        return
    try:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
    except Exception:
        pass

# ============================================================
# LIVE DEMO LAUNCHERS
# ============================================================

def launch_sse_demo():

    """Launch the Flask SSE demo in a separate process and leave it running."""
    print(Fore.GREEN + "\n🔵 Launching SSE IoT Demonstration...")
    print(Fore.CYAN + "The server will stream temperature, humidity, and light data.")
    print(Fore.YELLOW + "Opening browser in 2 seconds...")
    time.sleep(2)

    sse_code = '''from flask import Flask, Response
import time
import random
import json

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SSE IoT Sensor Dashboard</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #1a1a2e; color: #eee; }
            .sensor-card { background: #16213e; padding: 20px; margin: 10px; border-radius: 10px; display: inline-block; min-width: 150px; }
            .value { font-size: 2em; font-weight: bold; }
            .temp { color: #ff6b6b; }
            .humid { color: #4ecdc4; }
            .light { color: #ffe66d; }
            #data { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Live IoT Sensor Dashboard</h1>
        <div id="data">
            <div class="sensor-card"><div class="temp value" id="temp">--</div><div>Temperature (C)</div></div>
            <div class="sensor-card"><div class="humid value" id="humid">--</div><div>Humidity (%)</div></div>
            <div class="sensor-card"><div class="light value" id="light">--</div><div>Light (lux)</div></div>
        </div>
        <div id="history" style="margin-top: 30px;"></div>
        <script>
            const eventSource = new EventSource('/events');
            let count = 0;
            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                document.getElementById('temp').textContent = data.temperature;
                document.getElementById('humid').textContent = data.humidity;
                document.getElementById('light').textContent = data.light;
                count++;
                if (count % 3 === 0) {
                    const history = document.getElementById('history');
                    const entry = document.createElement('div');
                    entry.textContent = `[${new Date().toLocaleTimeString()}] Temp: ${data.temperature}C, Humidity: ${data.humidity}%, Light: ${data.light} lux`;
                    history.prepend(entry);
                    if (history.children.length > 10) {
                        history.removeChild(history.lastChild);
                    }
                }
            };
            eventSource.onerror = function() {
                document.body.innerHTML += '<p style="color: red;">Connection lost. Reloading...</p>';
                setTimeout(() => location.reload(), 3000);
            };
        </script>
    </body>
    </html>
    """

@app.route("/events")
def events():
    def generate():
        while True:
            temperature = round(random.uniform(18, 25), 1)
            humidity = random.randint(40, 70)
            light = random.randint(100, 800)
            data = {"temperature": temperature, "humidity": humidity, "light": light}
            yield f"data: {json.dumps(data)}\\n\\n"
            time.sleep(1)
    return Response(generate(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

    write_file_with_unicode("sse_iot_demo.py", sse_code)

    try:
        process = start_background_process(["python", "sse_iot_demo.py"], "SSE IoT dashboard", "http://localhost:5000")
        print(Fore.CYAN + "The dashboard updates every second with new sensor data.")
        print(Fore.YELLOW + "Press ENTER to continue to the next demo while leaving it running.")
        return process
    except Exception as e:
        print(Fore.RED + f"Error launching SSE demo: {e}")
        return None


def launch_mqtt_demo():
    """Demonstrate MQTT with a simple publisher/subscriber"""
    print(Fore.GREEN + "\n🔵 MQTT Demonstration")
    print(Fore.CYAN + "We'll simulate an MQTT system with a publisher and subscriber.")
    
    # Simple MQTT simulation (no actual broker needed)
    mqtt_code = '''import time
import random
import json

class SimpleMQTTBroker:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
    
    def publish(self, topic, message):
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                callback(message)

# Create broker
broker = SimpleMQTTBroker()

# Create subscribers
def monitor_callback(message):
    data = json.loads(message)
    print(f"[MONITOR] Temp={data['temperature']}C, Humidity={data['humidity']}%")

def logger_callback(message):
    data = json.loads(message)
    print(f"[LOGGER] {data}")

def dashboard_callback(message):
    data = json.loads(message)
    print(f"[DASHBOARD] Light={data['light']} lux")

# Subscribe to topic
broker.subscribe("sensor/data", monitor_callback)
broker.subscribe("sensor/data", logger_callback)
broker.subscribe("sensor/data", dashboard_callback)

print("MQTT System running...")
print("Publishing sensor data every 2 seconds...")
print("Press Ctrl+C to stop\\n")

# Publisher
try:
    while True:
        data = {
            "temperature": round(random.uniform(18, 25), 1),
            "humidity": random.randint(40, 70),
            "light": random.randint(100, 800),
            "timestamp": time.time()
        }
        print(f"[PUBLISHING] {data}")
        broker.publish("sensor/data", json.dumps(data))
        print("-" * 40)
        time.sleep(2)
except KeyboardInterrupt:
    print("\\nMQTT Demo stopped.")
    sys.exit(0)
'''
    
    write_file_with_unicode("mqtt_demo.py", mqtt_code)
    
    print(Fore.YELLOW + "\nRunning MQTT simulation...")
    print(Fore.CYAN + "Watch as one publisher sends data to multiple subscribers.")
    print(Fore.YELLOW + "This demo stays open in its own console so the tutorial can continue.\n")

    process = start_background_process(["python", "mqtt_demo.py"], "MQTT publisher/subscriber demo")
    print(Fore.YELLOW + "Press ENTER to continue to the next demo while leaving MQTT running.")
    return process


def launch_websocket_demo():
    """Launch a WebSocket chat or game demo"""
    print(Fore.GREEN + "\n🔵 WebSocket Demonstration")
    print(Fore.CYAN + "We'll create a simple WebSocket server for real-time communication.")
    
    # WebSocket server code
    websocket_code = '''import sys
import json
import time
import threading

try:
    from websockets.sync.server import serve
except ImportError:
    print("websockets library not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "websockets"])
    from websockets.sync.server import serve

# Simple in-memory game state
game_state = {
    "players": {},
    "messages": []
}

def handle_client(websocket):
    """Handle a client connection"""
    player_id = len(game_state["players"]) + 1
    game_state["players"][player_id] = {"score": 0, "connected": True}
    
    print(f"[Player {player_id} connected]")
    
    try:
        # Send welcome message
        websocket.send(json.dumps({
            "type": "welcome",
            "player_id": player_id,
            "message": f"Welcome Player {player_id}!"
        }))
        
        # Handle messages from client
        while True:
            message = websocket.recv()
            data = json.loads(message)
            
            if data.get("type") == "action":
                # Process game action
                if data.get("action") == "jump":
                    game_state["players"][player_id]["score"] += 10
                    response = {
                        "type": "event",
                        "event": "jump",
                        "player": player_id,
                        "score": game_state["players"][player_id]["score"],
                        "message": f"Player {player_id} jumped! +10 points"
                    }
                elif data.get("action") == "collect":
                    game_state["players"][player_id]["score"] += 25
                    response = {
                        "type": "event",
                        "event": "collect",
                        "player": player_id,
                        "score": game_state["players"][player_id]["score"],
                        "message": f"Player {player_id} collected a gem! +25 points"
                    }
                else:
                    response = {
                        "type": "error",
                        "message": f"Unknown action: {data.get('action')}"
                    }
                
                # Send response
                websocket.send(json.dumps(response))
                print(f"[Sent to Player {player_id}] {response}")
                
    except Exception as e:
        print(f"Player {player_id} disconnected: {e}")
    finally:
        if player_id in game_state["players"]:
            del game_state["players"][player_id]

print("WebSocket server running on ws://localhost:8765")
print("Press Ctrl+C to stop\\n")

# Start the server
try:
    with serve(handle_client, "localhost", 8765) as server:
        server.serve_forever()
except KeyboardInterrupt:
    print("\\nWebSocket server stopped.")
    sys.exit(0)
'''
    
    # WebSocket client code
    client_code = '''import sys
import json
import asyncio

try:
    import websockets
except ImportError:
    print("websockets library not installed.")
    print("Run: pip install websockets")
    sys.exit(1)

async def connect():
    """Connect to the WebSocket server"""
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to game server!")
            
            # Receive welcome message
            response = await websocket.recv()
            data = json.loads(response)
            print(f"[Received] {data['message']}")
            
            # Send some actions
            actions = ["jump", "collect", "jump", "collect", "collect"]
            for action in actions:
                print(f"[Sending action] {action}")
                await websocket.send(json.dumps({"type": "action", "action": action}))
                response = await websocket.recv()
                data = json.loads(response)
                print(f"[Received] {data.get('message', '')}")
                await asyncio.sleep(1)
            
            print("\\n✅ Demo complete! WebSocket allows two-way communication.")
            
    except ConnectionRefusedError:
        print("❌ Connection failed: Make sure the server is running.")
        print("   Run: python websocket_server.py")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(connect())
'''

    write_file_with_unicode("websocket_server.py", websocket_code)
    write_file_with_unicode("websocket_client.py", client_code)
    
    print(Fore.YELLOW + "\nStarting WebSocket server...")
    
    # Start server in background
    try:
        if os.name == "nt":  # Windows
            server_process = subprocess.Popen(["python", "websocket_server.py"],
                                            creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Linux/Mac
            server_process = subprocess.Popen(["python", "websocket_server.py"],
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)
        
        print(Fore.GREEN + "✅ WebSocket server started!")
        print(Fore.CYAN + "Now running the client to demonstrate two-way communication...")
        time.sleep(2)
        
        # Run the client
        try:
            subprocess.run(["python", "websocket_client.py"], capture_output=False)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nClient stopped by user.")
        except Exception as e:
            print(Fore.RED + f"Client error: {e}")
        
        print(Fore.YELLOW + "\n💡 WebSocket allows bidirectional real-time communication!")
        wait_for_enter()
        
        # Clean up - kill the server
        server_process.terminate()
        time.sleep(1)
        if server_process.poll() is None:
            server_process.kill()
            
    except Exception as e:
        print(Fore.RED + f"Error launching WebSocket demo: {e}")
        wait_for_enter()

# ============================================================
# EDUCATIONAL CONTENT
# ============================================================

def mqtt_animation():
    clear()
    header()
    box(
        "1. MQTT - IoT AND EVENT-DRIVEN MESSAGING",
        [
            "MQTT = Message Queuing Telemetry Transport",
            "A lightweight publish/subscribe messaging protocol.",
            "",
            "Think: sensors, devices, games and dashboards.",
            "",
            "KEY IDEA: Publisher -> Broker -> Subscribers"
        ],
        Fore.GREEN
    )
    
    print()
    print("          " + Fore.YELLOW + "PUBLISHER" + Style.RESET_ALL)
    print("              |")
    print("              | MQTT PUBLISH")
    print("              v")
    print("        +---------------+")
    print("        |   MOSQUITTO   |")
    print("        |     BROKER    |")
    print("        +-------+-------+")
    print("                |")
    print("       +--------+--------+")
    print("       v        v        v")
    print("   Monitor   Dashboard  Logger")
    
    print()
    type_text("The publisher does NOT need to know who is listening.", 0.02)
    type_text("The broker receives the message and distributes it to subscribers.", 0.02)
    print()
    print(Fore.CYAN + "✅ Let's see it in action!")
    wait_for_enter()
    
    # Run the MQTT demo
    launch_mqtt_demo()

def sse_animation():
    clear()
    header()
    box(
        "2. SSE - LIVE SERVER-TO-BROWSER UPDATES",
        [
            "SSE = Server-Sent Events",
            "A web technology for streaming events from a server.",
            "The browser keeps an HTTP connection open.",
            "",
            "Think: live dashboards, notifications and feeds.",
            "",
            "KEY IDEA: Server -> Browser (one-way)"
        ],
        Fore.MAGENTA
    )
    
    print()
    print("        +---------------+")
    print("        |  FLASK SERVER |")
    print("        +-------+-------+")
    print("                |")
    print("                | SSE EVENTS")
    print("                v")
    print("        +---------------+")
    print("        |    BROWSER    |")
    print("        +---------------+")
    
    print()
    type_text("The connection can remain open.", 0.025)
    type_text("The server can keep sending events as they happen.", 0.025)
    print()
    print(Fore.CYAN + "✅ Let's run the live IoT dashboard!")
    wait_for_enter()
    
    # Run the SSE demo
    launch_sse_demo()

def websocket_animation():
    clear()
    header()
    box(
        "3. WEBSOCKETS - TWO-WAY REAL-TIME COMMUNICATION",
        [
            "WebSockets provide a persistent two-way connection.",
            "Both the client and server can send messages.",
            "",
            "Think: online games, chat and interactive applications.",
            "",
            "KEY IDEA: Client <-> Server (two-way)"
        ],
        Fore.BLUE
    )
    
    print()
    print("        +---------------+")
    print("        |  PYTHON GAME  |")
    print("        +-------+-------+")
    print("                |")
    print("          WEBSOCKET")
    print("                |")
    print("        +-------+-------+")
    print("        |  GAME SERVER  |")
    print("        +---------------+")
    
    print()
    type_text("The game can send messages to the server.", 0.025)
    type_text("The server can send messages back.", 0.025)
    
    print()
    print(Fore.YELLOW + "For example:")
    print("GAME ---------> Player fired!")
    print("GAME SERVER --> Enemy destroyed!")
    print("GAME ---------> Player answered question")
    print("GAME SERVER --> +500 points")
    
    print()
    print(Fore.CYAN + "✅ Let's try it out!")
    wait_for_enter()
    
    # Run the WebSocket demo
    launch_websocket_demo()

def comparison():
    clear()
    header()
    box(
        "THE THREE COMMUNICATION MODELS",
        [
            "They can all support real-time systems.",
            "But they solve different communication problems."
        ],
        Fore.CYAN
    )
    
    print()
    print(Fore.GREEN + "MQTT")
    print("Publisher -> Broker -> Subscribers")
    print("Best fit: IoT, telemetry and event-driven messaging")
    
    print()
    print(Fore.MAGENTA + "SSE")
    print("Server -> Browser")
    print("Best fit: live server-to-browser updates")
    
    print()
    print(Fore.BLUE + "WebSockets")
    print("Client <-> Server")
    print("Best fit: two-way real-time applications")
    
    print()
    print(Fore.YELLOW + "💡 Remember:")
    print("Real-time does NOT automatically mean MQTT.")
    print("The communication model determines which technology makes sense.")
    
    wait_for_enter()

def security():
    clear()
    header()
    box(
        "CYBER SECURITY: REAL-TIME SYSTEMS NEED PROTECTION",
        [
            "A working connection is not automatically a secure connection.",
            "If a system is exposed to a network, think about security."
        ],
        Fore.RED
    )
    
    print()
    print("For MQTT, consider:")
    print()
    print("  ✓ Authentication")
    print("  ✓ Authorisation")
    print("  ✓ TLS encryption")
    print("  ✓ Access Control Lists (ACLs)")
    print("  ✓ Strong credentials")
    print("  ✓ Least privilege")
    print("  ✓ Input validation")
    print("  ✓ Network/firewall controls")
    print("  ✓ Monitoring and logging")
    
    print()
    print(Fore.YELLOW + "Ask yourself:")
    print("Who can CONNECT?")
    print("Who can PUBLISH?")
    print("Who can SUBSCRIBE?")
    print("What happens if someone sends fake data?")
    
    print()
    print(Fore.RED + "⚠️ Example attack:")
    print("A malicious client publishes:")
    print()
    print('{"player": "Player 1", "score": 9999999}')
    
    print()
    print("Your system should NOT simply trust every message.")
    print(Fore.RED + "Always validate input and implement proper authentication!")
    
    wait_for_enter()

def final_challenge():
    clear()
    header()
    box(
        "YOUR CHALLENGE",
        [
            "You have now seen three different real-time approaches.",
            "Now decide which technology fits each problem."
        ],
        Fore.CYAN
    )
    
    questions = [
        ("A temperature sensor needs to send readings to several applications.",
         "MQTT"),
        ("A browser needs a continuous stream of server updates.",
         "SSE"),
        ("An online game needs continuous two-way communication.",
         "WebSockets"),
        ("You're building a live sports score feed for websites.",
         "SSE"),
        ("Multiple smart home devices need to communicate with a central hub.",
         "MQTT"),
        ("You're building a real-time collaboration tool like Google Docs.",
         "WebSockets"),
    ]
    
    score = 0
    
    for i, (question, answer) in enumerate(questions, 1):
        print()
        print(f"{i}. " + Fore.YELLOW + question)
        choice = input(Fore.WHITE + "Your answer: ").strip().lower()
        
        if answer.lower() in choice:
            print(Fore.GREEN + "✅ Correct!")
            score += 1
        else:
            print(Fore.RED + f"❌ Not quite - a strong answer here is {answer}.")
        time.sleep(0.5)
    
    print()
    print(Fore.CYAN + Style.BRIGHT + f"📊 Score: {score}/{len(questions)}")
    
    if score == len(questions):
        print(Fore.GREEN + "🏆 Excellent! You understand the three communication models perfectly!")
    elif score >= len(questions) - 2:
        print(Fore.GREEN + "👏 Good work! You have a solid understanding.")
    else:
        print(Fore.YELLOW + "💪 Keep experimenting - running the systems yourself will make this clearer.")
    
    wait_for_enter()

def summary():
    clear()
    header()
    print()
    print(Fore.GREEN + Style.BRIGHT + "🎯 MISSION COMPLETE")
    print()
    print("You should now be able to explain:")
    print()
    print("  " + Fore.GREEN + "MQTT" + Fore.WHITE + "       -> IoT and event-driven messaging")
    print("  " + Fore.MAGENTA + "SSE" + Fore.WHITE + "        -> Live server-to-browser updates")
    print("  " + Fore.BLUE + "WebSockets" + Fore.WHITE + " -> Two-way real-time applications")
    print()
    print("And, importantly, you should be thinking about")
    print(Fore.RED + "SECURITY" + Fore.WHITE + " whenever you connect systems together.")
    print()
    print(Fore.CYAN + "🚀 Next steps:")
    print("  1. Build your own IoT sensor dashboard")
    print("  2. Create a multiplayer game with WebSockets")
    print("  3. Connect everything with MQTT")
    print("  4. Always implement security measures!")
    print()


def run_full_tutorial():
    """Run the complete lesson in the original order."""
    mqtt_animation()
    sse_animation()
    websocket_animation()
    comparison()
    security()
    final_challenge()
    summary()


def guided_demo_sequence():
    """Launch each demo in sequence while leaving earlier ones running."""
    running = []

    try:
        clear()
        header()
        print(Fore.CYAN + Style.BRIGHT + "🎓 Guided Demo Flow" + Style.RESET_ALL)
        print(Fore.WHITE + "Each demo stays running while you move forward to the next one.")
        print(Fore.YELLOW + "Use ENTER to continue through the sequence. Type q at any time to stop all running demos.")
        print()

        sse_proc = launch_sse_demo()
        running.append(sse_proc)
        print()
        if input(Fore.YELLOW + "Press ENTER to continue to MQTT... " + Style.RESET_ALL).strip().lower() == "q":
            raise KeyboardInterrupt

        mqtt_proc = launch_mqtt_demo()
        running.append(mqtt_proc)
        print()
        if input(Fore.YELLOW + "Press ENTER to continue to WebSockets... " + Style.RESET_ALL).strip().lower() == "q":
            raise KeyboardInterrupt

        ws_procs = launch_websocket_demo()
        running.extend(ws_procs)

        print()
        print(Fore.GREEN + "✅ All three demos are now running." + Style.RESET_ALL)
        print(Fore.CYAN + "Keep the browser tabs open and move between them freely.")
        print(Fore.YELLOW + "Type q and press ENTER to stop all demos.")

        while True:
            cmd = input(Fore.WHITE + "Your choice: " + Style.RESET_ALL).strip().lower()
            if cmd == "q":
                break
            print(Fore.RED + "Only q exits the guided demo session." + Style.RESET_ALL)

    finally:
        for proc in running:
            terminate_process(proc)

        print(Fore.GREEN + "\nAll demo processes have been stopped." + Style.RESET_ALL)


def plain_interface_menu():
    """A simpler, plain-text version of the lesson menu."""
    while True:
        print("\nReal-Time Systems - Plain Interface")
        print("1. MQTT")
        print("2. SSE")
        print("3. WebSockets")
        print("4. Comparison")
        print("5. Security")
        print("6. Quiz challenge")
        print("7. Run full tutorial")
        print("8. Guided demo sequence")
        print("0. Exit")

        choice = input("Select an option: ").strip().lower()

        if choice == "1":
            mqtt_animation()
        elif choice == "2":
            sse_animation()
        elif choice == "3":
            websocket_animation()
        elif choice == "4":
            comparison()
        elif choice == "5":
            security()
        elif choice == "6":
            final_challenge()
        elif choice == "7":
            run_full_tutorial()
            break
        elif choice == "8":
            guided_demo_sequence()
            break
        elif choice in ("0", "exit", "q"):
            print("Thanks for exploring real-time systems!")
            return
        else:
            print("Invalid choice. Please try again.")

        again = input("Explore another topic? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Returning to plain menu...")
            break

    print("Tutorial session complete. You can run the script again at any time.")


def interactive_menu():
    """Let the student choose a path through the lesson."""
    while True:
        clear()
        header()
        print(Fore.CYAN + Style.BRIGHT + "🎓 Choose your learning path" + Style.RESET_ALL)
        print()
        print(Fore.WHITE + "Pick a topic to explore, or run the full lesson.")
        print(Fore.YELLOW + "Prefer a simpler experience? Use the plain interface option instead." + Style.RESET_ALL)
        print()

        options = {
            "1": "MQTT",
            "2": "SSE",
            "3": "WebSockets",
            "4": "Comparison",
            "5": "Security",
            "6": "Quiz challenge",
            "7": "Run full tutorial",
            "8": "Guided demo sequence",
            "0": "Exit"
        }

        choice = prompt_choice("What would you like to do?", options)

        if choice == "1":
            mqtt_animation()
        elif choice == "2":
            sse_animation()
        elif choice == "3":
            websocket_animation()
        elif choice == "4":
            comparison()
        elif choice == "5":
            security()
        elif choice == "6":
            final_challenge()
        elif choice == "7":
            run_full_tutorial()
            break
        elif choice == "8":
            guided_demo_sequence()
            break
        elif choice == "0":
            print(Fore.YELLOW + "Thanks for exploring real-time systems!" + Style.RESET_ALL)
            return

        next_action = input(Fore.YELLOW + "\nDo you want to explore another topic? (y/n): " + Style.RESET_ALL).strip().lower()
        if next_action not in ("y", "yes"):
            print(Fore.CYAN + "Returning to the main menu..." + Style.RESET_ALL)
            break

    print(Fore.GREEN + "\n🎉 Tutorial session complete!" + Style.RESET_ALL)
    print(Fore.CYAN + "You can run this script again anytime to choose a new path." + Style.RESET_ALL)


def main():
    # Set up signal handler to prevent the whole program from exiting on Ctrl+C
    def signal_handler(sig, frame):
        print(Fore.YELLOW + "\nUse Ctrl+C within the demo to stop it, not here!")
        return
    
    signal.signal(signal.SIGINT, signal_handler)
    
    ui_mode = choose_interface()

    if ui_mode == "plain":
        print("\nPlain interface selected. You can switch back to the fancy interface later if you prefer.")
        print("The project still includes the richer terminal dashboard, but the plain view is available whenever you want it.")
        print()
    else:
        header()
        print(Fore.CYAN + Style.BRIGHT + "🎓 Welcome to Real-Time Systems!")
        print()
        type_text("Today you will explore three ways of building real-time systems.", 0.025)
        type_text("Each technology will be explained and then demonstrated live.", 0.025)
        
        print()
        print(Fore.YELLOW + "📚 You'll learn about:")
        print("  • MQTT - IoT messaging")
        print("  • SSE - Server-sent events")
        print("  • WebSockets - Two-way communication")
        print("  • Security considerations")
        print()
        print("Press ENTER when you're ready to begin.")

        wait_for_enter()

    try:
        if ui_mode == "plain":
            plain_interface_menu()
        else:
            interactive_menu()

        print()
        print(Fore.GREEN + "🎉 You've completed the Real-Time Systems tutorial!")
        print(Fore.CYAN + "All demo files have been created in your current directory:")
        print("  • sse_iot_demo.py - Flask SSE IoT Dashboard")
        print("  • mqtt_demo.py - MQTT Publisher/Subscriber simulation")
        print("  • websocket_server.py & websocket_client.py - WebSocket game")
        print()
        print(Fore.YELLOW + "💡 Run any of these demos again to explore them further!")
        print()

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Tutorial interrupted. Come back anytime to continue learning!")
        sys.exit(0)

if __name__ == "__main__":
    main()