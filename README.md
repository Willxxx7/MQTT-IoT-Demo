# Real-Time Systems Teaching Demo

This project is a classroom demo for exploring the main real-time communication patterns used in modern systems:

- MQTT
- Server-Sent Events (SSE)
- WebSockets
- Security considerations for real-time systems

The main entry point is:

```bash
python real_time_systems_teaching.py
```

It provides a guided teaching flow and launches the live demos for the student.

---

## What this project includes

- MQTT simulation demo
- SSE dashboard demo in the browser
- WebSocket client/server demo
- Interactive teaching flow
- Fancy and plain terminal interface options

---

## Quick start

### 1. Clone or download the project

```bash
git clone <your-github-repo-url>
cd MQTT-IoT-Demo
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the teaching demo

```bash
python real_time_systems_teaching.py
```

Then choose:

- 1 for the fancy interface
- 2 for the plain interface

---

## Demo flow

The main teaching script walks the learner through:

1. MQTT
2. SSE
3. WebSockets
4. Comparison of the three models
5. Security concepts
6. Practice quiz
7. Optional guided demo sequence

The demo is designed so one system can stay running while the learner moves on to the next example.

---

## File overview

```text
MQTT-IoT-Demo/
├── real_time_systems_teaching.py   # Main teaching app
├── mqtt_demo.py                    # MQTT simulation demo
├── sse_iot_demo.py                 # Flask SSE dashboard demo
├── websocket_server.py             # WebSocket server demo
├── websocket_client.py             # WebSocket client demo
├── requirements.txt                # Python dependencies
├── README.md                       # Project instructions
├── .gitignore                      # Ignores local env files
└── .venv/                          # Local virtual environment
```

---

## Notes for students

Students should use the main script to explore the concepts. If they prefer a simpler interface, they can choose the plain terminal view at startup.

---

## Sharing in Teams

To share with students:

1. Push this repo to GitHub
2. Copy the repository URL
3. Post it in Teams with a short message such as:

> Clone this repo and run the main teaching script from the project folder. Use the setup instructions in README.md.

This makes the project easy to update and easy for students to access.

---

## Suggested next steps

- Add a proper MQTT broker using Mosquitto
- Add a screenshot or short demo video for the class channel
- Add a lecture slide deck that aligns with the teaching script
- Tag a stable release such as v1.0 for the class

For example:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

This is a much better representation of an IoT device because one message represents the current state of the device.

---

# 6. Sensor Topic

The sensor publishes to:

```text
sensor/data
```

The important distinction is that:

```text
sensor/data
```

is an MQTT topic.

It is not a physical file or network address.

It is simply a named channel through which MQTT messages are published and received.

---

# 7. sensor.py

The sensor generates simulated readings.

The basic process is:

```text
Generate temperature
        |
Generate humidity
        |
Generate light
        |
        v
Create Python dictionary
        |
        v
Convert dictionary to JSON
        |
        v
MQTT PUBLISH
        |
        v
Mosquitto
```

The important Python code is:

```python
sensor_data = {
    "temperature": temperature,
    "humidity": humidity,
    "light": light
}
```

This creates a Python dictionary.

It is then converted to JSON:

```python
payload = json.dumps(sensor_data)
```

The message is then published:

```python
client.publish(TOPIC, payload)
```

---

# 8. monitor.py

monitor.py is an MQTT subscriber.

It connects to the broker:

```python
client.connect(BROKER, 1883, 60)
```

It then subscribes to:

```python
client.subscribe(TOPIC)
```

where:

```python
TOPIC = "sensor/data"
```

When a message arrives, MQTT calls:

```python
on_message()
```

The message arrives as bytes.

This line converts it into text:

```python
msg.payload.decode()
```

The JSON text is then converted into a Python dictionary:

```python
data = json.loads(msg.payload.decode())
```

The individual values can then be accessed:

```python
temperature = data["temperature"]
humidity = data["humidity"]
light = data["light"]
```

The program can then display:

```text
Temperature: 23.4 °C | Humidity: 61% | Light: 487
```

---

# 9. What Actually Happens When sensor.py Runs?

Suppose sensor.py generates:

```text
Temperature = 23.4
Humidity = 61
Light = 487
```

The Python dictionary becomes:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

sensor.py publishes this message to:

```text
sensor/data
```

Mosquitto receives it.

The broker looks at its list of subscriptions.

If monitor.py has subscribed to:

```text
sensor/data
```

Mosquitto forwards the message to monitor.py.

The complete process is:

```text
sensor.py

