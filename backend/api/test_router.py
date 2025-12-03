from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from agents.slow_mind import SlowMind
from executor.execution_context import ExecutionContext

test_router = APIRouter()

class TestTaskGenerateRequest(BaseModel):
    topic_id: str
    knowledge_node: Dict[str, Any]  # 知识点节点数据
    learning_content: Optional[Dict[str, Any]] = None  # 学习内容（如果已生成）

class TestTaskGenerateResponse(BaseModel):
    topic_id: str
    title: str
    description_md: str
    start_code: Dict[str, str]
    checkpoints: List[Dict[str, Any]]
    answer: Dict[str, str]

@test_router.post("/generate-test-task", response_model=TestTaskGenerateResponse)
async def generate_test_task(request: TestTaskGenerateRequest):
    """
    根据知识点生成测试题
    
    参数：
    - topic_id: 知识点ID
    - knowledge_node: 知识点节点数据
    - learning_content: 学习内容（可选）
    """
    try:
        # 初始化AI执行上下文
        context = ExecutionContext()
        slow_mind = SlowMind(context)
        
        # 生成测试题
        test_task = slow_mind.generate_test_task(request.knowledge_node, request.learning_content)
        
        return TestTaskGenerateResponse(**test_task)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"测试题生成失败: {str(e)}")