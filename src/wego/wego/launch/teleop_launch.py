from launch import LaunchDescription

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration

from launch.conditions import IfCondition

from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    wego_share_dir = get_package_share_directory('wego')
    rviz_config_path = os.path.join(wego_share_dir, 'rviz', 'display.rviz')

    viz_launch_arg = DeclareLaunchArgument(
        'viz',
        default_value='false'
    )

    return LaunchDescription([
        viz_launch_arg,

        IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('wego_description'), 'launch', 'load_launch.py'])
        ),
        
        IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('scout_base'), 'launch', 'scout_base.launch.py'])
        ),

        IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('velodyne'), 'launch', 'velodyne-all-nodes-VLP16-composed-launch.py'])
        ),

        IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('ublox_gps'), 'launch', 'ublox_gps_node_base-launch.py'])
        ),

        IncludeLaunchDescription(
            PathJoinSubstitution([FindPackageShare('ublox_gps'), 'launch', 'ublox_gps_node_rover-launch.py'])
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            condition=IfCondition(LaunchConfiguration('viz')),
            arguments=['-d', rviz_config_path]
        )
  ])