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

# Determine the file path the tool is trying to access
file_path = None
if tool_name in ['Write', 'Edit', 'Update', 'NotebookEdit']:
    file_path = tool_input.get('file_path') or tool_input.get('notebook_path')

if file_path:
    # Use git check-ignore to see if the file is ignored
    result = subprocess.run(
        ['git', 'check-ignore', '-q', file_path],
        capture_output=True
    )
    # Exit code 0 means the file IS ignored
    if result.returncode == 0:
        print(f"Error: Attempted to write to a gitignored file: {file_path}", file=sys.stderr)
        sys.exit(2)

# Exit code 0 allows the tool execution to proceed
sys.exit(0)
