# Freelance Marketplace MVP (independent learning project)

An original freelance marketplace starter inspired by common marketplace workflows. It does **not** use Upwork branding, proprietary assets, private APIs, or scraped private data. Publicly observable product behavior can inform requirements; implementation and UI should remain your own.

## Architecture
- `identity`: registration, login, refresh tokens, client/freelancer roles.
- `profiles`: freelancer/client profiles and portfolio items.
- `marketplace`: jobs, proposals, contracts/hiring.
- `chat`: persisted conversations/messages and JWT-authenticated WebSockets.
- Each service owns its PostgreSQL database. External user IDs are UUIDs; no cross-database foreign keys.
- Services share a JWT signing secret for this local MVP. This is convenient for local validation but should be replaced by asymmetric signing/JWKS or a dedicated identity validation strategy in production.

## Prerequisites
Docker Engine and Docker Compose v2.

## Start locally
1. Copy `.env.example` to `.env` and change secrets before exposing anything beyond localhost.
2. Run `docker compose up --build`. This starts services and runs migrations on startup. First startup may take a few minutes.
3. Frontend: http://localhost:5173. APIs: identity `http://localhost:8001`, profiles `:8002`, marketplace `:8003`, chat `:8004`. Swagger docs are available at each service's `/api/docs/`.
4. Register a client or freelancer in the UI. To create an admin, run for example:
   `docker compose exec identity python manage.py createsuperuser`

The frontend is a deliberately small functional starter, not a finished commercial UI. Hiring creates a contract and the frontend then creates a conversation for the hired participants. These are two separate service requests, so production implementations should add retries or an outbox/event workflow to handle partial failures. Use API endpoints and Swagger for workflows not yet surfaced in the interface.

## Deploy on a server with public IP 44.226.114.3

1. Copy `.env.example` to `.env` and set `PUBLIC_IP=44.226.114.3` and `BIND_IP=0.0.0.0`. Change all example secrets and the PostgreSQL password before starting.
2. Allow inbound TCP ports `5173`, `8001`, `8002`, `8003`, and `8004` in the cloud firewall/security group and the host firewall for a quick MVP test. Do **not** open PostgreSQL (5432) or Redis (6379). Restrict source IPs to your own IP while testing if possible.
3. Run `docker compose up --build -d`. The frontend uses the public IP for API and WebSocket URLs.
4. Visit `http://44.226.114.3:5173`. APIs are exposed on ports 8001–8004.
5. Verify the Compose configuration with `docker compose config` and inspect logs with `docker compose logs -f`.

This direct-port setup is for development/demo only: API traffic and WebSockets are unencrypted. Before production, put Nginx or another reverse proxy in front, expose only ports 80/443, configure a domain and TLS, route REST/WebSocket traffic through the proxy, and remove public host port mappings from the Django services. `PUBLIC_IP` controls the URLs embedded into the frontend; `BIND_IP` controls the local host interfaces used for Docker port publishing. On cloud VMs where the public IP is NAT-mapped, keep `BIND_IP=0.0.0.0` and `PUBLIC_IP=44.226.114.3`.

## Main API routes
- Identity: `POST /api/auth/register/`, `POST /api/auth/token/`, `POST /api/auth/token/refresh/`, `GET /api/me/`
- Profiles: `GET/PUT /api/profiles/me/`, `GET /api/profiles/<uuid>/`, `GET/POST /api/portfolio/`
- Marketplace: `GET/POST /api/jobs/`, `GET/PATCH /api/jobs/<uuid>/`, `GET/POST /api/proposals/`, `POST /api/proposals/<uuid>/hire/`
- Chat: `GET/POST /api/conversations/`, `GET /api/conversations/<uuid>/messages/`, WebSocket `/ws/chat/<conversation_uuid>/?token=<access_token>`

## Local security notes
- All passwords use Django password hashing.
- JWT access tokens expire quickly; refresh tokens rotate and blacklist old refresh tokens.
- Role checks and ownership checks are enforced server-side.
- WebSocket connections require a valid access token and conversation membership. Sender identity comes from the token, never from the message payload.
- Internal-service authentication uses `INTERNAL_SERVICE_TOKEN` for service-to-service calls; keep it server-side. This starter keeps cross-service calls minimal and validates external IDs at request boundaries.
- CORS is restricted to the local Vite origin by default. Set `CORS_ALLOWED_ORIGINS` explicitly for deployment.
- Do not use `.env.example` secrets in production. Add TLS, secure cookies or a carefully designed token storage strategy, rate limits, audit logs, backups, monitoring, secret management, and a production ASGI server configuration before deployment.

## Migrations and checks
Each service runs `python manage.py makemigrations core` and `python manage.py migrate` when its container starts in this starter. Before production, commit generated migration files to version control and remove runtime migration generation; run `python manage.py makemigrations --check --dry-run` in CI. To run tests: `docker compose exec <service> python manage.py test`. To inspect Compose configuration: `docker compose config`.

## Product discovery / reverse engineering ethics
Use a browser to manually observe public pages and your own account's permitted workflows. Record user goals, states, validation, navigation, and edge cases. Do not automate access in violation of site terms, bypass authentication/anti-bot controls, copy source/assets, or collect personal data. The actual internal architecture of a third-party platform cannot be inferred reliably from its UI.

### Cross-service JWT identity

The Identity service owns the UUID user model and issues signed JWTs containing
`user_id`, `role`, and `email`. Profiles, Marketplace, and Chat validate the JWT
signature with the same `JWT_SIGNING_KEY` but do not look up that UUID in their
own Django auth tables. They use `core.authentication.IdentityJWTAuthentication`
to expose a lightweight authenticated principal. Configure the exact same strong
`JWT_SIGNING_KEY` in all four services. Do not use the example development key in
production. This design assumes all services trust the Identity service's signing
key; for stronger isolation, consider asymmetric signing and publish only the
Identity service's public verification key to downstream services.
