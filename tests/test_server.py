from pathlib import Path

from digital_world.server import Handler


ROOT = Path(__file__).resolve().parents[1]


def test_server_module_loads():
    assert Handler is not None


def test_webgl_free_renderer_is_served():
    index = (ROOT / "web" / "index.html").read_text()
    renderer = (ROOT / "web" / "world2d.js").read_text()
    server = (ROOT / "digital_world" / "server.py").read_text()

    assert '/world2d.js' in index
    assert 'THREE' not in renderer
    assert '/world2d.js' in server
