#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import ButtonEvent

class roa():
  def __init__(self):
    # disable_signals so that ros won't stuck the flask server
    rospy.init_node('robot_amcl', anonymous=False, disable_signals=True)
    rospy.on_shutdown(self.shutdown)

    rospy.Subscriber("/mobile_base/events/button", ButtonEvent, self.button_event)

    # init sound handle
    self.sound_handle = SoundClient()
    rospy.sleep(1)

    # init actionlib
    self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("wait for the action server to come up")
    # wait for move_base server
    self.move_base.wait_for_server()

  def shutdown(self):
    rospy.loginfo("Shutdown...")

  def button_event(self, data):
    if (data.button == ButtonEvent.Button0):
      rospy.loginfo("Pressing button 0") 

  def run(self, point_x, point_y):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    # ros actionlib needs none zero quaternion, so add small w in quaternion 
    goal.target_pose.pose = Pose(Point(point_x, point_y, 0), Quaternion(0,0,0,1.0))
    self.move_base.send_goal(goal)
    is_success = self.move_base.wait_for_result()
    return is_success

  def sound_play(self, word):
    self.sound_handle.say(word)

if __name__ == '__main__':
  # just for test
  try:
    r = roa()
    r.run(0, 0)
  except rospy.ROSInterruptException:
    rospy.loginfo("Exception thrown")