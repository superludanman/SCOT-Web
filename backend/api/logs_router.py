from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import json
from datetime import datetime

logs_router = APIRouter()

class LogEntry(BaseModel):
    task_id: str
    timestamp: str
    files: List[str]
    status: str

class LogsResponse(BaseModel):
    logs: List[LogEntry]

@logs_router.get("/", response_model=LogsResponse)
async def get_logs():
    """
    日志查询接口
    """
    # 创建日志目录
    logs_dir = os.path.join("data", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    logs = []
    
    # 查找所有任务记录
    tasks_dir = os.path.join("data", "tasks")
    if os.path.exists(tasks_dir):
        for filename in os.listdir(tasks_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(tasks_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        task_data = json.load(f)
                    
                    # 构造日志条目
                    log_entry = LogEntry(
                        task_id=task_data.get("task_id", filename.replace(".json", "")),
                        timestamp=task_data.get("finished_at", task_data.get("created_at", datetime.now().isoformat())),
                        files=["index.html", "style.css"],  # 示例文件
                        status=task_data.get("status", "unknown")
                    )
                    logs.append(log_entry)
                except Exception:
                    continue
    
    # 按时间倒序排列
    logs.sort(key=lambda x: x.timestamp, reverse=True)
    
    return LogsResponse(logs=logs)

@logs_router.get("/{task_id}", response_model=LogEntry)
async def get_log_detail(task_id: str):
    """获取指定任务的日志详情"""
    tasks_dir = os.path.join("data", "tasks")
    task_file = os.path.join(tasks_dir, f"{task_id}.json")
    
    if not os.path.exists(task_file):
        raise HTTPException(status_code=404, detail="日志未找到")
    
    with open(task_file, "r", encoding="utf-8") as f:
        task_data = json.load(f)
    
    return LogEntry(
        task_id=task_data.get("task_id", task_id),
        timestamp=task_data.get("finished_at", task_data.get("created_at", datetime.now().isoformat())),
        files=["index.html", "style.css"],  # 示例文件
        status=task_data.get("status", "unknown")
    )

@logs_router.delete("/{task_id}")
async def delete_log(task_id: str):
    """删除指定任务的日志"""
    logs_dir = os.path.join("data", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # 查找并删除匹配的日志文件
    for filename in os.listdir(logs_dir):
        if filename.startswith(f"{task_id}_") and filename.endswith(".txt"):
            filepath = os.path.join(logs_dir, filename)
            os.remove(filepath)
            return {"message": "Log deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Log not found")