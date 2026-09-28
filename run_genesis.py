"""Launch Genesis and its live monitor."""

from digital_world.bootstrap import create_genesis
from digital_world.monitor import serve


if __name__ == "__main__":
    genesis = create_genesis()
    print("Genesis started.")
    print("Monitor: http://127.0.0.1:8765")
    serve(genesis)
