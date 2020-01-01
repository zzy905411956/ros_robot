#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import pi

    
def shutdown():
        rospy.loginfo("Stopping the robot...")
        cmd_vel.publish(Twist())
        rospy.sleep(1)
if __name__ == '__main__':
    cmd_vel = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    rospy.init_node('talker12345', anonymous=True)
    rospy.on_shutdown(shutdown)
    rate = 50
    r = rospy.Rate(rate) 
    linear_speed = 0.2
    goal_distance = 1.0
    linear_duration = goal_distance / linear_speed
    angular_speed = 0.2
    goal_angle = pi
    angular_duration = goal_angle / angular_speed
    move_cmd = Twist()
    move_cmd.linear.x = linear_speed
    #ticks = int(linear_duration * rate)
    cmd_vel.publish(move_cmd)
    rospy.sleep(linear_duration)
    r.sleep()
    move_cmd = Twist()
    cmd_vel.publish(move_cmd)
    rospy.sleep(1)
    move_cmd.angular.z = angular_speed
    ticks = int(goal_angle * rate)  
    for t in range(ticks):           
        cmd_vel.publish(move_cmd)
        r.sleep()
    move_cmd = Twist()
    cmd_vel.publish(move_cmd)
    rospy.sleep(1)    

