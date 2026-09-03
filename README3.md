
# Practical Learning Outcomes

By the end of this project, you should be able to demonstrate the following practical skills.

## 1. Build and run an MQTT system

You should be able to:

• Install and configure an MQTT broker such as Mosquitto.

• Start and stop the broker.

• Connect a Python application to the broker.

• Explain the role of the MQTT broker within the system.

You should be able to demonstrate:

```text
Python Application
        |
        | MQTT
        v
    Mosquitto
```

---

## 2. Create an MQTT Publisher

You should be able to write a Python program that publishes messages using MQTT.

For example:

```text
sensor.py
```

should be capable of publishing sensor information such as:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

You should understand:

```text
MQTT client
Broker address
Port
Topic
Payload
Publish
```

---

## 3. Create an MQTT Subscriber

You should be able to create a Python application that subscribes to an MQTT topic.

For example:

```text
monitor.py
```

could subscribe to:

```text
sensor/data
```

and display:

```text
Temperature: 23.4 °C
Humidity: 61%
Light: 487
```

You should understand how a subscriber receives messages without directly communicating with the publisher.

---

## 4. Use JSON to Structure Data

You should be able to create and process structured JSON data.

For example:

```json
{
    "temperature": 23.4,
    "humidity": 61,
    "light": 487
}
```

You should be able to:

• Create JSON data.

• Convert Python data into JSON.

• Publish JSON through MQTT.

• Receive JSON through MQTT.

• Decode JSON back into Python data.

• Validate that expected fields exist.

---

## 5. Understand MQTT Topics

You should be able to create an appropriate topic structure.

For example:

```text
sensor/data

game/events

game/player1/score

game/player1/security
```

You should understand why topics are used to organise messages.

You should also be able to use MQTT wildcards such as:

```text
#
+
```

For example:

```text
game/#
```

and:

```text
game/+/score
```

---

## 6. Build Multiple Subscribers

You should be able to demonstrate that one publisher can communicate with multiple subscribers.

For example:

```text
                    Mosquitto
                       Broker
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Monitor       Dashboard        Logger
```

You should understand that the publisher does not need to know which subscribers exist.

This demonstrates decoupling.

---

## 7. Build an Event-Driven Application

You should be able to identify events occurring within an application.

For example:

```text
Player answers question
        |
        v
Correct answer
        |
        v
Score increases
        |
        v
MQTT event published
```

You should understand the difference between an application repeatedly asking:

```text
"Has anything happened?"
```

and an event-driven application reacting when something happens.

---

## 8. Connect a Python Game to MQTT

You should be able to use MQTT within a Python game.

For example, when a player answers a cyber-security question, the game could publish:

```json
{
    "player": "Player 1",
    "event": "security_question",
    "correct": true,
    "score": 500,
    "lives": 3
}
```

The game therefore becomes an MQTT publisher.

---

## 9. Design a Game Event System

You should be able to identify different events within a game.

For example:

```text
game/player1/joined

game/player1/score

game/player1/lost_life

game/player1/security_question

game/player1/game_over
```

You should be able to decide which information belongs in each event.

---

## 10. Build a Real-Time Scoreboard or Dashboard

You should be able to create a second application that subscribes to game events.

For example:

```text
Retro Game
     |
     | game/events
     v
Mosquitto
     |
     v
Scoreboard
```

The scoreboard could display:

```text
PLAYER 1

Score: 2500
Lives: 2

Cyber Questions:
Correct: 8
Incorrect: 2
```

The scoreboard should update when new MQTT messages arrive.

---

## 11. Understand Different Communication Models

You should be able to explain the difference between:

```text
MQTT
SSE
WebSockets
REST/HTTP
AMQP
NATS
Kafka
Redis Pub/Sub
CoAP
```

You should be able to identify whether a technology uses:

```text
Request/response

Server → client

Client ↔ server

Publish/subscribe

Message queues

Event streams
```

You should also be able to explain why one technology might be more appropriate than another for a particular problem.

---

# 12. Understand Authentication

You should understand that a networked system needs to establish:

```text
WHO are you?
```

You should be able to configure or describe MQTT authentication using credentials.

You should understand why the following is insecure:

```text
Anonymous MQTT access
```

and why a production system should normally require authenticated clients.

---

# 13. Understand Authorisation

You should understand the difference between:

```text
Authentication
```

and:

```text
Authorisation
```

You should be able to explain:

```text
Authentication:
"Who are you?"

Authorisation:
"What are you allowed to do?"
```

For example:

```text
Sensor

CAN:
publish sensor/data

CANNOT:
publish game/events
```

You should understand the principle of least privilege.

---

# 14. Secure MQTT Topics

You should be able to consider security when designing MQTT topics.

For example:

```text
sensor/data
game/events
game/player1/score
```

You should ask:

```text
Who can publish?

Who can subscribe?

Should this information be public?

Could someone manipulate the data?

Could someone obtain information they shouldn't see?
```

This introduces access control lists and topic-based permissions.

---

# 15. Understand Encryption and TLS

You should understand why authentication alone is not sufficient.

You should be able to explain the purpose of TLS.

For example:

```text
Game
  |
  | encrypted MQTT
  v
Broker
```

You should understand that encryption helps protect information while it travels across a network.

You should also recognise the difference between:

```text
Authentication
Authorisation
Encryption
```

These solve different security problems.

---

# 16. Protect Credentials

You should understand why credentials should not be hard-coded into source code.

Avoid:

```python
USERNAME = "admin"
PASSWORD = "password123"
```

particularly in software that is going to be shared or uploaded to GitHub.

You should understand approaches such as:

