#!/usr/bin/env python3
import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Bool
from std_msgs.msg import String
import time

head_pitch_down_angle= 80
head_pitch_up_angle= 40
head_yaw_left_angle= 120
head_yaw_right_angle= 20

left_hand_pitch_up_angle= 0
left_hand_pitch_down_angle= 92
left_hand_roll_down_angle= 90
left_hand_roll_up_angle= 0

right_hand_pitch_up_angle= 95
right_hand_pitch_down_angle= 0
right_hand_roll_up_angle= 90
right_hand_roll_down_angle= 0

head_pitch_standby_angle= 60
head_yaw_standby_angle= 60
left_hand_pitch_standby_angle= 92
left_hand_roll_standby_angle= 90
right_hand_pitch_standby_angle= 0
right_hand_roll_standby_angle= 0


def interpolate_angle(start_angle, end_angle, percent):
    # Check if start angle is greater than end angle
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle
        percent = 100 - percent  # Invert percentage
    # Calculate the interpolated angle
    interpolated_angle = int(start_angle + (end_angle - start_angle) * percent / 100)
    return interpolated_angle


def left_hand_up():
    #shoulder down
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_down_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    #arm up
    left_pitch_ang_msg.data = left_hand_pitch_up_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
def left_hand_up_wave():
    #shoulder down
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_down_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    
    for swing in range(2):
        #arm up
        left_pitch_ang_msg.data =left_hand_pitch_up_angle
        left_hand_pitch_pub.publish(left_pitch_ang_msg)
        time.sleep(0.3)
        #arm down
        left_pitch_ang_msg.data = interpolate_angle(left_hand_pitch_up_angle,left_hand_pitch_down_angle,35)
        left_hand_pitch_pub.publish(left_pitch_ang_msg)
        time.sleep(0.3)
        left_pitch_ang_msg.data = left_hand_pitch_up_angle
        left_hand_pitch_pub.publish(left_pitch_ang_msg)
        time.sleep(0.3)
    
    #arm down
    left_pitch_ang_msg.data = left_hand_pitch_down_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
def right_hand_up():
    #shoulder down
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_down_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    #arm up
    right_pitch_ang_msg.data = right_hand_pitch_up_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
def right_hand_up_wave():
    #shoulder down
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_down_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    
    for swing in range(2):
        #arm up
        right_pitch_ang_msg.data = right_hand_pitch_up_angle
        right_hand_pitch_pub.publish(right_pitch_ang_msg)
        time.sleep(0.3)
        #arm down
        right_pitch_ang_msg.data = interpolate_angle(right_hand_pitch_up_angle,right_hand_pitch_down_angle,35)
        right_hand_pitch_pub.publish(right_pitch_ang_msg)
        time.sleep(0.3)
        right_pitch_ang_msg.data = right_hand_pitch_up_angle
        right_hand_pitch_pub.publish(right_pitch_ang_msg)
        time.sleep(0.3)
    
    #arm down
    right_pitch_ang_msg.data = right_hand_pitch_down_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
def both_hands_up():
    left_hand_up()
    right_hand_up()
def left_hand_flat():
    #shoulder down
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_down_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    #arm flat
    left_pitch_ang_msg.data = interpolate_angle(left_hand_pitch_up_angle,left_hand_pitch_down_angle,50)
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
def right_hand_flat():
    #shoulder down
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_down_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    #arm flat
    right_pitch_ang_msg.data = interpolate_angle(right_hand_pitch_up_angle,right_hand_pitch_down_angle,50)
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
def both_hand_flat():
    right_hand_flat()
    right_hand_flat()
def both_hands_flat_wave():
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_down_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_down_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    for swing in range(2):
        #arm up
        left_pitch_ang_msg.data = interpolate_angle(left_hand_pitch_up_angle,left_hand_pitch_down_angle,75)
        left_hand_pitch_pub.publish(left_pitch_ang_msg)
        right_pitch_ang_msg.data = interpolate_angle(right_hand_pitch_up_angle,right_hand_pitch_down_angle,75)
        right_hand_pitch_pub.publish(right_pitch_ang_msg)
        time.sleep(0.3)
        #arm down
        left_pitch_ang_msg.data = interpolate_angle(left_hand_pitch_up_angle,left_hand_pitch_down_angle,25)
        left_hand_pitch_pub.publish(left_pitch_ang_msg)
        right_pitch_ang_msg.data = interpolate_angle(right_hand_pitch_up_angle,right_hand_pitch_down_angle,25)
        right_hand_pitch_pub.publish(right_pitch_ang_msg)
        time.sleep(0.3)
    
    #arm down
    left_pitch_ang_msg.data = left_hand_pitch_down_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
    right_pitch_ang_msg.data = right_hand_pitch_down_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
def right_hand_front():
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_up_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    right_pitch_ang_msg.data = right_hand_pitch_down_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
def left_hand_front():
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_up_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    left_pitch_ang_msg.data = left_hand_pitch_down_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
def both_hands_front():
    right_hand_front()
    left_hand_front()
def right_hand_front_wave():
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_pitch_ang_msg.data = right_hand_pitch_down_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)
    for swing in range(2):
        #arm up
        right_roll_ang_msg.data = interpolate_angle(right_hand_roll_up_angle,right_hand_roll_down_angle,75)
        right_hand_roll_pub.publish(right_roll_ang_msg)
        time.sleep(0.3)
        #arm down
        right_roll_ang_msg.data = interpolate_angle(right_hand_roll_up_angle,right_hand_roll_down_angle,25)
        right_hand_roll_pub.publish(right_roll_ang_msg)
        time.sleep(0.3)
    
    #arm down
    right_roll_ang_msg.data = right_hand_roll_down_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
