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
    当前所处工作台

    ***时间价值系数，碰撞价值系数***

    """

    def __init__(self):
        """
        ID，int
        携带物品类型，int
        角速度，float
        线速度，x,y两个float
        朝向，float
        坐标，x,y两个float
        distances,[]
        target：workstationID int
        """
        pass

    """
    计算一个和一个工作台之间的距离
    返回距离
    """

    def get_distance(self):
        pass

    """
    机器人的面积
    """

    def get_area(self):
        pass

    """
    算质量
    """

    def get_mass(self):
        pass

    """
    计算一个机器人到一个工作台的时间
    """

    def get_time(self):
        pass

    """
    获取机器人当前的朝向
    """

    def get_orientation(self):
        pass

    """
    获取机器人当前的坐标
    """

    def get_axis(self):
        pass

    """
    获取机器人当前的速度
    """

    def get_velocity(self):
        pass

    """
    获取机器人携带的产品的类型
    """

    def get_current_product_type(self):
        pass

    """
    计算机器人与工作台的距离是否小于0.4m，如果有多个工作台，选最近的一个，
    如果一样近，那么以ID排在前面的工作台为准
    返回工作台的ID
    """

    def get_current_workstation(self):
        pass

    """
    设置机器人前进速度
    """

    def forward(self):
        pass

    """
    设置机器人的回退速度
    """

    def back_forward(self):
        pass

    """
    设置机器人的旋转速度
    """

    def rotate(self):
        pass

    """
    碰撞相关函数
    """

    def crash(self):
        pass

    """
    购买产品，设置机器人的buy指令，传给判题器
    """

    def buy_product(self):
        pass

    """
    卖出产品，设置target为null，设置机器人的sell指令，传给判题器
    """

    def sell_product(self):
        pass

    """
    销毁物品，设置机器人no destroy，传给判题器
    """

    def destroy_product(self):
        pass

    """
    接受需求队列任务，改变相应的朝向和速度，改变target为workStationID。
    """

    def send_task_request(self):
        pass

    """
    改变机器人的target，return 当前ID
    """

    def change_target(self):
        pass


class WorkStation:
    """
    工作台的属性有：
    ID，坐标，工作台类型，物品格，生产物品，生产周期，生产配方
    """

    def __init__(self):
        pass

    def get_axis(self):
        pass

    def get_type(self):
        pass

    """
    发送request到需求队列
    """

    def send_product_request(self):
        pass

    def get_cycle_time(self):
        pass

    """
    获取产品格状态，返回产品类型
    """

    def get_product_wait(self):
        pass

    """
    获取原材料格状态，获取产品类型
    """

    def get_product_making(self):
        pass

    """
    判断原材料格前后两帧的状态改变，判断二进制数是否减小，return true false
    """

    def judge_material_box(self):
        pass


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
    帧ID，工作台的请求
    """

    def __init__(self):
        pass

    def get_workstation_request(self):
        pass

    def get_robot_request(self):
        pass

    def push(self):
        pass

    def pop(self):
        pass


"""
return一个numpy array矩阵，所有机器人到所有工作台的距离
"""
def distance_robots_workstations():
    pass


"""
return所有工作台的剩余时间
"""
def time_workstations():
    pass

"""
return一个numpy array矩阵，所有机器人到所有工作台的时间
"""
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
