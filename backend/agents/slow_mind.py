"""
SlowMind：将用户的模糊需求生成详细方案（PRD）
拓展：生成多套方案供用户选择
"""

import json
import os
from openai import OpenAI
from typing import Dict, Any, Optional
from utils.prompts import (
    get_slow_mind_prompt_from_html,
    get_website_analysis_prompt,
    get_knowledge_points_prompt_from_html,
    get_knowledge_points_prompt,
    generate_demo_site_prompt,
    generate_learning_content_prompt,
    generate_test_task_prompt
)
from executor.execution_context import ExecutionContext


class SlowMind:
    """
    慢思考智能体：负责复杂任务的深度分析与生成
    """
    
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.client = context.get_client("slow")
        self.model = context.get_model("slow")
    
    def generate_prd_from_html(self, html_content: str, user_goal: str = "") -> str:
        """
        生成PRD文档
        :param user_goal: 用户输入的详细需求  
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
        
    def generate_learning_content(self, topic_info: dict) -> dict:
        """
        根据知识点信息生成学习内容
        
        :param topic_info: 包含知识点信息的字典
        :return: 生成的学习内容
        """
        # 生成提示词
        prompt = generate_learning_content_prompt(topic_info)
        
        print(f"正在生成知识点 {topic_info.get('topic_id')} 的学习内容...\n")
        
        if self.context.use_mock:
            print("使用 Mock 模式，返回模拟学习内容")
            return self._get_mock_learning_content(topic_info)
        
        try:
            # 获取执行上下文中的 client 和 model
            client = self.context.get_client("slow")
            model = self.context.get_model("slow")

            # 调用AI模型生成内容
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的前端开发导师，能够根据测试题目生成相关的学习内容。"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            raw_content = response.choices[0].message.content.strip()
            # 清理可能的代码标记
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
                
            # 解析JSON
            learning_content = json.loads(raw_content)
            return learning_content
            
        except Exception as e:
            print(f"生成学习内容时出错: {str(e)}")
            print("返回模拟学习内容")
            return self._get_mock_learning_content(topic_info)
    
    def _get_mock_learning_content(self, topic_info: dict) -> dict:
        """
        获取模拟的学习内容（调试用）
        
        :param topic_info: 知识点信息
        :return: 模拟的学习内容
        """
        topic_id = topic_info.get("topic_id", "unknown")
        label = topic_info.get("label", "未知知识点")
        select_elements = topic_info.get("select_element", [])
        
        return {
            "topic_id": topic_id,
            "title": label,
            "levels": [
                {
                    "level": 1,
                    "description": "这是入门级别的讲解内容。在这里我们会介绍最基本的概念和语法，帮助初学者建立起对该知识点的基本认识。内容应该足够详细，让完全没有基础的人也能理解。在HTML中，这些元素是非常基础且重要的组成部分，它们构成了网页内容的骨架。比如<h1>标签代表一级标题，是页面中最重要的标题元素。"
                },
                {
                    "level": 2,
                    "description": "这是进阶级别的讲解内容。在掌握了基础知识之后，我们可以进一步探讨这些知识点在实际开发中的常见应用场景和组合用法，帮助学习者提升实践能力。在实际项目中，这些元素往往不是单独使用的，而是需要和其他元素配合，形成完整的页面结构。"
                },
                {
                    "level": 3,
                    "description": "这是高级级别的讲解内容。在这个阶段，我们需要深入了解知识点背后的机制原理，以及在性能优化方面的考量，帮助学习者形成更加系统化的认知。理解这些元素的语义化特性对于SEO和无障碍访问都有重要意义。"
                },
                {
                    "level": 4,
                    "description": "这是实战级别的讲解内容。通过综合性的实战案例和拓展练习，学习者可以检验和突破现有的水平，将理论知识转化为实际的编程能力。例如：\n\n```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>示例页面</title>\n</head>\n<body>\n    <h1>主标题</h1>\n    <h2>副标题</h2>\n    <p>这是一个段落内容。</p>\n</body>\n</html>\n```\n\n通过这样的示例，可以更好地理解这些元素在实际项目中的应用。"
                }
            ]
        }
    
    def generate_test_task(self, topic_info: dict, learning_content: dict = None) -> dict:
        """
        根据知识点信息和学习内容生成测试题
        
        :param topic_info: 知识点信息
        :param learning_content: 学习内容（可选）
        :return: 生成的测试题
        """
        # 生成提示词
        prompt = generate_test_task_prompt(topic_info, learning_content)
        
        print(f"正在生成知识点 {topic_info.get('id')} 的测试题...\n")
        
        if self.context.use_mock:
            print("使用 Mock 模式，返回模拟测试题")
            return self._get_mock_test_task(topic_info)
        
        try:
            # 获取执行上下文中的 client 和 model
            client = self.context.get_client("slow")
            model = self.context.get_model("slow")

            # 调用AI模型生成测试题
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一名资历丰富的编程出题专家，专门为初学者设计HTML测试题。请严格按照要求的JSON格式输出，不要添加任何其他内容。"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            raw_content = response.choices[0].message.content.strip()
            # 清理可能的代码标记
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
                
            # 解析JSON
            test_task = json.loads(raw_content)
            return test_task
            
        except Exception as e:
            print(f"生成测试题时出错: {str(e)}")
            print("返回模拟测试题")
            return self._get_mock_test_task(topic_info)
    
    def _get_mock_test_task(self, topic_info: dict) -> dict:
        """获取模拟的测试题（调试用）"""
        topic_id = topic_info.get("id", "unknown")
        label = topic_info.get("label", "未知知识点")
        
        return {
            "topic_id": topic_id,
            "title": f"{label}测试题",
            "description_md": "# 任务描述：\n## 任务一：\n请使用相关HTML元素完成任务",
            "start_code": {
                "html": "",
                "css": "",
                "js": ""
            },
            "checkpoints": [
                {
                    "name": "元素存在检查",
                    "type": "assert_element",
                    "selector": "div",
                    "assertion_type": "exists",
                    "feedback": "请在代码中添加一个div元素。"
                }
            ],
            "answer": {
                "html": "<div>示例内容</div>",
                "css": "",
                "js": ""
            }
        }