temperature = 23.4
humidity = 61
light = 487

        |
        | json.dumps()
        v

{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}

        |
        | MQTT PUBLISH
        v

Mosquitto Broker

        |
        | MQTT SUBSCRIBE
        v

monitor.py

        |
        | json.loads()
        v

Python dictionary

        |
        v

Temperature: 23.4 °C
Humidity: 61%
Light: 487
```

---

# 10. Why Use JSON?

MQTT itself does not require JSON.

MQTT simply transports a payload.

The payload could be:

```text
23.4
```

or:

```text
Hello
```

or:

```text
PLAYER1
```

or:

```json
{
    "temperature": 23.4
}
```

JSON is useful because it allows structured information to be transmitted.

For example:

```json
{
    "player": "Player 1",
    "score": 1250,
    "lives": 3,
    "event": "enemy_destroyed"
}
```

This is much easier for another program to process than an arbitrary text string.

---

# 11. The Retro Game

The really interesting part of this project is that the same MQTT infrastructure can be used by a Python 1980s-style retro game.

The game can contain cyber security questions.

For example:

```text
====================================
       CYBER DEFENDER 1985
====================================

QUESTION:

Which password is strongest?

1. password123
2. 123456
3. Tr0ub4dor!
4. qwerty

Enter your answer:
```

Suppose the player selects option 3.

The game could publish:

```json
{
    "player": "Player 1",
    "event": "cyber_question",
    "question_id": 12,
    "correct": true,
    "score": 500,
    "lives": 3
}
```

The message could be published to:

```text
game/events
```

---

# 12. Game MQTT Topic

The game should use a separate topic from the physical sensor.

For example:

```text
sensor/data
```

for IoT sensor data.

And:

```text
game/events
```

for game events.

This gives us:

```text
sensor/data
```

and:

```text
game/events
```

The broker can handle both.

---

# 13. Example Game Event

When a player answers a cyber security question correctly:

```json
{
    "player": "Player 1",
    "event": "question_answered",
    "question_id": 7,
    "correct": true,
    "score": 500,
    "lives": 3
}
```

The game publishes:

```text
game/events
```

The MQTT broker receives it.

Any subscriber listening to:

```text
game/events
```

receives it.

---

# 14. Example Incorrect Answer

If the player gets a question wrong:

```json
{
    "player": "Player 1",
    "event": "question_answered",
    "question_id": 7,
    "correct": false,
    "score": 250,
    "lives": 2
}
```

The game does not need to tell the scoreboard.

It does not need to tell the dashboard.

It simply publishes the event.

The broker handles the distribution.

---

# 15. Example Enemy Destroyed Event

The game could publish:

```json
{
    "player": "Player 1",
    "event": "enemy_destroyed",
    "enemy": "malware",
    "score": 100,
    "lives": 3
}
```

Topic:

```text
game/events
```

A scoreboard could subscribe to:

```text
game/events
```

and update the score.

A dashboard could also subscribe to:

```text
game/events
```

and display the event.

A logging system could also subscribe.

The game doesn't need to know any of these applications exist.

---

# 16. Example Cyber Security Events

The game could eventually publish events such as:

```text
question_answered
enemy_destroyed
malware_detected
password_cracked
firewall_breached
phishing_blocked
level_completed
player_died
game_started
game_over
```

For example:

```json
{
    "player": "Player 1",
    "event": "malware_detected",
    "malware": "Trojan",
    "correct": true,
    "score": 750
}
```

Or:

```json
{
    "player": "Player 1",
    "event": "firewall_breached",
    "correct": false,
    "score": 1200,
    "lives": 1
}
```

---

# 17. Example Python Code in the Retro Game

The game can use exactly the same MQTT library:

```python
import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
TOPIC = "game/events"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect(BROKER, 1883, 60)
```

A function can then publish a game event:

```python
def publish_game_event(event, player, score, lives, **extra_data):

    data = {
        "player": player,
        "event": event,
        "score": score,
        "lives": lives
    }

    data.update(extra_data)

    payload = json.dumps(data)

    client.publish(TOPIC, payload)
