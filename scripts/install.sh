#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
user_home="${HOME:?HOME must be set}"

targets=(
  "${user_home}/.agents/skills/your-voice"
  "${user_home}/.hermes/skills/your-voice"
)

legacy_targets=(
  "${user_home}/.agents/skills/voicelatch"
  "${user_home}/.codex/skills/your-voice"
  "${user_home}/.codex/skills/voicelatch"
  "${user_home}/.hermes/skills/voicelatch"
)

openclaw_root="${user_home}/.openclaw"
if [[ -d "$openclaw_root" ]]; then
  targets+=("${openclaw_root}/skills/your-voice")
  legacy_targets+=("${openclaw_root}/skills/voicelatch")

  while IFS= read -r agent_dir; do
    targets+=("${agent_dir}/codex-home/skills/your-voice")
    legacy_targets+=("${agent_dir}/codex-home/skills/voicelatch")
  done < <(find "${openclaw_root}/agents" -mindepth 2 -maxdepth 2 -type d -name agent 2>/dev/null | sort)
fi

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

remove_legacy_link() {
  local target="$1"
  if [[ -L "$target" && "$(realpath "$target")" == "$repo_dir" ]]; then
    rm "$target"
  elif [[ -e "$target" || -L "$target" ]]; then
    echo "Refusing to remove non-canonical legacy target: $target" >&2
    exit 1
  fi
}

for target in "${targets[@]}"; do
  install_target "$target"
done

for target in "${legacy_targets[@]}"; do
  remove_legacy_link "$target"
done

printf 'Installed one Your Voice checkout into %s active skill roots.\n' "${#targets[@]}"
