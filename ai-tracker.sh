#!/bin/bash

# A script to track changes, update UPDATES.md, and commit with semi-automatic versioning.

# Usage: ai-tracker.sh [force] [-r <commit-hash>] [-v major|minor|patch|none]
#   -r: Specify a commit hash to generate diff from that commit to HEAD
#   -v: Version bump type (default: patch)
#       major: Breaking changes (x.0.0)
#       minor: New features (1.x.0)
#       patch: Bug fixes (1.2.x)
#       none:  No version change
#   force: Ignore AI-detected errors and proceed with commit

set -e
set -o pipefail

FORCE_MODE=false
if [ "$1" = "force" ]; then
    FORCE_MODE=true
    echo "🚀 Force mode enabled. AI-detected errors will be ignored."
    shift # remove 'force'
fi

# Function to increment version
increment_version() {
    local current_version=$1
    local bump_type=$2
    
    # Split version into components
    IFS='.' read -r major minor patch <<< "$current_version"
    
    # Handle missing components
    major=${major:-0}
    minor=${minor:-0}
    patch=${patch:-0}
    
    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        none)
            # No change
            ;;
        *)
            echo "Invalid bump type: $bump_type" >&2
            exit 1
            ;;
    esac
    
    echo "${major}.${minor}.${patch}"
}

# Check if inside a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1;
    then
    echo "Error: Not in a git repository."
    exit 1
fi

# Get the root directory of the git repository
GIT_ROOT=$(git rev-parse --show-toplevel)
UPDATES_FILE="$GIT_ROOT/UPDATES.md"

# Default values
DIFF_COMMAND="git diff --staged"
VERSION_BUMP="patch"  # Default to patch increment

# Parse arguments
while getopts ":r:v:" opt; do
  case ${opt} in
    r) 
      DIFF_COMMAND="git diff ${OPTARG}..HEAD"
      ;;
    v)
      VERSION_BUMP="${OPTARG}"
      if [[ ! "$VERSION_BUMP" =~ ^(major|minor|patch|none)$ ]]; then
        echo "Error: Invalid version bump type: ${OPTARG}" >&2
        echo "Valid options: major, minor, patch, none" >&2
        echo "Usage: $(basename "$0") [force] [-r <commit-hash>] [-v major|minor|patch|none]" >&2
        exit 1
      fi
      ;;
    ?)
      echo "Invalid option: -${OPTARG}" >&2
      echo "Usage: $(basename "$0") [force] [-r <commit-hash>] [-v major|minor|patch|none]" >&2
      exit 1
      ;;
    :)
      echo "Option -${OPTARG} requires an argument." >&2
      echo "Usage: $(basename "$0") [force] [-r <commit-hash>] [-v major|minor|patch|none]" >&2
      exit 1
      ;;
  esac
done

# Create a __version__.py file if it doesn't exist
VERSION_FILE="$GIT_ROOT/__version__.py"
if [ ! -f "$VERSION_FILE" ]; then
    echo "__version__ = \"0.0.1\"" > "$VERSION_FILE"
    echo "Created __version__.py at project root with initial version 0.0.1."
    git add "$VERSION_FILE"
fi

# Read current version
CURRENT_VERSION=$(sed -n 's/^__version__ = "\([^"]*\)"/\1/p' "$VERSION_FILE")

# Calculate new version
NEW_VERSION=$(increment_version "$CURRENT_VERSION" "$VERSION_BUMP")

# Show version change
if [ "$VERSION_BUMP" != "none" ]; then
    echo "📦 Version will be updated: $CURRENT_VERSION → $NEW_VERSION"
else
    echo "📦 Version will remain: $CURRENT_VERSION"
fi
echo ""

# Stage all modified/deleted files
git add -u

# Get the diff output, filtering for non-empty code changes
# First, check if we're using staged diff or commit range diff
if [[ "$DIFF_COMMAND" == "git diff --staged" ]]; then
    # For staged diff, exclude ai-tracker.sh using pathspec
    DIFF=$(git diff --staged -- . ':(exclude)ai-tracker.sh' ':(exclude)**/ai-tracker.sh' | grep -E '^(\+\+\+|---|\+|@@)' | grep -v '^[+ ]*$' | grep -v '^-*$')
