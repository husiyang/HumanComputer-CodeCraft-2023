#!/bin/bash
import json
import sys
from typing import Union, Tuple, List
from robot import Robot
from workstation import WorkStation
import numpy as np


class Product:
    """
    产品的属性有：
    产品类型
    """

    def __init__(self):
        pass

    def get_type(self):
        pass


# 需求队列
class Request:
    """
    工作台的ID,需要的产品类型
    """

    def __init__(self):
        pass

    def push(self):
        pass

    def pop(self):
        pass


"""
return一个numpy array矩阵，所有机器人到所有工作台的距离
"""


def distance_robots_workstations(robots: List[Robot], workstations: List[WorkStation]) -> dict:
    distances = {}
    for robot in robots:
        distance = robot.get_distance(workstations)
        distances[str(robot.get_robot_ID())] = distance
    return distances


"""
return所有工作台的剩余时间
"""


def time_workstations():
    pass


"""
return一个numpy array矩阵，所有机器人到所有工作台的时间
"""


def time_robots_workstations(robots: List[Robot], workstations: List[WorkStation]) -> dict:
    times = {}
    for robot in robots:
        time = robot.get_time()
        times[str(robot.get_robot_ID())] = time
    return times


def read_util_ok():
    while input() != "OK":
        pass


def finish():
    sys.stdout.write('OK\n')
    sys.stdout.flush()


def read_frame_data() -> Union[Tuple[int, dict], None]:
    """
    读取每一帧的数据
    :return: 每一帧的结构化字典数据
    """
    try:
        # 读取第一行帧序列和金钱数
        _frame, _coin = map(int, sys.stdin.readline().split())
    except ValueError:
        # 文件到达末尾
        return None

    # 读取工作台数量，来判断接下来要读几行数据
    work_num = int(sys.stdin.readline())

    # 初始化帧字典
    _frame_dict = {
        'coin': _coin,
        'work_num': work_num,
        'works': [],
        'robots': []
    }

    # f.write('%d %d' % (frame, coin))
    # f.write(str(work_num))

    # 读取工作台的状态数据
    for _ in range(work_num):
        lineCache = sys.stdin.readline()
        # f.write(lineCache)
        lineCache = lineCache.split()
        _frame_dict['works'].append({
            'type': int(lineCache[0]),
            'x': float(lineCache[1]),
            'y': float(lineCache[2]),
            'remain_time': int(lineCache[3]),
            'input_type': int(lineCache[4]),
            'output_type': int(lineCache[5])
        })

    # 读取机器人的状态数据
    for _ in range(4):
        lineCache = sys.stdin.readline()
        # f.write(lineCache)
        lineCache = lineCache.split()
        _frame_dict['robots'].append({
            'work_id': int(lineCache[0]),
            'item_type': int(lineCache[1]),
            'time_coef': float(lineCache[2]),
            'impact_coef': float(lineCache[3]),
            'vm': float(lineCache[4]),
            'vx': float(lineCache[5]),
            'vy': float(lineCache[6]),
            'toward': float(lineCache[7]),
            'x': float(lineCache[8]),
            'y': float(lineCache[9])
        })

    read_util_ok()

    return _frame, _frame_dict


if __name__ == '__main__':
    # 存放txt
    # f = open('input.txt', 'w')

    # 所有帧数据
    frames = []

    read_util_ok()
    finish()

    while True:
        try:
            frame_id, frame_dict = read_frame_data()
        except TypeError:
            # 文件到达末尾
            break

        frames.append(frame_dict)

        # 官方代码，控制机器人的行动
        sys.stdout.write('%d\n' % frame_id)
        line_speed, angle_speed = 3, 1.5
        for robot_id in range(4):
            sys.stdout.write('forward %d %d\n' % (robot_id, line_speed))
            sys.stdout.write('rotate %d %f\n' % (robot_id, angle_speed))
        finish()

    with open('input.json', 'w') as f:
        json.dump(frames, f)
