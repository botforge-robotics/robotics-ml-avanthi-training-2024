#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Bool
from std_msgs.msg import String


happy_face = 1
very_happy_face = 2
sad_face = 3
very_sad_face = 4
face_with_tongue_sticking_out = 5
dead_face = 6
scared_face = 7
sleep_face = 8
confusing_face = 9
bored_face = 10
love_face = 11
disgusted_face = 12
angry_face = 13
happy_speaking = 14
sad_speaking = 15
thinking = 16

chat_bot_expressions = {
    "greeting": happy_face,
    "farewell": sad_face,
    "joke": face_with_tongue_sticking_out,
    "hug": love_face,
}

expression_msg = UInt16()


def recognized_text_callback(msg):
    if msg.data:
        if not msg.data == "none":
            expression_msg.data = thinking
        else:
            expression_msg.data = happy_face
        expression_pub.publish(expression_msg)


def hotword_detected_callback(msg):
    if msg.data:
        expression_msg.data = confusing_face
        expression_pub.publish(expression_msg)


def chatbot_intent_tag_callback(msg):
    if msg.data in chat_bot_expressions:
        expression_msg.data = chat_bot_expressions[msg.data]
    else:
        expression_msg.data = happy_speaking


def speech_status_callback(msg):
    if msg.data:
        if not expression_msg.data:
            expression_msg.data = happy_speaking
    else:
        expression_msg.data = happy_face
    expression_pub.publish(expression_msg)


if __name__ == '__main__':
    rospy.init_node('emotions_node')
    expression_pub = rospy.Publisher('face_expression', UInt16, queue_size=2)
    rospy.Subscriber("recognized_text", String,
                     recognized_text_callback, queue_size=3)
    rospy.Subscriber("hotword_detected", Bool,
                     hotword_detected_callback, queue_size=3)
    rospy.Subscriber("chatbot_intent_tag", String,
                     chatbot_intent_tag_callback, queue_size=3)
    rospy.Subscriber("speech_status", Bool,
                     speech_status_callback, queue_size=3)
    rospy.spin()
