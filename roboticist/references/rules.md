# Beginner rules

Source keys resolve in [sources.md](sources.md). Severity is the default; raise or lower it only with a stated reason.

## Standards (STD)

| ID | Sev | Rule | Check | Source |
| --- | --- | --- | --- | --- |
| STD-001 | Warn | Lengths in metres, angles in radians, mass in kg. | Origins fit the robot's real size; any angle with abs > 2π suggests degrees. | [REP-103] |
| STD-002 | Warn | Frames are right-handed; base frame is X forward, Y left, Z up. | In RViz, `base_link` Z points up and X points to the robot's front. | [REP-103] · [MR] Ch 3 · [Craig] Ch 2 |
| STD-003 | Note | The robot base frame is named `base_link`. | Root link name, or the child of a fixed `world` joint. | [REP-105] |

## URDF

| ID | Sev | Rule | Check | Source |
| --- | --- | --- | --- | --- |
| URDF-001 | Blocker | The URDF parses. | `check_urdf` exits without error. | [URDF-J] [URDF-L] |
| URDF-002 | Blocker | Links form one tree: one root, one parent per link, no loops. | `check_urdf` tree; every link appears once. | [URDF-J] · [MR] Ch 4 |
| URDF-003 | Blocker | Revolute and prismatic joints have `<limit>` with `effort` and `velocity`. | Both attributes are present (the spec requires them). | [URDF-J] |
| URDF-004 | Warn | `lower` < `upper`; continuous joints omit both. | Compare values per joint. | [URDF-J] |
| URDF-005 | Warn | Joint `axis` is non-zero and normalized. | Vector length = 1. | [URDF-J] |
| URDF-006 | Warn | `rpy` is fixed-axis roll (X), pitch (Y), then yaw (Z), in radians. | Values like 90 or 180 mean degrees were used. | [URDF-J] · [Craig] Ch 2 · [MR] Ch 3 |
| URDF-007 | Warn | Mesh `scale` converts the mesh's native units to metres. | mm source files need `0.001`; RViz size matches the real robot. | [REP-103] [URDF-L] |
| URDF-008 | Warn | Mesh filenames use `package://<pkg>/...`, not absolute paths. | Inspect each `filename`. | [URDF-L] |
| URDF-009 | Blocker / Note | `<inertial>`: mass > 0, `ixx`, `iyy`, `izz` > 0, and each ≤ sum of the other two. | Blocker if present and invalid; Note if absent (RViz works, simulation needs it). Non-zero products → mark Not checked. | [URDF-L] · [MR] §8.2 · [Craig] Ch 6 |
| URDF-010 | Note | Links have `<collision>` geometry: primitives, or meshes with < 1000 faces. | Absent → Note (needed for MoveIt and Gazebo). | [URDF-L] |
| URDF-011 | Warn | Movable joint count matches the physical robot's DOF. | Compare with the vendor docs (e.g. Arctos: 6 arm axes, plus a gripper if fitted). | [MR] Ch 2 · [VENDOR] |

## Project (PROJ)

| ID | Sev | Rule | Check | Source |
| --- | --- | --- | --- | --- |
| PROJ-001 | Warn | Joint limits follow the project's documented limit rule. | Limits exist and their origin is documented; computing collision angles is Not checked. | [PROJECT] |
| PROJ-002 | Varies | Any other rule in the project's `AGENTS.md` / `CLAUDE.md` that touches robot design. | Cite the project file and line. | [PROJECT] |

## Packaging (PKG)

| ID | Sev | Rule | Check | Source |
| --- | --- | --- | --- | --- |
| PKG-001 | Warn | Package name is lowercase alphanumerics and `_`, starting with a letter. | `<name>` in `package.xml`. | [REP-144] |
| PKG-002 | Warn | `package.xml` uses format 3. | `<package format="3">`. | [REP-149] |
| PKG-003 | Blocker | Every package that launch files use is an `exec_depend`. | `Node(package=...)`, `get_package_share_directory(...)`, Python imports. | [REP-149] · [J-LAUNCH] |
| PKG-004 | Blocker | CMake `install()` covers every directory the launch files and URDF read. | `urdf`, `meshes`, `launch`, `rviz`, `config` as used. | [J-AMENT] |
| PKG-005 | Blocker | The package builds. | `colcon build --packages-select <pkg>` succeeds. | [J-COLCON] |
| PKG-006 | Blocker | Every `package://` URI resolves under `install/`. | `test -f` per URI. | [URDF-L] · [J-URDF] |
| PKG-007 | Warn | `robot_state_publisher` gets `robot_description`, and joint states are published for every movable joint. | Launch nodes and parameters. | [J-RSP] |
