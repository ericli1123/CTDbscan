from math import *
import time
import pandas as pd
class DBSCAN_Trans:
    def __init__(self, eps, min_time) -> None:
        self.eps = eps
        self.min_time = min_time

    def data_process(self, dataframe) -> list:
        """
        数据预处理, dataframe 转 list
        """
        output = []
        for i in range(len(dataframe)):
            lng = float(dataframe['longitude'].iloc[i])  # 经度
            lat = float(dataframe['latitude'].iloc[i])  # 纬度
            timeArrive = self.timeTransform(dataframe['positioning_time'].iloc[i]) if dataframe['positioning_time'].iloc[i] != '-1' else -1  # 定位时间

            output.append((lat, lng, timeArrive))  
        output.sort(key=lambda x: x[2])  # 车辆轨迹按定位时间进行排序
        return output

    def cal_spherical_distance(self, LaA, LaB, LoA, LoB) -> float:
        """
        计算两经纬度间距离
        """
        LoA = radians(LoA)
        LoB = radians(LoB)
        LaA= radians(LaA)
        LaB = radians(LaB)

        D_Lo = LoB - LoA
        D_La = LaB - LaA
        P = sin(D_La / 2)**2 + cos(LaA) * cos(LaB) * sin(D_Lo / 2)**2

        Q = 2 * asin(sqrt(P))
        R = 6371.393 * 1000
        distance = R * Q
        return distance

    def timeTransform(self, t) -> int:
        """
        时间转时间戳
        """
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timeArray))
        return timestamp

    def timeTransformBack(self, timestamp) -> str:
        """
        时间戳转时间
        """
        time_local = time.localtime(timestamp)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return t

    def find_neighbours(self, point, point_list) -> list(tuple()):
        """
        找到以 point 为中心, eps 为半径圆内的所有点
        """
        neighbours = []
        for p in point_list:
            distance = self.cal_spherical_distance(p[0], point[0], p[1], point[1])
            if distance < self.eps:
                neighbours.append(p)
            else:
                break
        return neighbours

    def cal_stay_time(self, point_list) -> list:
        """
        计算聚类轨迹点的停留时间
        """
        first_time = point_list[0][2]
        end_time = point_list[0][2]
        for p in point_list[1:]:
            if p[2] < first_time:
                first_time = p[2]
            if p[2] > end_time:
                end_time = p[2]
        stay_time = end_time - first_time
        first_time = self.timeTransformBack(first_time)
        end_time = self.timeTransformBack(end_time)
        return [first_time, end_time, stay_time]

    def cal_mean_postition(self, point_list) -> list:
        """
        计算聚类后轨迹点集的平均经纬度
        """
        total_lat = 0
        total_lng = 0
        for point in point_list:
            total_lng += point[1]
            total_lat += point[0]
        return [total_lng / len(point_list), total_lat / len(point_list)]

    def fit(self, dataframe) -> list:
        """
        对空间点进行 DBSCAN 聚类
        """
        point_list = self.data_process(dataframe)
        res = []
        point_copy = point_list[:]
        for point in point_list:

            if point not in point_copy:
                continue

            point_copy.remove(point)
            neighbours = self.find_neighbours(point, point_copy)

            if self.cal_stay_time([point] + neighbours)[2] > self.min_time:
                clusters_point = [point]

                for neighbour in neighbours:

                    if neighbour in point_copy:

                        clusters_point = list(set(clusters_point + [neighbour]))
                        neighbours_nb = self.find_neighbours(neighbour, point_copy)

                        if (
                            self.cal_stay_time([neighbour] + neighbours_nb)[2]
                            > self.min_time
                        ):

                            neighbours = list(set(neighbours + neighbours_nb))
                for cl_point in clusters_point:
                    if cl_point in point_copy:
                        point_copy.remove(cl_point)
                res.append(clusters_point)

        output = []
        for stop in res:
            mean_stop = self.cal_mean_postition(stop)
            stay_time = self.cal_stay_time(stop)
            output.append(mean_stop + stay_time)
        return output