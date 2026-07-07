#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="${MODEL_DIR:-/Volumes/External SSD/AI/models/glm}"
MODEL_REPO="${MODEL_REPO:-unsloth/GLM-5-GGUF}"
MODEL_FILE="${MODEL_FILE:-GLM-5-UD-TQ1_0.gguf}"
MODEL_URL="${MODEL_URL:-https://huggingface.co/${MODEL_REPO}/resolve/main/${MODEL_FILE}?download=true}"
EXPECTED_BYTES="${EXPECTED_BYTES:-176142433184}"
MODEL_PATH="${MODEL_PATH:-${MODEL_DIR}/${MODEL_FILE}}"

CTX_SIZE="${CTX_SIZE:-8192}"
THREADS="${THREADS:-32}"
THREADS_BATCH="${THREADS_BATCH:-${THREADS}}"
PREDICT="${PREDICT:-1024}"
N_GPU_LAYERS="${N_GPU_LAYERS:-auto}"
CACHE_TYPE_K="${CACHE_TYPE_K:-q8_0}"
CACHE_TYPE_V="${CACHE_TYPE_V:-q8_0}"
REASONING="${REASONING:-off}"

usage() {
  cat <<EOF
Usage:
  ./glm5.sh                 Download/resume the model, then run a smoke test
  ./glm5.sh download        Download/resume only
  ./glm5.sh test            Run smoke test only
  ./glm5.sh run "prompt"    Run one prompt
  ./glm5.sh chat            Start interactive chat
  ./glm5.sh path            Print model path

Defaults:
  MODEL_REPO=${MODEL_REPO}
  MODEL_FILE=${MODEL_FILE}
  MODEL_PATH=${MODEL_PATH}

Useful overrides:
  MODEL_DIR="/Volumes/External SSD/AI/models/glm" ./glm5.sh
  CTX_SIZE=16384 PREDICT=2048 REASONING=on ./glm5.sh chat
EOF
}

die_external_disk_permission() {
  cat >&2 <<EOF
Cannot write to:
  ${MODEL_DIR}

macOS is blocking this shell from writing to the external disk.
Fix it once, then rerun:
  System Settings -> Privacy & Security -> Full Disk Access
  enable your terminal app / Codex, or run this script from a terminal that already has access.

Command to rerun:
  cd "$(pwd)" && ./glm5.sh
EOF
  exit 13
}

file_size() {
  if stat -f '%z' "$1" >/dev/null 2>&1; then
    stat -f '%z' "$1"
  else
    stat -c '%s' "$1"
  fi
}

require_llama_cli() {
  if ! command -v llama-cli >/dev/null 2>&1; then
    echo "llama-cli not found. Install llama.cpp first." >&2
    exit 127
  fi
}

ensure_model_dir() {
  mkdir -p "${MODEL_DIR}" 2>/dev/null || die_external_disk_permission
  touch "${MODEL_DIR}/.glm-write-test" 2>/dev/null || die_external_disk_permission
  rm -f "${MODEL_DIR}/.glm-write-test" 2>/dev/null || true
}

download_model() {
  ensure_model_dir

  if [[ -f "${MODEL_PATH}" ]]; then
    actual_bytes="$(file_size "${MODEL_PATH}")"
    if [[ "${EXPECTED_BYTES}" != "0" && "${actual_bytes}" == "${EXPECTED_BYTES}" ]]; then
      echo "Model already present: ${MODEL_PATH}"
      return 0
    fi
    echo "Model exists but size is ${actual_bytes}; resuming download."
  fi

  echo "Downloading ${MODEL_REPO}/${MODEL_FILE}"
  echo "Target: ${MODEL_PATH}"

  curl \
    --fail \
    --location \
    --continue-at - \
    --retry 20 \
    --retry-delay 10 \
    --retry-all-errors \
    --connect-timeout 30 \
    --output "${MODEL_PATH}" \
    "${MODEL_URL}"

  actual_bytes="$(file_size "${MODEL_PATH}")"
  echo "Downloaded bytes: ${actual_bytes}"

  if [[ "${EXPECTED_BYTES}" != "0" && "${actual_bytes}" != "${EXPECTED_BYTES}" ]]; then
    echo "Expected ${EXPECTED_BYTES} bytes, got ${actual_bytes} bytes." >&2
    echo "Rerun ./glm5.sh download to resume." >&2
    exit 2
  fi

  echo "Download complete."
}

require_model() {
  if [[ ! -f "${MODEL_PATH}" ]]; then
    echo "Model not found: ${MODEL_PATH}" >&2
    echo "Run: ./glm5.sh download" >&2
    exit 1
  fi
}

smoke_test() {
  require_llama_cli
  require_model

  echo "Testing model: ${MODEL_PATH}"
  echo "Size: $(du -h "${MODEL_PATH}" | awk '{print $1}')"

  llama-cli \
    --model "${MODEL_PATH}" \
    --ctx-size 4096 \
    --threads 16 \
    --threads-batch 16 \
    --gpu-layers auto \
    --cache-type-k q8_0 \
    --cache-type-v q8_0 \
    --jinja \
    --reasoning off \
    --single-turn \
    --no-display-prompt \
    --predict 64 \
    --prompt "Answer in one short sentence: 84 * 3 / 2 = ?"
}

run_prompt() {
  require_llama_cli
  require_model

  args=(
    --model "${MODEL_PATH}"
    --ctx-size "${CTX_SIZE}"
    --threads "${THREADS}"
    --threads-batch "${THREADS_BATCH}"
    --gpu-layers "${N_GPU_LAYERS}"
    --cache-type-k "${CACHE_TYPE_K}"
    --cache-type-v "${CACHE_TYPE_V}"
    --jinja
    --reasoning "${REASONING}"
    --predict "${PREDICT}"
  )
  llama-cli "${args[@]}" --single-turn --no-display-prompt --prompt "$*"
}

chat() {
  require_llama_cli
  require_model

  args=(
    --model "${MODEL_PATH}"
    --ctx-size "${CTX_SIZE}"
    --threads "${THREADS}"
    --threads-batch "${THREADS_BATCH}"
    --gpu-layers "${N_GPU_LAYERS}"
    --cache-type-k "${CACHE_TYPE_K}"
    --cache-type-v "${CACHE_TYPE_V}"
    --jinja
    --reasoning "${REASONING}"
    --predict "${PREDICT}"
  )
  llama-cli "${args[@]}" --conversation
}

cmd="${1:-all}"
case "${cmd}" in
  all)
    download_model
    smoke_test
    ;;
  download)
    download_model
    ;;
  test)
    smoke_test
    ;;
  run)
    shift
    if [[ $# -eq 0 ]]; then
      echo "Missing prompt. Example: ./glm5.sh run \"hello\"" >&2
      exit 64
    fi
    run_prompt "$@"
    ;;
  chat)
    chat
    ;;
  path)
    echo "${MODEL_PATH}"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    run_prompt "$@"
    ;;
esac
