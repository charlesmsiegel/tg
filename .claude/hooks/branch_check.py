import json
import subprocess
import sys

# Load the tool call context from stdin
try:
    context = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    sys.exit(0)

tool_name = context.get('tool_name', '')
tool_input = context.get('tool_input', {})

# Only check for Bash commands containing git commit
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    if 'git commit' in command:
        # Check current branch
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            sys.exit(0)
        branch = result.stdout.strip()

        if branch in ('main', 'master'):
            print("----------------------------------------------------", file=sys.stderr)
            print(f"ERROR: You cannot commit directly to the {branch} branch.", file=sys.stderr)
            print("Please create a new branch using 'git checkout -b <new-branch-name>'", file=sys.stderr)
            print("----------------------------------------------------", file=sys.stderr)
            sys.exit(2)

sys.exit(0)
