---
name: infrastructure-as-code
description: "Full workflow for designing, writing, and auditing Infrastructure as Code. Covers Terraform, Pulumi, CloudFormation, and Ansible. Use when provisioning cloud resources, managing infrastructure state, or automating server configuration. Triggers on: infrastructure, terraform, pulumi, cloudformation, ansible, IaC, cloud, provisioning."
---

# Infrastructure as Code Skill

## When to Use

- Provisioning cloud resources (compute, networking, storage, databases)
- Managing infrastructure state and drift detection
- Automating server configuration and environment setup
- Designing multi-environment deployment topologies (dev/staging/prod)
- Auditing existing IaC for security, cost, and reliability

## Pipeline

### Phase 1 — Requirements Gathering

1. Identify the **target cloud provider(s)** (AWS, GCP, Azure, multi-cloud).
2. Define **infrastructure scope**: what resources are needed (compute, networking, storage, databases, CDN, DNS, etc.).
3. Determine **scale requirements**: expected traffic, data volume, autoscaling needs.
4. Establish **high-availability (HA) requirements**: multi-AZ, multi-region, failover strategy.
5. Clarify **compliance constraints**: PCI-DSS, HIPAA, SOC2, GDPR — these shape encryption, logging, and network isolation decisions.
6. Set **cost constraints**: monthly budget ceiling, reserved vs on-demand preference, spot instance tolerance.
7. Identify **existing infrastructure**: what already exists, what must be imported vs created fresh.
8. Document requirements in the enriched spec (`.ai/specs/`).

### Phase 2 — Architecture Design

1. Spawn the **Architect Agent** with the requirements spec.
2. Design the **network topology**: VPCs/VNets, subnets (public/private/isolated), peering, transit gateways.
3. Map **service dependencies**: which resources depend on which — database → compute → load balancer → DNS.
4. Define **security boundaries**: security groups, NACLs, IAM boundaries, service accounts.
5. Plan **environments**: workspace-based or directory-based separation for dev/staging/prod.
6. Specify **state management strategy**: remote backend (S3+DynamoDB, GCS, Azure Blob), state locking, state file per environment.
7. Output: architecture diagram (Mermaid) and resource dependency graph.

### Phase 3 — Module Design

1. Identify **reusable modules**: VPC/networking, compute (EC2/GCE/VM), database (RDS/CloudSQL/CosmosDB), load balancer, DNS, monitoring.
2. Define each module's **variable interface**: required inputs, optional inputs with defaults, validation rules.
3. Define each module's **outputs**: resource IDs, endpoints, ARNs — anything downstream modules consume.
4. Establish **naming conventions**: `{project}-{env}-{resource}` pattern, consistent tagging strategy.
5. Plan **module versioning**: pinned versions for stability, semantic versioning for internal modules.
6. Reference: [terraform-patterns.md](./references/terraform-patterns.md) for module structure conventions.

### Phase 4 — Implementation

1. Spawn the **Worker Agent** per module to write IaC code following the architecture design.
2. Configure **provider versions**: pin exact versions with `required_providers` block.
3. Set up **remote backend** before writing any resources — state must never be local in shared environments.
4. Implement modules bottom-up: networking → security → compute → databases → application layer → DNS/CDN.
5. Use **data sources** to reference existing infrastructure — never hardcode IDs or ARNs.
6. Apply **lifecycle rules** where appropriate: `prevent_destroy` on databases and state buckets, `create_before_destroy` on zero-downtime resources.
7. Mark sensitive variables and outputs with `sensitive = true`.
8. Structure `terraform.tfvars` per environment — never commit secrets, use SSM/Vault references.

### Phase 5 — Security Audit

1. Spawn the **Security Agent** with the full IaC codebase and the cloud security baseline.
2. Verify **IAM least privilege**: no `*` actions, no `*` resources, scoped service roles.
3. Check **encryption**: at rest (KMS/CMK for storage, databases, secrets) and in transit (TLS on all endpoints).
4. Validate **network segmentation**: databases in private subnets only, no direct internet-facing unless explicitly required.
5. Audit **secrets management**: no hardcoded credentials, secrets sourced from Vault/SSM/Secrets Manager.
6. Confirm **audit logging**: CloudTrail/audit logs enabled, log bucket with restricted access.
7. Reference: [cloud-security-baseline.md](./references/cloud-security-baseline.md) for minimum security requirements.

### Phase 6 — Cost Review

1. Run cost estimation (infracost or provider pricing calculator) against the plan output.
2. Flag resources exceeding **cost thresholds**: large instance types, provisioned IOPS, NAT gateway data transfer.
3. Recommend **cost optimizations**: reserved instances for stable workloads, spot/preemptible for batch jobs, right-sizing instances.
4. Verify **autoscaling boundaries**: min/max counts prevent runaway costs.
5. Check for **orphaned resources**: unused EIPs, detached volumes, idle load balancers.
6. Document estimated monthly cost in the plan and tag resources with cost center labels.

### Phase 7 — Plan Review

1. Generate plan output (`terraform plan`, `pulumi preview`, or equivalent) and capture as artifact.
2. Review for **destructive changes**: any destroy/replace actions must be explicitly justified.
3. Verify **resource counts**: expected number of creates, updates, and no-ops match the design.
4. Check for **drift**: if applying to an existing environment, ensure planned changes align with intent.
5. Validate **variable values** per environment — no dev values leaking into prod.
6. Gate: plan must be approved by the user before apply. Never auto-apply.

### Phase 8 — Documentation

1. Spawn the **Doc Updater Agent** to document the infrastructure.
2. Create **topology documentation**: architecture diagram, resource inventory, network layout.
3. Write **runbooks**: how to apply changes, how to roll back, how to handle state locks.
4. Document **disaster recovery procedures**: backup schedules, restore steps, RTO/RPO targets.
5. Update `docs/CODE_INVENTORY.md` with all IaC modules and their purposes.
6. Document environment-specific configurations and access patterns.

## Reference Files

- [Terraform Patterns](./references/terraform-patterns.md) — module structure, state management, provider configuration, lifecycle rules
- [Cloud Security Baseline](./references/cloud-security-baseline.md) — minimum security requirements for cloud infrastructure

## Tool-Specific Notes

### Terraform
- Primary reference tool for this skill. All patterns and examples use HCL syntax.
- Use `terraform fmt` and `terraform validate` before every commit.
- Pin provider versions. Pin Terraform version via `required_version`.

### Pulumi
- Translate module patterns to Pulumi component resources.
- Use stack references instead of remote state data sources.
- Leverage typed languages (TypeScript, Python) for compile-time safety.

### CloudFormation
- Map modules to nested stacks or AWS CDK constructs.
- Use `DeletionPolicy: Retain` on critical resources (equivalent to `prevent_destroy`).
- Prefer CDK over raw YAML/JSON for complex infrastructure.

### Ansible
- Use for server configuration management, not resource provisioning (prefer Terraform for provisioning).
- Roles map to modules — same reusability and interface principles apply.
- Encrypt secrets with `ansible-vault`, never commit plaintext credentials.
