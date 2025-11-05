from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import os

preview_router = APIRouter()

@preview_router.get("/{task_id}", response_class=HTMLResponse)
async def preview_website(task_id: str):
    """
    网页预览接口
    
    参数：
    - task_id: 任务 ID
    """
    # 构建结果文件路径 - 根据实际生成的文件结构调整路径
    result_dir = os.path.join("data", "results", "project", "public")
    html_path = os.path.join(result_dir, "index.html")
    
    # 检查文件是否存在
    if not os.path.exists(html_path):
        # 创建一个默认的预览页面
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>预览页面 - 任务 {task_id}</title>
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
            text-align: center;
        }}
        h1 {{
            color: #333;
        }}
        .status {{
            padding: 20px;
            margin: 20px 0;
            background-color: #e7f3ff;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SCOT-Web 网页预览</h1>
        <div class="status">
            <p>任务ID: {task_id}</p>
            <p>正在生成预览内容...</p>
        </div>
        <p>请稍等片刻，系统正在为您生成网页内容。</p>
    </div>
</body>
</html>
"""
        return HTMLResponse(content=html_content)
    
    # 返回实际的HTML文件内容
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return HTMLResponse(content=content)

@preview_router.get("/file/{task_id}/{file_path:path}")
async def get_preview_file(task_id: str, file_path: str):
    """获取预览文件（CSS, JS等）"""
    # 根据实际生成的文件结构调整路径
    result_dir = os.path.join("data", "results", "project", "public")
    full_path = os.path.join(result_dir, file_path)
    
    # 检查文件是否存在
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="文件未找到")
    
    return FileResponse(full_path)