from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import uuid
from datetime import datetime
from agents.slow_mind import SlowMind
from executor.task_executor import TaskExecutor
from executor.execution_context import ExecutionContext

executor_router = APIRouter()

class ReferenceInfo(BaseModel):
    title: str
    structure: List[Dict[str, Any]]
    text_blocks: List[str]

class PRDInfo(BaseModel):
    title: str
    content: str

class KnowledgeGraphInfo(BaseModel):
    name: str
    graph: dict

class ExecuteTaskRequest(BaseModel):
    prd: PRDInfo
    knowledge_graph: KnowledgeGraphInfo
    user_note: Optional[str] = None

class ExecuteTaskResponse(BaseModel):
    task_id: str
    files: List[str]
    status: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    message: str
    files: List[str]

@executor_router.post("/", response_model=ExecuteTaskResponse)
async def execute_task(task_request: ExecuteTaskRequest):
    """
    执行网页生成任务
    
    参数：
    - prd: PRD信息
    - knowledge_graph: 知识点图谱
    - user_note: 用户备注
    """
    try:
        # 创建任务ID
        task_id = str(uuid.uuid4())
        
        # 初始化执行上下文
        context = ExecutionContext()
        
        # 创建任务执行器
        executor = TaskExecutor(context)
        
        # 将PRD内容转换为dependency_context格式
        dependency_context = task_request.prd.content
        
        # 将知识点图谱转换为existing_code_context格式
        existing_code_context = json.dumps(task_request.knowledge_graph.graph, ensure_ascii=False)
        
        # 执行任务，传递user_note作为user_goal参数
        result = executor.execute_task(
            dependency_context=dependency_context,
            existing_code_context=existing_code_context,
            user_goal=task_request.user_note or ""
        )
        
        # 如果执行出错，抛出异常
        if "error" in result:
            raise HTTPException(status_code=500, detail=f"任务执行失败: {result['error']}")
        
        # 提取生成的文件列表
        generated_files = list(result.get("files", {}).keys())
        
        # 保存任务结果到文件
        results_dir = os.path.join("data", "results", "project")
        os.makedirs(results_dir, exist_ok=True)
        task_file = os.path.join(results_dir, f"{task_id}.json")
        
        task_data = {
            "task_id": task_id,
            "status": "success",
            "message": "任务执行成功",
            "files": generated_files,
            "result": result
        }
        
        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
        
        return ExecuteTaskResponse(
            task_id=task_id,
            files=generated_files,
            status="success"
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务执行失败: {str(e)}")

@executor_router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    获取任务执行状态
    
    参数：
    - task_id: 任务ID
    """
    try:
        # 读取任务结果文件
        results_dir = os.path.join("data", "results", "project")
        task_file = os.path.join(results_dir, f"{task_id}.json")
        
        if not os.path.exists(task_file):
            raise HTTPException(status_code=404, detail="任务未找到")
        
        with open(task_file, "r", encoding="utf-8") as f:
            task_data = json.load(f)
        
        return TaskStatusResponse(
            task_id=task_id,
            status=task_data.get("status", "unknown"),
            message=task_data.get("message", ""),
            files=task_data.get("files", [])
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务状态失败: {str(e)}")