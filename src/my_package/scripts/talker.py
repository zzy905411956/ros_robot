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
gear_reduction = 30.0  #jian su bi
wheel_track = 0.45   #lun jianju
#*******************************************************
speed_motorL =  ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x01','\x00','\x00','\x00','\x00']
speed_motorR =  ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x02','\x00','\x00','\x00','\x00']
motor_stop =    ['\x00','\x00','\x00','\x06','\x01','\x08','\x23','\x02','\x20','\x01','\x00','\x00','\x00','\x00']
read_modeR =   ['\x00','\x00','\x00','\x06','\x01','\x08','\x40','\x03','\x21','\x01','\x00','\x00','\x00','\x00']
read_modeL =   ['\x00','\x00','\x00','\x06','\x01','\x08','\x40','\x03','\x21','\x02','\x00','\x00','\x00','\x00']
#*********************************************************
def speed_set(RobotV,YawRate):
    if YawRate == 0:
        leftV = RobotV
	rightV = RobotV
    elif RobotV == 0:
	rightV = YawRate / 2.0
	leftV = -rightV
    else:
        leftV =  RobotV - YawRate / 2.0
        rightV = RobotV + YawRate / 2.0
    print leftV ,rightV
    LeftWheelV  = (leftV * 60 / 2 / pi / delta_t)
    RightWheelV = (rightV * 60 / 2 / pi / delta_t)
    intRightWheelV = int(RightWheelV)
    intLeftWheelV = int(LeftWheelV)
    print intRightWheelV ,intLeftWheelV
    speed_motorL[10] = struct.pack("<h",intLeftWheelV)[-2]
    speed_motorL[11] = struct.pack("<h",intLeftWheelV)[-1]

    speed_motorR[10] = struct.pack("<h",intRightWheelV)[-2]
    speed_motorR[11] = struct.pack("<h",intRightWheelV)[-1]
    #print speed_motorL[8:10]
    #print speed_motorR[8:10]
def shutdown():
    ser = serial.Serial("/dev/ttyTHS1",115200)
    rospy.loginfo("stop the robot")
    time.sleep(0.2)
    ser.write(motor_stop)
    time.sleep(1)
def callback(cmd_input):
    RobotV = cmd_input.linear.x
    YawRate = cmd_input.angular.z
    if RobotV==0 and YawRate==0:
	ser.write(motor_stop)
	time.sleep(0.2)
    else:
	speed_set(RobotV,YawRate)
	ser.write(speed_motorL)
	time.sleep(0.01)
	ser.write(speed_motorR)
	#print "change speed successful"
	rospy.sleep(0.02)
#***********************************************************

if __name__ == '__main__':
    print ("connect successful!!!!!!!!!11111111111")
    ser = serial.Serial("/dev/ttyTHS1",115200)
    rospy.init_node("base_controll",anonymous=True)#初始化节点
    rospy.Subscriber("cmd_vel",Twist,callback)
    rospy.spin()
    rospy.on_shutdown(shutdown)
    



