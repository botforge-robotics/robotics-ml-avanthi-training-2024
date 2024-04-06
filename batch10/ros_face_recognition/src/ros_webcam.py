#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class WebcamPublisher:
    def __init__(self):
        rospy.init_node('webcam_publisher', anonymous=True)
        self.bridge = CvBridge()
        self.raw_image_pub = rospy.Publisher(
            '/raw_image_topic', Image, queue_size=10)
        # Adjust the index if necessary (0 for the default webcam)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            rospy.logerr("Unable to open the webcam.")
            rospy.signal_shutdown("Unable to open the webcam.")
        else:
            rospy.loginfo("Webcam opened successfully.")

    def publish_images(self):
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if ret:
                # Convert OpenCV image to raw ROS message
                try:
                    raw_msg = self.bridge.cv2_to_imgmsg(
                        frame, "bgr8")  # Convert to ROS Image message
                    raw_msg.header.stamp = rospy.Time.now()
                    self.raw_image_pub.publish(raw_msg)
                except CvBridgeError as e:
                    rospy.logerr(e)
            else:
                rospy.logwarn("Failed to capture frame from webcam.")
            # Adjust the sleep duration based on the desired publishing rate
            rospy.sleep(0.1)

    def shutdown(self):
        rospy.loginfo("Shutting down...")
        self.cap.release()


if __name__ == '__main__':
    try:
        webcam_publisher = WebcamPublisher()
        webcam_publisher.publish_images()
    except rospy.ROSInterruptException:
        pass
