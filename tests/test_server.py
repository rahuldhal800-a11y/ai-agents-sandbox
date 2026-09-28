from digital_world.server import Handler


def test_server_module_loads():
    assert Handler is not None
