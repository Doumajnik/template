+++
id = "technologies/terraform"
title = "Terraform Best Practices"
agents = ["all"]
technologies = ["terraform", "hcl", "iac"]
category = "rule"
tags = ["terraform", "infrastructure", "iac", "cloud", "devops"]
version = 1
+++

### Module Structure

- Use the standard file layout in every module: `main.tf` for resources, `variables.tf` for inputs, `outputs.tf` for outputs, `versions.tf` for required providers and Terraform version constraints, and `locals.tf` for computed values.
- Split large modules by resource type — one file per AWS service or logical grouping (e.g., `iam.tf`, `networking.tf`, `compute.tf`) instead of a monolithic `main.tf` with hundreds of lines.
- Name child modules by their purpose, not their implementation — `modules/api-gateway/` not `modules/aws-apigw/`; module names should survive provider changes.
- Keep modules small and single-purpose — a module that provisions a VPC should not also create IAM roles; compose small modules from the root module instead.
- Use consistent naming for resources and data sources: `snake_case`, prefixed with the project or environment where appropriate (e.g., `aws_s3_bucket.app_assets` not `aws_s3_bucket.bucket1`).

### State Management

- Always use a remote backend (S3+DynamoDB for AWS, GCS for GCP, Azure Storage for Azure) — local state files are a single point of failure and block team collaboration.
- Enable state locking via DynamoDB (AWS) or native locking (GCS, Azure) — concurrent `terraform apply` runs without locking corrupt state.
- Never commit `*.tfstate` or `*.tfstate.backup` to version control — add both to `.gitignore`; state files contain secrets and sensitive resource attributes in plaintext.
- Encrypt state at rest — enable server-side encryption on the S3 bucket or storage account holding state; use a KMS key you control, not the default.
- Prefer directory-based isolation over workspaces for environments (dev/staging/prod) — workspaces share the same backend config and make it easy to accidentally apply to the wrong environment.
- Use `terraform state mv` and `moved` blocks for refactoring — never delete and recreate resources just to rename them; that causes downtime and data loss.
- Bootstrap the state backend infrastructure outside of Terraform or in a separate root module — the backend that stores state cannot be managed by the state it stores.

### Variables and Outputs

- Add a `description` to every variable — future maintainers and module consumers read descriptions, not your source code.
- Use `validation` blocks to enforce constraints at plan time — catch invalid CIDR ranges, disallowed instance types, or naming violations before they hit the API.
- Set `type` constraints on every variable — avoid `any`; use specific types (`string`, `number`, `list(string)`, `map(object({...}))`) to catch misuse early.
- Mark secrets with `sensitive = true` — this prevents Terraform from displaying the value in plan output and logs; apply it to passwords, API keys, and tokens.
- Provide sensible `default` values only when a safe default exists — required variables with no default force the caller to make an explicit decision.
### Resource Patterns

- Prefer `for_each` over `count` for collections — `for_each` uses map keys as resource identifiers, so removing an item from the middle doesn't force recreation of subsequent resources.
- Use `count` only for boolean toggles (e.g., `count = var.create_bucket ? 1 : 0`) — never use `count` with lists where item order matters.
- Use `depends_on` only when Terraform cannot infer the dependency from resource references — most dependencies are implicit; explicit `depends_on` hides the real data flow.
- Use `lifecycle { prevent_destroy = true }` on critical resources (databases, S3 buckets with data) — this blocks accidental `terraform destroy` from deleting irreplaceable resources.
- Use `lifecycle { ignore_changes = [...] }` when an external process legitimately modifies an attribute (e.g., ASG desired count managed by autoscaling) — avoids plan noise and unintended reverts.
- Use `dynamic` blocks to generate repeated nested blocks from a variable — but keep them simple; deeply nested dynamic blocks are unreadable; extract to a local if complex.

### Provider Configuration

- Pin every provider to a version range in `versions.tf` — use pessimistic constraint (`~> 5.0`) to allow patch updates but prevent breaking major changes.
- Declare all providers in the `required_providers` block — never rely on implicit provider installation; explicit declarations make `terraform init` reproducible.
- Use provider aliases for multi-region or multi-account deployments — e.g., `provider "aws" { alias = "us_west_2" region = "us-west-2" }` and pass the alias to resources with `provider = aws.us_west_2`.
- Pin the Terraform CLI version with `required_version` — e.g., `required_version = ">= 1.5, < 2.0"`; prevents running with an incompatible CLI version.
- Never hardcode AWS credentials, subscription IDs, or project IDs in provider blocks — use environment variables, IAM instance profiles, or workload identity federation.

### Security

- Never store secrets in `.tf` files or `terraform.tfvars` committed to Git — use a secrets manager (Vault, AWS Secrets Manager) and reference via data sources or environment variables.
- Require `terraform plan` review before every `apply` — in CI, save the plan file (`terraform plan -out=tfplan`) and apply only that exact plan (`terraform apply tfplan`) to prevent drift between plan and apply.
- Run static analysis with `tfsec`, `checkov`, or `trivy` in CI on every PR — fail the pipeline on HIGH/CRITICAL findings; these tools catch public S3 buckets, open security groups, and unencrypted resources.
- Enforce policy-as-code with Sentinel (Terraform Cloud/Enterprise) or OPA/Conftest (open source) — codify guardrails like "no public ingress on port 22" or "all resources must have required tags".
- Enable access logging on the state backend (S3 access logs, CloudTrail) — audit who read or modified state, since state contains sensitive data.
- Restrict who can run `terraform apply` using CI/CD pipeline permissions — developers should be able to plan, but apply should require approval or be limited to a service account.

### CI/CD

- Run `terraform fmt -check` in CI — reject PRs with formatting inconsistencies; `terraform fmt` is the canonical formatter and eliminates style debates.
- Run `terraform validate` after `fmt` — it catches syntax errors, invalid references, and type mismatches without needing provider credentials.
- Run `terraform plan` on every PR and post the plan output as a PR comment — reviewers must see what will change before approving.
- Apply only from CI, never from a developer's laptop — this ensures the apply uses the correct credentials, state backend, and variable values.
- Implement drift detection by scheduling `terraform plan` on a cron (e.g., nightly) and alerting when the plan is non-empty — manual changes in the console create drift that causes surprises on the next apply.
- Use separate CI pipelines or approval gates per environment — a merge to `main` should not automatically apply to production without explicit approval.
