+++
id = "technologies/docker"
title = "Docker Best Practices"
agents = ["all"]
technologies = ["docker", "containerization"]
category = "rule"
tags = ["docker", "containers", "devops", "security", "images"]
version = 1
+++

### Dockerfile Best Practices

- Use multi-stage builds to separate build dependencies from the final runtime image — keep the final stage minimal with only the compiled artifact and runtime deps.
- Order Dockerfile instructions from least-frequently changed to most-frequently changed — `COPY package.json` and `RUN npm install` before `COPY . .` so dependency layers are cached.
- Create a `.dockerignore` file in every project with a Dockerfile — exclude `.git/`, `node_modules/`, `__pycache__/`, `*.env`, build artifacts, and test files.
- Run the application as a non-root user — add `RUN addgroup --system app && adduser --system --ingroup app app` and `USER app` before `CMD`.
- Use `COPY` instead of `ADD` unless you specifically need tar extraction or URL fetching — `COPY` is explicit and predictable.
- Pin base image tags to specific versions (`python:3.12.4-slim`, not `python:latest`) — `:latest` causes non-reproducible builds and silent breakage.
- Combine related `RUN` commands with `&&` and `\` line continuations to minimize layers — e.g., `RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`.
- Lint Dockerfiles with `hadolint` in CI — it catches common anti-patterns like missing `--no-install-recommends`, pinning issues, and `COPY --chown` misuse.
- Set `WORKDIR` explicitly instead of relying on `RUN cd /path` — `WORKDIR` persists across layers and is self-documenting.
- Use `ARG` for build-time variables (versions, build flags) and `ENV` only for runtime configuration — don't leak build secrets via `ENV`.

### Image Security

- Scan images with `trivy image` or `grype` in CI before pushing to a registry — fail the pipeline on CRITICAL or HIGH vulnerabilities.
- Use minimal base images: prefer `distroless` for production (no shell, no package manager) or `alpine` when a shell is needed — full `ubuntu`/`debian` images carry hundreds of unnecessary packages.
- Never embed secrets (API keys, passwords, tokens) in image layers — secrets baked into `RUN`, `COPY`, or `ENV` persist in the image history even if deleted in a later layer.
- Use `--mount=type=secret` with BuildKit for build-time secrets (e.g., private registry tokens, SSH keys) — the secret is not persisted in any layer.
- Drop all Linux capabilities and add back only what's needed — run containers with `--cap-drop=ALL --cap-add=NET_BIND_SERVICE` or equivalent in Compose/Kubernetes.
- Set `--read-only` on the container filesystem where possible — use tmpfs mounts for directories that need write access (`/tmp`, `/var/run`).
- Run image vulnerability scans on a schedule (not just at build time) — new CVEs appear daily against already-deployed images.

### Compose Patterns

- Define service dependencies with `depends_on` plus a `condition: service_healthy` and a real healthcheck — bare `depends_on` only waits for the container to start, not for the service to be ready.
- Use named volumes for persistent data (`volumes: db_data:`) — anonymous volumes are hard to identify, back up, or reuse.
- Isolate services on separate networks — put the database on an internal network that only the backend can reach; do not expose it to the frontend or the host.
- Use `env_file` to load environment variables from a `.env` file instead of inline `environment:` blocks — keeps secrets out of `docker-compose.yml` and simplifies per-environment overrides.
- Use Compose profiles (`profiles: [debug]`) to group optional services (profiler, mailhog, adminer) that should only start when explicitly requested with `--profile debug`.
- Set `restart: unless-stopped` for production services and `restart: "no"` for one-shot tasks and migration containers.
- Pin service image tags in `docker-compose.yml` the same way as in Dockerfiles — never use `:latest` in Compose files checked into version control.

### Runtime

- Set memory limits on every container (`--memory=512m` or Compose `mem_limit`) — an unbounded container can OOM-kill the host.
- Set CPU limits (`--cpus=1.0` or Compose `cpus`) to prevent a single container from starving others on the same host.
- Define `HEALTHCHECK` in the Dockerfile or Compose file — use a lightweight probe (e.g., `curl -f http://localhost:8080/health || exit 1`) with appropriate `interval`, `timeout`, and `retries`.
- Use a PID 1 init process (`--init` flag, `tini`, or `dumb-init`) — the default entrypoint does not reap zombie processes or forward signals correctly.
- Configure a logging driver (`json-file` with `max-size` and `max-file`, or `journald`, or a centralized driver) — unbounded `json-file` logs fill the disk.
- Set `stop_grace_period` (Compose) or `--stop-timeout` (CLI) to give the application time to drain connections before SIGKILL — default 10s is often too short for long-lived requests.

### Development

- Use bind mounts (`volumes: - ./src:/app/src`) for source code during development — changes on the host are reflected immediately in the container without rebuilding.
- Configure hot reloading inside the dev container (e.g., `--reload` flag for uvicorn/gunicorn, `nodemon` for Node.js) so file changes trigger automatic restarts.
- Maintain separate Dockerfiles or build stages for development and production — the dev image can include debuggers, test tools, and a shell; the prod image should not.
- Enable BuildKit (`DOCKER_BUILDKIT=1` or set in `daemon.json`) for faster builds, better caching, secret mounts, and parallel stage execution.
- Use `docker compose watch` (Compose v2.22+) for automatic sync+restart — it replaces manual bind mount configurations with declarative file-watch rules.
- Cache package manager downloads in a named volume or BuildKit cache mount (`--mount=type=cache,target=/root/.cache/pip`) to avoid re-downloading dependencies on every build.

### Registry and Tagging

- Tag images with both a semantic version and the git commit SHA — e.g., `myapp:1.2.3` and `myapp:sha-a1b2c3d`; this allows rollback to any exact commit.
- Build multi-architecture images with `docker buildx build --platform linux/amd64,linux/arm64` — ensures the same image works on x86 servers and ARM-based environments (Apple Silicon, Graviton).
- Sign images with `cosign` or Docker Content Trust before pushing to a registry — verify signatures in your deployment pipeline to prevent tampered images.
- Set up automated image cleanup in the registry (retention policies by age and tag count) — stale images consume storage and increase scan surface.