else
    # For commit range diff, filter out ai-tracker.sh from the output
    DIFF=$(eval "$DIFF_COMMAND" | grep -v 'ai-tracker\.sh' | grep -E '^(\+\+\+|---|\+|@@)' | grep -v '^[+ ]*$' | grep -v '^-*$')
fi

if [[ -z "$DIFF" ]]; then
    echo "No relevant changes found. Exiting."
    exit 0
fi

# Escape backticks in the diff to prevent shell execution inside HEREDOC
ESCAPED_DIFF=$(printf "%s" "${DIFF}" | sed 's/`/\\`/g')

# --- Check for syntax errors with ruff ---
echo "🔍 Checking for syntax errors with ruff..."

# Get list of Python files being changed.
# We use eval to handle both 'git diff --staged' and 'git diff <commit>..HEAD'
PYTHON_FILES_TO_CHECK=$(eval "$DIFF_COMMAND" --name-only --diff-filter=AM | grep '\.py$' || true)

if [ -n "$PYTHON_FILES_TO_CHECK" ]; then
    # We pass the files to ruff. If it returns a non-zero exit code, it means there are errors.
    if ! ruff check $PYTHON_FILES_TO_CHECK; then
        if [ "$FORCE_MODE" = "true" ]; then
            echo "⚠️  Ruff found errors, but force mode is on. Proceeding..."
        else
            echo "❌ Ruff found errors. Aborting update." >&2
            echo "   Use 'force' as the first argument to override and commit anyway." >&2
            exit 1
        fi
    else
        echo "✅ No Python syntax errors found."
    fi
else
    echo "ℹ️ No Python files to check."
fi


# Prepare the prompt for Gemini
GEMINI_PROMPT="You are an expert technical writer and git user.

### CONTEXT ###
The user has provided a git diff output. Your task is to:
1.  Generate a summary of the changes suitable for a project update log.
2.  Generate a conventional git commit message.

