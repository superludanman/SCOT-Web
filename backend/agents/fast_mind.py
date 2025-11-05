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
        :param prd_text: 可选，SlowMind 生成的 PRD 文档内容（用于增强语义理解）
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

    def _get_mock_knowledge_points(self) -> dict:
        """模拟数据（调试用）"""
        return {
            "nodes": [
                {"data": {"id": "chapter1", "label": "模块一:文本与页面结构基础", "category": "media-block", "placementHint": "main-content"}},
                {"data": {"id": "text_paragraph", "label": "使用h元素和p元素体验标题与段落", "category": "media-block", "placementHint": "main-content"}},
                {"data": {"id": "style_basic", "label": "设置颜色与字体", "category": "media-block", "placementHint": "main-content"}}
            ]
        }