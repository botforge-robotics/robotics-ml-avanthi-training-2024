#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
import time
from std_msgs.msg import String

isObstacle = False

head_yaw_left_angle = 120
head_yaw_right_angle = 20
head_yaw_standby_angle = 60


def interpolate_angle(start_angle, end_angle, percent):
    # Check if start angle is greater than end angle
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle
        percent = 100 - percent  # Invert percentage
    # Calculate the interpolated angle
    interpolated_angle = int(
        start_angle + (end_angle - start_angle) * percent / 100)
    return interpolated_angle


def headyaw():
    head_yaw_ang_msg = UInt16()
    for swing in range(2):
        head_yaw_ang_msg.data = interpolate_angle(
            head_yaw_left_angle, head_yaw_right_angle, 75)
        head_yaw_pub.publish(head_yaw_ang_msg)
        time.sleep(0.3)

        head_yaw_ang_msg.data = interpolate_angle(
            head_yaw_left_angle, head_yaw_right_angle, 25)
        head_yaw_pub.publish(head_yaw_ang_msg)
        time.sleep(0.3)


def chatbot_intent_tag_callback(msg):
    if msg.data == "forward":
        foward()
    elif msg.data == "backward":
        backward()
    elif msg.data == "turn_left":
        turn_left()
    elif msg.data == "turn_right":
        turn_right()
    elif msg.data == "turn_around":
        turn_around()


def foward():
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = 0.25
    cmd_vel_msg.angular.z = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)
    start_time = rospy.Time.now()
    duration = rospy.Duration.from_sec(2)
    while rospy.Time.now() - start_time < duration and not isObstacle:
        pass
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)


def backward():
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = -0.25
    cmd_vel_msg.angular.z = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)
    time.sleep(2)
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)


def turn_left():
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_msg.angular.z = 1.0
    cmd_vel_pub.publish(cmd_vel_msg)
    time.sleep(0.6)
    cmd_vel_msg.angular.z = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)


def turn_right():
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_msg.angular.z = -1.0
    cmd_vel_pub.publish(cmd_vel_msg)
    time.sleep(0.6)
    cmd_vel_msg.angular.z = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)


def turn_around():
    cmd_vel_msg = Twist()
    cmd_vel_msg.linear.x = 0.0
    cmd_vel_msg.angular.z = 1.0
    cmd_vel_pub.publish(cmd_vel_msg)
    time.sleep(1.05)
    cmd_vel_msg.angular.z = 0.0
    cmd_vel_pub.publish(cmd_vel_msg)


def sonar_sensor_callback(msg):
    global isObstacle
    if msg.data < 35:
        isObstacle = True
    else:
        isObstacle = False


if __name__ == '__main__':
    rospy.init_node('motion_node')
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("chatbot_intent_tag", String,
                     chatbot_intent_tag_callback, queue_size=3)
    rospy.Subscriber("sonar", UInt16, sonar_sensor_callback, queue_size=10)
    head_yaw_pub = rospy.Publisher('head_yaw', UInt16, queue_size=15)
    rospy.spin()
