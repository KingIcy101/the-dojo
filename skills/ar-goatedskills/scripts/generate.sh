#!/usr/bin/env bash
# =============================================================================
# generate.sh — Nano Banana Pro Image Generator
# Wraps the Google Gemini image generation API with a clean shell interface.
#
# Usage:
#   bash generate.sh --prompt "..." --filename hero --resolution 2K
#   bash generate.sh --prompt "..." --input-image ./draft.png --resolution 4K
#   bash generate.sh --help
#
# API key resolution order:
#   1. --api-key argument
#   2. GEMINI_API_KEY environment variable
#   3. ~/.openclaw/openclaw.json → .skills.entries.nano-banana-pro.apiKey
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
PROMPT=""
FILENAME="generated"
RESOLUTION="1K"
INPUT_IMAGE=""
REF_IMAGES=()
API_KEY=""
OUTPUT_DIR=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

# Gemini image generation endpoint
API_BASE="https://generativelanguage.googleapis.com/v1beta/models"
MODEL="nano-banana-pro-preview"
ENDPOINT="${API_BASE}/${MODEL}:generateContent"

# ---------------------------------------------------------------------------
# Colors for output
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log_info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_step()  { echo -e "${CYAN}${BOLD}→${NC} $*"; }

usage() {
    cat <<EOF
${BOLD}🍌 Nano Banana Pro — Image Generator${NC}

USAGE:
    bash generate.sh [OPTIONS]

OPTIONS:
    --prompt TEXT         Image generation prompt (required)
    --filename NAME       Output filename base (default: generated)
    --resolution LEVEL    1K | 2K | 4K  (default: 1K)
    --input-image PATH    Input image for editing/iteration
    --ref-image PATH      Reference image for style matching (repeatable)
    --api-key KEY         Gemini API key (overrides env/config)
    --output-dir DIR      Output directory (default: ~/Desktop or cwd)
    --help                Show this help

RESOLUTION GUIDE:
    1K  → ~1024px  | Quick drafts, concept exploration     (~5s)
    2K  → ~2048px  | Refinement iterations, previews       (~12s)
    4K  → ~4096px  | Final deliverables, print quality     (~30s)

API KEY RESOLUTION:
    1. --api-key argument
    2. GEMINI_API_KEY environment variable
    3. ~/.openclaw/openclaw.json → .skills.entries.nano-banana-pro.apiKey

EXAMPLES:
    # Basic generation
    bash generate.sh --prompt "A golden retriever in autumn leaves, 16:9" \\
                     --filename dog_hero --resolution 1K

    # Edit existing image
    bash generate.sh --prompt "Add a red collar, keep everything else identical" \\
                     --input-image ./dog_hero_1K_20260221_143000.png \\
                     --filename dog_v2 --resolution 2K

    # With style reference
    bash generate.sh --prompt "A mountain lake in the style of the reference" \\
                     --ref-image ./style_reference.png \\
                     --filename mountain --resolution 2K

    # Multiple references
    bash generate.sh --prompt "..." \\
                     --ref-image ./ref1.png --ref-image ./ref2.png \\
                     --filename result --resolution 1K

    # Custom output directory
    bash generate.sh --prompt "..." --filename icon --resolution 4K \\
                     --output-dir ~/Projects/brand/
EOF
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt)        PROMPT="$2";           shift 2 ;;
        --filename)      FILENAME="$2";         shift 2 ;;
        --resolution)    RESOLUTION="${2^^}";   shift 2 ;;
        --input-image)   INPUT_IMAGE="$2";      shift 2 ;;
        --ref-image)     REF_IMAGES+=("$2");    shift 2 ;;
        --api-key)       API_KEY="$2";          shift 2 ;;
        --output-dir)    OUTPUT_DIR="$2";       shift 2 ;;
        --help|-h)       usage; exit 0 ;;
        *)
            log_error "Unknown argument: $1"
            echo ""
            usage
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Validate required arguments
# ---------------------------------------------------------------------------
if [[ -z "$PROMPT" ]]; then
    log_error "--prompt is required"
    echo ""
    usage
    exit 1
fi

