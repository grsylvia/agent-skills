#!/usr/bin/env bash
# Print build-readiness facts for one GitHub repo, read from the GitHub API.
# Usage: gh_repo_facts.sh <owner/repo | https://github.com/owner/repo[/...]>
set -euo pipefail

# Require one argument.
arg="${1:?usage: gh_repo_facts.sh <owner/repo | github-url>}"
# Drop any URL prefix and keep only owner/name.
repo="$(echo "${arg#*github.com/}" | cut -d/ -f1,2)"
# Drop a clone-URL .git suffix.
repo="${repo%.git}"

# Print identity, license, popularity, and links.
gh api "repos/$repo" --jq '
  "repo: \(.full_name)  url: \(.html_url)",
  "description: \(.description // "none")",
  "homepage: \(if (.homepage // "") == "" then "none" else .homepage end)",
  "license: \(.license.spdx_id // "NONE") (\(.license.name // "no license file"))",
  "stars: \(.stargazers_count)  forks: \(.forks_count)  archived: \(.archived)"'

# Print the newest commit date on the default branch.
gh api "repos/$repo/commits?per_page=1" --jq '"last_commit: \(.[0].commit.committer.date // "none")"'

# Print the newest release, or none.
gh api "repos/$repo/releases?per_page=1" --jq '"latest_release: \(if length == 0 then "none" else "\(.[0].tag_name) \(.[0].published_at)" end)"'

# Count files by role across the full file tree (case-insensitive).
gh api "repos/$repo/git/trees/HEAD?recursive=1" --jq '
  "(bom|bill.of.materials|parts.list)[^/]*\\.(csv|xlsx?|ods|md|pdf|txt|html?)$" as $bom
  | [.tree[] | select(.type == "blob") | .path] as $all
  | def n(re): [$all[] | select(test(re; "i"))] | length;
  "files: \($all | length)  tree_truncated: \(.truncated)",
  "print_files: stl=\(n("\\.stl$")) 3mf=\(n("\\.3mf$"))",
  "source_cad: step=\(n("\\.(step|stp)$")) fusion=\(n("\\.(f3d|f3z)$")) freecad=\(n("\\.fcstd$")) solidworks=\(n("\\.(sldprt|sldasm)$")) openscad=\(n("\\.scad$")) other=\(n("\\.(iges|igs|ipt|iam|x_t)$"))",
  "robot_model: urdf=\(n("\\.urdf$")) xacro=\(n("\\.xacro$")) ros_packages=\(n("(^|/)package\\.xml$")) mjcf=\(n("mjcf"))",
  "software: arduino=\(n("\\.ino$")) platformio=\(n("(^|/)platformio\\.ini$")) python=\(n("\\.py$"))",
  "bom_files: \(n($bom)) \([$all[] | select(test($bom; "i"))] | .[:5] | join(", "))",
  "docs: md=\(n("\\.md$")) pdf=\(n("\\.pdf$")) docs_dir=\(n("^docs?/"))"'

# Fetch the README as raw text; empty if missing.
readme="$(gh api "repos/$repo/readme" -H "Accept: application/vnd.github.raw" 2>/dev/null || true)"
# Count README lines.
lines="$(printf '%s' "$readme" | grep -c '' || true)"
# Count README lines that mention a BOM or parts list.
bom_mentions="$(printf '%s' "$readme" | grep -ciE '\bbom\b|bill of materials|parts list|shopping list' || true)"
# Count README lines that link to common part vendors.
vendor_links="$(printf '%s' "$readme" | grep -ciE 'amazon\.|amzn\.|aliexpress|digikey|mouser|mcmaster|misumi|robotis|feetech|pololu|adafruit|sparkfun|lcsc|stepperonline' || true)"
# Print README size and BOM signals.
echo "readme: lines=$lines  bom_mentions=$bom_mentions  vendor_links=$vendor_links"
