#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from sound_play.libsoundplay import SoundClient
from kobuki_msgs.msg import ButtonEvent

class roa():
  point_x = 0
  point_y = 0
  is_finish_fetching = False

  def __init__(self):
    rospy.init_node('robot_amcl', anonymous=False)
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
    rospy.loginfo("shutdown...")

  def button_event(self, data):
    if (data.button == ButtonEvent.Button0):
      self.is_finish_fetching = True
      rospy.loginfo("press button 0") 

  def run(self):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose = Pose(Point(self.point_x, self.point_y, 0), Quaternion(0,0,0,1.0))

    self.move_base.send_goal(goal)

    is_success = self.move_base.wait_for_result()

    if is_success:
      rospy.loginfo("Successful reach point")
      self.is_finish_fetching = False
      while (self.is_finish_fetching == False):
        self.sound_play("Please give me coffee, thanks!")
        rospy.sleep(4)
      self.sound_play("Thank you!") 
    else:
      rospy.loginfo("Not success, dumb robot...")

  def sound_play(self, word):
    self.sound_handle.say(word)

if __name__ == '__main__':
  try:
    r = roa()
    r.run()
  except rospy.ROSInterruptException:
    rospy.loginfo("Exception thrown")