if [[ "$RESOLUTION" != "1K" && "$RESOLUTION" != "2K" && "$RESOLUTION" != "4K" ]]; then
    log_error "--resolution must be 1K, 2K, or 4K (got: $RESOLUTION)"
    exit 1
fi

# ---------------------------------------------------------------------------
# Resolve API key
# ---------------------------------------------------------------------------
resolve_api_key() {
    # 1. Explicit argument
    if [[ -n "$API_KEY" ]]; then
        return
    fi

    # 2. Environment variable
    if [[ -n "${GEMINI_API_KEY:-}" ]]; then
        API_KEY="$GEMINI_API_KEY"
        log_info "Using API key from GEMINI_API_KEY environment variable"
        return
    fi

    # 3. openclaw.json
    if [[ -f "$OPENCLAW_CONFIG" ]]; then
        if command -v jq &>/dev/null; then
            local key
            key=$(jq -r '.skills.entries["nano-banana-pro"].apiKey // empty' "$OPENCLAW_CONFIG" 2>/dev/null || true)
            if [[ -n "$key" ]]; then
                API_KEY="$key"
                log_info "Using API key from openclaw.json"
                return
            fi
        else
            log_warn "jq not found — cannot read API key from openclaw.json. Install: sudo apt install jq"
        fi
    fi

    log_error "No API key found. Provide one via:"
    log_error "  --api-key KEY"
    log_error "  export GEMINI_API_KEY=your_key"
    log_error "  Set in ~/.openclaw/openclaw.json → .skills.entries.nano-banana-pro.apiKey"
    exit 1
}

# ---------------------------------------------------------------------------
# Resolve output directory
# ---------------------------------------------------------------------------
resolve_output_dir() {
    if [[ -n "$OUTPUT_DIR" ]]; then
        mkdir -p "$OUTPUT_DIR"
        return
    fi

    # Prefer ~/Desktop if it exists
    if [[ -d "$HOME/Desktop" ]]; then
        OUTPUT_DIR="$HOME/Desktop"
    else
        OUTPUT_DIR="$(pwd)"
    fi
}

# ---------------------------------------------------------------------------
# Map resolution to pixel guidance in prompt
# ---------------------------------------------------------------------------
resolution_to_guidance() {
    case "$RESOLUTION" in
        1K) echo "1024 pixel"  ;;
        2K) echo "2048 pixel"  ;;
        4K) echo "4096 pixel"  ;;
    esac
}

# ---------------------------------------------------------------------------
# Encode image to base64 with MIME type detection
# ---------------------------------------------------------------------------
encode_image() {
    local path="$1"
    if [[ ! -f "$path" ]]; then
        log_error "Image not found: $path"
        exit 1
    fi

    local ext="${path##*.}"
    ext="${ext,,}"  # lowercase

    local mime
    case "$ext" in
        jpg|jpeg)  mime="image/jpeg" ;;
        png)       mime="image/png"  ;;
        gif)       mime="image/gif"  ;;
        webp)      mime="image/webp" ;;
        *)
            # Try to detect via file command
            if command -v file &>/dev/null; then
                local detected
                detected=$(file --mime-type -b "$path")
                mime="$detected"
            else
                mime="image/png"
                log_warn "Unknown extension '$ext', assuming image/png"
            fi
            ;;
    esac

    local b64
    b64=$(base64 -w 0 "$path" 2>/dev/null || base64 "$path")  # Linux / macOS compat
    echo "${mime}|${b64}"
}

