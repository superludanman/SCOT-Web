"""
SlowMind：将用户的模糊需求生成详细方案（PRD）
拓展：生成多套方案供用户选择
"""

import os
import re
from typing import List
from utils.prompts import get_website_analysis_prompt
from utils.prompts import get_slow_mind_prompt_from_html
from executor.execution_context import ExecutionContext

class SlowMind:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.client = context.get_client("slow")
        self.model = context.get_model("slow")

    def generate_prd_from_html(self, html_content: str, user_goal: str = "") -> str:
        """
        生成PRD文档
        :param user_goal: 用户输入wyesse的详细需求  
        :param html_content: 用户上传的HTML内容
        :return: PRD文档内容
        """
        prompt = get_slow_mind_prompt_from_html(html_content,user_goal)

        print("正在分析上传的网页内容，生成结构化 PRD 文档...\n")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        plan = response.choices[0].message.content.strip()

        #  保存 PRD 到文件
        save_path = os.path.join("data", "prd", "html.txt")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"PRD文档 已保存到：{save_path}")

        return plan
    def generate_prd(self, user_input: str) -> str:
        """
        生成PRD文档
        :param user_input: 用户输入的参考网站URL
        :return: PRD文档内容
        """
        prompt = get_website_analysis_prompt(user_input)

        print("分析网站，生成网站技术文档\n")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        plan = response.choices[0].message.content.strip()

        #  保存 PRD 到文件
        save_path = os.path.join("data", "prd", "html.txt")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"PRD文档 已保存到：{save_path}")

        return plan