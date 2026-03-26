# Terraform Patterns Reference

## Module Directory Structure

```
modules/
  vpc/
    main.tf          # Resource definitions
    variables.tf     # Input variables with descriptions and validation
    outputs.tf       # Output values for downstream consumers
    versions.tf      # Required providers and Terraform version
    README.md        # Module usage examples
  compute/
    main.tf
    variables.tf
    outputs.tf
    versions.tf
environments/
  dev/
    main.tf          # Module calls with dev-specific values
    terraform.tfvars  # Variable values (never commit secrets)
    backend.tf       # Remote state config for dev
  staging/
    ...
  prod/
    ...
```

## Variable Naming Conventions

- Use `snake_case` for all variable names.
- Prefix booleans with `enable_` or `is_`: `enable_monitoring`, `is_public`.
- Group related variables with a common prefix: `vpc_cidr`, `vpc_name`, `vpc_tags`.
- Always include `description` and `type`. Add `validation` blocks for constrained values.
- Use `default = null` for truly optional variables — not empty strings.

## Output Conventions

- Output every resource ID, ARN, and endpoint that downstream modules may need.
- Use descriptive names: `vpc_id`, `private_subnet_ids`, `database_endpoint`.
- Mark sensitive outputs: `sensitive = true` on connection strings, passwords, keys.
- Include `description` on every output for self-documenting modules.

## Remote State Configuration

- **AWS**: S3 bucket + DynamoDB table for state locking. Enable versioning on the bucket.
- **GCP**: GCS bucket with object versioning. State locking is built-in.
- **Azure**: Azure Blob Storage with lease-based locking.
- Always encrypt state at rest — state files contain sensitive data.
- Never store state locally in shared or CI/CD environments.
- Use separate state files per environment to limit blast radius.

## Workspace vs Directory Separation

- **Directories** (recommended): separate `environments/{env}/` dirs with their own state and tfvars.
- **Workspaces**: lighter-weight but risk cross-environment confusion. Use only for simple setups.
- In either case, the module source code is shared — only variable values differ per environment.

## Provider Version Pinning

```hcl
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

- Pin Terraform version range. Pin provider minor version (`~> 5.0` allows `5.x` patches).
- Run `terraform init -upgrade` deliberately — never auto-upgrade in CI.

## Data Sources vs Resources

- Use **data sources** to reference existing infrastructure: `data.aws_vpc.existing`, `data.aws_ami.latest`.
- Never hardcode resource IDs, AMI IDs, or account numbers — always look them up.
- Use data sources for cross-stack references when remote state is not available.

## Lifecycle Rules

- `prevent_destroy`: protect critical resources (databases, S3 state buckets, encryption keys).
- `create_before_destroy`: zero-downtime replacements (launch templates, security groups).
- `ignore_changes`: when external processes modify attributes (ASG desired count, tags managed by other tools).
- Use lifecycle rules sparingly — each one is a maintenance burden. Document why it exists.

## Provisioners

- **Avoid provisioners** (`local-exec`, `remote-exec`) whenever possible.
- Prefer cloud-init user data, AMI baking (Packer), or configuration management (Ansible) instead.
- If unavoidable, use `local-exec` only and ensure idempotency.

## Importing Existing Resources

- Use `terraform import` to bring existing resources under management.
- Write the resource block first, then import. Run `terraform plan` to verify no diff.
- In Terraform 1.5+, prefer `import` blocks in config for reproducible imports.

## Sensitive Variables and tfvars

- Mark variables as `sensitive = true` when they contain credentials or keys.
- Never commit `terraform.tfvars` files with secrets — use `.gitignore`.
- Source secrets from environment variables (`TF_VAR_`), SSM Parameter Store, or Vault.
- Use a `terraform.tfvars.example` file with placeholder values for documentation.
