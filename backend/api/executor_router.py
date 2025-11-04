from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import uuid
from datetime import datetime

executor_router = APIRouter()

class ExecuteRequest(BaseModel):
    task_id: str
    user_note: Optional[str] = ""

class ExecuteResponse(BaseModel):
    status: str
    files: List[str]
    preview_url: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    created_at: str
    finished_at: Optional[str] = None

@executor_router.post("/", response_model=ExecuteResponse)
async def execute_task(exec_request: ExecuteRequest):
    """
    根据任务执行自动生成网页
    
    参数：
    - task_id: 任务 ID
    - user_note: 用户补充说明
    """
    # 创建结果目录
    results_dir = os.path.join("data", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    # 创建任务目录
    task_dir = os.path.join(results_dir, exec_request.task_id)
    os.makedirs(task_dir, exist_ok=True)
    
    # 生成示例HTML文件
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>生成页面 - 任务 {exec_request.task_id}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
        }}
        .note {{
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 10px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>自动生成的网页</h1>
        <p>任务ID: {exec_request.task_id}</p>
        <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="note">
            <strong>用户备注:</strong>
            <p>{exec_request.user_note if exec_request.user_note else "无备注"}</p>
        </div>
        
        <p>这是一个由SCOT-Web系统自动生成的网页示例。</p>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件
    html_path = os.path.join(task_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 保存CSS文件
    css_content = """
body {
    font-family: Arial, sans-serif;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
"""
    css_path = os.path.join(task_dir, "style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    
    # 创建任务记录
    tasks_dir = os.path.join("data", "tasks")
    os.makedirs(tasks_dir, exist_ok=True)
    
    task_record = {
        "task_id": exec_request.task_id,
        "status": "completed",
        "created_at": datetime.now().isoformat(),
        "finished_at": datetime.now().isoformat()
    }
    
    task_file = os.path.join(tasks_dir, f"{exec_request.task_id}.json")
    with open(task_file, "w", encoding="utf-8") as f:
        json.dump(task_record, f, ensure_ascii=False, indent=2)
    
    return ExecuteResponse(
        status="success",
        files=["index.html", "style.css"],
        preview_url=f"/api/preview/{exec_request.task_id}"
    )

@executor_router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """获取任务执行状态"""
    tasks_dir = os.path.join("data", "tasks")
    task_file = os.path.join(tasks_dir, f"{task_id}.json")
    
    if not os.path.exists(task_file):
        raise HTTPException(status_code=404, detail="任务未找到")
    
    with open(task_file, "r", encoding="utf-8") as f:
        task_data = json.load(f)
    
    return TaskStatusResponse(**task_data)