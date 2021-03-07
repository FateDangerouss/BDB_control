import robotic_arm
import time
import gpio
import threading
import multiprocessing as mp

detect = gpio.myGPIO([17, 'OUT', 18, 'IN', 27, 'IN', 22, 'IN', 23, 'IN', 24, 'IN', 25, 'IN', 4, 'IN', 5, 'IN', 6, 'OUT'])
#17: 工作状态信息输出
#18: 箱1输入信息
#27: 箱2输入信息
#22: 箱3输入信息
#23: 箱4输入信息
#24: 箱1集满信息
#25: 箱2集满信息
#4:  箱3集满信息
#5:  箱4集满信息
#6:  继电器控制输出


ra1 = robotic_arm.RoboticArm(0)
ra2 = robotic_arm.RoboticArm(4)
ra3 = robotic_arm.RoboticArm(8)

time.sleep(2)
def ra1run():
    ra1.run()
def ra2run():
    ra2.run()
def ra3run():
    ra3.run()
if __name__ == '__main__':
    list = []
    list.append(mp.Process(target=ra1run()))
    list.append(mp.Process(target=ra2run()))
    list.append(mp.Process(target=ra3run()))
    for t in list:
        t.start()