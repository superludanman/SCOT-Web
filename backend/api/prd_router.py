from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import uuid
from datetime import datetime

prd_router = APIRouter()

class PRDGenerateRequest(BaseModel):
    reference_html: dict
    user_input: Optional[str] = ""

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

def generate_prd_content(reference_html: dict, user_input: str) -> str:
    """
    根据参考网页结构和用户输入生成PRD内容
    实际项目中这里会调用AI模型生成内容
    """
    title = reference_html.get("title", "未命名项目")
    
    prd_content = f"""
# {title} 产品需求文档

## 1. 概述
基于用户需求和参考网页结构生成的产品需求文档。

用户需求描述:
{user_input if user_input else "未提供具体需求"}

## 2. 页面结构分析
参考网页包含以下主要结构:
{json.dumps(reference_html.get('structure', []), ensure_ascii=False, indent=2)}

## 3. 文本内容概要
参考网页主要文本内容:
{chr(10).join(reference_html.get('text_blocks', []))}

## 4. 功能需求
- 页面展示功能
- 用户交互功能
- 响应式设计
- 浏览器兼容性

## 5. 非功能需求
- 页面加载性能
- SEO友好
- 代码可维护性
- 安全性

## 6. 技术选型建议
- HTML5 + CSS3 + JavaScript
- 响应式布局
- 现代浏览器兼容
"""
    
    return prd_content

@prd_router.post("/generate", response_model=PRDGenerateResponse)
async def generate_prd(prd_request: PRDGenerateRequest):
    """
    基于上传网页结构生成 PRD
    
    参数：
    - reference_html: 提取的网页结构
    - user_input: 用户需求描述
    """
    # 生成PRD内容（实际项目中这里会调用AI模型）
    prd_text = generate_prd_content(prd_request.reference_html, prd_request.user_input)
    
    return PRDGenerateResponse(
        prd_text=prd_text,
        status="success"
    )

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