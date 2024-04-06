#!/usr/bin/env python3
from tortoisebot_launcher_api.srv import TortoisebotApi, TortoisebotApiResponse
import roslaunch
import rospy
import rospkg
r = rospkg.RosPack()

# TODO: Need to convert to class objects

real_nav_launch_file = r.get_path(
    'tortoisebot_navigation') + '/launch/tortoisebot_navigation.launch'
map_launch_file = r.get_path('tortoisebot_slam') + \
    '/launch/tortoisebot_slam.launch'
map_saver_launch_file = r.get_path('tortoisebot_slam') + \
    '/launch/map_saver.launch'

uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)
global map_parent, start_map_launch_flag, stop_map_launch_flag, map_running, \
    real_nav_parent, start_real_nav_launch_flag, stop_real_nav_launch_flag, real_nav_running, \
    map_saver_parent, start_map_saver_launch_flag, stop_map_saver_launch_flag, map_saver_running

start_map_launch_flag = False
stop_map_launch_flag = False
map_running = False
start_map_saver_launch_flag = False
stop_map_saver_launch_flag = False
map_saver_running = False
start_real_nav_launch_flag = False
stop_real_nav_launch_flag = False
real_nav_running = False


def handleLauncherStart(req):
    global map_parent, start_map_launch_flag, map_running, \
        real_nav_parent, start_real_nav_launch_flag, real_nav_running, \
        map_saver_parent, start_map_saver_launch_flag, map_saver_running
    if req.file == "map":
        if map_running:
            return TortoisebotApiResponse(False)
        else:
            cli_args = [map_launch_file] + \
                str(req.args).split(" ")
            roslaunch_file = [
                (roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], cli_args[1:])]
            map_parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
            start_map_launch_flag = True
            map_running = True

            return TortoisebotApiResponse(True)
    elif req.file == "map_saver":
        if map_saver_running:
            return TortoisebotApiResponse(False)
        else:
            cli_args = [map_saver_launch_file] + \
                str(req.args).split(" ")
            roslaunch_file = [
                (roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], cli_args[1:])]
            map_saver_parent = roslaunch.parent.ROSLaunchParent(
                uuid, roslaunch_file)
            start_map_saver_launch_flag = True
            map_saver_running = True
            return TortoisebotApiResponse(True)
    elif req.file == "real_nav":
        if real_nav_running:
            return TortoisebotApiResponse(False)
        else:

            cli_args = [real_nav_launch_file] + \
                str(req.args).split(" ")
            roslaunch_file = [
                (roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], cli_args[1:])]
            real_nav_parent = roslaunch.parent.ROSLaunchParent(
                uuid, roslaunch_file)
            start_real_nav_launch_flag = True
            real_nav_running = True

            return TortoisebotApiResponse(True)


def handleLauncherStop(req):
    global stop_map_launch_flag, map_running, \
        stop_real_nav_launch_flag, real_nav_running, \
        stop_map_saver_launch_flag, map_saver_running
    if req.file == "map":
        if not map_running:
            return TortoisebotApiResponse(False)
        else:
            stop_map_launch_flag = True
            map_running = False
            return TortoisebotApiResponse(True)
    elif req.file == "map_saver":
        if not map_saver_running:
            return TortoisebotApiResponse(False)
        else:
            stop_map_saver_launch_flag = True
            map_saver_running = False
            return TortoisebotApiResponse(True)
    elif req.file == "real_nav":
        if not real_nav_running:
            return TortoisebotApiResponse(False)
        else:
            stop_real_nav_launch_flag = True
            real_nav_running = False
            return TortoisebotApiResponse(True)


def main():
    global map_parent, start_map_launch_flag, stop_map_launch_flag, \
        real_nav_parent, start_real_nav_launch_flag, stop_real_nav_launch_flag, \
        map_saver_parent, start_map_saver_launch_flag, stop_map_saver_launch_flag
    rospy.init_node('tortoisebot_launcher_api_server')
    rospy.Service('tortoisebot_launcher_api_start',
                  TortoisebotApi, handleLauncherStart)
    rospy.Service('tortoisebot_launcher_api_stop',
                  TortoisebotApi, handleLauncherStop)
    while not rospy.is_shutdown():
        if start_map_launch_flag:
            map_parent.start()
            start_map_launch_flag = False
        if stop_map_launch_flag:
            map_parent.shutdown()
            stop_map_launch_flag = False
        if start_map_saver_launch_flag:
            map_saver_parent.start()
            start_map_saver_launch_flag = False
        if stop_map_saver_launch_flag:
            map_saver_parent.shutdown()
            stop_map_saver_launch_flag = False
        if start_real_nav_launch_flag:
            real_nav_parent.start()
            start_real_nav_launch_flag = False
        if stop_real_nav_launch_flag:
            real_nav_parent.shutdown()
            stop_real_nav_launch_flag = False


if __name__ == "__main__":
    main()
