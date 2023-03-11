#!/bin/bash
import json
from typing import Tuple

from main import Request

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
    """
    工作台的属性有：
    ID，坐标，工作台类型，物品格，生产物品，生产周期，生产配方
    """

    def __init__(self):
        self.id = None
        self.x = None
        self.y = None
        self.type = None
        self.pre_input = None
        self.input = None
        self.output = None
        self.cycle_time = None

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

    def send_product_request(self, request: Request):
        """
        发送request到需求队列
        """
        products = self.get_product_making()
        for product_type in range(products.bit_length()):
            if (products >> product_type) & 1:
                # 发送requests到需求队列
                request.push((self.id, product_type))

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
        return self.type if self.output else 0

    def get_product_making(self) -> int:
        """
        获取原材料格状态
        :return: 目前需求的产品类型，若此时不需要原材料，则返回 0
        """
        return self.input ^ WORK_INFO[self.type]['input'] if self.type > 3 else 0

    def judge_material_box(self) -> bool:
        """
        判断原材料格前后两帧的状态改变，判断二进制数是否减小
        :return: true false
        """
        return self.pre_input > self.input if self.pre_input is not None else True


if __name__ == '__main__':
    ws = []
    with open('input.json', 'r') as f:
        d = json.load(f)
    for i, work in enumerate(d[0]['works']):
        w = WorkStation()
        w.id = i + 1
        # w.type = work['type']
        w.type = 1
        w.x = work['x']
        w.y = work['y']
        w.cycle_time = work['remain_time']
        w.input = work['input_type']
        w.output = work['output_type']
        ws.append(w)
        print(w.id, w.type, w.get_product_making(), bin(w.get_product_making())[2:].zfill(8), w.get_product_wait())
        # w.send_product_request()
        break
