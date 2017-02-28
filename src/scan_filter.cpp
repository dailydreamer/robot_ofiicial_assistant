#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
sensor_msgs::LaserScan input_scan;
//sensor_msgs::LaserScan filtered_scan;

void filterCallback(const sensor_msgs::LaserScan& msg) {
//	ROS_INFO("I heard: [%f]", msg.ranges[0]);
  input_scan = msg ;
	for (int i=0; i < input_scan.ranges.size(); i++) {
  	if (std::isnan(input_scan.ranges[i])) {
    	input_scan.ranges[i] = 9;
    }
	}
}

int main(int argc, char **argv) {
	ros::init(argc,argv, "filter");
 	
  ros::NodeHandle n;

	ros::Subscriber sub = n.subscribe("/scan_raw", 1000, filterCallback);
	ros::Publisher pub = n.advertise<sensor_msgs::LaserScan>("/scan", 1000);
  ros::Rate r(30);
	while (ros::ok()) {
		ros::spinOnce();
		r.sleep();
   	pub.publish(input_scan);		
	}	
}  
