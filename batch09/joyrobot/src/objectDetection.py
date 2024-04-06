#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError
import cv2
from std_srvs.srv import SetBool, SetBoolResponse
import torch
from std_msgs.msg import UInt16

class ImageProcessor:
    def __init__(self):
        rospy.init_node('object_detection_node')
        gesture_pub = rospy.Publisher('gesture', UInt16, queue_size=15)
        self.bridge = CvBridge()

        # Subscribers
        rospy.Subscriber('/camera/image/compressed', CompressedImage, self.image_callback)
        rospy.Service('/detect_objects', SetBool, self.detect_objects)
        self.model = torch.hub.load('/home/ubuntu/yolov5', 'custom','/home/ubuntu/yolov5/yolov5s.pt', source="local") 
        self.confidence_threshold = 0.4
        self.rotated_image = None
        rospy.loginfo("object_detection_node_ready")
        gesture_msg = UInt16()
        gesture_msg.data = 18
        gesture_pub.publish(gesture_msg)
    def image_callback(self, data):
        try:
            # Convert compressed image to OpenCV image
            cv_image = self.bridge.compressed_imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return
        # Rotate the image by 180 degrees
        self.rotated_image = cv2.rotate(cv_image, cv2.ROTATE_180)

    def detect_objects(self,data):
        responce = SetBoolResponse()
        responce.success = False
        if(data.data):
            results = self.model(self.rotated_image)
            results_df = results.pandas().xyxy[0]
            filtered_results = results_df[results_df['confidence']
                                          > self.confidence_threshold]
            results_count = filtered_results['name'].value_counts()

            # Check if there is at least one predicted class
            if not results_count.empty:
                result_keywords = " , ".join(
                    [f"{count} {name}" for name, count in results_count.items()])
                responce.success = True
                responce.message = result_keywords
            else:
                responce.success = False
        return responce

    def run(self):
        rate = rospy.Rate(30)  # 10 Hz
        while not rospy.is_shutdown():
            rate.sleep()


if __name__ == '__main__':
    try:
        image_processor = ImageProcessor()
        image_processor.run()
    except rospy.ROSInterruptException:
        pass