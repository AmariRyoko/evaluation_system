#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime
import numpy as np
import matplotlib.pyplot as plt

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int64

sys.path.append("/home/amigos/ros/src/evaluation_system/scripts")
import reader

os.chdir("/home/amigos/")

class yfactor(object):
    def __init__(self):

        self.pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)
        self.pub_speed = rospy.Publisher("chopper_spd",Int64, queue_size=1)
        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")

    def measure(self, initv, interval, repeat):
        da_all = []
        speed = 5000
        msg = Int64()
        msg.data = speed
        self.pub_speed.publish(speed)
        for i in range(repeat+1):
            da = []
            vol = initv+interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(3)
            ret = reader.piv_reader()
            da.append(ret[0])
            da.append(ret[1])
            da.append(ret[2])
            print(da)
            da_all.append(da)
            np.savetxt("yfactor_{0}.txt".format(self.ut), np.array(da_all), delimiter=" ")
        speed = 0
        msg = Int64()
        msg.data = speed
        self.pub_speed.publish(speed)
        yf.pv_iv_plot()

    def pv_iv_plot(self):
        plt.title("yfactor-PV-IV")
        plt.xlabel("V[mV]")
        piv = np.loadtxt("yfactor_{0}.txt".format(self.ut))
        fig ,ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(piv[:,0], piv[:,1],linestyle='solid', marker=None, color="red")
        ax2.plot(piv[:,0], piv[:,2],linestyle='solid', marker=None, color="blue")
        plt.savefig("yfactor_{0}.png".format(self.ut))
        plt.show()

    def pv_plot(self):
        plt.title("PV")
        plt.xlabel("V[mV]")
        plt.ylabel("P[dBm]")
        iv = np.loadtxt("yfactor_{0}.txt".format(self.ut))
        plt.plot(iv[:,0], iv[:,2], linestyle='solid', marker=None, color="red")
        plt.savefig("yfactor_{0}.png".format(self.ut))
        plt.show()


if __name__ == "__main__" :
    rospy.init_node("yfactor_measure")
    reader = reader.reader()
    yf = yfactor()
    initv = int(input("start_voltage = ? [mV]"))
    lastv = int(input("finish_voltage = ? [mV]"))
    interval = float(input("interval_voltage = ? [mV]"))
    repeat = int((lastv-initv)/interval)
    sys.exit(yf.measure(initv,interval,repeat))