```

The game could then call:

```python
publish_game_event(
    "question_answered",
    "Player 1",
    1250,
    3,
    question_id=7,
    correct=True
)
```

This produces:

```json
{
    "player": "Player 1",
    "event": "question_answered",
    "score": 1250,
    "lives": 3,
    "question_id": 7,
    "correct": true
}
```

and publishes it to:

```text
game/events
```

---

# 18. One Game, Many Subscribers

This is where MQTT becomes particularly powerful.

The architecture could become:

```text
                         RETRO GAME
                             |
                             |
                       MQTT PUBLISH
                             |
                             v
                    +----------------+
                    |                |
                    |   MOSQUITTO    |
                    |     BROKER     |
                    |                |
                    +-------+--------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        SCOREBOARD     DASHBOARD      GAME LOGGER
```

All three applications can subscribe to:

```text
game/events
```

The game only publishes.

It doesn't need to know that three applications are listening.

---

# 19. Combining the IoT System and Game

Eventually the project can combine both types of information.

```text
                     +----------------+
                     | Python Sensor  |
                     +-------+--------+
                             |
                             | sensor/data
                             v
                       +-----------+
                       |           |
                       | Mosquitto |
                       |           |
                       +-----------+
                             ^
                             |
                             | game/events
                             |
                     +-------+--------+
                     |                |
                     |   Retro Game   |
                     |                |
                     | Cyber Security |
                     | Questions      |
                     +----------------+
```

The broker transports both types of messages.

For example:

```text
sensor/data
```

contains:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

while:

```text
game/events
```

contains:

```json
{
    "player": "Player 1",
    "event": "question_answered",
    "correct": true,
    "score": 1250,
    "lives": 3
}
```

MQTT does not need to understand either message.

It simply transports them.

---

# 20. MQTT Topic Hierarchy

As the project becomes larger, topics can be organised hierarchically.

For example:

```text
sensor/data
```

could become:

```text
iot/sensor/data
```

Game messages could become:

```text
game/events
```

or:

```text
game/player1/events
```

or:

```text
game/player1/score
```

or:

```text
game/player1/security
```

This makes the system scalable.

For example:

```text
game/player1/score
game/player2/score
game/player3/score
```

A subscriber could listen to one player:

```text
game/player1/#
```

or potentially listen to all game messages:

```text
game/#
```

The `#` character is an MQTT wildcard.

---

# 21. MQTT Wildcards

MQTT supports wildcards for subscriptions.

For example:

```text
game/#
```

means:

Subscribe to everything underneath `game`.

Therefore:

```text
game/events
game/player1/score
game/player1/security
game/player2/score
```

could all be received.

Another wildcard is:

```text
+
```

which represents one topic level.

For example:

```text
game/+/score
```

could match:

```text
game/player1/score
game/player2/score
game/player3/score
```

but not:

```text
game/player1/security/score
```

This provides a useful teaching opportunity for MQTT topic design.

---

# 22. Why MQTT Is Different From SSE

This project is particularly useful because it can be compared with the previous SSE demonstration.

SSE is essentially:

```text
Server
  |
  | HTTP connection
  |
  v
Browser
```

MQTT is:

