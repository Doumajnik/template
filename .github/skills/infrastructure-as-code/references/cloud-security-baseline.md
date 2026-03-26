# Cloud Security Baseline

Minimum security requirements for all cloud infrastructure. Every IaC deployment must meet these standards before going to production.

## IAM and Access Control

- **Least privilege**: no IAM policy should use `"Action": "*"` or `"Resource": "*"`.
- **Service roles**: every compute resource gets a dedicated service role — never share roles across services.
- **MFA enforcement**: require MFA for all human IAM users and root account access.
- **No long-lived credentials**: use IAM roles, instance profiles, or workload identity — never static access keys in code.
- **Permission boundaries**: apply IAM permission boundaries to limit the maximum permissions any role can have.
- **Regular access review**: tag roles with owner and purpose for audit trail.

## Encryption at Rest

- **Storage**: S3/GCS/Blob buckets encrypted with KMS/CMK — not just default provider encryption.
- **Databases**: RDS/CloudSQL/CosmosDB encrypted at rest with customer-managed keys where compliance requires.
- **EBS/Disk volumes**: encrypted by default. Enforce via SCP or organization policy.
- **Secrets**: stored in Vault, SSM Parameter Store, or Secrets Manager — never in tfvars, env files, or source code.
- **State files**: Terraform state contains sensitive data — encrypt the backend storage and restrict access.

## Encryption in Transit

- **TLS everywhere**: all load balancers, API gateways, and service endpoints must terminate TLS 1.2+.
- **Internal traffic**: use service mesh or mTLS between internal services where possible.
- **Database connections**: enforce SSL/TLS on all database connections — reject plaintext.
- **Certificate management**: use ACM, Let's Encrypt, or managed certificates — no self-signed certs in production.

## Network Security

- **VPC design**: separate public, private, and isolated subnets. Databases and internal services go in private subnets only.
- **NAT gateway**: private subnets reach the internet through NAT — never attach public IPs to backend services.
- **Security groups**: default deny all inbound. Open only required ports to specific CIDR ranges or security groups.
- **NACLs**: use as a secondary defense layer with explicit deny rules for known bad ranges.
- **VPC flow logs**: enable on all VPCs for network traffic auditing.
- **No public access for data stores**: S3/GCS buckets, RDS/CloudSQL instances must block public access by default.

## Storage Security (S3/GCS/Blob)

- **Block public access**: enable account-level and bucket-level public access blocks.
- **Versioning**: enable on all buckets storing state, backups, or audit logs.
- **Lifecycle rules**: auto-expire old versions and transition to cheaper tiers.
- **Bucket policies**: restrict access to specific IAM roles/accounts — no wildcard principals.
- **Object lock**: enable for compliance-critical data that must not be deleted.

## Database Security

- **No public accessibility**: databases must not have public endpoints.
- **Encryption**: encrypted at rest and in transit (enforce SSL).
- **IAM authentication**: use IAM database auth where supported (RDS, CloudSQL) instead of password-only.
- **Automated backups**: enable with retention period matching RPO requirements.
- **Deletion protection**: enable on production databases to prevent accidental destruction.
- **Parameter groups**: disable insecure features, enforce audit logging.

## Secrets Management

- **Vault, SSM, or Secrets Manager**: all credentials, API keys, and certificates stored in managed secrets store.
- **Rotation**: enable automatic rotation for database passwords and API keys.
- **Access logging**: audit every secrets access for forensic capability.
- **No secrets in IaC code**: not in variables, not in tfvars, not in environment files committed to git.

## Audit and Logging

- **CloudTrail / audit logs**: enabled in all regions, writing to a dedicated log bucket.
- **Log bucket protection**: separate account or restricted access — operators cannot delete audit logs.
- **Retention**: minimum 90 days online, 1 year archived — adjust to compliance requirements.
- **Alerting**: CloudWatch/Stackdriver alerts on root login, IAM changes, security group changes.

## Web Application Protection

- **WAF**: deploy on all internet-facing load balancers and API gateways.
- **Rate limiting**: configure rate-based rules to mitigate volumetric attacks.
- **DDoS protection**: enable AWS Shield Standard (free) or equivalent provider protection.
- **Bot mitigation**: add managed rule groups for known bad bots and scanners.

## Compliance Tags

- Every resource must have at minimum: `Environment`, `Project`, `Owner`, `CostCenter`.
- Add `DataClassification` tag for resources handling sensitive data.
- Use tag policies (AWS Organizations / Azure Policy) to enforce required tags.
