"""
SlowMind：将用户的模糊需求生成详细方案（PRD）
拓展：生成多套方案供用户选择
"""

import os
import re
from typing import List
from utils.prompts import get_website_analysis_prompt
from executor.execution_context import ExecutionContext

class SlowMind:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.client = context.get_client("slow")
        self.model = context.get_model("slow")

    def generate_prd(self, user_input: str) -> str:
        """
        生成PRD文档
        :param user_input: 用户输入的参考网站URL
        :return: PRD文档内容
        """
        prompt = get_website_analysis_prompt(user_input)

        print("🧠 分析网站，生成网站技术文档\n")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        plan = response.choices[0].message.content.strip()

        return plan