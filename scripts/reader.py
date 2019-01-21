#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32


class reader(object):
    def __init__(self):
        rospy.Subscriber("sis_vol", Float64, self.vol_switch)
        rospy.Subscriber("sis_cur", Float64, self.cur_switch)
        rospy.Subscriber("pm_power",Float64, self.power_switch)

    def vol_switch(self,q):
        self.vol = q.data

    def cur_switch(self,q):
        self.cur = q.data

    def power_switch(self,q):
        self.power = q.data

    def iv_reader(self):
        ad = []
        ad.append(self.vol)
        ad.append(self.cur)
        return ad

    def piv_reader(self):
        ad = []
        ad.append(self.vol)
        ad.append(self.cur)
        ad.append(self.power)
        return ad

if __name__ == "__main__" :
    rospy.init_node("reader")
    rospy.spin()
