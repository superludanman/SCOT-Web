#!/usr/bin/env python3
"""
API接口测试脚本
用于测试后端REST API接口
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("健康检查通过")
            print(f"响应内容: {response.json()}")
            return True
        else:
            print(f"健康检查失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"健康检查异常: {e}")
        return False

def test_prd_api():
    """测试PRD相关接口"""
    print("\n=== 测试PRD相关接口 ===")
    
    # 生成PRD
    try:
        generate_data = {
            "reference_url": "https://example.com"
        }
        response = requests.post(f"{BASE_URL}/api/prd/generate", json=generate_data)
        if response.status_code == 200:
            prd_result = response.json()
            print("PRD生成成功")
            print(f"PRD内容长度: {len(prd_result.get('prd_text', ''))} 字符")
            return prd_result
        else:
            print(f"PRD生成失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"PRD生成异常: {e}")
        return None

def test_knowledge_api():
    """测试知识图谱相关接口"""
    print("\n=== 测试知识图谱相关接口 ===")
    
    # 提取知识点
    try:
        extract_data = {
            "reference_url": "https://example.com"
        }
        response = requests.post(f"{BASE_URL}/api/knowledge/extract", json=extract_data)
        if response.status_code == 200:
            knowledge_result = response.json()
            print("知识点提取成功")
            print(f"知识点数量: {len(knowledge_result.get('graph', {}).get('nodes', []))}")
            return knowledge_result
        else:
            print(f"知识点提取失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"知识点提取异常: {e}")
        return None

def test_execute_api():
    """测试执行器相关接口"""
    print("\n=== 测试执行器相关接口 ===")
    
    # 执行任务
    try:
        execute_data = {
            "reference_info": "示例网站信息",
            "knowledge_points": {
                "nodes": [
                    {"data": {"id": "chapter1", "label": "模块一:文本与页面结构基础", "category": "media-block", "placementHint": "main-content"}},
                    {"data": {"id": "text_paragraph", "label": "使用h元素和p元素体验标题与段落", "category": "media-block", "placementHint": "main-content"}},
                    {"data": {"id": "style_basic", "label": "设置颜色与字体", "category": "media-block", "placementHint": "main-content"}}
                ]
            },
            "user_note": "测试生成网页"
        }
        response = requests.post(f"{BASE_URL}/api/execute", json=execute_data)
        if response.status_code == 200:
            execute_result = response.json()
            print("任务执行成功")
            print(f"任务ID: {execute_result.get('task_id')}")
            print(f"生成文件: {execute_result.get('files')}")
            return execute_result
        else:
            print(f"任务执行失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"任务执行异常: {e}")
        return None

def test_preview_api(task_id):
    """测试预览接口"""
    print("\n=== 测试预览接口 ===")
    
    if not task_id:
        print("没有任务ID，跳过预览测试")
        return False
        
    try:
        response = requests.get(f"{BASE_URL}/api/preview/{task_id}")
        if response.status_code == 200:
            print("预览接口测试成功")
            print(f"返回内容长度: {len(response.text)} 字符")
            return True
        else:
            print(f"预览接口测试失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"预览接口测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试后端API接口...")
    
    # 测试健康检查
    health_ok = test_health_check()
    
    if not health_ok:
        print("健康检查失败，退出测试")
        return False
    
    # 测试PRD API
    prd_result = test_prd_api()
    
    # 测试知识图谱 API
    knowledge_result = test_knowledge_api()
    
    # 测试执行器 API
    execute_result = test_execute_api()
    
    # 测试预览 API
    task_id = execute_result.get('task_id') if execute_result else None
    preview_ok = test_preview_api(task_id)
    
    # 汇总结果
    print("\n=== API测试结果汇总 ===")
    print(f"健康检查接口: {'通过' if health_ok else '失败'}")
    print(f"PRD生成接口: {'通过' if prd_result else '失败'}")
    print(f"知识点提取接口: {'通过' if knowledge_result else '失败'}")
    print(f"任务执行接口: {'通过' if execute_result else '失败'}")
    print(f"预览接口: {'通过' if preview_ok else '失败'}")
    
    if health_ok and prd_result and knowledge_result and execute_result and preview_ok:
        print("\n所有API接口测试通过！")
        return True
    else:
        print("\n部分API接口测试失败！")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)