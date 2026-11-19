import pytest

from gameplay import perception_memory as mod

CASES = [
    pytest.param('facing_from_animation', (350.0, 10.0, 0.5), 0.0, True, id='01_animation_facing_sync'),
    pytest.param('occlusion_recheck', (0.0, 0.1, 0.05), True, False, id='02_dynamic_occlusion_recheck'),
    pytest.param('hearing_in_range', ((5.0, 0.0), (0.0, 0.0), 0.0, 340.0, 10.0, 0.02), True, False, id='03_delayed_hearing'),
    pytest.param('decay_memory', (1.0, 2.0, 1.0), 0.25, True, id='04_time_based_decay'),
    pytest.param('blackboard_key', ('guard7', 'seen'), 'guard7:seen', False, id='05_guard_private_blackboard'),
    pytest.param('validate_async', ((0.0, 0.0), (3.0, 0.0), 5.0), True, False, id='06_async_target_validation'),
    pytest.param('visibility_channels', (True, 'audio'), True, False, id='07_invisibility_audio_only'),
    pytest.param('occlusion_mask', (1, 2), 3, False, id='08_door_glass_layer_mask'),
    pytest.param('alert_update', (0.5, 0.5, True), 0.5, True, id='09_alert_cooldown'),
    pytest.param('cone_samples', (12,), 64, False, id='10_fixed_cone_samples'),
    pytest.param('visible_in_cone', ((0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 0.0, 90.0), True, False, id='11_target_in_cone'),
    pytest.param('hearing_at_time', (10.0, 340.0), 0.029411764705882353, True, id='12_hearing_delay'),
    pytest.param('forget_memory', (0.1, 0.2), True, False, id='13_memory_forgotten'),
    pytest.param('share_event', ('A', 'seen'), {'A': 'seen'}, False, id='14_private_event_share'),
    pytest.param('layer_opaque', (False, True), 3, False, id='15_unified_occlusion_layers'),
]


def assert_close(actual, expected):
    if isinstance(expected, tuple):
        assert isinstance(actual, tuple) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_close(actual[key], expected[key])
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_perception_memory_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert_close(result, expected)
    else:
        assert result == expected
