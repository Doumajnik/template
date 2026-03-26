+++
id = "technologies/kubernetes"
title = "Kubernetes Best Practices"
agents = ["all"]
technologies = ["kubernetes", "k8s", "helm"]
category = "rule"
tags = ["kubernetes", "k8s", "orchestration", "devops", "deployment"]
version = 1
+++

### Pod Design

- Run one process per container — sidecar containers are fine, but do not pack multiple application processes into a single container; it breaks independent scaling, logging, and lifecycle management.
- Set both `resources.requests` and `resources.limits` on every container — requests ensure scheduling; limits prevent a single pod from consuming all node resources.
- Configure a `readinessProbe` to gate traffic — the pod only receives Service traffic after the readiness probe passes; use an HTTP endpoint (e.g., `/healthz`) or TCP check.
- Configure a `livenessProbe` to restart stuck processes — set `initialDelaySeconds` high enough to avoid killing slow-starting apps; a failing liveness probe triggers a container restart.
- Add a `startupProbe` for applications with long initialization — it disables liveness/readiness checks until the app is ready, preventing premature kills during startup.
- Handle `SIGTERM` gracefully in your application — Kubernetes sends SIGTERM on pod termination; drain in-flight requests, close database connections, and exit cleanly within `terminationGracePeriodSeconds`.
- Use a `preStop` lifecycle hook (e.g., `sleep 5`) to allow the endpoints controller to deregister the pod from the Service before the app starts shutting down — this prevents traffic being routed to a terminating pod.
### Deployments

- Use `RollingUpdate` strategy with `maxUnavailable: 0` for zero-downtime deploys — this ensures at least the desired replica count is always available during rollouts.
- Define a `PodDisruptionBudget` (PDB) for every production workload — set `minAvailable` or `maxUnavailable` to prevent voluntary disruptions (node drains, cluster upgrades) from killing all replicas.
- Use `HorizontalPodAutoscaler` (HPA) based on CPU, memory, or custom metrics — set `minReplicas` ≥ 2 for HA and configure `behavior.scaleDown.stabilizationWindowSeconds` to avoid flapping.
- Use `topologySpreadConstraints` to distribute pods across zones and nodes — set `maxSkew: 1` with `whenUnsatisfiable: DoNotSchedule` for even distribution.
- Apply pod anti-affinity rules for high-availability workloads — `preferredDuringSchedulingIgnoredDuringExecution` with `topologyKey: kubernetes.io/hostname` spreads replicas across nodes.
- Set `revisionHistoryLimit` to a reasonable value (3–5) — keeping too many old ReplicaSets wastes etcd storage; keeping too few limits rollback options.

### Configuration

- Use `ConfigMap` for non-sensitive configuration (feature flags, URLs, tuning parameters) — mount as environment variables or volume files; prefer volume mounts for config files that need hot-reload.
- Use `Secret` for credentials, API keys, and certificates — never store secrets in ConfigMaps, environment variables in pod specs, or baked into container images.
- Consider `external-secrets-operator` or `sealed-secrets` to sync secrets from an external vault (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) — avoid storing raw secrets in Git.
- Reference ConfigMap and Secret values via `envFrom` or `valueFrom` in the pod spec rather than duplicating values across deployments — a single ConfigMap update propagates to all consumers.
- Mark ConfigMaps and Secrets as `immutable: true` when they should not change after creation — immutable objects reduce API server load and prevent accidental mutation.

### Networking

- Apply a default-deny `NetworkPolicy` on every namespace (`ingress: []`, `egress: []`) and then explicitly allow required traffic — this enforces zero-trust networking between services.
- Use `ClusterIP` as the default Service type for internal communication — expose via `LoadBalancer` or `Ingress` only when external access is needed.
- Use an Ingress controller (nginx, traefik, or cloud-native) with path-based or host-based routing rather than creating one LoadBalancer per service — reduces cost and IP exhaustion.
- Automate TLS certificate provisioning with `cert-manager` and Let's Encrypt — annotate Ingress resources with `cert-manager.io/cluster-issuer` to auto-issue and renew certificates.
### Storage

- Use `PersistentVolumeClaim` (PVC) for any data that must survive pod restarts — ephemeral storage (`emptyDir`) is lost when the pod is evicted or rescheduled.
- Define `StorageClass` resources with appropriate `reclaimPolicy` — use `Retain` for production databases (prevents accidental data loss) and `Delete` for ephemeral test workloads.
- Use `StatefulSet` for stateful workloads (databases, message brokers) that need stable network identities and ordered, persistent storage — one PVC per replica via `volumeClaimTemplates`.
- Implement backup strategies for PVCs: use CSI volume snapshots (`VolumeSnapshot`) or application-level backups (pg_dump, mongodump) on a schedule — PVCs alone are not a backup.

### Security

- Enforce Pod Security Standards at the namespace level using `pod-security.kubernetes.io/enforce: restricted` — the `restricted` profile blocks privilege escalation, host namespaces, and dangerous capabilities.
- Create a dedicated `ServiceAccount` per workload and set `automountServiceAccountToken: false` on pods that don't need Kubernetes API access — never use the `default` ServiceAccount.
- Apply RBAC with least privilege — bind Roles (not ClusterRoles) scoped to the minimum required namespace, resources, and verbs; audit with `kubectl auth can-i --list`.
- Set `securityContext.runAsNonRoot: true` and `securityContext.readOnlyRootFilesystem: true` on every container — use `emptyDir` or tmpfs mounts for directories that need writes.
- Disable privilege escalation with `allowPrivilegeEscalation: false` and drop all capabilities with `capabilities: { drop: ["ALL"] }` — add back only specific capabilities if absolutely required.

### Observability

- Expose a `/metrics` endpoint in Prometheus format from every service — use client libraries (`prometheus_client` for Python, `prom-client` for Node.js) and scrape with `ServiceMonitor` or pod annotations.
- Emit structured logs as JSON to stdout — use a log aggregator (Fluentd, Fluent Bit, or a cloud logging agent) to collect, parse, and index; never write logs to files inside the container.
- Instrument services with distributed tracing (OpenTelemetry) — propagate trace context headers (`traceparent`) across service boundaries for end-to-end request visibility.
- Monitor Kubernetes events (`kubectl get events --watch`) and set up alerts for `OOMKilled`, `CrashLoopBackOff`, `FailedScheduling`, and `Evicted` — these indicate systemic issues.
### Helm

- Version Helm charts independently from the application — use semantic versioning in `Chart.yaml` (`version` for chart, `appVersion` for the app) and maintain a changelog.
- Structure `values.yaml` with clear top-level keys per component (e.g., `api:`, `worker:`, `redis:`) — document every value with inline comments and provide sensible defaults.
- Use Helm hooks (`pre-install`, `post-upgrade`) for database migrations and one-time setup tasks — set `helm.sh/hook-delete-policy: before-hook-creation` to clean up old hook pods.
- Use `{{- if .Values.feature.enabled }}` conditionals to make resources optional — don't deploy monitoring sidecars or debug tools in production unless explicitly enabled.
- Test charts with `helm lint`, `helm template` (renders locally without a cluster), and `helm test` (in-cluster test pods) in CI before merging — catch template errors and misconfigurations early.
