#!/usr/bin/env python
import rospy, ipfsapi
from robonomics_liability.msg import Liability
from std_srvs.srv import Empty
from std_msgs.msg import String

objective = ""


if __name__ == "__main__":
        print("let the game begin")
        rospy.init_node('publish_hash_node')
        pub = rospy.Publisher("sensor_data_hash", String, queue_size=10)
        ipfs = ipfsapi.connect("localhost", 5001)

        def callback(data):
                global objective
                rospy.loginfo("Inside callback")
                service_name = '/liability/' + objective + '/finish'
                rospy.loginfo("Service name: " + service_name)
                try:
                        liability_service = rospy.ServiceProxy(service_name, Empty)
                except rospy.ServiceException as e:
                        print ("Service call failed: ")

                #print("Inside callback")
                hash = ipfs.add("/home/akru/storage", recursive=True)
                rospy.loginfo("Now publishing..." + hash[-1]['Hash'])
                pub.publish(hash[-1]['Hash'])
                resp1 = liability_service()
                rospy.loginfo("Done")

        def save_objective(data):
                global objective
                objective = data.objective
                rospy.loginfo("New objective is " + objective)

        print("subscribing...")
        rospy.Subscriber("/task", String, callback)
        rospy.Subscriber("/liability/incoming", Liability, save_objective)
        rospy.spin()