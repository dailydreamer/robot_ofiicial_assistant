#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist

point_x = 0
point_y = 0
point_z = 0

def init():
  rospy.init_node('robot_amcl', anonymous=False)
  rospy.on_shutdown(shutdown)
  move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
  rospy.loginfo("wait for the action server to come up")
  # wait for move_base server
  move_base.wait_for_server()
  
  goal = MoveBaseGoal()
  goal.target_pose.header.frame_id = 'map'
  goal.target_pose.header.stamp = rospy.Time.now()
  goal.target_pose.pose = Pose(Point(point_x, point_y, point_z), Quaternion(0,0,0,0))

  move_base.send_goal(goal)

  is_success = move_base.wait_for_result()

  if is_success:
    rospy.loginfo("Successful reach point")
  else:
    rospy.loginfo("Not success, dumb robot...")

def shutdown():
  rospy.loginfo("shutdown...")

if __name__ == '__main__':
  try:
    init()
  except rospy.ROSInterruptException:
    rospy.loginfo("Exception thrown")
