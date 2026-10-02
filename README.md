# nav2_bot

> **Note:** This package builds on third-party starting points (credited below). The robot and sensor configuration, parameter tuning and integration are by Kleber Cabral. The README documentation and the 2026-10-02 cleanup were done with AI assistance (Claude).

A ROS 2 package with a simulated differential-drive robot (Gazebo Classic +
ros2_control), set up as a sandbox for experimenting with Nav2 and slam_toolbox
sensor and parameter settings.

**Credits:** the robot description and simulation launch layout follow the Articulated
Robotics `my_bot` template and tutorial series by Josh Newans
([joshnewans/my_bot](https://github.com/joshnewans/my_bot)).
`navigation_launch.py` and `localization_launch.py` are adapted from Nav2's
`nav2_bringup` (Apache 2.0, original copyright headers kept). The Nav2 and slam_toolbox
parameter files start from those projects' defaults.

## Structure

```
nav2_bot/
├── description/   # URDF/xacro: chassis, lidar, depth camera, ros2_control / Gazebo diff-drive
├── launch/
│   ├── launch_sim.launch.py      # Gazebo + robot + controllers + joystick + twist_mux
│   ├── rsp.launch.py             # robot_state_publisher from the xacro
│   ├── joystick.launch.py        # joy + teleop_twist_joy (publishes /cmd_vel_joy)
│   ├── online_async_launch.py    # slam_toolbox (async)
│   ├── navigation_launch.py      # Nav2 navigation servers
│   └── localization_launch.py    # map_server + AMCL
├── config/        # controllers, twist_mux, joystick, Nav2 + slam_toolbox params, rviz layouts
└── worlds/        # empty.world, my_room.world
```

## What it does

- **Robot model** (`description/`): a two-wheel differential-drive base with a 360°
  lidar (publishing `/scan`) and a depth camera. By default it's driven through
  ros2_control (`diff_controller` + `joint_broadcaster`, configured in
  `config/my_controllers.yaml`). With `use_ros2_control:=false` it falls back to
  Gazebo's diff-drive plugin.
- **Simulation** (`launch_sim.launch.py`): starts robot_state_publisher, Gazebo, spawns
  the robot, and starts the controllers, joystick teleop and `twist_mux`.
  `twist_mux` gives the joystick (`/cmd_vel_joy`) priority over Nav2 (`/cmd_vel`) and
  feeds the result to `diff_controller`.
- **SLAM** (`online_async_launch.py`): slam_toolbox in async mode, using
  `config/mapper_params_online_async.yaml`.
- **Navigation** (`navigation_launch.py`, `localization_launch.py`): the Nav2 servers
  and map_server + AMCL, using `config/nav2_params.yaml`. That file is where the
  parameter experiments happen.

## Install

Clone into a colcon workspace and build:

```bash
mkdir -p ~/dev_ws/src && cd ~/dev_ws/src
git clone https://github.com/klebermc/nav2_bot.git
cd ~/dev_ws
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
source install/setup.bash
```

## Run

Each step goes in its own terminal (with the workspace sourced):

```bash
# Simulation (starts an empty Gazebo world; open worlds/my_room.world from the Gazebo GUI if wanted)
ros2 launch nav2_bot launch_sim.launch.py

# Mapping / localization with slam_toolbox
ros2 launch nav2_bot online_async_launch.py use_sim_time:=true

# Nav2
ros2 launch nav2_bot navigation_launch.py use_sim_time:=true

# Optional: rviz
rviz2 -d src/nav2_bot/config/map_view.rviz
```

`config/mapper_params_online_async.yaml` is set to `mode: localization`, loading the
serialized map `my_map` from the directory you launch from. To build a new map, set
`mode: mapping`, drive around, and save it with slam_toolbox's "Serialize Map" in rviz.

## Key dependencies

ROS 2 (Gazebo Classic era) with `gazebo_ros`, `gazebo_ros2_control`, `ros2_control`
(`diff_drive_controller`, `joint_state_broadcaster`), `xacro`,
`robot_state_publisher`, `joy`, `teleop_twist_joy`, `twist_mux`, `slam_toolbox` and
Nav2 (`nav2_bringup`).

## Status

Learning/experimentation project, not actively developed.

## Cleanup notes

- **2026-10-02:** Reverted the lidar topic to `/scan`. The last commit had renamed it to
  `scan_ideal` for a Gaussian-noise republisher node, which was never finished, so
  nothing was publishing `/scan` for SLAM or Nav2. Removed that stub node, a scratch copy of
  the Nav2 params, and a placeholder file. Replaced a hardcoded home-directory map path
  with a relative one. Filled in `package.xml` (description, license, runtime
  dependencies, noreply maintainer email), and added this README and a `.gitignore`.

## License

Apache 2.0 — see [LICENSE.md](LICENSE.md). This matches the template and the `nav2_bringup` files it builds on.
