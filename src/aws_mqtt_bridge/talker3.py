#!/usr/bin/env python
import rospy
import json
from aws_mqtt_bridge.msg import MQTT_publish
from vesc_msgs.msg import VescStateStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from std_msgs.msg import String
import time

import pandas

class Cloudclass():
	def __init__(self):

		Cloudclass.cloudAPI(self)


	def callback_main(self, data):
		start_time = time.time()
		#rospy.loginfo(rospy.get_caller_id() + " I heard '%s'", data)
		#Store  the subscribed message here in new variables
		self.voltage_input = data.state.voltage_input
		self.temperature_pcb = data.state.temperature_pcb
		self.current_motor = data.state.current_motor
		self.current_input = data.state.current_input
		self.speed = data.state.speed
		self.duty_cycle = data.state.duty_cycle
		self.charge_drawn = data.state.charge_drawn
		self.charge_regen = data.state.charge_regen
		self.energy_drawn = data.state.energy_drawn
		self.energy_regen = data.state.energy_regen
		self.displacement = data.state.displacement
		self.distance_traveled = data.state.distance_traveled
		self.sequence = data.header.seq
		self.timestamp_sec = data.header.stamp.secs
		self.timestamp_nanosec = data.header.stamp.nsecs





		message = {}
		#print(self.voltage_input)
		#Store the data in a JSON format
		message['voltage_input'] = self.voltage_input
		message['temperature_pcb'] = self.temperature_pcb
		message['current_motor'] = self.current_motor
		message['current_input'] = self.current_input
		message['speed'] = self.speed
		message['duty_cycle'] = self.duty_cycle
		message['charge_drawn'] = self.charge_drawn
		message['charge_regen'] = self.charge_regen
		message['energy_drawn'] = self.energy_drawn
		message['energy_regen'] = self.energy_regen
		message['displacement'] = self.displacement
		message['distance_traveled'] = self.distance_traveled
		message['RCcarNumber'] = self.RCcarNumber
		message['sequence'] = self.sequence
		message['timestamp'] = rospy.get_time()
		#message['timestamp_nanosec'] = self.timestamp_nanosec

		message['position_x'] = self.position_x
		message['position_y'] = self.position_y
		message['acceleration'] = self.acceleration
		message['turning_gyro'] = self.turning_gyro

		#Dump the message into a payload
		self.msg.payload = json.dumps(message)
		#rospy.loginfo(rospy.get_caller_id() + " Send %s to %s" % (self.msg.payload, self.msg.topic))
		self.t = self.t + 1
		if self.t == self.pub_rate:
			#Publish the payload to the MQTT broker
			self.pub.publish(self.msg)
			self.t = 0
		print("--- %s seconds ---" % (time.time() - start_time))

	def callback_odom(self, data):
		self.position_x = data.pose.pose.position.x
		self.position_y = data.pose.pose.position.y
		self.acceleration = data.twist.twist.linear.x
		self.turning_gyro = data.twist.twist.angular.z

	def cloudAPI(self):
		self.voltage_input = 0
		self.temperature_pcb = 0
		self.current_motor = 0
		self.current_input = 0
		self.speed = 0
		self.duty_cycle = 0
		self.charge_drawn = 0
		self.charge_regen = 0
		self.energy_drawn = 0
		self.energy_regen = 0
		self.displacement = 0
		self.distance_traveled = 0
		self.RCcarNumber = 1
		self.sequence = 0
		self.timestamp_sec = 0
		self.timestamp_nanosec = 0

		self.position_x =  0
		self.position_y = 0
		self.acceleration = 0
		self.turning_gyro = 0
		self.pub_rate = 10 #50 = hz, 50/pub_rate = frequency
		self.t = self.pub_rate-1 #So we send the first message and not wait

		#Publisher(TOPICNAME,MESSAGETYPE,QUE) TOPICNAME is STATIC
		self.pub = rospy.Publisher('publish_to_aws', MQTT_publish, queue_size=1) #0 is Infinitewhich is danger
		#init_node(NODENAME, add random extenstion)
		rospy.init_node('cloudAPI', anonymous=True)

		rospy.Subscriber("vesc/sensors/core", VescStateStamped, self.callback_main)
		rospy.Subscriber("vesc/odom", Odometry, self.callback_odom)

		print(rospy.get_rostime()) #detailed time as long int
		print(rospy.get_time()) #Time as a float
		print(time.time())

		#rate = rospy.Rate(5) # #Rate(frequency)
		self.msg = MQTT_publish() #Set the message type
		self.msg.topic = "RCcar/dashboard" #Set the AWS IoT Topic name

		#spin() simply keeps python from exiting until this node is stopped
		rospy.spin()


if __name__ == '__main__':
	try:
		Cloudclass()
	except rospy.ROSInterruptException:
		pass