```text
Environment variables
Configuration files
Secret stores
Protected deployment settings
```

You should also understand why real credentials should never be committed to a public repository.

---

# 17. Validate Incoming Data

You should understand that data received from another system should not automatically be trusted.

For example, a subscriber might receive:

```json
{
    "temperature": "HELLO"
}
```

or:

```json
{
    "score": 999999999
}
```

Your program should consider:

```text
Is this valid JSON?

Are the required fields present?

Are the values the correct type?

Are the values within sensible limits?

Is the message from an authorised source?

Is the event type recognised?
```

---

# 18. Investigate MQTT Security

You should be able to investigate what happens when security controls are missing.

For example:

```text
Can an unauthenticated client connect?

Can an unauthorised client publish?

Can an unauthorised client subscribe?

Can a fake score be injected?

Can one player see another player's information?

What happens when incorrect credentials are supplied?

What happens when invalid JSON is received?
```

This should be performed in a controlled learning environment.

The objective is to understand the security weakness and then implement an appropriate defence.

---

# 19. Understand QoS

You should understand the purpose of MQTT Quality of Service.

You should be able to describe:

```text
QoS 0
QoS 1
QoS 2
```

and understand that MQTT delivery reliability is different from security.

For example:

```text
QoS ≠ Encryption

QoS ≠ Authentication

QoS ≠ Authorisation
```

---

# 20. Understand Retained Messages

You should understand the concept of an MQTT retained message.

You should be able to explain why a newly connected subscriber might receive the most recently retained value.

You should also be able to consider the security implications:

```text
What information is being retained?

Who can retrieve it?

Could the retained information contain sensitive data?
```

---

# 21. Compare Local and Networked MQTT

Initially you will probably use:

```text
localhost
```

For example:

```text
Python
   |
   v
localhost
   |
   v
Mosquitto
```

You should understand that a real IoT system might instead look like:

```text
IoT Device
    |
    | Network / Internet
    v
MQTT Broker
    |
    +----> Dashboard
    +----> Database
    +----> Monitoring
```

You should understand why exposing an MQTT broker to a network introduces additional security requirements.

---

# 22. Troubleshoot an MQTT System

You should be able to investigate common problems.

For example:

```text
Broker isn't running

Wrong broker address

Wrong port

Incorrect topic

Publisher isn't connected

Subscriber isn't connected

Invalid JSON

Incorrect credentials

Permission denied

Firewall blocking communication
```

You should develop a systematic troubleshooting process rather than simply changing random settings.

---

# 23. Explain the Complete System

At the end of the project, you should be able to explain the complete communication flow:

```text
Python Sensor
      |
      | MQTT PUBLISH
      v
Mosquitto Broker
      |
      | MQTT
      +----------> Monitor
      |
      +----------> Dashboard
      |
      +----------> Logger
```

and the game:

```text
Python Retro Game
      |
      | MQTT PUBLISH
      v
Mosquitto Broker
      |
      +----------> Scoreboard
      |
      +----------> Dashboard
      |
      +----------> Event Logger
```

You should be able to explain what each component does and why it exists.

---

# 24. Design a Secure Version

You should then be able to propose improvements to the architecture.

For example:

```text
                    Internet
                       |
                    Firewall
                       |
                       v
                +-------------+
                |  Mosquitto  |
                |    Broker   |
                |             |
                |    TLS      |
                |    Auth     |
                |    ACLs     |
                +------+------+
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Sensor        Game       Dashboard
          |            |            |
       limited       limited      limited
       access        access       access
```

You should be able to explain why each security control has been introduced.

---

# 25. Apply Cyber-Security Knowledge to the Game

The game should not merely ask questions about cyber security.

The architecture itself should demonstrate cyber-security principles.

For example:

```text
Game
 |
 | authenticated MQTT connection
 |
 v
Broker
 |
 | authorisation
 |
 v
Dashboard
```

The game can teach:

```text
Passwords
Phishing
Malware
Encryption
Authentication
Authorisation
MFA
Firewalls
Social engineering
Network security
```

while the underlying MQTT system demonstrates:

```text
Authentication
Authorisation
Encryption
Access control
Input validation
Least privilege
Monitoring
```

---

# 26. Higher-Level Learning Outcome

By completing the project, you should be able to look at a system and ask:

```text
What information needs to be communicated?

Who produces the information?

Who needs to receive it?

Does the communication need to be real-time?

Is it request/response or publish/subscribe?

Does the system need a broker?

How should messages be structured?

How should the system be secured?

Who is allowed to publish?

Who is allowed to subscribe?

How will data be validated?

What happens if a component fails?
```

These questions are more important than simply memorising MQTT commands.

---

# 27. Final Practical Challenge

Your final system should aim to demonstrate:

```text
                PYTHON IoT SENSOR
                       |
                       | MQTT
                       v
                +-------------+
                |             |
                |  MOSQUITTO  |
                |    BROKER   |
                |             |
                +------+------+
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Monitor     Dashboard      Logger


                PYTHON RETRO GAME
                       |
                       | MQTT
                       v
                +-------------+
                |             |
                |  MOSQUITTO  |
                |    BROKER   |
                |             |
                +------+------+
                       |
          +------------+------------+
          |            |            |
          v            v            v
     Scoreboard    Dashboard      Logger
```

And the secure version should introduce:

```text
Authentication
       +
Authorisation
       +
TLS
       +
Access Control
       +
Least Privilege
       +
Input Validation
       +
Secure Credential Management
       +
Monitoring
```

The final goal is therefore not simply:

"I made an MQTT program."

The goal is:

"I can design, build, explain, test and secure a small distributed IoT and event-driven system."

That is a much more valuable computing skill.
