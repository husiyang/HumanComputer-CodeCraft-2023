import math
from typing import Tuple, List
from workstation import WorkStation
from main import Request
import numpy as np


class Robot:
    """
    机器人的属性有：
    ID，坐标，半径（常态），半径（持有物品），面积，密度，质量，操作（前进、后退、旋转），
    携带的产品类型，角速度（最大旋转速度），线速度（最大前进速度，最大后退速度），朝向，
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
        self.ID = None
        self.workstation_ID = None
        self.axis_x = None
        self.axis_y = None
        self.velocity = None
        self.ang_velocity = None
        self.orientation = None
        self.target_ID = None
        self.product_type = None
        self.time_value = None
        self.crash_value = None
        self.work_ID = None
        self.distances = []
        self.times = []
        self.distances_robot = []
        self.radius = None

    def get_robot_ID(self) -> int:
        return self.ID

    """
    计算一个机器人到所有工作台之间的距离,返回距离list
    """

    def get_distance(self, workstations: List[WorkStation]) -> List[float]:
        for workstation in workstations:
            workstation_x, workstation_y = workstation.get_axis()
            dis_x = self.axis_x - workstation_x
            dis_y = self.axis_y - workstation_y
            distance = math.sqrt(dis_x * dis_x + dis_y * dis_y)
            self.distances.append(distance)
        return self.distances

    """
    机器人的面积
    """

    def area(self) -> float:
        return self.radius * self.radius * math.pi

    """
    算质量
    """

    def get_mass(self) -> float:
        return self.area() * 20

    """
    计算一个机器人到所有工作台的时间
    """

    def get_time(self) -> List[float]:
        for distance in self.distances:
            self.times.append(distance / self.velocity)
        return self.times

    """
    获取机器人当前的朝向
    """

    def get_orientation(self) -> float:
        return self.orientation

    """
    获取机器人当前的坐标
    """

    def get_axis(self) -> Tuple[float, float]:
        return self.axis_x, self.axis_y

    """
    计算机器人当前速度
    """

    def calculate_velocity(self, velo_x, velo_y):
        self.velocity = math.sqrt(velo_x * velo_x + velo_y * velo_y)

    """
    获取机器人当前的速度
    """

    def get_velocity(self, velo_x, velo_y) -> float:
        return self.velocity

    """
    获取机器人携带的产品的类型
    """

    def get_current_product_type(self) -> int:
        return self.product_type

    """
    附近工作台的ID
    """

    def get_current_workstation(self) -> int:
        return self.workstation_ID

    """
    计算一个机器人到其他机器人的距离
    """

    def distance_robot(self, robots: List['Robot']) -> List[float]:
        for robot in robots:
            robot_x, robot_y = robot.get_axis()
            dis_x = self.axis_x - robot_x
            dis_y = self.axis_y - robot_y
            distance = math.sqrt(dis_x * dis_x + dis_y * dis_y)
            self.distances_robot.append(distance)
        return self.distances_robot

    """
    碰撞检测函数
    """
    def crash_detect(self) -> bool:
        if min(self.distances_robot) <= 6:
            return True

    """
    减速以避免碰撞函数
    """

    def crash_avoid(self) -> Tuple[float, float]:
        if self.velocity != 0:
            return 0, -2
        else:
            return 0, 0

    """
    机器人重新加速
    """
    def restart(self) -> float:
        return 6

    """
    购买产品，设置机器人的buy指令，传给判题器
    """

    def buy_product(self) -> int:
        if self.workstation_ID == self.work_ID:
            if self.product_type == 0:
                return 1

    """
    卖出产品，设置target为null，设置机器人的sell指令，传给判题器
    """

    def sell_product(self) -> int:
        if self.workstation_ID == self.target_ID:
            if self.product_type != 0:
                self.target_ID = None
                return 1

    """
    销毁物品，设置机器人no destroy，传给判题器
    """

    def destroy_product(self) -> int:
        if self.product_type != 0:
            return 1

    """
    接受需求队列任务，改变target为workStationID，确定所有可达的工作站中距离最短的那个，返回工作站ID。
    """

    def send_task_request(self, workstations: List[WorkStation], request: Request) -> int:
        request_cache = request.pop()
        target_ID, product_type = request_cache.split()
        target_ID = int(target_ID)
        product_type = int(product_type)
        self.target_ID = target_ID
        IDs = []
        for workstation in workstations:
            if workstation.get_type() == product_type:
                IDs.append(workstation.id)
        self.work_ID = self.distances[IDs[0]]
        for ID in IDs:
            if ID <= self.work_ID:
                self.work_ID = ID
        return self.work_ID

    """
    前往工作站取材料，设置相应的角速度和线速度
    """

    def toward_work(self, work: WorkStation) -> Tuple[float, float]:
        work_x, work_y = work.get_axis()
        v1 = np.array([1, 0])
        v2 = np.array([work_y - self.axis_y, work_x - self.axis_x])
        work_angle = dot_product_angle(v1, v2)
        gap = self.orientation - work_angle
        line_speed = self.velocity
        angle_speed = gap
        if gap < 0 and math.fabs(gap) < math.pi:
            angle_speed = math.fabs(gap)
        elif gap < 0 and math.fabs(gap) > math.pi:
            angle_speed = 2 * math.pi - math.fabs(gap)
        elif 0 < gap < math.pi:
            angle_speed = 0 - gap
        elif gap > math.pi:
            angle_speed = 2 * math.pi - gap
        elif gap == 0:
            line_speed = 6
            angle_speed = 0
        return angle_speed, line_speed


def dot_product_angle(v1, v2):
    length_v1 = np.sqrt(v1.dot(v1))
    length_v2 = np.sqrt(v2.dot(v2))
    arccos = np.arccos((v1.dot(v2)) / (length_v1 * length_v2))
    if v2[1] < v1[1]:
        arccos = 0 - arccos
    return arccos
