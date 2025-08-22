from uvicorn import run
from src.global_config import GlobalConfig

config = GlobalConfig()

run("__init__:app")
