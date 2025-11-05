"""
TaskExecutor：执行任务，调用OpenAI接口，处理异常
核心功能：执行单个任务，整合依赖任务的接口和文件信息
"""
import os
import re
import json
import datetime
from utils.prompts import generate_demo_site_prompt
from executor.execution_context import ExecutionContext

# 检查是否存在已有的 PRD 文件
def check_existing_prd():
    prd_path = os.path.join("data", "prd", "html.txt")
    return prd_path if os.path.exists(prd_path) else None

# 加载知识点数据
def load_knowledge_data(path: str = "data/knowledge/knowledge_graph.json") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError("未检测到知识点文件，请先生成知识点文件")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TaskExecutor:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.client = context.get_client("executor")
        self.model = context.get_model("executor")

    def execute_task(self, dependency_context: str, existing_code_context: str, user_goal: str = "") -> dict:
        """
        执行单个任务，生成结构化代码并保存到对应目录
        :param dependency_context: 参考网站信息
        :param existing_code_context: 知识点信息
        :param user_goal: 用户目标
        :return: 执行结果描述字典
        """
       
        prompt = generate_demo_site_prompt(dependency_context, existing_code_context,user_goal)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.choices[0].message.content.strip()

            # 解析代码块
            files = self._parse_code_blocks(raw)
            # 解析接口描述块
            interfaces = self._parse_interfaces_block(raw)
            # 所有代码集中写入 project 文件夹
            task_dir = os.path.join("data", "results", "project")  
            os.makedirs(task_dir, exist_ok=True)

            for filename, code in files.items():
                filepath = os.path.join(task_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code.strip())

            print(f"示例网页生成完成，生成至 {task_dir}\n")

            result = {
                "files": files,
                "interfaces": interfaces,
                "raw_response": raw
            }

            return result

        except Exception as e:
            print(f"执行任务出错：{str(e)}")
            return {"error": str(e)}

    def _parse_code_blocks(self, content: str) -> dict:
        """解析 LLM 返回的多个代码块"""
        pattern = re.compile(r"```(?:\w+)? filename=(.+?)\n(.*?)```", re.DOTALL)
        matches = pattern.findall(content)
        return {filename.strip(): code.strip() for filename, code in matches}
    
    def _parse_interfaces_block(self, content: str) -> dict:
        """提取模型输出中的接口描述块"""
        match = re.search(r"```json\n(.*?)```", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception as e:
                print("⚠️ 接口描述解析失败：", e)
        return {}