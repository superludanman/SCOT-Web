from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import uuid
from datetime import datetime
from executor.task_executor import TaskExecutor
from executor.execution_context import ExecutionContext

executor_router = APIRouter()

class ExecuteRequest(BaseModel):
    reference_info: str
    knowledge_points: dict
    user_note: Optional[str] = ""

class ExecuteResponse(BaseModel):
    status: str
    task_id: str
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
    - reference_info: 参考网站信息
    - knowledge_points: 知识点信息
    - user_note: 用户补充说明
    """
    try:
        # 初始化AI执行上下文
        context = ExecutionContext()
        executor = TaskExecutor(context)
        
        # 执行任务
        result = executor.execute_task(exec_request.reference_info, exec_request.knowledge_points)
        
        if "error" in result:
            raise Exception(result["error"])
        
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 创建结果目录
        results_dir = os.path.join("data", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        # 创建任务目录
        task_dir = os.path.join(results_dir, task_id)
        os.makedirs(task_dir, exist_ok=True)
        
        # 保存生成的文件
        saved_files = []
        for filename, code in result["files"].items():
            file_path = os.path.join(task_dir, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            saved_files.append(filename)
        
        # 创建任务记录
        tasks_dir = os.path.join("data", "tasks")
        os.makedirs(tasks_dir, exist_ok=True)
        
        task_record = {
            "task_id": task_id,
            "status": "completed",
            "created_at": datetime.now().isoformat(),
            "finished_at": datetime.now().isoformat()
        }
        
        task_file = os.path.join(tasks_dir, f"{task_id}.json")
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task_record, f, ensure_ascii=False, indent=2)
        
        return ExecuteResponse(
            status="success",
            task_id=task_id,
            files=saved_files,
            preview_url=f"/api/preview/{task_id}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务执行失败: {str(e)}")

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