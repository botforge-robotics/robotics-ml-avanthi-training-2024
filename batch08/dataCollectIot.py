#!/usr/bin/env python3

import rospy
from std_srvs.srv import Trigger, TriggerResponse
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import time
from Adafruit_IO import MQTTClient, Client
import board
import adafruit_dht

class DataCollectServer:
    def __init__(self):
        rospy.init_node('iot_data_node')
        self.move_base_client = actionlib.SimpleActionClient(
            'move_base', MoveBaseAction)
        self.move_base_client.wait_for_server()
        self.docking_service = rospy.Service(
            'move_to_docking_station', Trigger, self.move_to_collect_data)
        self.ADAFRUIT_IO_KEY = "e072eec983034a54ae1bceaa43b09232"
        self.ADAFRUIT_IO_USERNAME = "nagachaitanya948"
        self.locations = [(-0.5, 0.5, 1.0), (0.5, 0.5, 1.0)]
        self.mqtt_client = MQTTClient(
            self.ADAFRUIT_IO_USERNAME, self.ADAFRUIT_IO_KEY)
        self.aio = Client(self.ADAFRUIT_IO_USERNAME, self.ADAFRUIT_IO_KEY)
        self.mqtt_client.on_connect = self.mqtt_connected
        self.mqtt_client.on_disconnect = self.mqtt_disconnected
        self.mqtt_client.on_message = self.Mqtt_message
        self.mqtt_client.on_subscribe = self.mqtt_subscribe
        self.mqtt_feedId = "start"
        time.sleep(2)
        self.mqtt_client.connect()
        self.mqtt_client.loop_background()
        self.temp_feed = self.aio.feeds("temperature")
        self.humid_feed = self.aio.feeds("humidity")
        self.status_feed = self.aio.feeds("status")
        self.current_temp_value = 0.0
        self.current_humid_value = 0.0
        self.sensor = adafruit_dht.DHT11(board.D4)
    def mqtt_connected(self, client):
        rospy.loginfo(
            'Connected to Adafruit IO!  Listening for {0} changes...'.format(self.mqtt_feedId))
        client.subscribe(self.mqtt_feedId)

    def mqtt_subscribe(self, client, userdata, mid, granted_qos):
        # This method is called when the client subscribes to a new feed.
        rospy.loginfo('Subscribed to {0} with QoS {1}'.format(
            self.mqtt_feedId, granted_qos[0]))

    def mqtt_disconnected(self, client):
        # Disconnected function will be called when the client disconnects.
        rospy.loginfo('Disconnected from Adafruit IO!')

    def Mqtt_message(self, client, feed_id, payload):
        # Message function will be called when a subscribed feed has a new value.
        # The feed_id parameter identifies the feed, and the payload parameter has
        # the new value.
        rospy.loginfo(
            'Feed {0} received new value: {1}'.format(feed_id, payload))
        if feed_id == "start" and int(payload) == 1:
            self.move_to_collect_data({})

    def move_to_collect_data(self, req):
        self.aio.send_data(self.status_feed.key, 1)
        for location in self.locations:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = location[0]
            pose.pose.position.y = location[1]
            pose.pose.orientation.w = location[2]

            result = self.move_to_pose(pose)
            if result:
                metadata = {'lat': location[0],
                            'lon': location[1],
                            'ele': location[2],
                            'created_at': None}
                self.current_temp_value = sensor.temperature
                self.current_humid_value = sensor.humidity
                self.aio.send_data(self.temp_feed.key,
                                   self.current_temp_value, metadata)
                self.aio.send_data(self.humid_feed.key,
                                   self.current_humid_value, metadata)
                time.sleep(3)

        self.aio.send_data(self.status_feed.key, 0)
        return TriggerResponse(success=True, message="data collected succefully!")

    def move_to_pose(self, pose):
        goal = MoveBaseGoal()
        goal.target_pose = pose
        self.move_base_client.send_goal(goal)
        self.move_base_client.wait_for_result()
        return self.move_base_client.get_state() == actionlib.GoalStatus.SUCCEEDED


if __name__ == '__main__':
    try:
        data_collect_server = DataCollectServer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
