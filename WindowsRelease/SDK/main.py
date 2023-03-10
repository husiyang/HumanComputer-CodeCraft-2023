#!/bin/bash
import json
import sys
from typing import Union, Tuple


class Robot:

    """
    机器人的属性有：
    ID，坐标，半径（常态），半径（持有物品），面积，密度，质量，操作（前进、后退、旋转），
    携带的产品类型，角速度（最大旋转速度），线速度（最大前进速度，最大后退速度），朝向，
    最大牵引力（机器人的加速/减速/防侧滑均由牵引力驱动），
    最大力矩（机器人的旋转由力矩驱动），
    当前所处工作台，资金
    """
    def __init__(self):
        pass

    def get_distance(self):
        pass

    def get_area(self):
        pass

    def get_mass(self):
        pass

    def get_time(self):
        pass

    def get_orientation(self):
        pass

    def get_axis(self):
        pass

    def get_velocity(self):
        pass

    def get_money(self):
        pass

    def get_current_product_type(self):
        pass

    def get_current_workstation(self):
        pass

    def forward(self):
        pass

    def back_forward(self):
        pass

    def rotate(self):
        pass

    def crash(self):
        pass

    def buy_product(self):
        pass

    def sell_product(self):
        pass

    def destroy_product(self):
        pass


class WorkStation:

    """
    工作台的属性有：
    ID，坐标，工作台类型，物品格，存储物品，生产物品，生产周期，生产配方
    """
    def __init__(self):
        pass

    def get_axis(self):
        pass

    def get_type(self):
        pass

    def get_recipe(self):
        pass

    def get_cycle_time(self):
        pass

    def get_product_wait(self):
        pass

    def get_product_making(self):
        pass

    def store(self):
        pass


class Product:

    """
    产品的属性有：
    ID，产品类型，购买价，原始售出价，真实售价，时间价值系数，碰撞价值系数，
    持有帧数，持有时累计碰撞冲量
    """
    def __init__(self):
        pass

    def get_type(self):
        pass

    def get_purchase_price(self):
        pass

    def get_sale_price(self):
        pass

    def get_real_sale_price(self):
        pass

    def get_time_value(self):
        pass

    def get_crash_value(self):
        pass

    def get_FPS_all(self):
        pass

    def get_crash_all(self):
        pass


def get_current_FPS():
    pass


def get_current_money():
    pass


def distance_robots_workstations():
    pass


def time_workstations():
    pass


def time_robots_workstations():
    pass


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
