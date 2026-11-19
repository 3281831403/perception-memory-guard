# 守卫感知：朝向同步、按秒记忆与隔离黑板

守卫视野用动画未播完的朝向、门开后遮挡不重查、听觉按当前半径丢延迟声、记忆按帧衰减、多个守卫共享黑板。本仓库把视觉与听觉通道拆开验证。

- 领域：游戏、图形与多媒体
- 子方向：其他
- 语言/框架：Python 3, pytest
- 初始状态：15 个参数化用例全部失败

## 目录结构

```
README.md
conftest.py
.gitignore
gameplay/__init__.py
gameplay/perception_memory.py
tests/test_perception_memory.py
```

## 需要修复的 10 个问题

1. 视野锥朝向来自动画当前朝向，转身未播完不提前换向
2. 遮挡射线按时间间隔重查，移动门打开后立即更新
3. 听觉事件按到达时间与事件时刻判定，不丢延迟声音
4. 记忆按秒指数衰减，低帧率下不会忘得更快
5. 每个守卫使用独立感知黑板，一个看到不共享给全体
6. 异步导航结果返回时校验目标是否仍有效
7. 隐身状态只影响视觉通道，不影响听觉
8. 门和玻璃使用统一的遮挡层配置
9. 警戒等级下降时有冷却，新事件不能直接置满
10. 视野锥按固定采样点数量生成，帧率不影响细缝可见性

## 15 条验收契约

    01. animation facing sync — `facing_from_animation`
    02. dynamic occlusion recheck — `occlusion_recheck`
    03. delayed hearing — `hearing_in_range`
    04. time based decay — `decay_memory`
    05. guard private blackboard — `blackboard_key`
    06. async target validation — `validate_async`
    07. invisibility audio only — `visibility_channels`
    08. door glass layer mask — `occlusion_mask`
    09. alert cooldown — `alert_update`
    10. fixed cone samples — `cone_samples`
    11. target in cone — `visible_in_cone`
    12. hearing delay — `hearing_at_time`
    13. memory forgotten — `forget_memory`
    14. private event share — `share_event`
    15. unified occlusion layers — `layer_opaque`

## 当前状态

`gameplay/perception_memory.py` 只保留函数签名与文档字符串，所有函数体统一
`raise NotImplementedError`。`tests/test_perception_memory.py` 使用一个
`@pytest.mark.parametrize` 装载 15 条契约，初始全部失败且没有 collection error。

```bash
python -m pytest -q
```

预期输出包含 `15 failed`。实现 `gameplay/perception_memory.py` 后，15 条契约应全部通过。
