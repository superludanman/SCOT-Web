from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import uuid
from datetime import datetime
from agents.fast_mind import FastMind
from executor.execution_context import ExecutionContext

knowledge_router = APIRouter()

class ReferenceInfo(BaseModel):
    title: str
    structure: List[Dict[str, Any]]
    text_blocks: List[str]

class KnowledgeExtractRequest(BaseModel):
    reference_url: Optional[str] = None
    reference_info: Optional[ReferenceInfo] = None

class KnowledgeExtractResponse(BaseModel):
    graph: dict
    status: str

class KnowledgeSaveRequest(BaseModel):
    name: str
    graph: dict

class KnowledgeSaveResponse(BaseModel):
    id: str
    name: str
    created_at: str

class KnowledgeListItem(BaseModel):
    id: str
    name: str
    created_at: str

class KnowledgeListResponse(BaseModel):
    knowledge_graphs: List[KnowledgeListItem]

@knowledge_router.post("/extract", response_model=KnowledgeExtractResponse)
async def extract_knowledge(extract_request: KnowledgeExtractRequest):
    """
    从参考网站URL或参考信息中提取知识点
    
    参数：
    - reference_url: 参考网站URL
    - reference_info: 参考信息
    """
    try:
        # 初始化AI执行上下文
        context = ExecutionContext()
        fast_mind = FastMind(context)
        
        # 根据提供的参数提取知识点
        if extract_request.reference_info:
            # 基于参考信息提取知识点
            # 创建一个模拟的对象来传递参考信息
            class MockReference:
                def __init__(self, info):
                    self.title = info.title
                    self.structure = info.structure
                    self.text_blocks = info.text_blocks
            
            mock_ref = MockReference(extract_request.reference_info)
            knowledge_data = fast_mind.extract_knowledge_points_from_info(mock_ref)
        elif extract_request.reference_url:
            # 基于URL提取知识点
            knowledge_data = fast_mind.extract_knowledge_points(extract_request.reference_url)
        else:
            raise HTTPException(status_code=422, detail="必须提供参考URL或参考信息")
        
        return KnowledgeExtractResponse(
            graph=knowledge_data,
            status="success"
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识点提取失败: {str(e)}")

@knowledge_router.post("/save", response_model=KnowledgeSaveResponse)
async def save_knowledge_graph(knowledge_data: KnowledgeSaveRequest):
    """保存知识点图谱"""
    # 创建知识点目录
    knowledge_dir = os.path.join("data", "knowledge")
    os.makedirs(knowledge_dir, exist_ok=True)
    
    # 生成唯一ID
    knowledge_id = str(uuid.uuid4())
    file_path = os.path.join(knowledge_dir, f"{knowledge_id}.json")
    
    # 创建知识点数据
    knowledge_record = {
        "id": knowledge_id,
        "name": knowledge_data.name,
        "graph": knowledge_data.graph,
        "created_at": datetime.now().isoformat()
    }
    
    # 保存到文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(knowledge_record, f, ensure_ascii=False, indent=2)
    
    return KnowledgeSaveResponse(
        id=knowledge_id,
        name=knowledge_data.name,
        created_at=knowledge_record["created_at"]
    )

@knowledge_router.get("/", response_model=KnowledgeListResponse)
async def list_knowledge_graphs():
    """获取知识点图谱列表"""
    knowledge_dir = os.path.join("data", "knowledge")
    os.makedirs(knowledge_dir, exist_ok=True)
    
    knowledge_graphs = []
    if os.path.exists(knowledge_dir):
        for filename in os.listdir(knowledge_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(knowledge_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        knowledge_data = json.load(f)
                        knowledge_graphs.append(KnowledgeListItem(
                            id=knowledge_data["id"],
                            name=knowledge_data["name"],
                            created_at=knowledge_data["created_at"]
                        ))
                except Exception:
                    continue
    
    return KnowledgeListResponse(knowledge_graphs=knowledge_graphs)

@knowledge_router.get("/{knowledge_id}")
async def get_knowledge_graph(knowledge_id: str):
    """获取指定知识点图谱详情"""
    file_path = os.path.join("data", "knowledge", f"{knowledge_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="知识点图谱未找到")
    
    with open(file_path, "r", encoding="utf-8") as f:
        knowledge_data = json.load(f)
    
    return knowledge_data

@knowledge_router.delete("/{knowledge_id}")
async def delete_knowledge_graph(knowledge_id: str):
    """删除指定知识点图谱"""
    file_path = os.path.join("data", "knowledge", f"{knowledge_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="知识点图谱未找到")
    
    os.remove(file_path)
    
    return {"message": "知识点图谱删除成功"}