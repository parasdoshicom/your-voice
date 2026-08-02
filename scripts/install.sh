#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
targets=(
  "/Users/${USER}/.codex/skills/your-voice"
  "/Users/${USER}/.openclaw/skills/your-voice"
)

legacy_targets=(
  "/Users/${USER}/.codex/skills/voicelatch"
  "/Users/${USER}/.openclaw/skills/voicelatch"
)

while IFS= read -r agent_dir; do
  targets+=("${agent_dir}/codex-home/skills/your-voice")
  legacy_targets+=("${agent_dir}/codex-home/skills/voicelatch")
done < <(find "/Users/${USER}/.openclaw/agents" -mindepth 2 -maxdepth 2 -type d -name agent 2>/dev/null | sort)

install_target() {
  local target="$1"
  mkdir -p "$(dirname "$target")"
  if [[ -e "$target" && "$(realpath "$target")" == "$repo_dir" ]]; then
    return 0
  fi
  if [[ -e "$target" || -L "$target" ]]; then
    echo "Refusing to replace existing target: $target" >&2
    exit 1
  fi
  ln -s "$repo_dir" "$target"
}

for target in "${targets[@]}"; do
  install_target "$target"
done

for target in "${legacy_targets[@]}"; do
  install_target "$target"
done

printf 'Installed Your Voice into %s skill roots; legacy voicelatch aliases remain available.\n' "${#targets[@]}"
