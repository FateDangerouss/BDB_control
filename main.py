import robotic_arm
import time
import gpio

state = 0

pm_1 = 3
pm_2 = 4
pm_3 = 5
pm_4 = 6

IO = gpio.myGPIO([17, 'OUT', 18, 'IN', 27, 'IN', 22, 'IN', 23, 'IN', 24, 'IN', 25, 'IN', 4, 'IN', 5, 'IN', 6, 'OUT'])
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

ra_1 = robotic_arm.RoboticArm(0)
ra_2 = robotic_arm.RoboticArm(4)
ra_3 = robotic_arm.RoboticArm(8)


while True:
    if state == 0:
        if IO.input(18) == 1:
            state = 1
            IO.output(17, 'HIGH')
            IO.output(6, 'HIGH')
            time.sleep(pm_1)
            IO.output(6, 'LOW')
            ra_1.run()
            IO.output(17, 'LOW')
            state = 0
        elif IO.input(27) == 1:
            state = 1
            IO.output(17, 'HIGH')
            IO.output(6, 'HIGH')
            time.sleep(pm_2)
            IO.output(6, 'LOW')
            ra_2.run()
            IO.output(17, 'LOW')
            state = 0
        elif IO.input(22) == 1:
            state = 1
            IO.output(17, 'HIGH')
            IO.output(6, 'HIGH')
            time.sleep(pm_3)
            IO.output(6, 'LOW')
            ra_3.run()
            IO.output(17, 'LOW')
            state = 0
        elif IO.input(23) == 1:
            state = 1
            IO.output(17, 'HIGH')
            IO.output(6, 'HIGH')
            time.sleep(pm_4)
            IO.output(6, 'LOW')
            IO.output(17, 'LOW')
            state = 0
        else:
            time.sleep(0.1)