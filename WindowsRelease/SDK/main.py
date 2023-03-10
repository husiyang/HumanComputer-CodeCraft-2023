#!/bin/bash
import sys


def read_util_ok():
    while input() != "OK":
        pass


def finish():
    sys.stdout.write('OK\n')
    sys.stdout.flush()


if __name__ == '__main__':
    # 存放txt
    f = open('input.txt', 'w')

    read_util_ok()
    finish()
    while True:
        # 读取第一行帧序列和金钱数
        line = sys.stdin.readline()

        # 读取工作台数量，来判断接下来要读几行数据
        work_num = int(sys.stdin.readline())
        temp = sys.stdout
        sys.stdout = f
        num = 1
        print(line)
        print(work_num)
        while num <= work_num:
            lineCache = sys.stdin.readline()
            print(lineCache)
            num += 1

        # 读取机器人的状态数据
        robot_line = 1
        while robot_line <= 4:
            lineCache = sys.stdin.readline()
            print(lineCache)
            robot_line += 1
        sys.stdout = temp

        # 官方代码，主要是获取帧数ID
        if not line:
            break
        parts = line.split(' ')
        frame_id = int(parts[0])
        read_util_ok()

        # 官方代码，控制机器人的行动
        sys.stdout.write('%d\n' % frame_id)
        line_speed, angle_speed = 3, 1.5
        for robot_id in range(4):
            sys.stdout.write('forward %d %d\n' % (robot_id, line_speed))
            sys.stdout.write('rotate %d %f\n' % (robot_id, angle_speed))
        finish()
