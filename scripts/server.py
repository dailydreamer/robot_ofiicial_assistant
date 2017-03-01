#!/usr/bin/env python

import rospy
from roa import roa

from flask import Flask
from flask import request
from flask import render_template
from werkzeug.contrib.cache import SimpleCache
app = Flask(__name__)
cache = SimpleCache()
r = roa()

fetch_x = 0.0
fetch_y = 0.0
return_x = 0.0
return_y = 0.0

@app.route("/")
def hello():
  rospy.loginfo("Hello world!")
  r.sound_play("Hello world!")
  return "Hello World!"

@app.route("/wants")
def wants():
  wants = cache.get("wants")
  return render_template("wants.html", watns=wants)
  
def get_location(dx, dy):
  x = dx
  y = dy
  try:
    x = float(request.args.get('x'))
  except Exception:
    rospy.loginfo("Invalid x")
  try:
    y = float(request.args.get('y'))  
  except Exception:
    rospy.loginfo("Invalid y")
  rospy.loginfo("x: "+str(x) + " y: "+str(y))
  return x, y

# /fetch?x=fetch_x&y=fetch_y&wants=coffee
@app.route("/fetch")
def fetch():
  x, y = get_location(fetch_x, fetch_y)
  wants = "coffee"
  try:
    wants = float(request.args.get('wants'))
  except Exception:
    rospy.loginfo("Invalid wants")
  cache.set("wants", wants)
  rospy.loginfo("Fetching...")
  # location of drinking room
  is_success = r.run(x, y)
  if is_success:
    rospy.loginfo("Successful reach point")
    for _ in range(2):
      r.sound_play("Please give me "+wants+", thanks!")
      rospy.sleep(4)
  else:
    rospy.loginfo("Not success, dumb robot...")
  return "fetch"

# /return?x=return_x&y=return_y
@app.route("/return")
def ret():
  r.sound_play("Thank you!")
  x, y = get_location(return_x, return_y)
  rospy.loginfo("Returning...")
  # location of service caller
  is_success = r.run(x, y)
  if is_success:
    rospy.loginfo("Successful reach point")
    r.sound_play("At your service!")
  else:
    rospy.loginfo("Not success, dumb robot...")
  return "return"    

if __name__ == "__main__":
  rospy.loginfo("Server start at port 3000")
  app.run(port=3000)
  rospy.loginfo("Server shutdown")
  # handle shutdown manully cause disable_signals is True
  rospy.signal_shutdown("Server shutdown")