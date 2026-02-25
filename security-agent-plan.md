# Plan for Security Review Agent Development

## Objectives
- Automate security and vulnerability detection in repositories.
- Generate actionable, clear Markdown reports with prioritized findings.
- Adapt to various programming languages and frameworks.

## Features to Include
- **Static Code Analysis**: Detect security issues such as SQL injections, XSS, hardcoded secrets, etc.
- **Dependency Scanning**: Flag outdated or vulnerable dependencies by integrating with tools like Snyk or Dependabot.
- **Configuration Analysis**: Scan files like `.env`, `Dockerfile`, or `config.yml` for misconfigurations.
- **Secrets Scanning**: Identify exposed API keys, credentials, or tokens in the code.
- **Policy Enforcement**: Check adherence to organization-specific secure coding guidelines.

## Tools & Frameworks
- **AI Model Integration**:
  - Use GitHub Copilot for deep code insights.
  - Experiment with custom LLMs (like Anthropic Claude or OpenAI Codex) for advanced reasoning.
- **Existing Security Tools**:
  - **Bandit**: Python security linter.
  - **Checkmarx/Sonarqube**: Full-fledged code security analysis tools.
  - **OWASP Dependency-Check**: Scans dependencies for known issues.
- **GitHub Actions**: Automate scans and logs.
- **GitHub Comments/Actions**: Inline comments for detected issues.

## Workflow
1. **Repository Initialization**:
   - Add a dedicated YAML workflow file
   - Configure triggers for scanning Pull Requests and Scheduled runs.
2. **Analysis**:
   - Perform static code analysis.
   - Scan dependencies and configurations.
3. **Reporting**:
   - Generate Markdown reports categorized as:
     - **Critical**
     - **High**
     - **Medium**
     - **Low**
   - Store reports in a dedicated `security/` folder.
4. **Results Delivery**:
   - Post findings as pull request comments.
   - Summarize findings in the GitHub Actions log.
5. **Continuous Improvements**:
   - Fine-tune AI and algorithms based on historical issues.
   - Update detection patterns dynamically.

## Integration Points

  - Automate the scan routine and ensure reports get back into the team's workflow.
- **Configurable Agent Settings**:
  - Allow users to disable checks not relevant to their project.
- **Secure Deployment**:
  - Avoid sending sensitive data outside the organization.

## Learning from the Industry
- **Innovative Security Agents**: Deploy security bots using a configuration-driven policy approach, e.g., markdown files defining rules.
- **Real-Time Suggestions**:
  - User-triggered inline code suggestions.
  - Continuous scanning during key events (push, PR, etc.).
- **Multi-Stack Analysis**:
  - Roll out tool enhancements stacked for Java, JS, Python, etc.

## Inspiration Checks
### Researching from AI Code Tools
1. Build modular prompts for security-focused feedback (Anthropic Claude prompting or OpenAI fine-tunes focus).
2. Gather insights on decision-making vulnerabilities.
### Researching Example Security Problems Public Projects.