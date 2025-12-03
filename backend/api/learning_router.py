from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from agents.slow_mind import SlowMind
from executor.execution_context import ExecutionContext

learning_router = APIRouter()

class KnowledgePointGenerateRequest(BaseModel):
    id: str
    label: str
    type: str
    select_element: List[str]

class KnowledgePointGenerateResponse(BaseModel):
    topic_id: str
    title: str
    levels: List[Dict[str, Any]]

@learning_router.post("/generate-knowledge-point", response_model=KnowledgePointGenerateResponse)
async def generate_knowledge_point(request: KnowledgePointGenerateRequest):
    """
    根据知识点ID和选择的元素生成学习内容
    
    参数：
    - id: 知识点ID
    - label: 知识点标签
    - type: 知识点类型
    - select_element: 选择的元素列表
    """
    try:
        # 初始化AI执行上下文
        context = ExecutionContext()
        slow_mind = SlowMind(context)
        
        # 构造知识点信息
        topic_info = {
            "topic_id": request.id,
            "label": request.label,
            "type": request.type,
            "select_element": request.select_element
        }
            
        # 生成知识点内容
        knowledge_content = slow_mind.generate_learning_content(topic_info)
        
        return KnowledgePointGenerateResponse(**knowledge_content)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识点生成失败: {str(e)}")
