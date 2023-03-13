#!/bin/bash
import json
from typing import Tuple

# from main import Request

WORK_INFO = {
    1: {'input': None, 'output': 1, 'cycle_time': 50},
    2: {'input': None, 'output': 2, 'cycle_time': 50},
    3: {'input': None, 'output': 3, 'cycle_time': 50},
    4: {'input': 0b00000110, 'output': 4, 'cycle_time': 500},
    5: {'input': 0b00001010, 'output': 5, 'cycle_time': 500},
    6: {'input': 0b00001100, 'output': 6, 'cycle_time': 500},
    7: {'input': 0b01110000, 'output': 7, 'cycle_time': 1000},
    8: {'input': 0b10000000, 'output': None, 'cycle_time': 1},
    9: {'input': 0b11111110, 'output': None, 'cycle_time': 1}
}


class WorkStation:
    def __init__(self, ID: int, x: float, y: float, work_type: int, input_status: int, output_status: int,
                 cycle_time: int):
        """
        工作台类
        :param ID: 工作台 ID
        :param x: 工作台的横坐标
        :param y: 工作台的纵坐标
        :param work_type: 工作台的类型
        :param input_status: 工作台的原材料格状态，使用二进制位表示拥有的物品
        :param output_status: 工作台的产品格状，1 表示有产品、0 表示没有产品
        :param cycle_time: 工作台的剩余生产时间，-1 表示没有生产、0 表示生产因输出格满而阻塞、>=0 表示剩余生产帧数
        """
        self.id = ID
        self.x = x
        self.y = y
        self.type = work_type
        self.pre_input = None
        self._input_status = input_status
        self.output_status = output_status
        self.cycle_time = cycle_time

    @property
    def input_status(self):
        return self._input_status

    @input_status.setter
    def input_status(self, value):
        self.pre_input = self._input_status
        self._input_status = value

    def get_axis(self) -> Tuple[float, float]:
        """
        获取工作台坐标
        :return: (x, y)
        """
        return self.x, self.y

    def get_type(self) -> int:
        """
        获取工作台类型
        :return: 工作台类型
        """
        return self.type

    def get_cycle_time(self) -> int:
        """
        获取剩余生产时间
        :return: 剩余生产时间。-1 表示没有生产；0 表示生产因输出格满而阻塞；>=0 表示剩余生产帧数
        """
        return self.cycle_time

    def get_product_wait(self) -> int:
        """
        获取产品格状态
        :return: 产品类型，若此时没有产品则返回 0
        """
        return self.type if self.output_status else 0

    def get_product_making(self) -> int:
        """
        获取原材料格状态
        :return: 目前需求的产品类型，若此时不需要原材料，则返回 0
        """
        return self.input_status ^ WORK_INFO[self.type]['input'] if self.type > 3 else 0

    def send_product_request(self, request: "Request"):
        """
        发送request到需求队列
        """
        products = self.get_product_making()
        for product_type in range(products.bit_length()):
            if (products >> product_type) & 1:
                # 发送requests到需求队列
                request.push((self.id, product_type))

    def judge_material_box(self) -> bool:
        """
        判断原材料格前后两帧的状态改变，判断二进制数是否减小
        :return: true false
        """
        return self.pre_input > self.input_status if self.pre_input is not None else True


if __name__ == '__main__':
    with open('input.json', 'r') as f:
        d = json.load(f)
    for i, work in enumerate(d[0]['works']):
        w = WorkStation(i + 1, work['x'], work['y'], 7, work['input_type'], work['output_type'], work['remain_time'])
        print(w.id, w.type, w.get_product_making(), bin(w.get_product_making())[2:].zfill(8), w.get_product_wait())
        # w.send_product_request()
        print(w.input_status, w.pre_input)
        w.input_status = 48
        print(w.input_status, w.pre_input)
        w.input_status = 1
        print(w.input_status, w.pre_input)
        w.input_status = 3
        print(w.input_status, w.pre_input)
        break
