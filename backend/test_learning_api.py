#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识点生成功能测试脚本
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_knowledge_point_generation():
    """
    测试知识点生成功能
    """
    print("开始测试知识点生成功能...")
    
    # 测试数据
    test_data = {
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
    }
    
    # 发送POST请求到知识点生成接口
    url = f"{BASE_URL}/api/learning/generate-knowledge-point"
    try:
        response = requests.post(url, json=test_data)
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            print("知识点生成成功!")
            print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 验证返回数据结构
            required_fields = ['topic_id', 'title', 'levels']
            for field in required_fields:
                if field not in result:
                    print(f"错误: 返回数据缺少必要字段 '{field}'")
                    return False
                    
            # 验证levels结构
            if 'levels' in result:
                if len(result['levels']) != 4:
                    print(f"错误: levels应该包含4个等级，实际包含{len(result['levels'])}个")
                    return False
                    
                for i, level in enumerate(result['levels']):
                    if 'level' not in level or 'description' not in level:
                        print(f"错误: levels[{i}] 缺少必要字段 'level' 或 'description'")
                        return False
                        
            print("数据结构验证通过!")
            return True
        else:
            print(f"知识点生成失败，状态码: {response.status_code}")
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
        "id": "1_1"
        # 缺少select_element字段
    }
    
    url = f"{BASE_URL}/api/learning/generate-knowledge-point"
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
            
    except Exception as e:
        print(f"发生异常: {str(e)}")
        return False

def main():
    """
    主测试函数
    """
    print("=" * 50)
    print("知识点生成功能测试")
    print("=" * 50)
    
    # 测试正常请求
    success1 = test_knowledge_point_generation()
    
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