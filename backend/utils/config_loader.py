import os
from dotenv import load_dotenv

def load_config():
    """
    加载环境配置
    """
    load_dotenv()
    
    config = {
        "API_KEY": os.getenv("API_KEY", ""),
        "FAST_MODEL": os.getenv("FAST_MODEL", "gpt-3.5-turbo"),
        "SLOW_MODEL": os.getenv("SLOW_MODEL", "gpt-4"),
        "EXECUTOR_MODEL": os.getenv("Executor_MODEL", "gpt-4"),
    }
    
    return config