```text
Publisher
    |
    v
 Broker
    |
    +------> Subscriber 1
    |
    +------> Subscriber 2
    |
    +------> Subscriber 3
```

SSE is primarily designed for a server pushing events to connected web clients.

MQTT is designed around publish/subscribe messaging.

The publisher and subscriber are decoupled.

That distinction is extremely useful when teaching distributed systems and IoT.

---

# 23. Why JSON Makes the Game Extensible

One of the most useful features of this architecture is that new information can be added to messages without changing MQTT itself.

For example:

```json
{
    "player": "Player 1",
    "event": "enemy_destroyed",
    "enemy": "ransomware",
    "score": 500,
    "lives": 3,
    "level": 4
}
```

Later we could add:

```json
{
    "player": "Player 1",
    "event": "enemy_destroyed",
    "enemy": "ransomware",
    "score": 500,
    "lives": 3,
    "level": 4,
    "difficulty": "hard",
    "time_remaining": 42
}
```

The MQTT broker doesn't need to change.

The transport mechanism remains:

```text
PUBLISH
```

The payload has simply become richer.

---

# 24. Potential Classroom Demonstration

The project could be demonstrated progressively.

## Level 1 – MQTT Basics

Students see:

```text
Publisher → Broker → Subscriber
```

---

## Level 2 – IoT Sensor

Students see:

```text
Temperature
Humidity
Light
```

being published as JSON.

---

## Level 3 – Multiple Subscribers

Students run:

```text
monitor.py
```

and:

```text
dashboard.py
```

at the same time.

Both receive the same sensor messages.

---

## Level 4 – Game Integration

The retro game becomes another MQTT publisher.

For example:

```text
Correct cyber security answer
        |
        v
MQTT PUBLISH
        |
        v
game/events
```

---

## Level 5 – Event-Driven Architecture

The game publishes:

```text
question_answered
enemy_destroyed
level_completed
game_over
```

Other applications react to those events.

---

## Level 6 – Advanced MQTT

Students can investigate:

```text
QoS
Retained Messages
Last Will and Testament
Wildcards
Authentication
Access Control Lists
TLS
MQTT Clients
Topic Design
JSON Payloads
```

---

# 25. Security Considerations

The current demonstration uses:

```text
localhost
port 1883
```

This is deliberately simple for development.

It should not be considered a production-secure MQTT deployment.

A real IoT system should consider:

```text
Authentication
Authorisation
TLS encryption
Access Control Lists
Strong credentials
Certificate management
Network segmentation
Firewall configuration
Secure topic design
Input validation
```

For example, instead of allowing any client to publish to:

```text
game/events
```

a real system could restrict which clients are allowed to publish and subscribe.

This is particularly relevant to the cyber security game.

The game itself can therefore become part of the security demonstration.

---

# 26. Cyber Security Teaching Possibilities

The game could deliberately introduce security concepts as gameplay.

For example:

Password Security:

```text
Which password is strongest?
```

Phishing:

```text
Which email is suspicious?
```

Authentication:

```text
What is multi-factor authentication?
```

Encryption:

```text
Why is HTTPS important?
```

Malware:

```text
Which type of malware encrypts files and demands payment?
```

Social Engineering:

```text
Why should you verify unexpected requests for passwords?
```

Network Security:

```text
What does a firewall do?
```

IoT Security:

```text
Why should IoT devices not use default passwords?
```

The player's answer can become an MQTT event.

---

# 27. Example Cyber Security Question Event

A correct answer could generate:

```json
{
    "player": "Player 1",
    "event": "cyber_question_answered",
    "question_id": 14,
    "category": "password_security",
    "correct": true,
    "score": 500,
    "lives": 3
}
```

An external dashboard could then display:

```text
PLAYER 1

Cyber Security Question
Category: Password Security

Correct Answer!

+500 points

Score: 1250
Lives: 3
```

The dashboard has no direct connection to the game.

It simply receives the MQTT event.

