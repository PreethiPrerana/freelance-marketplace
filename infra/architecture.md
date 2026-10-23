# Architecture and trust boundaries

```text
React/Vite -> Identity (JWT)
           -> Profiles (profile data; external user UUID)
           -> Marketplace (jobs/proposals/contracts; external user UUID)
           -> Chat (conversation/message data; external user UUID)

Identity DB | Profiles DB | Marketplace DB | Chat DB (independent PostgreSQL instances)
Chat -> Redis channel layer -> authenticated WebSocket groups
```

The MVP validates access tokens locally using a shared signing key, so downstream services do not need a synchronous identity call on every request. This is not the same as a fully isolated internal service-authentication scheme. For production, use asymmetric JWT signing and publish a JWKS endpoint, validate issuer/audience, rotate keys, and use service credentials/mTLS for privileged service-to-service requests. Keep user-facing authorization separate from service authentication.
