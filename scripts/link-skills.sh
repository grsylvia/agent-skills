#!/usr/bin/env bash
# Install the external skills in external-skills.txt, then link every skill
# into the Codex and Claude Code skill directories.
#
# Usage:
#   scripts/link-skills.sh                  install and link
#   scripts/link-skills.sh --check-updates  list upstream commits newer than each pin
#
# Run it after you clone or pull. It is safe to run again:
#   - It clones missing external skills and checks out their pinned commits.
#   - It adds links for new skills.
#   - It removes broken links that point into this repository or the external directory.
#   - It never replaces a real file or folder, or a link that points somewhere else.
#
# Override the locations with AGENTS_SKILLS_DIR, CLAUDE_SKILLS_DIR, and EXTERNAL_SKILLS_DIR.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
manifest="$repo/external-skills.txt"
agents="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
claude="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
external="${EXTERNAL_SKILLS_DIR:-$HOME/.agents/external}"

# Print the physical path of a directory, or nothing if it does not resolve.
physical() { (cd "$1" 2>/dev/null && pwd -P) || true; }

# Print "name url commit" for each entry in the manifest.
external_skills() {
    [ -f "$manifest" ] || return 0
    sed -e 's/#.*//' "$manifest" | awk 'NF == 3 { print $1, $2, $3 }'
}

if [ "${1:-}" = "--check-updates" ]; then
    external_skills | while read -r name url commit; do
        upstream="$(git ls-remote "$url" HEAD | cut -f1)"
        if [ "$upstream" = "$commit" ]; then
            echo "$name: up to date ($commit)"
            continue
        fi
        echo "$name: pinned $commit, upstream $upstream"
        dir="$external/$name"
        if [ -d "$dir/.git" ]; then
            git -C "$dir" fetch --quiet origin
            git -C "$dir" log --oneline "$commit..$upstream"
            echo "  review: git -C $dir diff $commit $upstream"
        fi
    done
    exit 0
elif [ $# -gt 0 ]; then
    sed -n '5,7p' "$0" >&2
    exit 2
fi

# Clone each external skill outside this repository, pin it, and link it in.
# The link is listed in .git/info/exclude so it never appears as a change.
exclude="$(git -C "$repo" rev-parse --git-path info/exclude)"
case "$exclude" in /*) ;; *) exclude="$repo/$exclude" ;; esac
external_skills | while read -r name url commit; do
    dir="$external/$name"
    if [ ! -d "$dir/.git" ]; then
        mkdir -p "$external"
        git clone --quiet "$url" "$dir"
        echo "cloned  $dir"
    elif [ "$(git -C "$dir" remote get-url origin)" != "$url" ]; then
        echo "skipped $dir: origin is not $url" >&2
        continue
    fi
    if [ "$(git -C "$dir" rev-parse HEAD)" != "$commit" ]; then
        if [ -n "$(git -C "$dir" status --porcelain --untracked-files=no)" ]; then
            echo "skipped $dir: has local changes; not moved to $commit" >&2
            continue
        fi
        git -C "$dir" cat-file -e "$commit^{commit}" 2>/dev/null || git -C "$dir" fetch --quiet origin
        git -C "$dir" -c advice.detachedHead=false checkout --quiet "$commit"
        echo "pinned  $name at $commit"
    fi
    target="$repo/$name"
    if [ ! -e "$target" ] && [ ! -L "$target" ]; then
        ln -s "$dir" "$target"
        echo "linked  $target -> $dir"
    elif [ "$(physical "$target")" != "$(physical "$dir")" ]; then
        echo "skipped $target: exists and is not $dir" >&2
    fi
    mkdir -p "$(dirname "$exclude")"
    grep -qxF "/$name" "$exclude" 2>/dev/null || echo "/$name" >> "$exclude"
done

# Codex reads the whole directory, so link the repository itself.
if [ ! -e "$agents" ] && [ ! -L "$agents" ]; then
    mkdir -p "$(dirname "$agents")"
    ln -s "$repo" "$agents"
    echo "linked  $agents -> $repo"
elif [ "$(physical "$agents")" != "$repo" ]; then
    echo "skipped $agents: exists and is not this repository" >&2
fi

# Claude Code also keeps synced skills in its directory, so link each skill.
mkdir -p "$claude"
for skill in "$repo"/*/; do
    skill="${skill%/}"
    [ -f "$skill/SKILL.md" ] || continue
    name="$(basename "$skill")"
    target="$claude/$name"
    if [ ! -e "$target" ] && [ ! -L "$target" ]; then
        ln -s "$skill" "$target"
        echo "linked  $target -> $skill"
    elif [ "$(physical "$target")" != "$(physical "$skill")" ]; then
        echo "skipped $target: exists and is not this skill" >&2
    fi
done

# Remove broken links left by skills that were deleted or renamed.
for link in "$claude"/*; do
    [ -L "$link" ] && [ ! -e "$link" ] || continue
    dest="$(readlink "$link")"
    case "$dest" in
        "$repo"/* | "$agents"/* | "$external"/*)
            rm "$link"
            echo "removed $link (broken: $dest)"
            ;;
    esac
done
