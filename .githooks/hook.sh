#!/usr/bin/env sh

set -e

HOOK_NAME=$(basename "$0")
STAGED_FILES=$(git diff --staged --name-only)
STAGED_EXISTING_FILES=$(git diff --staged --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ] && [ "$HOOK_NAME" = "pre-commit" ]; then
  exit 0
fi

COMMIT_MSG_FILE="$1"
HOOK_ARGS=${COMMIT_MSG_FILE:-$STAGED_EXISTING_FILES}

# Run poe based hooks
echo "Running Python $HOOK_NAME hook..."
poetry run poe git --hook "$HOOK_NAME" "$HOOK_ARGS" || exit $?
echo "$STAGED_EXISTING_FILES" | xargs -r git add

# General commit style check
if [ "$HOOK_NAME" = "commit-msg" ] ; then
  COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
  CONVENTIONAL_COMMIT_REGEX="^(feat|fix|chore|ci|docs|revert)(\(\w+\))?!?: .+"

  if ! echo "$COMMIT_MSG" | grep -qE "$CONVENTIONAL_COMMIT_REGEX"; then
    echo "Error: The provided commit message does not adhere to conventional commit style!"
    echo "Validation Regex: $CONVENTIONAL_COMMIT_REGEX"
    echo "Your commit message: $COMMIT_MSG"
    exit 1
  fi
fi
