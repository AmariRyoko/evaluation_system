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

os.chdir("/home/amigos/DSB")

class yfactor(object):
    def __init__(self):

        self.pub_vol = rospy.Publisher("sis_vol_cmd", Float64, queue_size=1)
        self.t = datetime.datetime.now()
        self.ut = self.t.strftime("%Y%m%d-%H%M%S")

    def measure_hot(self, initv, interval, repeat):
        da_all = []
        for i in range(repeat+1):
            da = []
            vol = initv+interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(0.1)
            ret = reader.piv_reader()
            time.sleep(0.01)
            da.append(ret[0])
            da.append(ret[1])
            da.append(ret[2])
            print(da)
            da_all.append(da)
            time.sleep(0.01)
            np.savetxt("yfactor_hot_{0}.txt".format(self.ut), np.array(da_all), delimiter=" ")

    def measure_cold(self, initv, interval, repeat):
        da_all = []
        for i in range(repeat+1):
            da = []
            vol = initv+interval*i
            msg = Float64()
            msg.data = vol
            self.pub_vol.publish(vol)
            time.sleep(0.1)
            ret = reader.piv_reader()
            time.sleep(0.01)
            da.append(ret[0])
            da.append(ret[1])
            da.append(ret[2])
            print(da)
            da_all.append(da)
            time.sleep(0.01)
            np.savetxt("yfactor_cold_{0}.txt".format(self.ut), np.array(da_all), delimiter=" ")

    def pv_iv_plot(self):
        hot = np.loadtxt("yfactor_hot_{0}.txt".format(self.ut))
        cold = np.loadtxt("yfactor_cold_{0}.txt".format(self.ut))
        fig ,ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.scatter(hot[:,0], hot[:,1],linestyle='solid', marker=".", color="green" ,label='I-V')
        ax2.scatter(hot[:,0], hot[:,2],linestyle='solid', marker=".", color="red", label='HOT')
        ax2.scatter(cold[:,0], cold[:,2],linestyle='solid', marker=".", color="blue", label='COLD')
        ax1.set_title("yfactor_Hot_Cold_measurement")
        ax1.set_xlabel("voltage[mV]")
        ax1.set_ylabel("current[uA]")
        ax2.set_ylabel("power[dBm]")
        ax2.legend(loc='upper right')
        plt.savefig("yfactor_{0}.png".format(self.ut))
        plt.show()


if __name__ == "__main__" :
    rospy.init_node("yfactor_hotcold")
    reader = reader.reader()
    yf = yfactor()
    initv = int(input("start_voltage = ? [mV]"))
    lastv = int(input("finish_voltage = ? [mV]"))
    interval = float(input("interval_voltage = ? [mV]"))
    repeat = int((lastv-initv)/interval)
    input("Are you ready HOT measurement?\n Press enter")
    print("Measuring HOT")
    yf.measure_hot(initv,interval,repeat)
    input("Are you ready COLD measurement?\n Press enter")
    print("Measuring COLD")
    yf.measure_cold(initv,interval,repeat)
    sys.exit(yf.pv_iv_plot())

#20181129
#written by H.Kondo
