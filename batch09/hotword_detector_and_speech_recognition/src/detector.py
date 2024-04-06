#!/usr/bin/env python3

import rospy
from snowboydecoder import snowboydecoder
from std_msgs.msg import Bool, String
import os
import rospkg
import time
import speech_recognition as sr

class HotwordSpeechRecognitionNode:
    def __init__(self):
        rospy.init_node('hotword_speechrecognition_node')
        self.hotword_detected_pub = rospy.Publisher('hotword_detected', Bool, queue_size=10)
        self.rec_text_publisher = rospy.Publisher('recognized_text', String, queue_size=10)
        self.recognizer = sr.Recognizer()
        self.rospack = rospkg.RosPack()

    def hotword_detected_callback(self):
        msg = Bool()
        msg.data = True
        self.hotword_detected_pub.publish(msg)
        snowboydecoder.play_audio_file()

    def audio_recorder_callback(self, fname):
        with sr.AudioFile(fname) as source:
            audio = self.recognizer.record(source)
        rec_text = "none"
        try:
            text = self.recognizer.recognize_google(audio, language="english")
            rospy.loginfo(f'Recognized text: {text}')
            rec_text = text
        except sr.UnknownValueError:
            rospy.loginfo('Unable to recognize spoken text')
        except sr.RequestError as e:
            rospy.logerr(f'Error calling the speech recognition service: {e}')
        msg = String()
        msg.data = rec_text
        self.rec_text_publisher.publish(msg)
        snowboydecoder.play_audio_file(fname=snowboydecoder.DETECT_DONG)

    def run(self):
        sensitivity = rospy.get_param('hotword_detector_node/sensitivity')
        audio_gain = rospy.get_param('hotword_detector_node/audio_gain')
        model_path = "dataset/snowboy_models/" + rospy.get_param("hotword_detector_node/model_name") + ".umdl"
        detector = snowboydecoder.HotwordDetector(
            os.path.join(self.rospack.get_path('hotword_detector_and_speech_recognition'),  model_path),
            sensitivity=sensitivity,
            audio_gain=audio_gain
        )
        detector.start(detected_callback=self.hotword_detected_callback, audio_recorder_callback=self.audio_recorder_callback, sleep_time=0.01,silent_count_threshold=2)
        rospy.spin()
        detector.terminate()

if __name__ == '__main__':
    node = HotwordSpeechRecognitionNode()
    node.run()
