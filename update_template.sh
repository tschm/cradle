#!/bin/bash
# Script: update.sh
# Description: Safely downloads and extracts configuration templates from GitHub repository
# Author: Thomas Schmelzer (with revisions)

set -euo pipefail

# ---- Configuration ----
REPO_URL="https://github.com/tschm/.config-templates"
BRANCH_NAME="config-sync"
TEMP_DIR="$(mktemp -d -t config-templates-XXXXXXXXXX)"
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
SCRIPT_NAME=$(basename "$0")
LOG_FILE="/tmp/${SCRIPT_NAME}.log"

# ---- Colors ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ---- Command-line flags ----
YES=false
DRY_RUN=false
VERBOSE=false

# ---- Initialize logging ----
exec > >(tee -a "$LOG_FILE") 2>&1

# ---- Helper Functions ----
die() {
  echo -e "${RED}❌ Error:${NC} $*" >&2
  echo -e "${BLUE}ℹ️ See detailed logs at: $LOG_FILE${NC}" >&2
  exit 1
}

info() {
  echo -e "${BLUE}🔹 $*${NC}"
}

success() {
  echo -e "${GREEN}✅ $*${NC}"
}

warning() {
  echo -e "${YELLOW}⚠️ $*${NC}"
}

prompt_confirm() {
  if [[ $YES == true ]]; then
    return 0
  fi

  while true; do
    read -rp "$1 [y/N] " reply
    case "$reply" in
      [yY][eE][sS]|[yY]) return 0 ;;
      [nN][oO]|[nN]|"") return 1 ;;
      *) echo "Please answer yes or no." ;;
    esac
  done
}

check_dependencies() {
  local missing=()
  for cmd in curl unzip git; do
    if ! command -v "$cmd" >/dev/null; then
      missing+=("$cmd")
    fi
  done

  if [[ ${#missing[@]} -gt 0 ]]; then
    die "Missing dependencies: ${missing[*]}. Please install them first."
  fi

  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    die "Not inside a Git repository. Please run this script from within a git repository."
  fi
}

show_changes() {
  info "The following changes will be made:"
  git --no-pager diff --name-status || true
  echo ""
}

# ---- Main Script ----
main() {
  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --yes|-y) YES=true ;;
      --dry-run|-n) DRY_RUN=true ;;
      --verbose|-v) VERBOSE=true ;;
      --help|-h)
        echo "Usage: $0 [options]"
        echo "Options:"
        echo "  -y, --yes       Skip confirmation prompts"
        echo "  -n, --dry-run   Simulate execution without making changes"
        echo "  -v, --verbose   Show detailed output"
        echo "  -h, --help      Show this help message"
        exit 0
        ;;
      *) die "Unknown option: $1" ;;
    esac
    shift
  done

  check_dependencies

  # Check for uncommitted changes
  if ! git diff-index --quiet HEAD --; then
    warning "Uncommitted changes detected in working directory."
    show_changes
    if ! prompt_confirm "Continue with uncommitted changes?"; then
      die "Aborted by user."
    fi
  fi

  # Confirm overwrite
  if [[ $DRY_RUN == false ]]; then
    if ! prompt_confirm "This may overwrite files in your current directory. Continue?"; then
      die "Aborted by user."
    fi
  fi

  # Checkout or create branch
  if [[ "$(git rev-parse --abbrev-ref HEAD)" != "$BRANCH_NAME" ]]; then
    if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
      info "Checking out existing branch '$BRANCH_NAME'..."
      git checkout "$BRANCH_NAME" || die "Failed to checkout branch"
    else
      info "Creating and checking out new branch '$BRANCH_NAME'..."
      git checkout -b "$BRANCH_NAME" || die "Failed to create new branch"
    fi
  fi

  # Download templates
  info "Downloading templates from $REPO_URL..."
  if ! curl -sSL -o templates.zip "$REPO_URL/archive/refs/heads/main.zip"; then
    die "Failed to download templates. Check your internet connection."
  fi

  # Extract templates
  info "Extracting templates..."
  if ! unzip -q templates.zip -d "$TEMP_DIR"; then
    die "Failed to unzip templates. The download might be corrupted."
  fi
  rm -f templates.zip

  EXTRACTED_DIR="${TEMP_DIR}/.config-templates-main"
  if [[ ! -d "$EXTRACTED_DIR" ]]; then
    die "Extracted directory structure doesn't match expectations."
  fi

  # Dry run exit point
  if [[ $DRY_RUN == true ]]; then
    info "The following files would be copied:"
    find "$EXTRACTED_DIR" -type f -printf "  - %P\n"
    success "Dry-run complete. No files were actually copied or committed."
    exit 0
  fi

  # Copy files
  info "Copying template files..."
  if ! cp -Rf "$EXTRACTED_DIR/." .; then
    die "Failed to copy template files. Check permissions."
  fi

  # Commit changes
  info "Checking for file changes..."
  if git diff-index --quiet HEAD --; then
    success "No changes to commit."
  else
    show_changes
    if git add . && git commit -m "Update configuration templates from $REPO_URL" --no-verify; then
      success "Changes committed."
    else
      warning "Failed to commit changes."
    fi
  fi

  # Push branch
  info "Pushing branch '$BRANCH_NAME' to origin..."
  if git push -u origin "$BRANCH_NAME"; then
    success "Branch successfully pushed to remote."
  else
    warning "Could not push to remote. You may need to push manually."
  fi

  # Final status
  git status --short
  success "Operation completed successfully!"
}

# ---- Cleanup ----
cleanup() {
  if [[ $VERBOSE == true ]]; then
    info "Cleaning up temporary files..."
  fi
  rm -rf "$TEMP_DIR" templates.zip 2>/dev/null || true

  if [[ "$(git rev-parse --abbrev-ref HEAD)" != "$ORIGINAL_BRANCH" ]]; then
    if git show-ref --quiet "refs/heads/${ORIGINAL_BRANCH}"; then
      if [[ $VERBOSE == true ]]; then
        info "Returning to original branch '$ORIGINAL_BRANCH'..."
      fi
      git checkout "$ORIGINAL_BRANCH" >/dev/null 2>&1 || true
    else
      warning "Original branch '${ORIGINAL_BRANCH}' no longer exists."
    fi
  fi
}

trap cleanup EXIT

main "$@"

