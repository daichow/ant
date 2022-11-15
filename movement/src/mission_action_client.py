#! /usr/bin/env python3

from sys import exc_info
import rospy
import rospkg
import actionlib
# from gen3_configuration.msg import MissionMsgAction, MissionMsgFeedback, MissionMsgGoal, MissionMsgResult
from std_msgs.msg import Float32MultiArray, Empty
import yaml
import json
from pprint import pprint

rospack = rospkg.RosPack()

# SAVED_TRAJECTORIES_DIR = rospack.get_path(
#     'movement') + "/home/"

POSITION_FILES_DIR = rospack.get_path(
    'movement') + "/src/"


class WaypointMissionOperator:

    def __init__(self):
        self.preplanned_path = None
        self.waypoint_path = None

    # def feedback_callback(self, msg):
    #     print('Feedback received:', msg)

    # def call_server(self):

    #     client = actionlib.SimpleActionClient('mission_ac')

    #     client.wait_for_server()

    #     goal = MissionMsgGoal()

    #     goal.waypoint_mission = [str(d) for d in mission_op.waypoint_path]

    #     client.send_goal(goal, feedback_cb=self.feedback_callback)

    #     client.wait_for_result()

    #     result = client.get_result()

    #     return result

    # def read_from_trajectory_file(self, file_name):
    #     try:
    #         with open(file_name, 'r') as file_open:
    #             return yaml.unsafe_load(file_open)
    #     except Exception as e:
    #         rospy.logerr(e, exc_info=True)
    #         rospy.loginfo("ERROR 5: File " + file_name +
    #                       " cannot be found, opened, or read")
    #         return None

    def read_from_plan_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return yaml.load(file, Loader=yaml.FullLoader)
        except:
            rospy.loginfo("ERROR 1: File " + file_name +
                          " cannot be found, opened, or read")
            return None


if __name__ == '__main__':
    try:
        rospy.init_node('waypoint_action_client', anonymous=False)

        mission_op = WaypointMissionOperator()

        mission_op.waypoint_path = mission_op.read_from_plan_file(
            f"{POSITION_FILES_DIR}/home.yaml")['sequence']

        pprint(mission_op.waypoint_path)

        # result = mission_op.call_server()

    except rospy.ROSInterruptException as e:
        print('Something went wrong:', e)
