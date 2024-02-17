#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import rclpy
import math
from rclpy.node import Node
from rclpy.clock import Clock, ClockType
from rclpy.executors import ExternalShutdownException
from rclpy.time import Time

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import tf2_geometry_msgs
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

class RobotController(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # 速度制御用
        # https://docs.ros2.org/latest/api/geometry_msgs/msg/Twist.html
        self.pub_cmd_vel = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.05  # 20Hzで速度指令を送信する。
        self.timer = self.create_timer(timer_period, self.on_timer)
        self.clock = Clock(clock_type=ClockType.ROS_TIME)
        self.tm_start = self.clock.now()
        self.tm_old = self.tm_start
        # ★ トピック名 '/scan'、型 LaserScan のサブスクライバを生成する。
        # self.sub_scan = self.create_subscription(LaserScan, 'scan', self.scan_cb, 10) # ☆ 修正方法はセミナ中で説明します。
        # ★ 座標変換用
        # self.tf_buffer = Buffer() # ☆ 修正方法はセミナ中で説明します。
        # self.tf_listener = TransformListener(self.tf_buffer, self) # ☆ 修正方法はセミナ中で説明します。

    def update(self):
        tm = self.clock.now()
        delta = (tm - self.tm_old).nanoseconds / 1000000000
        elapsed = (tm - self.tm_start).nanoseconds / 1000000000
        self.tm_old = tm
        return delta, elapsed

    def test_run(self, delta, elapsed):
        if elapsed <= 2.0: # 前進。2秒間継続する。
            msg = Twist()  # ★ Twist型の変数を定義する。ロボットへの速度指令が入る。
            msg.linear.x = 0.25 # ★ 0.25m／秒で前進する指令を作成する。
            self.pub_cmd_vel.publish(msg) # ★ 速度指令をパブリッシュする。
        elif elapsed <= 5.0: # 左旋回。3秒間継続する。
            msg = Twist() # ★ Twist型の変数を定義する。ロボットへの速度指令が入る。
            msg.angular.z = math.radians(30) # ★ 30度／秒で左旋回する指令を作成する。
            self.pub_cmd_vel.publish(msg) # ★ 速度指令をパブリッシュする。
        elif elapsed <= 6.0:
            # しばらく停止速度を送信する。
            msg = Twist()
            self.pub_cmd_vel.publish(msg)
        else:
            twist = Twist()
            self.pub_cmd_vel.publish(twist)
            raise SystemExit

    def scan_cb(self, msg):
        # LiDARデータの受信時に呼ばれる関数。
        self.get_logger().info('%s:%d' % (type(msg), len(msg.ranges)))  # 動作を理解したらコメントアウトする

    def on_timer(self):
        # 前フレームからの経過時間と、プログラム開始時点からの経過時間を得る
        delta, elapsed = self.update()
        self.get_logger().info('%f, %f' % (delta, elapsed)) # 動作を理解したらコメントアウトする
        self.test_run(delta, elapsed)

def main(args=None):
    script_name = os.path.basename(__file__)
    node_name = os.path.splitext(script_name)[0]
    rclpy.init(args=args)
    node = RobotController(node_name)
    try:
        rclpy.spin(node)    
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except SystemExit:
        print(node_name, 'SystemExit')
        rclpy.shutdown()
    finally:
        print(node_name, 'destroy_node')
        node.destroy_node()

if __name__ == '__main__':
    main()
