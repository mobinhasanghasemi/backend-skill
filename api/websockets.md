# WebSockets & Real-Time

## Identity
- ID: api.websockets
- Type: technology
- Status: active
- Importance: high

## Purpose
Bidirectional, long-lived connections for live data (chat, dashboards, presence, games). The cost is connection state — choose by actual need, not default fashion.

## When WebSockets win
- server-push latency matters (chat < 1s, trading)
- bidirectional interactive (cursor presence, multiplayer)
When NOT: 
- request/response APIs, periodic polls fine, one-way notifications better via SSE/WebSocket lite or server-sent events!

## Core decisions
1. **Infra**: managed (Pusher/Ably/AWS API GW websockets) vs self-hosted (Django Channels + ASGI, Node + ws). Managed first unless cost/control demands otherwise.
2. **Scaling**: sticky sessions / connection fanout via Redis pub/sub (horizontal), backpressure, reconnect storms
3. **Auth**: token in query/subprotocol at connect (not cookies-only), re-auth on reconnect
4. **Messages**: schema-versioned envelope `{type, version, payload, correlation_id}`; idempotent event ids
5. **Heartbeats**: ping/pong to detect dead connections

## Code tiers

### ❌ Bad
```python
# every user keeps a direct DB-polling interval loop  # N² load, socket leaks, no auth
```

### ✅ Good — Channels with JWT + Redis fanout
```python
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await auth_token(self.scope)       # auth at connect
        await self.channel_layer.group_add(f"room_{room_id}", self.channel_name)
        await self.accept()
    async def chat_message(self, event):          # from Redis pub/sub
        await self.send(json.dumps(event["payload"]))
    async def receive(self, text_data):
        await self.channel_layer.group_send(room_grp, {"type": "chat_message", "payload": validate(text_data)})
```

### ⚡ Better
```python
# per-room presence tracking, heartbeat every 30s, 
# max_connections per user, reconnect token (no full re-login)
# messages: {type, version, payload, id} — dedupe on client
```

### 🏆 Excellent
```text
- channel layer: Redis with pub/sub; auto-scale consumers; backpressure (slow consumer isolation)
- auth: short-lived JWT + user reconnect; server enforces room membership ACL (no leaks!)
- metrics: active conns, message rate/latency, reconnect rate, dead connections
- tests: connect/auth fail, room isolation, burst backpressure, reconnect storm (chaos)
- fallback: SSE or short-poll when CDN/web infra doesn't support WS
```

## Failure modes
- no auth on connect → open sockets for everyone (DoS + data leak)
- no heartbeat → zombie connections consuming memory
- broadcast loops (echo) → message storms
- shared state inside single process → breaks on scale-out (use Redis layer)

## Security
- ACL on every room/entity; validate message size; rate limit messages per user

## Evidence
- WebSocket frames/handshake: SUPPORTED practice (RFC 6455 — pin on next refresh)
