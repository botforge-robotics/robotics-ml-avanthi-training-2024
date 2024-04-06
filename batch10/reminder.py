#!/usr/bin/env python3

import rospy
import time
from joyrobot.srv import Reminder, ReminderResponse
from face_recognition.msg import RecogByNameAction, RecogByNameGoal
from actionlib import SimpleActionClient
from std_msgs.msg import String


def facerecognition_client(person):
    fr_client = SimpleActionClient('recognise_person', RecogByNameAction)
    fr_client.wait_for_server()
    # Creates a goal to send to the action server.
    goal = RecogByNameGoal(name=person, duration=15)

    # Sends the goal to the action server.
    fr_client.send_goal(goal)

    # Goal State
    # PENDING = 0
    # ACTIVE = 1
    # DONE = 2
    # WARN = 3
    # ERROR = 4

    result_state = fr_client.get_state()

    rate = rospy.Rate(30)

    while result_state < 2:
        rate.sleep()
        result_state = fr_client.get_state()
        rospy.loginfo("result_state: " + str(result_state))
        # fr_client.cancel_goal()

    return fr_client.get_result()  # A FibonacciResult


def handle_request(req):
    resp = ReminderResponse()  # variable to store responce data
    result = facerecognition_client(req.name)
    if (result.found):
        resp.success = True
        text_to_speech_pub = rospy.Publisher(
            'text_to_say', String, queue_size=2)
        text_to_speech_msg = String()
        text_to_speech_msg.data = req.reminder
        text_to_speech_pub.publish(text_to_speech_msg)
    else:
        resp.success = False
    return resp


if __name__ == '__main__':
    rospy.init_node('reminder_node')
    s = rospy.Service('reminder', Reminder, handle_request)
    rospy.spin()
