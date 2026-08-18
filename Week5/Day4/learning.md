# websockets

- What WebSockets are
- WebSocket vs HTTP
- WebSocket lifecycle
- WebSocket communication flow
- Multi-client handling
- Building a WebSocket server in Python
- Broadcasting messages

### Definition

> A WebSocket is a communication protocol that provides a persistent, full-duplex connection between a client and server.

| HTTP | WebSocket |
| --- | --- |
| Request-response model | Persistent connection |
| Client sends request | Both sides can send messages |
| Usually independent request/response exchanges | Long-lived connection |
| Great for REST APIs | Great for real-time communication |
| Stateless application style is common | Connection state is commonly maintained |
| Uses `http://` or `https://` | Uses `ws://` or `wss://` |

## WebSocket Lifecycle

1\. Connect

     |

     v

2\. HTTP Upgrade Handshake

     |

     v

3\. Connection Established

     |

     v

4\. Send / Receive Messages

     |

     v

5\. Connection Closed

### Echo Server

An echo server sends back what it receives.