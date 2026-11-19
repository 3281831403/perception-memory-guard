"""守卫感知：朝向同步、按秒记忆与隔离黑板。"""

from __future__ import annotations

import math

# 视野锥固定采样数，与帧率无关
CONE_SAMPLE_COUNT = 64


def facing_from_animation(current_yaw, anim_yaw, blend):
    """按动画播放进度混合出的当前朝向（最短弧插值，处理 360 度回绕）。"""
    delta = (anim_yaw - current_yaw + 180.0) % 360.0 - 180.0
    return (current_yaw + delta * blend) % 360.0


def occlusion_recheck(last_check, now, interval):
    """是否到达下一次遮挡重查时间（动态遮挡需按间隔重查）。"""
    return now - last_check >= interval


def hearing_in_range(event_pos, guard_pos, event_time, speed, radius, now):
    """按声音到达时间判定听觉范围：声音须已到达且距离在半径内。"""
    dx = event_pos[0] - guard_pos[0]
    dy = event_pos[1] - guard_pos[1]
    distance = math.hypot(dx, dy)
    if distance > radius:
        return False
    arrival = event_time + distance / speed
    return arrival <= now


def decay_memory(confidence, dt, half_life):
    """按秒半衰的记忆衰减（与帧率无关）。"""
    return confidence * 0.5 ** (dt / half_life)


def blackboard_key(guard_id, fact):
    """守卫私有黑板键。"""
    return f"{guard_id}:{fact}"


def validate_async(result_pos, target_pos, max_distance):
    """异步结果返回时校验目标是否仍在有效距离内。"""
    dx = result_pos[0] - target_pos[0]
    dy = result_pos[1] - target_pos[1]
    return math.hypot(dx, dy) <= max_distance


def visibility_channels(invisible, channel):
    """隐身只影响视觉通道，不影响听觉等其他通道。"""
    if channel == "visual":
        return not invisible
    return True


def occlusion_mask(door_layer, glass_layer):
    """合并门与玻璃的遮挡层（统一按位或）。"""
    return door_layer | glass_layer


def alert_update(level, event_strength, cooldown):
    """警戒冷却期间等级不被新事件直接置满。"""
    if cooldown:
        return level
    return min(1.0, level + event_strength)


def cone_samples(requested):
    """固定视野锥采样数，忽略随帧率变化的请求值。"""
    return CONE_SAMPLE_COUNT


def visible_in_cone(target_pos, guard_pos, facing_deg, fov_deg):
    """目标是否在视野锥内（facing 0 度朝 +z，半角判定）。"""
    dx = target_pos[0] - guard_pos[0]
    dz = target_pos[2] - guard_pos[2]
    if dx == 0.0 and dz == 0.0:
        return True
    target_yaw = math.degrees(math.atan2(dx, dz))
    delta = (target_yaw - facing_deg + 180.0) % 360.0 - 180.0
    return abs(delta) <= fov_deg / 2.0


def hearing_at_time(distance, speed):
    """声音到达所需时间。"""
    return distance / speed


def forget_memory(confidence, threshold):
    """记忆是否低于遗忘阈值。"""
    return confidence < threshold


def share_event(guard_id, event):
    """把事件写入指定守卫的私有黑板。"""
    return {guard_id: event}


def layer_opaque(door_open, glass_present):
    """门与玻璃的视觉遮挡掩码：关着的门与玻璃均遮挡。"""
    mask = 0
    if not door_open:
        mask |= 1
    if glass_present:
        mask |= 2
    return mask
