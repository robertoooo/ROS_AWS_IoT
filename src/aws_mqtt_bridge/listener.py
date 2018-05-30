#!/usr/bin/env python
import rospy
import json
from std_msgs.msg import Float64

def callback(data):
    delay = rospy.get_time() - data.data
    rospy.loginfo(rospy.get_caller_id() + " I heard '%s'", delay)

def listener():
    # init node
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("timestamptopic", Float64, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
