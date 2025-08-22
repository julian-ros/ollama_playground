from uvicorn import run
from .src.global_config import GlobalConfig

config = GlobalConfig()

if __name__ == "__main__":
    run("__init__:app", host="0.0.0.0", port=8000, reload=False)