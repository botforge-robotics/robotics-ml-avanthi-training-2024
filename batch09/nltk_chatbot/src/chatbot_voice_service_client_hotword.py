#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from nltk_chatbot_msg.srv import VoiceService,VoiceServiceRequest



def recognized_text_callback(recognized_text_msg):
    # Call the voice service with the recognized text
    request = VoiceServiceRequest()
    request.query_text = recognized_text_msg.data
    response = voice_service_client(request)
    if(response.success):
        # Print the response from the service
        rospy.loginfo(f"chatbot responded: {response.success}")



if __name__ == '__main__':
    rospy.init_node("recognized_text_subscriber_node")
    # Create a service client for the voice service
    voice_service_client = rospy.ServiceProxy(
         "/chatbot_interpreter_node/voice_service",VoiceService)
    # Wait for the service to become available
    rospy.wait_for_service("/chatbot_interpreter_node/voice_service")

    # Create a subscriber for the recognized text topic
    recog_text_sub = rospy.Subscriber(
         "recognized_text",String, recognized_text_callback, queue_size=10)

    rospy.loginfo("Chatbot Voice Service Client ready!!")
    
    rospy.spin()

