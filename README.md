# Robot Official Assistant

## Overview

This is an ros indigo package test on Ubuntu 14.04 LTS for turtlebot kobuki.

Launch folder contains ros launch files.

Param folder contains some config files used by move_base node.

Src folder contains the code of scan filter that filter the nan number of kinnect.

Scripts folder contains python scipts. `server.py` is a flask server host the webpage shown to people in charge of the food and drinks, and accpet request to control robot. `roa.py` is the ros node that control the robot and used by `server.py`.

## Install

Put `robot_official_assistant` in src folder of your catkin workspace, then run

```bash
rosdep update
rosdep install robot_official_assistant
catkin_make
```

## Usage

### Mapping

Launch gmapping_demo

```bash
roslaunch robot_official_assistant gmapping_demo.Launch
```

Open a new terminal, launch rviz to see the mapping.

```bash
roslaunch turtlebot_rviz_launchers view_navigation.launch
```

Open a new terminal, launch keyboard_teleop use keyboard to control turtlebot

```bash
roslaunch turtlebot_teleop keyboard_teleop.launch 
```

or use bluetooth with an APP.

After finishing mapping, save the map

```bash
 rosrun map_server map_saver -f /path/to/yourmap
```

### Navigation

Launch amcl_demo with your map

```bash
roslaunch robot_official_assistant amcl_demo.Launch map_file:=/path/to/yourmap
```

Now you can use rviz to specify a point for turtlebot to navigate, or start server.py by

```bash
rosrun robot_official_assistant server.py
```

and receive request from the web.


