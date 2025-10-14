#!/usr/bin/env bash
set -e

ISAACSIM_PATH="$HOME/isaacsim-5.0"

unset PYTHONPATH
unset AMENT_PREFIX_PATH
unset COLCON_PREFIX_PATH
unset ROS_VERSION
unset ROS_PYTHON_VERSION
export ROS_DISTRO=humble

export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
# export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$ISAACSIM_PATH/exts/isaacsim.ros2.bridge/humble/lib"

echo "Internal bridge libs:"
ls -1 "$ISAACSIM_PATH/exts/isaacsim.ros2.bridge/humble/lib" || true

exec "$ISAACSIM_PATH/isaac-sim.sh"
