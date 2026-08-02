#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
targets=(
  "/Users/${USER}/.codex/skills/voicelatch"
  "/Users/${USER}/.openclaw/skills/voicelatch"
)

while IFS= read -r agent_dir; do
  targets+=("${agent_dir}/codex-home/skills/voicelatch")
done < <(find "/Users/${USER}/.openclaw/agents" -mindepth 2 -maxdepth 2 -type d -name agent 2>/dev/null | sort)

for target in "${targets[@]}"; do
  mkdir -p "$(dirname "$target")"
  if [[ -L "$target" && "$(readlink "$target")" == "$repo_dir" ]]; then
    continue
  fi
  if [[ -e "$target" || -L "$target" ]]; then
    echo "Refusing to replace existing target: $target" >&2
    exit 1
  fi
  ln -s "$repo_dir" "$target"
done

printf 'Installed VoiceLatch into %s skill roots.\n' "${#targets[@]}"