# ---------------------------------------------------------------------------
# Build JSON payload
# ---------------------------------------------------------------------------
build_payload() {
    local prompt="$1"
    local input_image="$2"
    shift 2
    local ref_images=("$@")

    # Start building the parts array for the user turn
    local parts_json=""

    # Add reference images first (style context before the prompt)
    for ref in "${ref_images[@]}"; do
        local encoded
        encoded=$(encode_image "$ref")
        local mime="${encoded%%|*}"
        local b64="${encoded#*|}"
        log_step "Encoding reference image: $(basename "$ref") (${mime})" >&2
        if [[ -n "$parts_json" ]]; then
            parts_json+=","
        fi
        parts_json+=$(cat <<EOF
{
    "inline_data": {
        "mime_type": "${mime}",
        "data": "${b64}"
    }
}
EOF
)
    done

    # Add input image if provided (for editing)
    if [[ -n "$input_image" ]]; then
        local encoded
        encoded=$(encode_image "$input_image")
        local mime="${encoded%%|*}"
        local b64="${encoded#*|}"
        log_step "Encoding input image for editing: $(basename "$input_image") (${mime})" >&2
        if [[ -n "$parts_json" ]]; then
            parts_json+=","
        fi
        parts_json+=$(cat <<EOF
{
    "inline_data": {
        "mime_type": "${mime}",
        "data": "${b64}"
    }
}
EOF
)
    fi

    # Add the text prompt last
    if [[ -n "$parts_json" ]]; then
        parts_json+=","
    fi
    # Escape the prompt for JSON
    local escaped_prompt
    escaped_prompt=$(printf '%s' "$prompt" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" 2>/dev/null \
        || printf '%s' "$prompt" | sed 's/"/\\"/g; s/\n/\\n/g' | awk '{printf "%s", $0}')

    parts_json+=$(cat <<EOF
{
    "text": ${escaped_prompt}
}
EOF
)

    # Build full payload
    cat <<EOF
{
    "contents": [
        {
            "role": "user",
            "parts": [
                ${parts_json}
            ]
        }
    ],
    "generationConfig": {
        "responseModalities": ["IMAGE", "TEXT"],
        "temperature": 1.0
    }
}
EOF
}

# ---------------------------------------------------------------------------
# Call the API and extract image
# ---------------------------------------------------------------------------
call_api() {
    local payload="$1"
    local output_path="$2"

    log_step "Calling Gemini API (model: ${MODEL})..." >&2

    local response_file
    response_file=$(mktemp /tmp/gemini_response_XXXXXX.json)

    # Make the API call
    local http_code
    http_code=$(curl -s -w "%{http_code}" \
        -X POST "${ENDPOINT}?key=${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "@-" \
        -o "$response_file" \
        <<< "$payload")

    if [[ "$http_code" != "200" ]]; then
        log_error "API call failed with HTTP $http_code"
        if [[ -f "$response_file" ]]; then
            log_error "Response body:"
            cat "$response_file" >&2
        fi
        rm -f "$response_file"
        exit 1
    fi

    # Check for API-level errors
    if command -v jq &>/dev/null; then
        local api_error
        api_error=$(jq -r '.error.message // empty' "$response_file" 2>/dev/null || true)
        if [[ -n "$api_error" ]]; then
            log_error "API error: $api_error"
            rm -f "$response_file"
            exit 1
        fi
    fi

    # Extract base64 image data
    log_step "Extracting image from response..." >&2

    local b64_data=""
    local mime_type=""

    if command -v jq &>/dev/null; then
        # Use jq for reliable extraction
        b64_data=$(jq -r '
            .candidates[0].content.parts[] |
            select(.inline_data != null or .inlineData != null) |
            (.inline_data.data // .inlineData.data)
        ' "$response_file" 2>/dev/null | head -1 || true)

        mime_type=$(jq -r '
            .candidates[0].content.parts[] |
            select(.inline_data != null or .inlineData != null) |
            (.inline_data.mime_type // .inlineData.mimeType)
        ' "$response_file" 2>/dev/null | head -1 || true)

        # Also print any text response from the model
        local text_response
        text_response=$(jq -r '
            .candidates[0].content.parts[] |
            select(.text != null) |
            .text
        ' "$response_file" 2>/dev/null || true)

        if [[ -n "$text_response" ]]; then
            echo "" >&2
            echo -e "${CYAN}Model response:${NC} $text_response" >&2
            echo "" >&2
        fi
    else
        # Fallback: python3-based extraction
        b64_data=$(python3 -c "
import json, sys
with open('$response_file') as f:
    data = json.load(f)
parts = data['candidates'][0]['content']['parts']
for p in parts:
    if 'inline_data' in p:
        print(p['inline_data']['data'])
        break
    if 'inlineData' in p:
        print(p['inlineData']['data'])
        break
" 2>/dev/null || true)

        mime_type=$(python3 -c "
import json, sys
with open('$response_file') as f:
    data = json.load(f)
parts = data['candidates'][0]['content']['parts']
for p in parts:
    if 'inline_data' in p:
        print(p['inline_data'].get('mime_type','image/png'))
        break
    if 'inlineData' in p:
        print(p['inlineData'].get('mimeType','image/png'))
        break
" 2>/dev/null || "image/png")
    fi

    rm -f "$response_file"

    if [[ -z "$b64_data" ]]; then
        log_error "No image data found in API response"
        log_error "The model may have declined to generate the image, or there was a parsing error"
        log_error "Try simplifying the prompt or checking your API key permissions"
        exit 1
    fi

    # Determine file extension from mime type
    local ext="png"
    case "${mime_type:-image/png}" in
        image/jpeg) ext="jpg" ;;
        image/webp) ext="webp" ;;
        image/gif)  ext="gif" ;;
        *)          ext="png" ;;
    esac

    # Update output path if extension differs
    local final_output="${output_path%.png}.${ext}"

    # Decode base64 to file
    log_step "Decoding image to file..." >&2
    echo "$b64_data" | base64 -d > "$final_output" 2>/dev/null \
        || echo "$b64_data" | base64 --decode > "$final_output"

    echo "$final_output"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    echo ""
    echo -e "${BOLD}${CYAN}🍌 Nano Banana Pro — Image Generator${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    resolve_api_key
    resolve_output_dir

    # Check dependencies
    if ! command -v curl &>/dev/null; then
        log_error "curl is required but not found. Install: sudo apt install curl"
        exit 1
    fi

    if ! command -v base64 &>/dev/null; then
        log_error "base64 is required but not found (should be part of coreutils)"
        exit 1
    fi

    if ! command -v python3 &>/dev/null && ! command -v jq &>/dev/null; then
        log_warn "Neither python3 nor jq found. JSON processing may be limited."
        log_warn "Recommend: sudo apt install jq"
    fi

    # Build output filename with timestamp
    local timestamp
    timestamp=$(date +"%Y%m%d_%H%M%S")
    local output_filename="${FILENAME}_${RESOLUTION}_${timestamp}.png"
    local output_path="${OUTPUT_DIR}/${output_filename}"

    # Log what we're doing
    log_info "Prompt:     $(echo "$PROMPT" | head -c 120)..."
    log_info "Resolution: $RESOLUTION"
    log_info "Output:     $output_path"
    [[ -n "$INPUT_IMAGE" ]] && log_info "Input img:  $INPUT_IMAGE"
    for ref in "${REF_IMAGES[@]}"; do
        log_info "Ref img:    $ref"
    done
    echo ""

    # Augment prompt with resolution guidance
    local res_guidance
    res_guidance=$(resolution_to_guidance)
    local augmented_prompt="${PROMPT}

[Technical note: Render at ${RESOLUTION} / ${res_guidance} resolution quality.]"

    # Build payload
    log_step "Building API payload..."
    local payload
    payload=$(build_payload "$augmented_prompt" "$INPUT_IMAGE" "${REF_IMAGES[@]}")

    # Call API
    local start_time
    start_time=$(date +%s)

    local final_path
    final_path=$(call_api "$payload" "$output_path")

    local end_time
    end_time=$(date +%s)
    local elapsed=$((end_time - start_time))

    # Success
    echo ""
    echo -e "${GREEN}${BOLD}✓ Image generated successfully!${NC}"
    echo -e "  📁 File:     ${BOLD}${final_path}${NC}"
    echo -e "  ⏱  Time:     ${elapsed}s"
    echo -e "  📐 Resolution: ${RESOLUTION}"

    # Get file size if possible
    if command -v du &>/dev/null; then
        local filesize
        filesize=$(du -h "$final_path" 2>/dev/null | cut -f1 || echo "unknown")
        echo -e "  💾 Size:     ${filesize}"
    fi

    echo ""

    # Print the next-step command for iteration
    echo -e "${CYAN}Next step — iterate on this image:${NC}"
    local script_path
    script_path="$(realpath "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")"
    echo -e "  bash \"${script_path}\" \\"
    echo -e "    --prompt \"[Your refinement prompt]\" \\"
    echo -e "    --input-image \"${final_path}\" \\"
    echo -e "    --filename \"${FILENAME}_v2\" \\"
    echo -e "    --resolution 2K"
    echo ""
}

main
