from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import shutil
from pathlib import Path
import json
import uuid
from datetime import datetime
from agents.slow_mind import SlowMind
from agents.fast_mind import FastMind
from executor.execution_context import ExecutionContext

upload_router = APIRouter()

class UploadResponse(BaseModel):
    title: str
    structure: List[Dict[str, Any]]
    text_blocks: List[str]
    message: str

class PRDGenerateResponse(BaseModel):
    prd_text: str
    status: str

class KnowledgeExtractResponse(BaseModel):
    graph: dict
    status: str

class HTMLStructure(BaseModel):
    tag: str
    id: Optional[str]
    classes: List[str]
    text: Optional[str]
    children: List['HTMLStructure'] = []

# 为递归模型更新forward references
HTMLStructure.update_forward_refs()

def extract_html_structure(content: str) -> dict:
    """
    简单提取HTML结构信息
    实际项目中可以使用BeautifulSoup或其他HTML解析库进行更详细的分析
    """
    # 这里是一个简化的实现，实际项目中应该更复杂
    structure = []
    text_blocks = []
    
    # 简单提取标题
    import re
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "未命名页面"
    
    # 简单提取文本块
    text_matches = re.findall(r'<(h[1-6]|p|div)[^>]*>(.*?)</\1>', content, re.IGNORECASE | re.DOTALL)
    for tag, text in text_matches:
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        if clean_text:
            text_blocks.append(clean_text)
    
    # 构造简单的结构信息
    structure.append({
        "tag": "html",
        "children": [
            {"tag": "head", "children": [{"tag": "title", "text": title}]},
            {"tag": "body", "children": []}
        ]
    })
    
    return {
        "title": title,
        "structure": structure,
        "text_blocks": text_blocks[:10]  # 限制文本块数量
    }

@upload_router.post("/html", response_model=UploadResponse)
async def upload_html(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None)
):
    """
    上传 HTML 文件或输入 URL，提取网页结构
    
    参数：
    - file: HTML 文件
    - url: 可选网页链接
    """
    # 创建上传目录
    upload_dir = os.path.join("data", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    if file and file.filename:
        # 保存上传的文件
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in [".html", ".htm"]:
            raise HTTPException(status_code=400, detail="只支持HTML文件")
        
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # 提取结构信息
        structure_info = extract_html_structure(content)
        
        return UploadResponse(
            title=structure_info["title"],
            structure=structure_info["structure"],
            text_blocks=structure_info["text_blocks"],
            message="HTML文件上传并解析成功"
        )
    
    elif url:
        # 处理URL情况（简化实现）
        return UploadResponse(
            title="从URL获取的页面",
            structure=[{"tag": "html", "children": []}],
            text_blocks=[f"从以下URL获取内容: {url}"],
            message="URL接收成功"
        )
    
    else:
        raise HTTPException(status_code=422, detail="请提供HTML文件或URL")

@upload_router.post("/generate-prd", response_model=PRDGenerateResponse)
async def generate_prd_from_file(file: UploadFile = File(...)):
    """
    通过上传的HTML文件生成PRD文档
    
    参数：
    - file: HTML 文件
    """
    try:
        # 读取上传的文件内容
        content = await file.read()
        html_content = content.decode('utf-8')
        
        # 初始化AI执行上下文
        context = ExecutionContext()
        slow_mind = SlowMind(context)
        
        # 使用正确的函数生成PRD内容，传递HTML内容而不是文件路径
        prd_text = slow_mind.generate_prd_from_html(html_content)
        
        return PRDGenerateResponse(
            prd_text=prd_text,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PRD生成失败: {str(e)}")

@upload_router.post("/extract-knowledge", response_model=KnowledgeExtractResponse)
async def extract_knowledge_from_file(file: UploadFile = File(...)):
    """
    通过上传的HTML文件提取知识点
    
    参数：
    - file: HTML 文件
    """
    try:
        # 读取上传的文件内容
        content = await file.read()
        html_content = content.decode('utf-8')
        
        # 初始化AI执行上下文
        context = ExecutionContext()
        fast_mind = FastMind(context)
        
        # 使用正确的函数提取知识点，传递HTML内容而不是文件路径
        knowledge_data = fast_mind.extract_knowledge_points_from_html(html_content)
        
        return KnowledgeExtractResponse(
            graph=knowledge_data,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识点提取失败: {str(e)}")

@upload_router.get("/list")
async def list_uploaded_files():
    """列出所有上传的文件"""
    upload_dir = os.path.join("data", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    files = []
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
    
    return {"files": files}