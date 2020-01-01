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
base_frame = 'base_link'
#******默认起始位置
x = 0
y = 0
th = 0
#*****机器人默认前进速度
vx = 0
vy = 0
vth = 0
delta_t = 0.1	#lun ban jing	
#gear_reduction = 30.0  #jian su bi
wheel_track = 0.45   #lun jianju
multiplier = 4
#*******************************************************
speed_motorL =  ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x01','\x00','\x00','\x00','\x00']
speed_motorR =  ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x02','\x00','\x00','\x00','\x00']
motor_stop =    ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x01','\x00','\x00','\x00','\x00']
read_modeR =   ['\x00','\x00','\x00','\x06','\x01','\x08','\x40','\x03','\x21','\x01','\x00','\x00','\x00','\x00']
read_modeL =   ['\x00','\x00','\x00','\x06','\x01','\x08','\x40','\x03','\x21','\x02','\x00','\x00','\x00','\x00']
def listener():                                                                                                                                                                                                                                                                                                      
    x = 0
    ax = 0
    bx = 0
    y = 0
    th = 0
    odom_right = 0
    odom_left = 0
    rospy.loginfo("pub")
    rospy.init_node("listener",anonymous=True)#初始化节点catkin_ws/src/my_package/scripts/listener.py", line 70, in listener
    ser.write(read_modeR)
    time.sleep(0.2)
    ser.write(read_modeL)
    time.sleep(0.2)
    odomPub = rospy.Publisher('odom',Odometry,queue_size=5)
    odomBroadcaster = TransformBroadcaster()
    rate = rospy.Rate(50)
    rospy.loginfo("ggggggggggggggggg")
    rospy.on_shutdown(shutdown)
    while not rospy.is_shutdown():
	rospy.loginfo("true")
#**************************read speed********************
	last_time = rospy.Time.now()
	a_list = []
	n = ser.inWaiting()
	ser.flush()
	if n :
		data = ser.read(n)
		a_list.append(data)
		for i in range(n):
			if a_list[0][i] =='\x1b':
				if len(a_list[0][i+4:i+6])==2:
				    a = struct.unpack(">h",a_list[0][i+4:i+6])
				    ax = a[0]
				    odom_right = a[0] / 60 * 0.065 * pi
				    break
		for i in range(n):
			if a_list[0][i] =='+':
				if len(a_list[0][i+4:i+6])==2:
				    b = struct.unpack(">h",a_list[0][i+4:i+6])
				    bx = b[0]
				    odom_left = b[0] / 60 * 2 * delta_t * pi	
				    break
		print ax,bx		    
		ser.flushInput()
	else:
		shutdown()
#*************************************************************
	now = rospy.Time.now()
	dt = (rospy.Time.now()-last_time).to_sec()
	rospy.loginfo(dt)
	dx = (ax+bx) / 60 * 2 * delta_t * pi / 2.0
        dth = (ax-bx) * 2 * delta_t * pi / 60 / wheel_track
	vx = dx/dt
	vth = dth/dt
	print vx,vth
	if dx != 0:
	    fx = cos(dth)*dx
	    fy = -sin(dth)*dx
	    x += (cos(th)*fx - sin(th)*fy)
	    y += (sin(th)*fx + cos(th)*fy)	
	if dth != 0:
	    th += dth
	delta_x = (vx * cos(th) - vy * sin(th)) * dt
	delta_y = (vx * sin(th) + vy * cos(th)) * dt 
	delta_th = dth
	x += delta_x
        y += delta_y
        th += delta_th
	print x,y,th
	#***************************************
	quaternion = Quaternion()
	quaternion.x = 0.0
	quaternion.y = 0.0
	quaternion.z = sin(th/2.0)
	quaternion.w = cos(th/2.0)
	odomBroadcaster.sendTransform((x,y,0),(quaternion.x,quaternion.y,quaternion.z,quaternion.w),rospy.Time.now(),base_frame,'odom')
	odom = Odometry()
	odom.header.frame_id = "odom"
	odom.child_frame_id = base_frame
	odom.header.stamp = rospy.Time.now()
	odom.pose.pose.position.x = x
	odom.pose.pose.position.y = y
	odom.pose.pose.position.z = 0
	
	odom.twist.twist.linear.x = vx
	odom.twist.twist.linear.y = 0
	odom.twist.twist.angular.z = vth
	odomPub.publish(odom)
	rospy.loginfo("pub successful")
	last_time = now
	rate.sleep()
def shutdown():
    ser = serial.Serial("/dev/ttyTHS1",115200)
    #rospy.loginfo("stop the robot11111")
    time.sleep(0.2)
    ser.write(motor_stop)
    time.sleep(1)
if __name__ == '__main__':
    print ("connect successful!!!!!!!!!11111111111")
    ser = serial.Serial("/dev/ttyTHS1",115200)
    time.sleep(0.5)
    try:
        listener()
    except rospy.ROSInterruptException:
	pass
