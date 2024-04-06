#!/usr/bin/env python3

import rospy
from std_srvs.srv import Trigger, TriggerResponse
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import time
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2.aruco as aruco
import numpy as np
from geometry_msgs.msg import Twist


class DockingServer:
    def __init__(self):
        rospy.init_node('docking_server')
        self.move_base_client = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)
        self.move_base_client.wait_for_server()
        self.docking_service = rospy.Service(
            'move_to_docking_station', Trigger, self.handle_move_to_docking)
        self.image_pub = rospy.Publisher(
            "/detected_markers", Image, queue_size=1)
        self.id_pub = rospy.Publisher("/arudo_ID", String, queue_size=1)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(
            "/raspicam_node/image", Image, self.image_callback)
        self.marker_id = 0
        self.marker_area = 0
        self.marker_center = (0, 0)
        self.image = None
        self.min_marker_area = 7000
        self.max_marker_area = 30000
        self.marker_confidence = 100

    def handle_move_to_docking(self, req):

        docking_pose = PoseStamped()
        docking_pose.header.frame_id = 'map'
        docking_pose.pose.position.x = 0.4
        docking_pose.pose.position.y = 0.0
        docking_pose.pose.orientation.w = 1.0

        result = self.move_to_pose(docking_pose)
        if result:
            if (self.image is not None and self.marker_id != 0):
                while True:
                    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
                    move = Twist()

                    # move forward backward
                    if (self.marker_area > self.min_marker_area and self.marker_area < self.max_marker_area):
                        move.linear.x = 0.05
                        move.angular.z = 0.0
                    if (self.marker_area > self.max_marker_area):
                        move.linear.x = 0
                        move.angular.z = 0
                        vel_pub.publish(move)
                        break

                    # turn left or right
                    width = self.image.shape[1]
                    left_margin = (width / 2) - (0.05 * width)
                    right_margin = (width / 2) + (0.05 * width)

                    if (self.marker_center[0] < left_margin and self.marker_center[0] != 0):
                        move.angular.z = 0.1
                    elif (self.marker_center[0] > right_margin and self.marker_center[0] != 0):
                        move.angular.z = -0.1
                    else:
                        move.angular.z = 0.0
                    vel_pub.publish(move)
            return TriggerResponse(success=True, message="Moved to docking station successfully!")
        else:
            return TriggerResponse(success=False, message="Failed to move to docking station.")

    def move_to_pose(self, pose):
        goal = MoveBaseGoal()
        goal.target_pose = pose
        self.move_base_client.send_goal(goal)
        self.move_base_client.wait_for_result()
        return self.move_base_client.get_state() == actionlib.GoalStatus.SUCCEEDED

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.image = cv_image
        except CvBridgeError as e:
            print(e)

        markers_img, ids_list = self.detect_aruco(cv_image)

        if ids_list is None:
            self.id_pub.publish(ids_list)
        else:
            ids_str = ''.join(str(e) for e in ids_list)
            self.id_pub.publish(ids_str)

        try:
            self.image_pub.publish(
                self.bridge.cv2_to_imgmsg(markers_img, "bgr8"))
        except CvBridgeError as e:
            print(e)

    def calculate_quadrilateral_area(self, corners):
        # Calculate the area of a quadrilateral given its corner coordinates
        x = corners[:, 0]
        y = corners[:, 1]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def calculate_centroid(self, corners):
        # Calculate the centroid of a polygon given its corner coordinates
        centroid = np.mean(corners, axis=0)
        return centroid.flatten()

    def detect_aruco(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(
            aruco_dict, detectorParams=parameters)
        # detect the sruco markers and display its aruco id.
        markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(
            gray)

        for i in range(len(markerCorners)):
            if (markerIds[i] == 393):
                self.marker_confidence += 1
                if self.marker_confidence > 100:
                    self.marker_confidence = 100
                self.marker_id = 393
                rospy.loginfo(self.marker_area)
            else:
                self.marker_confidence -= 1
                if self.marker_confidence < 0:
                    self.marker_confidence = 0
                if self.marker_confidence < 50:
                    self.marker_id = 0
                    self.marker_area = 0
                    self.marker_center = (0, 0)
            marker_corners = markerCorners[0][0]
            self.marker_area = self.calculate_quadrilateral_area(
                marker_corners)
            self.marker_center = self.calculate_centroid(marker_corners)
        output = aruco.drawDetectedMarkers(img, markerCorners, markerIds)
        return output, markerIds


if __name__ == '__main__':
    try:
        docking_server = DockingServer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
