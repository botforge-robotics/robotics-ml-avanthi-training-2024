#!/usr/bin/env python3
import os
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import time
import face_recognition
from ros_face_recognition.srv import TrainPerson, TrainPersonResponse
from ros_face_recognition.srv import DeletePerson, DeletePersonResponse
from ros_face_recognition.srv import RecognisePersonsOnce, RecognisePersonsOnceResponse
from ros_face_recognition.msg import RecogByNameAction, RecogByNameResult, RecogByNameFeedback
from actionlib import SimpleActionServer
import rospkg
import numpy as np
import shutil


class FaceTrainer():
    def __init__(self):
        rospy.init_node("face_trainer_node")
        self.rospack = rospkg.RosPack()
        self.bridge = CvBridge()
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.training_dir = os.path.join(
            self.rospack.get_path('ros_face_recognition'), "Face_Images")
        self.labels = []

        rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)
        rospy.Service('register_person', TrainPerson, self.train_person)
        rospy.Service('delete_person', DeletePerson, self.delete_person)
        rospy.Service('recognise_persons_once',
                      RecognisePersonsOnce, self.recognise_persons_once)
        rospy.Service('list_of_person_in_model',
                      RecognisePersonsOnce, self.list_of_person_in_model)
        self.recog_action_server = SimpleActionServer(
            "recognise_person", RecogByNameAction, execute_cb=self.recognise_face, auto_start=False)
        self.recog_action_server.start()
        self.train_model()

    def train_person(self, req):
        response = TrainPersonResponse()
        person_name = req.name.strip()
        person_dir = os.path.join(self.training_dir, person_name)

        if not os.path.exists(person_dir):
            os.makedirs(person_dir)
        self.face_locations = face_recognition.face_locations(self.cv_image)
        if self.face_locations:
            # Extract face location coordinates
            top, right, bottom, left = self.face_locations[0]
            # Crop the face region from the image
            face_image = self.cv_image[top:bottom, left:right]
            # Encode the face image
            face_encoding = face_recognition.face_encodings(face_image)
            if len(face_encoding) > 0:
                np.save(os.path.join(
                    person_dir, f"{person_name}.npy"), face_encoding[0])
                response.success = True
                self.train_model()
                return response

        response.success = False
        return response

    def delete_person(self, req):
        response = DeletePersonResponse()
        person_name = req.name.strip()
        person_dir = os.path.join(self.training_dir, person_name)

        if os.path.exists(person_dir):
            shutil.rmtree(person_dir)
            self.train_model()  # Retrain model after deleting person
            response.success = True
        else:
            response.success = False

        return response

    def recognise_persons_once(self, req):
        response = RecognisePersonsOnceResponse()
        self.face_locations = face_recognition.face_locations(self.cv_image)
        self.face_encodings = face_recognition.face_encodings(
            self.cv_image, self.face_locations)

        self.face_names = []
        if self.face_encodings:
            # Perform face recognition on the current frame
            names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    names.append(name)
                    response.success = True
                else:
                    response.success = False
            response.persons = names
        else:
            response.success = False

        return response

    def list_of_person_in_model(self, req):
        response = RecognisePersonsOnceResponse()
        response.success = True
        response.persons = self.labels
        return response

    def recognise_face(self, goal):
        feedback = RecogByNameFeedback()
        result = RecogByNameResult()
        person_name = goal.name.strip()
        start_time = rospy.Time.now()
        while not rospy.is_shutdown() and (rospy.Time.now() - start_time).to_sec() < goal.duration:
            # Find faces in the current frame
            self.face_locations = face_recognition.face_locations(
                self.cv_image)
            self.face_encodings = face_recognition.face_encodings(
                self.cv_image, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    self.face_names.append(name)
            if person_name in self.face_names:
                result.found = True
                feedback.found = True
                result.status = True
                self.recog_action_server.publish_feedback(feedback)
                self.recog_action_server.set_succeeded(result)
                return
            else:
                feedback.found = False
                self.recog_action_server.publish_feedback(feedback)

        result.found = False
        feedback.found = False
        result.status = True
        self.recog_action_server.publish_feedback(feedback)
        self.recog_action_server.set_succeeded(result)

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(
                data, desired_encoding="bgr8")
            small_frame = cv2.resize(cv_image, (0, 0), fx=0.25,
                                     fy=0.25)  # Reduce frame size

            # Convert the image from BGR color to RGB color
            self.cv_image = small_frame[:, :, ::-1]

        except CvBridgeError as e:
            rospy.logerr(e)
            return

    def train_model(self):
        # Load training data from directories
        self.labels = [name for name in os.listdir(
            self.training_dir) if os.path.isdir(os.path.join(self.training_dir, name))]
        self.known_face_encodings = []
        self.known_face_names = []
        for label in self.labels:
            person_dir = os.path.join(self.training_dir, label)
            for file in os.listdir(person_dir):
                if file.endswith(".npy"):
                    face_encoding = np.load(os.path.join(person_dir, file))
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(label)

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        face_trainer = FaceTrainer()
        face_trainer.run()
    except rospy.ROSInterruptException:
        pass