---

# 28. The Game as an IoT Device

An interesting way to explain this to students is that the game can effectively behave like an IoT device.

A physical IoT device might publish:

```text
temperature
humidity
light
```

The game publishes:

```text
score
lives
questions
security events
game state
```

Both use exactly the same basic mechanism:

```text
Create data
     |
     v
Create JSON
     |
     v
MQTT PUBLISH
     |
     v
Mosquitto
     |
     v
Subscribers
```

This demonstrates an important principle:

MQTT is not really about temperature sensors.

It is about messaging between distributed systems.

---

# 29. Complete Proposed Architecture

The finished teaching demonstration could eventually look like this:

```text
                         +----------------------+
                         |                      |
                         |    PYTHON IoT        |
                         |      SENSOR          |
                         |                      |
                         +----------+-----------+
                                    |
                                    | sensor/data
                                    |
                                    v
                         +----------------------+
                         |                      |
                         |     MOSQUITTO        |
                         |       BROKER         |
                         |                      |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             v                      v                      v
       +-----------+          +-----------+          +-----------+
       | monitor   |          | dashboard |          |   other   |
       |   .py     |          |    .py    |          | clients   |
       +-----------+          +-----------+          +-----------+


                         +----------------------+
                         |                      |
                         |   1980s RETRO GAME   |
                         |                      |
                         | Cyber Security       |
                         | Questions            |
                         |                      |
                         +----------+-----------+
                                    |
                                    | game/events
                                    |
                                    v
                         +----------------------+
                         |                      |
                         |     MOSQUITTO        |
                         |       BROKER         |
                         |                      |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             v                      v                      v
       +-----------+          +-----------+          +-----------+
       | Scoreboard|          | dashboard |          |   event   |
       |           |          |           |          |   logger  |
       +-----------+          +-----------+          +-----------+
```

The two systems can coexist because MQTT supports many publishers, topics and subscribers.

---

# 30. The Most Important Concept

The most important thing for students to understand is this:

The game does not send data directly to the dashboard.

The sensor does not send data directly to monitor.py.

The publisher does not need to know who is listening.

Instead:

```text
PUBLISHER
    |
    | message
    v
BROKER
    |
    | forwards message
    v
SUBSCRIBER
```

This is the fundamental MQTT pattern.

---

# 31. Current Implementation

At the current stage the system consists of:

```text
sensor.py
    |
    | PUBLISH sensor/data
    v
Mosquitto
    |
    | SUBSCRIBE sensor/data
    v
monitor.py
```

The sensor publishes:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

The monitor receives and decodes the JSON.

---

# 32. Next Development Stage

The next stage is to add:

```text
dashboard.py
```

so that there are multiple subscribers.

The architecture becomes:

```text
sensor.py
      |
      v
 Mosquitto
      |
      +-----------> monitor.py
      |
      +-----------> dashboard.py
```

After that, the retro game can be introduced:

```text
                    sensor.py
                        |
                        v
                  +-----------+
                  | Mosquitto |
                  +-----------+
                        ^
                        |
                    retro_game.py
```

Then the game can publish:

```text
game/events
```

containing cyber security events.

---

# 33. Final Learning Model

The complete project can therefore teach the progression:

```text
Python
  ↓
JSON
  ↓
MQTT
  ↓
Publisher
  ↓
Broker
  ↓
Subscriber
  ↓
Multiple Subscribers
  ↓
Event-Driven Architecture
  ↓
IoT
  ↓
Cyber Security
  ↓
Distributed Systems
  ↓
MQTT Security
```

The particularly useful aspect of the project is that the same underlying technology is being reused for both physical-style IoT data and game events.

The sensor might say:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

while the game might say:

```json
{
    "player": "Player 1",
    "event": "cyber_question_answered",
    "correct": true,
    "score": 1250,
    "lives": 3
}
```

To MQTT, both are simply messages.

That is the core concept this demonstration is designed to teach.
