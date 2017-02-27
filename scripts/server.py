#!/usr/bin/env python

import rospy
from roa import roa

from flask import Flask
app = Flask(__name__)
r = roa()

@app.route("/")
def hello():
  rospy.loginfo("Hello world!")
  r.sound_play("Hello world!")  
  return "Hello World!"

@app.route("/fetch")
def fetch():
  rospy.loginfo("Fetching...")
  # location of drinking room
  is_success = r.run(0, 0)
  if is_success:
    rospy.loginfo("Successful reach point")
    for _ in range(2):
      r.sound_play("Please give me coffee, thanks!")
      rospy.sleep(4)
  else:
    rospy.loginfo("Not success, dumb robot...")

@app.route("/return")
def ret():
  self.sound_play("Thank you!")
  # location of service caller
  is_success = r.run(0, 0)
  if is_success:
    rospy.loginfo("Successful reach point")
    r.sound_play("Your coffee!")
  else:
    rospy.loginfo("Not success, dumb robot...")

if __name__ == "__main__":
  rospy.loginfo("Server start at port 3000")
  app.run(port=3000)
  rospy.loginfo("Server shutdown")
  # handle shutdown manully cause disable_signals is True
  rospy.signal_shutdown("Server shutdown")