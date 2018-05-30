#!/usr/bin/env python
import rospy
import json
from aws_mqtt_bridge.msg import MQTT_publish
from vesc_msgs.msg import VescStateStamped
from std_msgs.msg import Float64
from std_msgs.msg import String


import pandas

class Cloudclass():
	def __init__(self):

		Cloudclass.cloudAPI(self)


	def callback(self, data):
		#rospy.loginfo(rospy.get_caller_id() + " I heard '%s'", data)
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


		message = {}
		#print(self.voltage_input)
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
		self.msg.payload = json.dumps(message)
		rospy.loginfo(rospy.get_caller_id() + " Send %s to %s" % (self.msg.payload, self.msg.topic))

		self.pub.publish(self.msg)

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
		#Publisher(TOPICNAME,MESSAGETYPE,QUE) TOPICNAME is STATIC
		self.pub = rospy.Publisher('publish_to_aws', MQTT_publish, queue_size=10)
		#init_node(NODENAME, add random extenstion)
		rospy.init_node('cloudAPI', anonymous=True)

		rospy.Subscriber("vesc/sensors/core", VescStateStamped, self.callback)

		rate = rospy.Rate(2) # #Rate(frequency)
		self.msg = MQTT_publish() #Set the message type
		self.msg.topic = "RCcar/dashboard" #Set the AWS IoT Topic name

		#spin() simply keeps python from exiting until this node is stopped
		rospy.spin()

		###########################################################################
		#attributes_GPS = ['IMU_GPSLongetude', 'IMU_GPSLatetude[deg]','IMU_speedSpeed_IMU']
		#datasheet_all = pandas.read_csv("/media/sf_VM_Shared_Folder/MachineLearning/Formula-DataMining-MachineLearning-Batch/Drive_KTH_Formula_Student_1december.csv")
		#datasheet_GPS = pandas.DataFrame(datasheet_all, columns=attributes_GPS)
		#datasheet_GPS = datasheet_GPS[300:]
		#datasetvals_GPS = datasheet_GPS.values
		#initialvalue = 0
		###########################################################################

		#while not rospy.is_shutdown():

			#initialvalue = initialvalue + 1

			#rate.sleep()


if __name__ == '__main__':
	try:
		Cloudclass()
	except rospy.ROSInterruptException:
		pass
