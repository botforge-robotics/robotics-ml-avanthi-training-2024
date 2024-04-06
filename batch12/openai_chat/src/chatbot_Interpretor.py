#!/usr/bin/env python3.7

import rospy
from nltk_chatbot_msg.srv import VoiceService, VoiceServiceResponse
import rospkg
from std_msgs.msg import String
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

rospack = rospkg.RosPack()

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


def gpt_response(query):
    client = OpenAI()
    gpt_msgs.append({"role": "user", "content": query})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=gpt_msgs
    )
    gpt_response = completion.choices[0].message.content
    gpt_msgs.append({"role": "assistant", "content": gpt_response})
    return gpt_response


rospy.init_node('chatgpt_interpreter_node')
# Create the service servers
srv_string_to_speech = rospy.Service(
    'chatgpt_interpreter_node/voice_service', VoiceService, chat_gpt_voice_service_callback)
intent_tag_pub = rospy.Publisher('chatbot_intent_tag', String, queue_size=2)
text_to_speech_pub = rospy.Publisher('text_to_say', String, queue_size=2)
if __name__ == "__main__":
    gpt_msgs = [
        {"role": "system", "content": "You are a interactive robot named snowboy and give me answers only in 2 sentences."}
    ]

rospy.loginfo("chatgpt interpretor ready!!")
rospy.spin()