### PRIMARY TASK ###
#### Part 1: Summary Generation
1.  **Review for breakpoints**: Check for breakpoints (e.g., 'pdb.set_trace()', 'breakpoint()').
2.  **Summarize and categorize changes**:
    - Summarize and categorize the changes from the git diff.
    - Use a category for each change (e.g., 'What's New', 'Bugfix', 'Refactor').
    - If you found breakpoints, add a 'Warnings' section at the top of your summary.

#### Part 2: Commit Message Generation
1.  Based on the changes, generate a concise and relevant git commit message.
2.  The first line should be the subject, following Conventional Commits format (e.g., 'feat: add new feature').
3.  The subject should be a maximum of 50 characters.
4.  The body should contain a brief, 1-2 sentence description if necessary.

### SPECIFICATIONS & INSTRUCTIONS ###
- Group summary changes by category, then by file.
- Do not include spaces, newlines, or whitespace-only changes in the summary.
- The most recent update must be placed at the top of the file.
- The current date is $(date +%Y-%m-%d).

### OUTPUT FORMAT & CONSTRAINTS ###
- Provide your response as raw text, with the summary and commit message separated by a unique delimiter.
- DO NOT include any explanations or conversational text.

Use this exact format for your output:
==SUMMARY_START==
<Your generated summary here>
==SUMMARY_END==
==COMMIT_MSG_START==
<Your generated commit message here>
==COMMIT_MSG_END==

Act autonomously. Do not ask for clarification. Begin analysis immediately when invoked.

${ESCAPED_DIFF}
"

# --- Generate summary and commit message with Gemini ---
AI_OUTPUT=$(printf "%s" "$GEMINI_PROMPT" | gemini -m gemini-2.5-flash) || {
    echo "Error: Gemini command failed. Please check its configuration and the error messages above." >&2
    exit 1
}

# Parse the AI output
SUMMARY=$(echo "$AI_OUTPUT" | sed -n '/==SUMMARY_START==/,/==SUMMARY_END==/p' | sed '1d;$d')
COMMIT_MSG=$(echo "$AI_OUTPUT" | sed -n '/==COMMIT_MSG_START==/,/==COMMIT_MSG_END==/p' | sed '1d;$d')

# Validate parsing
if [ -z "$SUMMARY" ] || [ -z "$COMMIT_MSG" ]; then
    echo "Error: Failed to parse AI output. Could not find summary or commit message." >&2
    echo "AI Output:" >&2
    echo "$AI_OUTPUT" >&2
    exit 1
fi

# Auto-detect version bump type if not specified and not none
if [ "$VERSION_BUMP" = "patch" ] && [ "$1" != "-v" ]; then
    # Check summary for keywords to suggest version bump
    if echo "$SUMMARY" | grep -qiE "breaking change|breaking:|incompatible|major change"; then
        echo "🔍 Detected breaking changes in commit. Suggesting MAJOR version bump."
        echo "   Use -v major to confirm, or -v minor/patch to override."
        VERSION_BUMP="major"
    elif echo "$SUMMARY" | grep -qiE "new feature|feat:|feature|add.*functionality|implement"; then
        echo "🔍 Detected new features in commit. Suggesting MINOR version bump."
        echo "   Use -v minor to confirm, or -v patch to override."
        VERSION_BUMP="minor"
    else
        echo "🔍 Detected bug fixes/refactoring. Using PATCH version bump."
    fi
    
    # Recalculate new version with detected bump type
    NEW_VERSION=$(increment_version "$CURRENT_VERSION" "$VERSION_BUMP")
    echo "📦 Version will be updated: $CURRENT_VERSION → $NEW_VERSION"
    echo ""
    
    # Give user 3 seconds to cancel if they disagree
    echo "Press Ctrl+C within 3 seconds to cancel and specify version manually..."
    sleep 3
fi

# Prepend the new content to UPDATES.md
if [ -f "$UPDATES_FILE" ]; then
    CURRENT_CONTENT=$(cat "$UPDATES_FILE")
    echo -e "${SUMMARY}\n\n${CURRENT_CONTENT}" > "$UPDATES_FILE"
else
    echo -e "${SUMMARY}" > "$UPDATES_FILE"
fi

# Update version file if needed
if [ "$VERSION_BUMP" != "none" ]; then
    # Check if the new version tag already exists
    if git rev-parse "v$NEW_VERSION" >/dev/null 2>&1; then
        echo "⚠️  Warning: Tag v$NEW_VERSION already exists!"
        echo "Please manually update the version or use a different bump type."
        exit 1
    fi
    
    # Update the version file
    echo "__version__ = \"$NEW_VERSION\"" > "$VERSION_FILE"
    git add "$VERSION_FILE"
    echo "✅ Updated __version__.py to $NEW_VERSION"
fi

# Add the updated UPDATES.md to staged files
git add "$UPDATES_FILE"

# Commit the changes
git commit -m "$COMMIT_MSG"

# --- Create git tag ---
# Use the NEW_VERSION if we bumped it, otherwise use CURRENT_VERSION
if [ "$VERSION_BUMP" != "none" ]; then
    FINAL_VERSION="$NEW_VERSION"
else
    FINAL_VERSION="$CURRENT_VERSION"
fi

# Extract subject line from commit message
TAG_MESSAGE=$(echo "$COMMIT_MSG" | head -n 1)

# Create annotated tag
git tag -a "v$FINAL_VERSION" -m "$TAG_MESSAGE"

echo "✅ Git tag v$FINAL_VERSION created successfully."

echo "✅ Changes summarized, UPDATES.md updated, and committed successfully."

# Display git push instructions
echo ""
echo "📌 To push your changes and tag to remote, run:"
echo "   git push origin $(git branch --show-current)"
echo "   git push origin v$FINAL_VERSION"