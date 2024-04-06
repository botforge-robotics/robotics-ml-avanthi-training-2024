#!/usr/bin/env python3

import rospy
from std_srvs.srv import Trigger
from geometry_msgs.msg import Twist
from threading import Timer
import time


class DockingMonitor:
    def __init__(self):
        rospy.init_node('docking_monitor')
        self.last_msg_time = time.time()
        self.docking_service = rospy.ServiceProxy(
            'move_to_docking_station', Trigger)
        self.cmd_vel_subscriber = rospy.Subscriber(
            '/cmd_vel', Twist, self.cmd_vel_callback)
        self.docking_timer = None

    def cmd_vel_callback(self, msg):
        self.last_msg_time = time.time()
        if self.docking_timer:
            self.docking_timer.cancel()
        self.docking_timer = Timer(5, self.check_docking_timeout)
        self.docking_timer.start()

    def check_docking_timeout(self):
        current_time = time.time()
        if current_time - self.last_msg_time > 30:  # Check if 30sec have passed
            rospy.loginfo(
                "No cmd_vel messages received for 30sec. Initiating docking.")
            try:
                self.docking_service()  # Call the docking service
            except rospy.ServiceException as e:
                rospy.logerr("Service call failed: %s", e)
            finally:
                if self.docking_timer:
                    self.docking_timer.cancel()
        else:
            rospy.loginfo("Checking again in 5sec")
            self.docking_timer = Timer(
                5, self.check_docking_timeout)  # Check again in 5sec
            self.docking_timer.start()

    def start(self):
        # Start checking for docking after 30secs
        self.docking_timer = Timer(5, self.check_docking_timeout)
        self.docking_timer.start()
        rospy.spin()


if __name__ == '__main__':
    try:
        monitor = DockingMonitor()
        monitor.start()
    except rospy.ROSInterruptException:
        pass
