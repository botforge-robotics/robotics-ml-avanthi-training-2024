#!/usr/bin/env python3.7

import rospy
import os
from nltk_chatbot_msg.srv import VoiceService, VoiceServiceResponse
import rospkg
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2
from openai import OpenAI
from dotenv import load_dotenv
import base64
import requests

load_dotenv()

rospack = rospkg.RosPack()
bridge = CvBridge()
rotated_image = None

# voice service


def chat_gpt_voice_service_callback(req):
    res = VoiceServiceResponse()
    if not req.query_text == "none":
        processed_string = gpt_response(req.query_text)
        text_to_speech_msg = String()
        text_to_speech_msg.data = processed_string

        text_to_speech_pub.publish(text_to_speech_msg)
        intent_tag_msg = String()
        intent_tag_msg.data == "nothing"
        intent_tag_pub.publish(intent_tag_msg)
        # Set the response to be True
        res.success = True

    else:
        res.success = False
    return res


def image_process(encodedImage, query):
    if query in "describe this item":
        image_query = [
            'describe the item in this image in 3 senstences, Answer like you are a robot and you are watching this']
    else:
        image_query = [
            'provide a description for this image in 3 senstences, Answer like you are a robot and you are watching this']
    for query in image_query:
        # Getting the base64 string

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": query
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encodedImage}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = response.json()
        return response['choices'][0]['message']['content']


def gpt_response(query):
    client = OpenAI()
    if query.lower().strip() in "what do you see describe this item":
        if rotated_image is not None:
            retval, buffer = cv2.imencode('.jpg', rotated_image)
            base64_image = base64.b64encode(buffer).decode('utf-8')
            return image_process(base64_image, query)
        else:
            return "cant read from camera."


def image_callback(data):
    global rotated_image
    global bridge
    try:
        # Convert compressed image to OpenCV image
        cv_image = bridge.compressed_imgmsg_to_cv2(
            data, desired_encoding="bgr8")
    except CvBridgeError as e:
        rospy.logerr(e)
        return
    # Rotate the image by 180 degrees
    rotated_image = cv2.rotate(cv_image, cv2.ROTATE_180)


rospy.init_node('chatgpt_interpreter_node')
# Create the service servers
srv_string_to_speech = rospy.Service(
    'chatgpt_interpreter_node/voice_service', VoiceService, chat_gpt_voice_service_callback)
intent_tag_pub = rospy.Publisher('chatbot_intent_tag', String, queue_size=2)
text_to_speech_pub = rospy.Publisher('text_to_say', String, queue_size=2)
rospy.Subscriber('/camera/image/compressed', CompressedImage, image_callback)
if __name__ == "__main__":
    gpt_msgs = [
        {"role": "system", "content": "You are a interactive robot named snowboy and give me answers only in 2 sentences."}
    ]

rospy.loginfo("chatgpt interpretor ready!!")
rospy.spin()
