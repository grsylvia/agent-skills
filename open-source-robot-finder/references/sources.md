# Sources

Where to find candidates. Search all of them: GitHub gives the most checkable facts, but many good builds live on Hackaday, Printables, or a vendor site.

| Source | Good for | How to search |
| --- | --- | --- |
| GitHub | License, activity, file counts | `gh search repos` (below) |
| [Hugging Face LeRobot](https://huggingface.co/docs/lerobot) | Low-cost arms and mobile bases with ready software | WebFetch the docs; follow the hardware pages |
| Hackaday.io | Build logs, full writeups | WebSearch, `allowed_domains: ["hackaday.io"]` |
| Printables | STL-first; license on each model page | WebSearch, `allowed_domains: ["printables.com"]` |
| Thingiverse | Like Printables, older designs | WebSearch, `allowed_domains: ["thingiverse.com"]` |
| [OSHWA certified list](https://certification.oshwa.org/list.html) | Verified open licenses | WebFetch; filter Project Type = Robotics |
| Awesome lists | Seed candidates | Read the README of `mjyc/awesome-robotics-projects`, `delftopenhardware/awesome-open-hardware` |
| Open web | Vendor-hosted projects | WebSearch `open source <type> robot STL BOM` |

## GitHub

```bash
# Search a topic, most-starred first, with the fields the gates need.
gh search repos --topic <topic> --sort stars --limit 20 --json fullName,description,stargazersCount,pushedAt,license,url
# Search two or three keywords the same way.
gh search repos "<keywords>" --sort stars --limit 20 --json fullName,description,stargazersCount,pushedAt,license,url
# Read an awesome list's README as raw text.
gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw"
```

| Robot type | Topics | Keywords |
| --- | --- | --- |
| Arm | `robot-arm`, `robotic-arm`, `lerobot` | `robot arm 3d printed`, `desktop robot arm` |
| Mobile base | `mobile-robot`, `lerobot` | `mobile robot 3d printed`, `diy rover` |
| Legged | `quadruped`, `humanoid` | `quadruped 3d printed`, `biped robot` |
| Gripper or hand | — | `robot gripper 3d printed`, `robot hand open source` |
| Any | `3d-printed`, `open-source-hardware` | `open source robot 3d printed` |

## Search pitfalls

| Pitfall | Example | Handling |
| --- | --- | --- |
| Long keyword queries match little | `AR4 robot arm annin` → 0 results | Use 2–3 words, or topics |
| Topic results include software | `pantor/ruckig` (motion library) under `robot-arm` | Gate G1 drops it |
| Toy designs dominate Printables | 9 g hobby-servo arms | Fine for "weekend"; score S2 honestly |
| One project, many listings | Thor on GitHub and Hackaday.io | Merge; keep the primary source |
