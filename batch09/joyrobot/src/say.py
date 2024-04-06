#!/usr/bin/env python3.7
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import String
from gtts import gTTS
from subprocess import call
from pydub import AudioSegment

def speech_callback(msg):
    if msg.data:
        speech_status_msg = Bool()
        tts = gTTS(msg.data)
        tts.save('output.mp3')
        sound = AudioSegment.from_mp3("output.mp3")
       
        sound.export("output.wav", format="wav")
        speech_status_msg.data =True
        speech_status_pub.publish(speech_status_msg)
        call(["aplay", "output.wav"])
        speech_status_msg.data = False
        speech_status_pub.publish(speech_status_msg)

if __name__ == '__main__':
    rospy.init_node('text_to_speech_node')
    speech_status_pub = rospy.Publisher('speech_status', Bool, queue_size=2)
    rospy.Subscriber("text_to_say",String, speech_callback, queue_size=3)
    rospy.spin()
