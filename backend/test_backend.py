#!/usr/bin/env python3
"""
后端功能测试脚本
用于测试PRD生成、知识图谱提取和网页生成功能
"""

import os
import sys
import json
from dotenv import load_dotenv

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.slow_mind import SlowMind
from agents.fast_mind import FastMind
from executor.task_executor import TaskExecutor
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

def test_prd_generation():
    """测试PRD生成功能"""
    print("=== 测试PRD生成功能 ===")
    
    # 初始化上下文
    context = ExecutionContext()
    slow_mind = SlowMind(context)
    
    # 测试URL
    test_url = "https://www.wcf-bestcat.de/"
    
    try:
        prd_content = slow_mind.generate_prd(test_url)
        print(f"PRD生成成功，长度: {len(prd_content)} 字符")
        print(f"PRD内容预览: {prd_content[:200]}...")
        return prd_content
    except Exception as e:
        print(f"PRD生成失败: {e}")
        return None

def test_knowledge_extraction():
    """测试知识图谱提取功能"""
    print("\n=== 测试知识图谱提取功能 ===")
    
    # 初始化上下文
    context = ExecutionContext()
    fast_mind = FastMind(context)
    
    # 测试URL
    test_url = "https://www.wcf-bestcat.de/"
    
    try:
        knowledge_data = fast_mind.extract_knowledge_points(test_url)
        print(f"知识点提取成功")
        print(f"知识点数量: {len(knowledge_data.get('nodes', []))}")
        if knowledge_data.get('nodes'):
            print(f"第一个知识点: {knowledge_data['nodes'][0]['data']['label']}")
        return knowledge_data
    except Exception as e:
        print(f"知识点提取失败: {e}")
        return None

def test_web_generation():
    """测试网页生成功能"""
    print("\n=== 测试网页生成功能 ===")
    
    # 初始化上下文
    context = ExecutionContext()
    executor = TaskExecutor(context)
    
    # 准备测试数据
    prd_path = check_existing_prd()
    with open(prd_path, "r", encoding="utf-8") as f:
        reference_info = f.read()

    knowledge_points = load_knowledge_data()
    
    try:
        result = executor.execute_task(reference_info, knowledge_points)
        if "error" in result:
            print(f"网页生成失败: {result['error']}")
            return None
            
        print(f"网页生成成功")
        print(f"生成的文件数量: {len(result.get('files', {}))}")
        if result.get('files'):
            filenames = list(result['files'].keys())
            print(f"生成的文件: {filenames}")
        return result
    except Exception as e:
        print(f"网页生成失败: {e}")
        return None

def main():
    """主测试函数"""
    print("开始测试后端功能...")
    
    # 测试PRD生成
    prd_result = test_prd_generation()
    
    # 测试知识图谱提取
    knowledge_result = test_knowledge_extraction()
    
    # 测试网页生成
    web_result = test_web_generation()
    
    # 汇总结果
    print("\n=== 测试结果汇总 ===")
    print(f"PRD生成功能: {'通过' if prd_result else '失败'}")
    print(f"知识图谱提取功能: {'通过' if knowledge_result else '失败'}")
    print(f"网页生成功能: {'通过' if web_result else '失败'}")
    
    if prd_result and knowledge_result and web_result:
        print("\n所有功能测试通过！")
        return True
    else:
        print("\n部分功能测试失败！")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)