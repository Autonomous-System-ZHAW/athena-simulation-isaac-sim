# athena_sim_bringup/launch/sim.launch.py
import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_vicon_arg = DeclareLaunchArgument(
        "use_vicon",
        default_value="true",
        description="Start the Vicon client (requires lab network)",
    )

    overrides = PathJoinSubstitution(
        [FindPackageShare("athena_sim_bringup"), "config", "overrides.yaml"]
    )

    autonomy = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("athena_autonomous_racing"),
                    "launch",
                    "autonomy.launch.py",
                ]
            )
        ),
        launch_arguments={
            "use_sim_time": "true",
            "override_params": overrides,
        }.items(),
    )

    # TODO: Vicon uses wall-clock timestamps while autonomy runs on sim time.
    vicon_cfg_path = os.path.join(
        get_package_share_directory("athena_sim_bringup"), "config", "vicon.yaml"
    )
    with open(vicon_cfg_path) as f:
        vicon_args = {k: str(v) for k, v in yaml.safe_load(f).items()}

    vicon_tracker = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("vicon_receiver"), "launch", "client.launch.py"]
            )
        ),
        launch_arguments=vicon_args.items(),
        condition=IfCondition(LaunchConfiguration("use_vicon")),
    )

    return LaunchDescription(
        [
            use_vicon_arg,
            autonomy,
            vicon_tracker,
        ]
    )
