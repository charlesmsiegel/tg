# Fix PR Review Issues

Review pull request $ARGUMENTS and address all code review feedback.

If $ARGUMENTS is empty, first run `gh pr view` to detect the current branch's PR.

## Steps

1. **Fetch PR information**: Use `gh pr view $ARGUMENTS` to get the PR description and `gh pr diff $ARGUMENTS` to see the changes.

2. **Get review comments**: Run `gh pr view $ARGUMENTS --comments` and use the GitHub API to retrieve all inline review comments for the PR.

3. **Analyze feedback**: Identify all actionable items from reviewers—requested changes, nitpicks, questions that imply issues, and suggested improvements.

4. **Fix each issue**: For each piece of feedback:
   - Locate the relevant file and line
   - Understand the reviewer's concern
   - Implement the fix or improvement
   - If a suggestion is unclear or you disagree, note it for my review rather than guessing

5. **Verify changes**: Run any relevant tests or linters to ensure fixes don't introduce new problems.

6. **Summarize**: Provide a brief summary of what was fixed and flag anything that needs my input.
