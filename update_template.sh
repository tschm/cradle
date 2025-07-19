#!/bin/bash
# Script: update.sh
# Description: Safely updates config files from GitHub without branch switching
# Author: Thomas Schmelzer

set -euo pipefail

# ---- Configuration ----
REPO_URL="https://github.com/tschm/.config-templates"
TEMP_DIR="$(mktemp -d)"

# ---- Colors ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ---- Helper Functions ----
die() {
  echo -e "${RED}❌ Error:${NC} $*" >&2
  exit 1
}

info() {
  echo -e "${BLUE}🔹 $*${NC}"
}

success() {
  echo -e "${GREEN}✅ $*${NC}"
}

# ---- Main Script ----
main() {
  # Check dependencies
  command -v curl >/dev/null || die "curl required"
  command -v unzip >/dev/null || die "unzip required"

  # Download templates
  info "Downloading templates..."
  curl -sSL -o templates.zip "$REPO_URL/archive/refs/heads/main.zip" || die "Download failed"

  # Extract templates
  info "Extracting..."
  unzip -q templates.zip -d "$TEMP_DIR" || die "Extraction failed"
  rm -f templates.zip

  EXTRACTED_DIR="${TEMP_DIR}/.config-templates-main"
  [ -d "$EXTRACTED_DIR" ] || die "Invalid template structure"

  # Safe copy (only updates existing files)
  updated=0
  while IFS= read -r -d '' file; do
    target_file="./${file#$EXTRACTED_DIR/}"
    #if [ -f "$target_file" ]; then
    if ! cmp -s "$file" "$target_file"; then
      cp -v "$file" "$target_file"
      ((updated++))
    fi
    #fi
  done < <(find "$EXTRACTED_DIR" -type f -print0)

  success "Done. $updated files updated."
  echo "Note: No files were deleted or newly created."
}

# Cleanup
cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

main "$@"