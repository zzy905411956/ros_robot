#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import rospy
import roslib
from math import sin, cos, pi
from std_msgs.msg import String
import serial
import time
import struct
from geometry_msgs.msg import Quaternion, Twist, Pose
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
#******************************************************
def talk():
    
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    rospy.loginfo(rate)
    current_time = rospy.get_time()
    last_time = rospy.get_time()
    while not rospy.is_shutdown():
	dt = (current_time-last_time)
	#a = 2*dt
        pub.publish(current_time)
	rospy.loginfo(dt)
        rate.sleep()

if __name__ == '__main__':
    try:
        talk()
    except rospy.ROSInterruptException:
	pass
