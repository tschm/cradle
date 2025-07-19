#!/bin/bash
# Script: update.sh
# Description: Safely downloads and extracts configuration templates from GitHub repository
# Author: Thomas Schmelzer (with revisions)

set -euo pipefail

# ---- Configuration ----
REPO_URL="https://github.com/tschm/.config-templates"
BRANCH_NAME="config-sync"
TEMP_DIR="$(mktemp -d -t config-templates-XXXXXXXX)"
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# ---- Command-line flags ----
YES=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --yes|-y) YES=true ;;
    --dry-run|-n) DRY_RUN=true ;;
    *) echo "❓ Unknown option: $arg"; exit 1 ;;
  esac
done

# ---- Helper Functions ----
die() {
  echo "❌ Error: $*" >&2
  exit 1
}

info() {
  echo "🔹 $*"
}

# ---- Cleanup ----
cleanup() {
  echo "🧹 Cleaning up..."
  rm -rf "$TEMP_DIR" templates.zip
  if [[ "$(git rev-parse --abbrev-ref HEAD)" != "$ORIGINAL_BRANCH" ]]; then
    if git show-ref --quiet "refs/heads/${ORIGINAL_BRANCH}"; then
      git checkout "$ORIGINAL_BRANCH"
    else
      echo "⚠️ Original branch '${ORIGINAL_BRANCH}' no longer exists."
    fi
  fi
}
trap cleanup EXIT

# ---- Dependency Checks ----
command -v curl >/dev/null || die "curl is not installed."
command -v unzip >/dev/null || die "unzip is not installed."
command -v git >/dev/null || die "git is not installed."

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Not inside a Git repository."

# ---- Check for uncommitted changes ----
if ! git diff-index --quiet HEAD --; then
  echo "⚠️ Uncommitted changes detected in working directory."
fi

# ---- Confirm Overwrite ----
if [[ $YES == false && $DRY_RUN == false ]]; then
  read -p "⚠️ This may overwrite files in your current directory. Continue? (y/N): " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || die "Aborted by user."
fi

# ---- Checkout or Create Branch ----
if [[ "$(git rev-parse --abbrev-ref HEAD)" != "$BRANCH_NAME" ]]; then
  if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
    info "Checking out existing branch '$BRANCH_NAME'..."
    git checkout "$BRANCH_NAME"
  else
    info "Creating and checking out new branch '$BRANCH_NAME'..."
    git checkout -b "$BRANCH_NAME"
  fi
fi

# ---- Download ----
info "Downloading templates from $REPO_URL..."
curl -sSL -o templates.zip "$REPO_URL/archive/refs/heads/main.zip" || die "Failed to download templates."

# ---- Extract ----
info "Extracting templates..."
unzip -q templates.zip -d "$TEMP_DIR" || die "Failed to unzip."
rm -f templates.zip

EXTRACTED_DIR="${TEMP_DIR}/.config-templates-main"
[[ -d "$EXTRACTED_DIR" ]] || die "Extracted directory structure doesn't match expectations."

# ---- Dry Run Exit Point ----
if [[ $DRY_RUN == true ]]; then
  echo "🧪 Dry-run complete. No files were copied or committed."
  exit 0
fi

# ---- Copy Files ----
info "Copying template files..."
cp -Rf "$EXTRACTED_DIR/." . || die "Failed to copy template files."

# ---- Commit Changes ----
info "Checking for file changes..."
if git diff-index --quiet HEAD --; then
  echo "✅ No changes to commit."
else
  git add .
  git commit -m "Update configuration templates from $REPO_URL" --no-verify && \
    echo "✅ Changes committed." || echo "⚠️ Failed to commit changes."
fi

# ---- Push Branch ----
info "Pushing branch '$BRANCH_NAME' to origin..."
git push -u origin "$BRANCH_NAME" || echo "⚠️ Could not push to remote."

# ---- Final Status ----
git status
echo "✨ Done!"