def left_hand_front_wave():
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    left_pitch_ang_msg.data = left_hand_pitch_down_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
    for swing in range(2):
        #arm up
        left_roll_ang_msg.data = interpolate_angle(left_hand_roll_up_angle,left_hand_roll_down_angle,75)
        left_hand_roll_pub.publish(left_roll_ang_msg)
        time.sleep(0.3)
        #arm down
        left_roll_ang_msg.data = interpolate_angle(left_hand_roll_up_angle,left_hand_roll_down_angle,25)
        left_hand_roll_pub.publish(left_roll_ang_msg)
        time.sleep(0.3)
    
    #arm down
    left_roll_ang_msg.data = left_hand_roll_down_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
def no():
    standby()
    head_yaw_ang_msg = UInt16()
    for swing in range(2):
        head_yaw_ang_msg.data = interpolate_angle(head_yaw_left_angle,head_yaw_right_angle,75)
        head_yaw_pub.publish(head_yaw_ang_msg)
        time.sleep(0.3)
        
        head_yaw_ang_msg.data = interpolate_angle(head_yaw_left_angle,head_yaw_right_angle,25)
        head_yaw_pub.publish(head_yaw_ang_msg)
        time.sleep(0.3)
    standby()
def yes():
    standby()
    head_pitch_ang_msg = UInt16()
    for swing in range(2):
        head_pitch_ang_msg.data = interpolate_angle(head_pitch_angle,head_pitch_angle,75)
        head_pitch_pub.publish(head_pitch_ang_msg)
        time.sleep(0.3)
        
        head_pitch_ang_msg.data = interpolate_angle(head_pitch_angle,head_pitch_angle,25)
        head_pitch_pub.publish(head_pitch_ang_msg)
        time.sleep(0.3)
    standby()
def standby():
    left_roll_ang_msg = UInt16()
    left_pitch_ang_msg = UInt16()
    head_pitch_ang_msg = UInt16()
    head_yaw_ang_msg = UInt16()
    left_roll_ang_msg.data = left_hand_roll_standby_angle
    left_hand_roll_pub.publish(left_roll_ang_msg)
    left_pitch_ang_msg.data = left_hand_pitch_standby_angle
    left_hand_pitch_pub.publish(left_pitch_ang_msg)
    right_roll_ang_msg = UInt16()
    right_pitch_ang_msg = UInt16()
    right_roll_ang_msg.data = right_hand_roll_standby_angle
    right_hand_roll_pub.publish(right_roll_ang_msg)
    right_pitch_ang_msg.data = right_hand_pitch_standby_angle
    right_hand_pitch_pub.publish(right_pitch_ang_msg)

    head_yaw_ang_msg.data = head_yaw_standby_angle
    head_yaw_pub.publish(head_yaw_ang_msg)
    head_pitch_ang_msg.data = head_pitch_standby_angle
    head_pitch_pub.publish(head_pitch_ang_msg)
def gesture_callback(msg):
    if msg.data == 1:
        left_hand_up()
    elif msg.data == 2:
        left_hand_up_wave()
    elif msg.data == 3:
        right_hand_up()
    elif msg.data == 4:
        right_hand_up_wave()
    elif msg.data == 5:
        both_hands_up()
    elif msg.data == 6:
        left_hand_flat()
    elif msg.data == 7:
        right_hand_flat()
    elif msg.data == 8:
        both_hand_flat()
    elif msg.data == 9:
        both_hands_flat_wave()
    elif msg.data == 10:
        right_hand_front()
    elif msg.data == 11:
        left_hand_front()
    elif msg.data == 12:
        both_hands_front()
    elif msg.data == 13:
        right_hand_front_wave()
    elif msg.data == 14:
        left_hand_front_wave()
    elif msg.data == 15:
        no()
    elif msg.data == 16:
        yes()
    elif msg.data == 17:
        standby()
    else:
        standby()

def hotword_detected_callback(msg):
    standby()
def speech_status_callback(msg):
    if msg.data == False:
        standby()
def chatbot_intent_tag_callback(msg):
    if msg.data == "hug":
        time.sleep(2)
        both_hands_front()
        time.sleep(7)
        standby()
    elif msg.data == "greeting":
        time.sleep(1)
        left_hand_up()
        time.sleep(3)
        standby()
    elif msg.data == "farewell":
        time.sleep(1)
        left_hand_up_wave()
        time.sleep(2)
        standby()
if __name__ == '__main__':
    rospy.init_node('gestures_node')
    left_hand_pitch_pub = rospy.Publisher('left_hand_pitch', UInt16, queue_size=15)
    left_hand_roll_pub = rospy.Publisher('left_hand_roll', UInt16, queue_size=15)
    right_hand_pitch_pub = rospy.Publisher('right_hand_pitch', UInt16, queue_size=15)
    right_hand_roll_pub = rospy.Publisher('right_hand_roll', UInt16, queue_size=15)
    head_pitch_pub = rospy.Publisher('head_pitch', UInt16, queue_size=15)
    head_yaw_pub = rospy.Publisher('head_yaw', UInt16, queue_size=15)

    rospy.Subscriber("chatbot_intent_tag",String, chatbot_intent_tag_callback, queue_size=3)
    rospy.Subscriber("hotword_detected",Bool, hotword_detected_callback, queue_size=3)
    rospy.Subscriber("gesture",UInt16, gesture_callback, queue_size=3)
    rospy.Subscriber('speech_status', Bool,speech_status_callback ,queue_size=2)
    rospy.spin()