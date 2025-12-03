# fast_mind.py
import os
import re
import json
from utils.prompts import get_knowledge_points_prompt
from utils.prompts import get_knowledge_points_prompt_from_html
from executor.execution_context import ExecutionContext

class FastMind:
    def __init__(self, context: ExecutionContext):
        self.context = context
        self.client = context.get_client("fast")
        self.model = context.get_model("fast")

    def extract_knowledge_points_from_html(self, html_content: str, prd_text: str = "") -> dict:
        """
        根据用户上传的 HTML 内容生成知识点文件或任务树 JSON

        :param html_content: 用户上传的 HTML 内容字符串
        :param prd_text: 可选，SlowMind 生成的 PRD 文件内容（用于增强语义理解）
        :return: 生成的知识点数据（Python dict 格式）
        """
        prompt = get_knowledge_points_prompt_from_html(html_content, prd_text)

        if self.context.use_mock:
            print("使用 Mock 模式，返回模拟知识点")
            knowledge_tree = self._get_mock_knowledge_points()
        else:
            print("正在分析 HTML 内容并生成知识图谱 / 任务树...\n")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = response.choices[0].message.content.strip()
                raw_cleaned = re.sub(r"[\x00-\x1f\x7f]", "", raw)  # 移除非法字符
                knowledge_tree = json.loads(raw_cleaned)

                print("\n生成知识点：\n")
                for node in knowledge_tree.get("nodes", []):
                    print(f"{node['data']['id']} - {node['data']['label']}")

            except Exception as e:
                print("模型原始返回：", raw[:500])
                print("解析知识点失败:", e)
                knowledge_tree = self._get_mock_knowledge_points()

        # 保存 JSON 到文件
        save_path = os.path.join("data", "knowledge", "knowledge_graph.json")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_tree, f, ensure_ascii=False, indent=2)
        print(f"知识点已保存到：{save_path}")

        return knowledge_tree
    
    def extract_knowledge_points(self, reference_url: str) -> dict:
        """
        分析参考网站，提炼前端知识点（nodes 数组 JSON 格式）
        :param reference_url: 示例网站链接
        :return: 知识点树（JSON）
        """
        prompt = get_knowledge_points_prompt(reference_url)

        if self.context.use_mock:
            print("使用 Mock 模式，返回模拟知识点")
            knowledge_tree = self._get_mock_knowledge_points()
        else:
            print("正在分析网站知识点...\n")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = response.choices[0].message.content.strip()
                raw_cleaned = re.sub(r"[\x00-\x1f\x7f]", "", raw)  # 移除非法字符
                knowledge_tree = json.loads(raw_cleaned)

                print("\n生成知识点：\n")
                for node in knowledge_tree.get("nodes", []):
                    print(f"{node['data']['id']} - {node['data']['label']}")

            except Exception as e:
                print("模型原始返回：", raw[:500])
                print("解析知识点失败:", e)
                knowledge_tree = self._get_mock_knowledge_points()

        # 保存 JSON 到文件
        save_path = os.path.join("data", "knowledge", "knowledge_graph.json")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_tree, f, ensure_ascii=False, indent=2)
        print(f"知识点已保存到：{save_path}")

        return knowledge_tree

    def generate_learning_content(self, topic_info: dict) -> dict:
        """
        根据知识点信息生成学习内容
        
        :param topic_info: 包含知识点信息的字典
        :return: 生成的学习内容
        """
        # 这里应该实现实际的AI调用逻辑
        # 目前返回模拟数据
        
        topic_id = topic_info.get("topic_id", "unknown")
        select_elements = topic_info.get("select_element", [])
        
        # 模拟生成的学习内容
        learning_content = {
            "topic_id": topic_id,
            "title": f"关于{', '.join(select_elements) if select_elements else 'HTML'}的知识点",
            "levels": [
                {
                    "level": 1,
                    "description": "这是入门级别的讲解内容。在这里我们会介绍最基本的概念和语法，帮助初学者建立起对该知识点的基本认识。内容应该足够详细，让完全没有基础的人也能理解。"
                },
                {
                    "level": 2,
                    "description": "这是进阶级别的讲解内容。在掌握了基础知识之后，我们可以进一步探讨这些知识点在实际开发中的常见应用场景和组合用法，帮助学习者提升实践能力。"
                },
                {
                    "level": 3,
                    "description": "这是高级级别的讲解内容。在这个阶段，我们需要深入了解知识点背后的机制原理，以及在性能优化方面的考量，帮助学习者形成更加系统化的认知。"
                },
                {
                    "level": 4,
                    "description": "这是实战级别的讲解内容。通过综合性的实战案例和拓展练习，学习者可以检验和突破现有的水平，将理论知识转化为实际的编程能力。"
                }
            ]
        }
        
        return learning_content

    def _get_mock_knowledge_points(self) -> dict:
        """模拟数据（调试用）"""
        return {
            "nodes": [
                {"data": {"id": "chapter1", "label": "模块一:文本与页面结构基础", "category": "media-block", "placementHint": "main-content"}},
                {"data": {"id": "text_paragraph", "label": "使用h元素和p元素体验标题与段落", "category": "media-block", "placementHint": "main-content"}},
                {"data": {"id": "style_basic", "label": "设置颜色与字体", "category": "media-block", "placementHint": "main-content"}}
            ]
        }