# Onboarding Report Targets

These are the files that the onboarding pipeline creates or updates.

## Documentation Files
| File | Agent | Content |
| --- | --- | --- |
| `docs/BUSINESS_LOGIC.md` | Doc Updater | System business logic, data flows, module responsibilities |
| `docs/CODE_INVENTORY.md` | Doc Updater | Every exported symbol, function, class, with file paths |
| `docs/API_DOCUMENTATION.md` | Doc Updater | Exposed endpoints and consumed external APIs |
| `docs/files/{path}.md` | Doc Updater | Per-file documentation for key source files |

## Audit Reports
| File | Agent | Content |
| --- | --- | --- |
| `docs/SECURITY_REPORT.md` | Security | Vulnerabilities, hardcoded secrets, injection risks |
| `docs/QUALITY_REPORT.md` | Code Quality | Duplication, dead code, complexity, code smells |
| `docs/DEPENDENCY_REPORT.md` | Dependency | Outdated packages, vulnerabilities, license issues |
| `docs/ERROR_HANDLING_REPORT.md` | Error Handling | Silent catches, swallowed exceptions |
| `docs/TYPE_SAFETY_REPORT.md` | Type Safety | Missing types, unsafe casts, schema drift |
| `docs/MONITORING_REPORT.md` | Monitoring | Missing logging, health checks, alerting |

## Planning Files
| File | Agent | Content |
| --- | --- | --- |
| `.ai/plans/{date}_test-baseline.md` | Integration Tester | Test run results |
| `.ai/todos/{date}_onboarding-improvements.todo.md` | Planning | Prioritized improvement tasks |
