"""
Tool Guard — PreToolUse hook for enforcing tool restrictions.

Reads JSON from stdin (VS Code Copilot PreToolUse event), checks the tool name
against denied patterns, and outputs a permission decision on stdout.

Enforcement rules are defined inline below (sourced from .ai/TOOL_MANIFEST.md).
Only the Research agent is allowed to use web access tools.
Test Writer is denied source file reading tools (black-box testing enforcement).
"""

import json
import re
import sys


# --- Denied tool patterns (from TOOL_MANIFEST.md) ---
# Patterns matched against the tool name (case-insensitive)
WEB_ACCESS_PATTERNS = [
    r"fetch_webpage",
    r"mcp_playwright_",
    r"open_browser_page",
]

# Agents allowed to use web access tools (case-insensitive match)
WEB_ACCESS_ALLOWED_AGENTS = {"research"}

# Source file reading tools — denied for Test Writer on src/ paths
SOURCE_READ_TOOLS = {"read_file", "grep_search", "semantic_search"}

# Agents denied from reading source files (black-box testing)
SOURCE_READ_DENIED_AGENTS = {"test writer", "test_writer", "testwriter"}

# Path patterns that count as source/implementation files
SOURCE_PATH_PATTERNS = [
    r"[\\/]src[\\/]",
    r"^src[\\/]",
]


def read_stdin():
    """Read the full PreToolUse JSON payload from stdin."""
    return json.load(sys.stdin)


def get_tool_name(payload):
    """Extract the tool name from the hook payload."""
    return payload.get("toolName", payload.get("tool_name", ""))


def get_agent_name(payload):
    """Extract the calling agent name from the hook payload.

    The hook payload structure may vary — try several known paths.
    Falls back to empty string if agent identity is unavailable.
    """
    for key in ("agentName", "agent_name", "agent"):
        if key in payload:
            return payload[key]
    context = payload.get("context", {})
    for key in ("agentName", "agent_name", "agent"):
        if key in context:
            return context[key]
    return ""


def is_web_tool(tool_name):
    """Check if the tool name matches any web access pattern."""
    for pattern in WEB_ACCESS_PATTERNS:
        if re.search(pattern, tool_name, re.IGNORECASE):
            return True
    return False


def is_source_read_tool(tool_name):
    """Check if the tool is a source file reading tool."""
    return tool_name.lower() in SOURCE_READ_TOOLS


def targets_source_path(payload):
    """Check if the tool call targets a source file path (src/)."""
    args = payload.get("toolParameters", payload.get("parameters", {}))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except (json.JSONDecodeError, TypeError):
            return False
    if not isinstance(args, dict):
        return False
    for key in ("filePath", "file_path", "path", "includePattern", "query"):
        val = args.get(key, "")
        if isinstance(val, str):
            for pat in SOURCE_PATH_PATTERNS:
                if re.search(pat, val, re.IGNORECASE):
                    return True
    return False


def check_permission(tool_name, agent_name, payload):
    """Return (decision, reason) tuple. decision is 'allow' or 'deny'."""
    if is_web_tool(tool_name):
        if agent_name.lower() in WEB_ACCESS_ALLOWED_AGENTS:
            return "allow", f"Agent '{agent_name}' is allowed web access"
        if not agent_name:
            return "deny", (
                f"Tool '{tool_name}' requires web access. "
                "Agent identity unknown — denied by default. "
                "Only the Research agent may use web tools."
            )
        return "deny", (
            f"Tool '{tool_name}' denied for agent '{agent_name}'. "
            "Only the Research agent may use web access tools. "
            "See .ai/TOOL_MANIFEST.md for details."
        )

    if (agent_name.lower() in SOURCE_READ_DENIED_AGENTS
            and is_source_read_tool(tool_name)
            and targets_source_path(payload)):
        return "deny", (
            f"Tool '{tool_name}' denied for agent '{agent_name}' on source files. "
            "Test Writer must not read implementation code (black-box testing). "
            "Use the Librarian-provided context brief for function signatures. "
            "See .ai/TOOL_MANIFEST.md for details."
        )

    return "allow", ""


def make_response(decision, reason=""):
    """Build the PreToolUse hook response JSON."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }


def main():
    try:
        payload = read_stdin()
    except (json.JSONDecodeError, EOFError):
        # If we can't parse input, allow by default to avoid blocking
        json.dump(make_response("allow", "Could not parse hook input"), sys.stdout)
        return

    tool_name = get_tool_name(payload)
    agent_name = get_agent_name(payload)
    decision, reason = check_permission(tool_name, agent_name, payload)
    json.dump(make_response(decision, reason), sys.stdout)


if __name__ == "__main__":
    main()
