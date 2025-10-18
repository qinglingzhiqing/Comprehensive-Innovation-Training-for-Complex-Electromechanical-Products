'''
Author: ZHAO qinglingzhiqing@126.com
Date: 2025-10-18 11:41:03
LastEditors: ZHAO qinglingzhiqing@126.com
LastEditTime: 2025-10-18 11:53:02
FilePath: \Comprehensive-Innovation-Training-for-Complex-Electromechanical-Products\dronebridge\test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pymavlink import mavutil
# 连接到DroneBridge。这里的IP和端口需根据DroneBridge的实际设置调整。
# 常见格式如下，默认UDP端口通常是14550:cite[1]。
connection = mavutil.mavlink_connection('udp:192.168.2.1:14550') # 示例IP和端口
# 等待接收飞控的心跳包，确认连接
print("等待飞控心跳...")
connection.wait_heartbeat()
print("飞控连接成功！")

# 解锁无人机。前提是无人机已处于GUIDED模式:cite[5]。
# 设置飞行模式为GUIDED
connection.mav.set_mode_send(
    connection.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    'GUIDED'  # 对于ArduPilot，GUIDED模式通常对应编号为4的定制模式
)

# 解锁电机
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0  # 参数1为1表示解锁
)

# 发送起飞指令，让无人机上升至目标高度（例如5米）
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0, 0, 0, 5  # 最后一个参数是目标高度（米）
)


def send_velocity_command(vx, vy, vz):
    """
    发送速度控制命令。
    参数vx: 前后速度 (m/s)，前进为正
    参数vy: 左右速度 (m/s)，右行为正
    参数vz: 上下速度 (m/s)，下降为正
    """
    connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
        10, connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_NED, # 使用机体坐标系
        int(0b0000111111000111),  # 控制掩码，表示忽略除速度外的其他信息
        0, 0, 0,  # x, y, z 位置 (忽略)
        vx, vy, vz,  # vx, vy, vz 速度
        0, 0, 0,  # 加速度 (忽略)
        0, 0  # yaw, yaw_rate (忽略)
    ))

# 控制示例：
# send_velocity_command(1, 0, 0)   # 前进 1 m/s
# send_velocity_command(-1, 0, 0)  # 后退 1 m/s
# send_velocity_command(0, 1, 0)   # 右移 1 m/s
# send_velocity_command(0, -1, 0)  # 左移 1 m/s


# 发送降落指令
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_LAND,
    0,
    0, 0, 0, 0, 0, 0, 0
)

# 等待一段时间确保无人机已着陆，然后锁定电机
import time
time.sleep(20)  # 等待20秒，可根据实际情况调整

# 锁定电机
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    0, 0, 0, 0, 0, 0, 0  # 参数1为0表示锁定
)