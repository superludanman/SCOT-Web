#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试题生成功能测试脚本
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_test_task_generation():
    """
    测试测试题生成功能
    """
    print("开始测试测试题生成功能...")
    
    # 测试数据
    test_data = {
        "topic_id": "1_1",
        "knowledge_node": {
            "id": "1_1",
            "label": "使用 h 元素和 p 元素体验标题与段落",
            "type": "knowledge",
            "select_element": [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "p"
            ]
        },
        "learning_content": {
            "topic_id": "1_1",
            "title": "使用 h 元素和 p 元素体验标题与段落",
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
    }
    
    # 发送POST请求到测试题生成接口
    url = f"{BASE_URL}/api/test/generate-test-task"
    try:
        response = requests.post(url, json=test_data)
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            print("测试题生成成功!")
            print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 验证返回数据结构
            required_fields = ['topic_id', 'title', 'description_md', 'start_code', 'checkpoints', 'answer']
            for field in required_fields:
                if field not in result:
                    print(f"错误: 返回数据缺少必要字段 '{field}'")
                    return False
                    
            # 验证start_code结构
            if 'start_code' in result:
                start_code_fields = ['html', 'css', 'js']
                for field in start_code_fields:
                    if field not in result['start_code']:
                        print(f"错误: start_code缺少必要字段 '{field}'")
                        return False
                        
            # 验证answer结构
            if 'answer' in result:
                answer_fields = ['html', 'css', 'js']
                for field in answer_fields:
                    if field not in result['answer']:
                        print(f"错误: answer缺少必要字段 '{field}'")
                        return False
                        
            print("数据结构验证通过!")
            return True
        else:
            print(f"测试题生成失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务，请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return False

def test_invalid_request():
    """
    测试无效请求
    """
    print("\n开始测试无效请求...")
    
    # 发送无效数据（缺少必要字段）
    invalid_data = {
        "topic_id": "1_1"
        # 缺少knowledge_node和learning_content字段
    }
    
    url = f"{BASE_URL}/api/test/generate-test-task"
    try:
        response = requests.post(url, json=invalid_data)
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(invalid_data, ensure_ascii=False, indent=2)}")
        
        if response.status_code == 422:
            print("正确处理了无效请求，返回422状态码")
            return True
        else:
            print(f"意外的状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到后端服务，请确保后端服务正在运行")
        return False
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return False

def main():
    """
    主测试函数
    """
    print("=" * 50)
    print("测试题生成功能测试")
    print("=" * 50)
    
    # 测试正常请求
    success1 = test_test_task_generation()
    
    # 测试无效请求
    success2 = test_invalid_request()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
    print("=" * 50)

if __name__ == "__main__":
    main()