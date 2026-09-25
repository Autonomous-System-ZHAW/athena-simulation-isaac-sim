#!/usr/bin/env bash
# .devcontainer/post_create.sh
# Runs once when the container is created.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WS_DIR="$(dirname "$REPO_DIR")"

echo ">>> Importing repositories"
mkdir -p "$REPO_DIR/src"
vcs import --skip-existing --input "$REPO_DIR/sim.repos" "$REPO_DIR/src"
vcs import --skip-existing --input "$REPO_DIR/src/athena_autonomous_racing/athena.repos" "$REPO_DIR/src"

echo ">>> Installing ROS dependencies"
sudo apt-get update
rosdep update
rosdep install --from-paths "$REPO_DIR" --ignore-src --rosdistro "$ROS_DISTRO" -r -y

echo ">>> Installing Python dependencies"
pip install --break-system-packages --no-deps -r "$REPO_DIR/.devcontainer/requirements.txt"

echo ">>> Configuring shell"
BASHRC="$HOME/.bashrc"
grep -qxF "source /opt/ros/$ROS_DISTRO/setup.bash" "$BASHRC" \
    || echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> "$BASHRC"
grep -qxF "[ -f $WS_DIR/install/setup.bash ] && source $WS_DIR/install/setup.bash" "$BASHRC" \
    || echo "[ -f $WS_DIR/install/setup.bash ] && source $WS_DIR/install/setup.bash" >> "$BASHRC"

echo ">>> Done. Build with: cd $WS_DIR && colcon build --symlink-install"