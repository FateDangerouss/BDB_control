import robotic_arm
import time
import gpio
import threading
import upload
import conveyor_belt

state = 0

pm_1 = 1.5
pm_2 = 4
pm_3 = 7
pm_4 = 9

send_1 = 0
send_2 = 0
send_3 = 0
send_4 = 0

IO = gpio.myGPIO([17, 'OUT', 18, 'IN', 27, 'IN', 22, 'IN', 23, 'IN', 24, 'IN', 25, 'IN', 4, 'IN', 5, 'IN', 6, 'IN', 13, 'OUT', 12, 'OUT'])
# 17: 工作状态信息输出
# 18: 箱1输入信息
# 27: 箱2输入信息
# 22: 箱3输入信息
# 23: 箱4输入信息
# 24: 箱1集满信息
# 25: 箱2集满信息
# 4:  箱3集满信息
# 5:  箱4集满信息
IO.output(17, 'LOW')
IO.output(12, 'LOW')

cb = conveyor_belt.Conveyor_belt()
cb.run(2)

up_1 = upload.Upload(1)
up_2 = upload.Upload(2)
up_3 = upload.Upload(3)
up_4 = upload.Upload(4)

ra_1 = robotic_arm.RoboticArm(0)
ra_2 = robotic_arm.RoboticArm(4)
ra_3 = robotic_arm.RoboticArm(8)
ra_1.run()
ra_2.run()
ra_3.run()

while True:
    while True:
        if state == 0:
            if IO.input(18) == 1:
                state = 1
                IO.output(17, 'HIGH')
                cb.run(pm_1)
                ra_1.run()
                IO.output(17, 'LOW')
                state = 0
            elif IO.input(27) == 1:
                state = 1
                IO.output(17, 'HIGH')
                cb.run(pm_2)
                ra_2.run()
                IO.output(17, 'LOW')
                state = 0
            elif IO.input(22) == 1:
                state = 1
                IO.output(17, 'HIGH')
                cb.run(pm_3)
                ra_3.run()
                IO.output(17, 'LOW')
                state = 0
            elif IO.input(23) == 1:
                state = 1
                IO.output(17, 'HIGH')
                cb.run(pm_4)
                IO.output(17, 'LOW')
                state = 0
            else:
                time.sleep(0.1)
                
        if send_1 == 0:
            if IO.input(24) == 1:
                try:
                    up_1.uploaddata()
                    send_1 = 1
                except IndexError:
                    pass
        else:
            if IO.input(24) == 0:
                send_1 = 0
        if send_2 == 0:
            if IO.input(25) == 1:
                try:
                    up_2.uploaddata()
                    send_2 = 1
                except IndexError:
                    pass
        else:
            if IO.input(25) == 0:
                send_2 = 0
        if send_3 == 0:
            if IO.input(4) == 1:
                try:
                    up_3.uploaddata()
                    send_3 = 1
                except IndexError:
                    pass
        else:
            if IO.input(4) == 0:
                send_3 = 0
        if send_4 == 0:
            if IO.input(5) == 1:
                try:
                    up_4.uploaddata()
                    send_4 = 1
                except IndexError:
                    pass
        else:
            if IO.input(5) == 0:
                send_4 = 0
        if IO.input(6) == 1:
            IO.output(13, 'HIGH')
        else:
            IO.output(13, 'LOW')
        time.sleep(0.1)
    

# th_run = threading.Thread(target = run)
# th_fullsend = threading.Thread(target = fullsend)
# 
# th_run.start()
# th_fullsend.start()
# th_run.join()
# th_fullsend.join()