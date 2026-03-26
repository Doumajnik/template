+++
id = "technologies/aws"
title = "AWS Best Practices"
agents = ["all"]
technologies = ["aws", "cloud"]
category = "rule"
tags = ["aws", "cloud", "infrastructure", "security", "devops"]
version = 1
+++

### IAM

- Follow least privilege — grant only the permissions required for the specific task; start with zero permissions and add incrementally based on access errors, never start with `*`.
- Never create long-lived IAM access keys for human users — use IAM Identity Center (SSO) with short-lived session credentials; if CLI access is needed, use `aws sso login`.
- Assign IAM roles to services instead of embedding credentials — EC2 uses instance profiles, ECS uses task roles, Lambda uses execution roles; no access keys in code or environment variables.
- Use permission boundaries on all IAM roles created by developers — boundaries set the maximum permissions a role can ever have, even if the policy attached is overly broad.
- Enable Service Control Policies (SCPs) at the AWS Organization level — restrict dangerous actions (e.g., disabling CloudTrail, leaving the organization) across all accounts.
- Run IAM Access Analyzer to identify resources shared externally — it detects S3 buckets, KMS keys, IAM roles, and Lambda functions accessible from outside your account.
- Require MFA for all human users, especially for the root account — store root account credentials in a physical safe and use them only for account recovery.

### Networking

- Design VPCs with a 3-tier architecture: public subnets (ALB, NAT Gateway), private subnets (application, compute), and isolated subnets (databases, no internet route) — each tier gets its own route table.
- Use at least 2 Availability Zones for every production workload — single-AZ deployments fail completely during AZ outages; spread subnets across AZs.
- Deploy NAT Gateways in public subnets for private subnet internet access — use one NAT Gateway per AZ in production to avoid cross-AZ data transfer costs and single-AZ failure.
- Use VPC endpoints (Gateway for S3/DynamoDB, Interface for other services) to keep traffic off the public internet — reduces latency, cost, and attack surface.
- Prefer Security Groups over NACLs for access control — Security Groups are stateful and easier to manage; use NACLs only for broad subnet-level deny rules as a defense-in-depth layer.

### Compute

- Right-size instances using AWS Compute Optimizer recommendations — review utilization metrics monthly and downsize over-provisioned instances; most workloads are over-provisioned by 30–50%.
- Use Savings Plans or Reserved Instances for steady-state workloads — commit to 1-year or 3-year terms for 30–60% savings; use Compute Savings Plans for flexibility across instance families.
- Use Spot Instances for fault-tolerant, stateless workloads (batch processing, CI runners, dev environments) — combine with on-demand in an ASG mixed instances policy for reliability.
- Prefer ECS Fargate or Lambda over self-managed EC2 for new workloads — eliminate patching, scaling, and capacity planning overhead unless you need GPU, custom kernels, or sustained high CPU.
- Use Lambda for event-driven, short-duration workloads (API handlers, S3 triggers, SQS consumers) — set memory proportional to CPU needs and configure reserved concurrency to prevent runaway scaling.

### Storage

- Enable S3 versioning on all buckets storing important data — versioning protects against accidental deletes and overwrites; combine with lifecycle rules to expire old versions after 30–90 days.
- Enable S3 Intelligent-Tiering for buckets with unpredictable access patterns — it automatically moves objects between frequent and infrequent access tiers with no retrieval fees.
- Block public access at the account level with S3 Block Public Access — override per-bucket only when explicitly required (e.g., static website hosting); audit exceptions quarterly.
- Encrypt all EBS volumes with AWS-managed or customer-managed KMS keys — enable default EBS encryption at the account level so every new volume is encrypted automatically.

### Database

- Deploy RDS with Multi-AZ for production workloads — the standby replica in another AZ provides automatic failover in under 60 seconds; never run production on single-AZ.
- Use read replicas for read-heavy workloads — direct read traffic to replicas via a reader endpoint; this offloads the primary and improves response times.
- Choose Aurora for critical workloads that need 5x throughput over standard MySQL/PostgreSQL — Aurora's storage layer is distributed across 3 AZs with 6-way replication.
- Use DynamoDB for high-scale key-value and document workloads — prefer on-demand capacity for unpredictable traffic; use provisioned with auto-scaling for steady-state; always define GSIs carefully to avoid hot partitions.
- Deploy ElastiCache (Redis) for session storage, API response caching, and rate limiting — use cluster mode for horizontal scaling; enable encryption in transit and at rest with AUTH tokens.

### Observability

- Create CloudWatch alarms for key metrics on every resource: CPU utilization, memory (via CloudWatch Agent), error rates, queue depth, and latency percentiles (p50, p95, p99) — alarm on thresholds, not averages.
- Enable AWS X-Ray for distributed tracing across Lambda, API Gateway, ECS, and inter-service calls — propagate trace headers to identify bottlenecks and failure points across microservices.
- Enable CloudTrail in all regions of all accounts with a centralized S3 bucket — CloudTrail records every API call; set up CloudWatch Logs integration for real-time alerting on sensitive actions.
- Enable VPC Flow Logs on all VPCs and publish to CloudWatch Logs or S3 — use them to debug connectivity issues, detect unauthorized access attempts, and support forensic investigations.

### Security

- Enable AWS Config rules to continuously monitor resource compliance — use managed rules for common checks (encrypted EBS, public S3, unrestricted security groups) and custom rules for organization-specific policies.
- Enable GuardDuty in all accounts and regions — it detects compromised credentials, cryptocurrency mining, unusual API calls, and C2 communication with zero configuration.
- Aggregate findings in Security Hub with the AWS Foundational Security Best Practices standard enabled — Security Hub normalizes findings from GuardDuty, Inspector, Config, and third-party tools into a single pane.
- Deploy AWS WAF in front of CloudFront and ALB — enable managed rule groups (Core Rule Set, SQL injection, Known Bad Inputs) and add rate-based rules to block DDoS at the application layer.
- Use KMS customer-managed keys (CMKs) for encryption of sensitive data — rotate keys annually; use separate keys per service (one for RDS, one for S3, one for Secrets Manager) with key policies restricting access.
- Store secrets in AWS Secrets Manager with automatic rotation enabled — never store database passwords, API keys, or tokens in Parameter Store (no rotation), environment variables, or code.

### Cost

- Implement a mandatory tagging strategy — require at minimum `Environment`, `Team`, `Service`, and `CostCenter` tags on every resource; enforce with AWS Config or SCPs that deny untagged resource creation.
- Review Cost Explorer weekly and set up AWS Budgets with alerts at 50%, 80%, and 100% of monthly targets — configure SNS notifications to both email and Slack/Teams.
- Run regular unused resource cleanup: delete unattached EBS volumes, release unused Elastic IPs, remove old snapshots, terminate idle RDS instances, and delete unused NAT Gateways — automate with Lambda or AWS Trusted Advisor.
- Use S3 lifecycle rules to transition infrequently accessed data to Glacier or Glacier Deep Archive — data older than 90 days with rare access should not remain in Standard storage class.
