#!/bin/bash
# Script: update.sh
# Description: Safely downloads and extracts configuration templates from GitHub repository
# Author: Thomas Schmelzer
# Usage: ./update.sh

set -euo pipefail  # Fail on errors, undefined variables, and pipeline failures

# ---- Configuration ----
REPO_URL="https://github.com/tschm/.config-templates"
TEMP_DIR=".temp_templates"  # Avoid naming conflicts with possible existing dirs
BRANCH_NAME="config-sync"
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# ---- Helper Functions ----
die() {
  echo "❌ Error: $*" >&2
  exit 1
}

# ---- Cleanup Function ----
cleanup() {
  # This runs on script exit (normal or error)
  echo "🧹 Cleaning up temporary files..."
  rm -rf "${TEMP_DIR}" templates.zip
  git checkout --quiet "${ORIGINAL_BRANCH}"
}

# ---- Register cleanup trap ----
trap cleanup EXIT

# ---- Check Dependencies ----
command -v curl >/dev/null || die "🌐 curl is not installed."
command -v unzip >/dev/null || die "📂 unzip is not installed."
command -v git >/dev/null || die "🔄 git is not installed."

echo "🔍 Check in a repo"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "🚫 Not inside a Git repository."

# Checkout/Create branch
if git show-ref --verify "refs/heads/${BRANCH_NAME}"; then
  echo "🔀 Checking out existing branch ${BRANCH_NAME}..."
  git checkout "${BRANCH_NAME}"
else
  echo "🌱 Creating and checking out new branch ${BRANCH_NAME}..."
  git checkout -b "${BRANCH_NAME}"
fi

git status

# ---- Download Templates ----
echo "⬇️ Downloading templates from ${REPO_URL}..."
if ! curl -sSL -o templates.zip "${REPO_URL}/archive/refs/heads/main.zip"; then
  die "❌ Failed to download templates."
fi

# ---- Extract Templates ----
echo "📦 Extracting templates..."
if ! unzip -q templates.zip -d "${TEMP_DIR}"; then
  die "❌ Failed to extract templates."
fi

echo "🗑️ Remove the zip file..."
rm templates.zip

# ---- Verify Extraction ----
if [[ ! -d "${TEMP_DIR}/.config-templates-main" ]]; then
  die "❌ Extracted directory structure doesn't match expectations."
fi

# ---- Git Operations ----
echo "🔄 Updating git repository..."

# Stash any existing changes to avoid conflicts
# git stash push --quiet --include-untracked --message "update.sh auto-stash"

# Copy new files (preserving existing files with --ignore-existing)
echo "📋 Copying template files to current directory..."
cp -fR "${TEMP_DIR}/.config-templates-main/." . || {
  die "❌ Failed to copy templates"
}

echo "🗑️ Removing temporary directory..."
rm -rf "${TEMP_DIR}"

echo "🔄 Checking for changes..."
git diff-index --quiet HEAD --

# Commit changes if there are any
if git diff-index --quiet HEAD --; then
  echo "✅ No changes to commit."
else
  git add .
  if git commit -m "Update configuration templates from ${REPO_URL}" --no-verify; then
    echo "✅ Changes committed."
  else
    echo "⚠️ Could not commit changes."
  fi
fi

# Always push the branch to ensure it exists on GitHub
echo "🚀 Ensuring branch '${BRANCH_NAME}' is pushed to GitHub..."
git push -u origin "${BRANCH_NAME}" || echo "⚠️ Could not push '${BRANCH_NAME}' to remote."

echo "🔍 Status of current branch..."
git status

echo "✨ Done!"
