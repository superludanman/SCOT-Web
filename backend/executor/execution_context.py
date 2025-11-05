import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx

class ExecutionContext:
    def __init__(self, use_mock: bool = False):
        load_dotenv()

        self.use_mock = use_mock

        # 从环境变量读取 API Key 和模型配置
        self.api_key = os.getenv("API_KEY", "")

        self.fast_model = os.getenv("FAST_MODEL", "gpt-3.5-turbo")
        self.slow_model = os.getenv("SLOW_MODEL", "gpt-4")
        self.executor_model = os.getenv("Executor_MODEL", "gpt-4")

        # 创建httpx客户端解决版本兼容性问题
        self.http_client = httpx.Client() if self.api_key else None

        # 初始化两个独立的 OpenAI 客户端（可选：未来支持不同 Key）
        self.fast_client = OpenAI(api_key=self.api_key, http_client=self.http_client) if self.api_key else None
        self.slow_client = OpenAI(api_key=self.api_key, http_client=self.http_client) if self.api_key else None
        self.executor_client = OpenAI(api_key=self.api_key, http_client=self.http_client) if self.api_key else None

    def get_client(self, role: str = "fast") -> OpenAI:
        if self.use_mock:
            print(f"✅ 使用 Mock 模式，跳过真实调用。({role})")
            return None  # 或返回 mock client

        if role == "fast":
            return self.fast_client
        elif role == "slow":
            return self.slow_client
        elif role == "executor":
            return self.executor_client
        else:
            raise ValueError(f"未知角色类型: {role}")

    def get_model(self, role: str = "fast") -> str:
        if role == "fast":
            return self.fast_model
        elif role == "slow":
            return self.slow_model
        elif role == "executor":
            return self.executor_model
        else:
            raise ValueError(f"未知角色类型: {role}")

    def test_api(self) -> bool:
        """
        测试 client 是否能正常连接（默认测试 fast 模型）
        """
        if not self.fast_client:
            print("❌ API Key未配置")
            return False
            
        try:
            print(f"🔍 正在测试 OpenAI API：模型 = {self.fast_model}")
            response = self.fast_client.chat.completions.create(
                model=self.fast_model,
                messages=[{"role": "user", "content": "你好，1+1=？"}],
                timeout=5
            )
            print("✅ API 响应成功")
            print("💬 返回内容:", response.choices[0].message.content)
            return True
        except Exception as e:
            print(f"❌ API 调用失败：{e}")
            return False

    def __del__(self):
        # 清理http客户端
        if self.http_client:
            self.http_client.close()