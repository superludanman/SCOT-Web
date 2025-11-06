from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import uuid
from datetime import datetime
from agents.slow_mind import SlowMind
from executor.execution_context import ExecutionContext
import urllib.parse

prd_router = APIRouter()

class ReferenceInfo(BaseModel):
    title: str
    structure: List[Dict[str, Any]]
    text_blocks: List[str]

class PRDGenerateRequest(BaseModel):
    reference_url: Optional[str] = None
    reference_info: Optional[ReferenceInfo] = None

class PRDGenerateResponse(BaseModel):
    prd_text: str
    status: str

class PRDSaveRequest(BaseModel):
    title: str
    content: str

class PRDSaveResponse(BaseModel):
    id: str
    title: str
    created_at: str

class PRDListItem(BaseModel):
    id: str
    title: str
    created_at: str

class PRDListResponse(BaseModel):
    prds: List[PRDListItem]

@prd_router.post("/generate", response_model=PRDGenerateResponse)
async def generate_prd(prd_request: PRDGenerateRequest):
    """
    基于参考网站URL或参考信息生成 PRD
    
    参数：
    - reference_url: 参考网站URL
    - reference_info: 参考信息
    """
    try:
        # 初始化AI执行上下文
        context = ExecutionContext()
        slow_mind = SlowMind(context)
        
        # 根据提供的参数生成PRD内容
        if prd_request.reference_url:
            # 基于URL生成PRD
            prd_text = slow_mind.generate_prd(prd_request.reference_url)
        else:
            raise HTTPException(status_code=422, detail="必须提供参考URL或参考信息")
        
        return PRDGenerateResponse(
            prd_text=prd_text,
            status="success"
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PRD生成失败: {str(e)}")

@prd_router.post("/save", response_model=PRDSaveResponse)
async def save_prd(prd_data: PRDSaveRequest):
    """保存PRD文档"""
    # 创建PRD目录
    prd_dir = os.path.join("data", "prd")
    os.makedirs(prd_dir, exist_ok=True)
    
    # 生成唯一ID
    prd_id = str(uuid.uuid4())
    file_path = os.path.join(prd_dir, f"{prd_id}.json")
    
    # 创建PRD数据
    prd_record = {
        "id": prd_id,
        "title": prd_data.title,
        "content": prd_data.content,
        "created_at": datetime.now().isoformat()
    }
    
    # 保存到文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(prd_record, f, ensure_ascii=False, indent=2)
    
    return PRDSaveResponse(
        id=prd_id,
        title=prd_data.title,
        created_at=prd_record["created_at"]
    )

@prd_router.get("/", response_model=PRDListResponse)
async def list_prds():
    """获取PRD列表"""
    prd_dir = os.path.join("data", "prd")
    os.makedirs(prd_dir, exist_ok=True)
    
    prds = []
    if os.path.exists(prd_dir):
        for filename in os.listdir(prd_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(prd_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        prd_data = json.load(f)
                        prds.append(PRDListItem(
                            id=prd_data["id"],
                            title=prd_data["title"],
                            created_at=prd_data["created_at"]
                        ))
                except Exception:
                    continue
    
    return PRDListResponse(prds=prds)

@prd_router.get("/{prd_id}")
async def get_prd(prd_id: str):
    """获取指定PRD详情"""
    file_path = os.path.join("data", "prd", f"{prd_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PRD未找到")
    
    with open(file_path, "r", encoding="utf-8") as f:
        prd_data = json.load(f)
    
    return prd_data

@prd_router.delete("/{prd_id}")
async def delete_prd(prd_id: str):
    """删除指定PRD"""
    file_path = os.path.join("data", "prd", f"{prd_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PRD未找到")
    
    os.remove(file_path)
    
    return {"message": "PRD删除成功"}

@prd_router.get("/download/{prd_id}")
async def download_prd(prd_id: str):
    """下载指定PRD文档"""
    file_path = os.path.join("data", "prd", f"{prd_id}.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PRD未找到")
    
    # 获取PRD标题用于文件名
    with open(file_path, "r", encoding="utf-8") as f:
        prd_data = json.load(f)
    
    # 使用URL编码处理文件名，避免特殊字符导致的编码问题
    filename = f"{prd_data['title']}.json"
    return FileResponse(path=file_path, filename=filename)