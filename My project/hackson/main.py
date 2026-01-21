"""
学术论文翻译网站 - FastAPI 主应用
"""
import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from app.services.factory import create_ai_service
from app.parsers.factory import create_parser
from app.translator.translator import TranslationManager

load_dotenv()

app = FastAPI(title="学术论文翻译工具", version="1.0.0")

# 挂载静态文件和模板
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# 存储目录
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 翻译任务状态存储 (生产环境应使用 Redis)
translation_tasks: dict = {}


class TranslationRequest(BaseModel):
    file_id: str
    provider: str  # openai, qianwen, claude
    api_key: str
    model: Optional[str] = None


class TranslationStatus(BaseModel):
    task_id: str
    status: str  # pending, processing, completed, failed
    progress: int
    message: str
    result_file: Optional[str] = None


@app.get("/")
async def home(request: Request):
    """首页 - 文件上传界面"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/translate/{task_id}")
async def translate_page(request: Request, task_id: str):
    """翻译进度页面"""
    if task_id not in translation_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    return templates.TemplateResponse("translate.html", {
        "request": request,
        "task_id": task_id
    })


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件 API"""
    # 验证文件类型
    allowed_extensions = {".pdf", ".docx", ".md", ".markdown", ".txt"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的文件类型。支持的类型: {', '.join(allowed_extensions)}"
        )
    
    # 验证文件大小 (最大 20MB)
    content = await file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小超过 20MB 限制")
    
    # 保存文件
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "size": len(content),
        "type": file_ext
    }


@app.post("/api/translate")
async def start_translation(
    request: TranslationRequest,
    background_tasks: BackgroundTasks
):
    """启动翻译任务 API"""
    # 查找上传的文件
    file_path = None
    for ext in [".pdf", ".docx", ".md", ".markdown", ".txt"]:
        potential_path = UPLOAD_DIR / f"{request.file_id}{ext}"
        if potential_path.exists():
            file_path = potential_path
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 创建任务
    task_id = str(uuid.uuid4())
    translation_tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "message": "准备开始翻译...",
        "result_file": None,
        "file_path": str(file_path),
        "provider": request.provider,
        "api_key": request.api_key,
        "model": request.model
    }
    
    # 后台执行翻译
    background_tasks.add_task(
        execute_translation,
        task_id,
        file_path,
        request.provider,
        request.api_key,
        request.model
    )
    
    return {"task_id": task_id, "status": "pending"}


async def execute_translation(
    task_id: str,
    file_path: Path,
    provider: str,
    api_key: str,
    model: Optional[str]
):
    """执行翻译任务"""
    try:
        translation_tasks[task_id]["status"] = "processing"
        translation_tasks[task_id]["message"] = "正在解析文件..."
        translation_tasks[task_id]["progress"] = 10
        
        # 解析文件
        parser = create_parser(file_path.suffix)
        document = parser.parse(file_path)
        
        translation_tasks[task_id]["message"] = "正在初始化 AI 服务..."
        translation_tasks[task_id]["progress"] = 20
        
        # 创建 AI 服务
        ai_service = create_ai_service(provider, api_key, model)
        
        # 创建翻译管理器
        manager = TranslationManager(ai_service)
        
        # 定义进度回调
        def progress_callback(progress: int, message: str):
            translation_tasks[task_id]["progress"] = 20 + int(progress * 0.7)
            translation_tasks[task_id]["message"] = message
        
        # 根据文件类型决定输出格式
        is_pdf = file_path.suffix.lower() == ".pdf"
        
        if is_pdf:
            # PDF 文件：生成带图片的 PDF
            output_filename = f"{task_id}.pdf"
            output_path = OUTPUT_DIR / output_filename
            
            await manager.translate_to_pdf(
                document, 
                output_path, 
                progress_callback
            )
            
            translation_tasks[task_id]["result_file"] = output_filename
            translation_tasks[task_id]["media_type"] = "application/pdf"
        else:
            # 其他文件：生成 Markdown
            translated_content = await manager.translate_document(document, progress_callback)
            
            translation_tasks[task_id]["message"] = "正在保存结果..."
            translation_tasks[task_id]["progress"] = 95
            
            output_filename = f"{task_id}.md"
            output_path = OUTPUT_DIR / output_filename
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(translated_content)
            
            translation_tasks[task_id]["result_file"] = output_filename
            translation_tasks[task_id]["media_type"] = "text/markdown"
        
        translation_tasks[task_id]["status"] = "completed"
        translation_tasks[task_id]["progress"] = 100
        translation_tasks[task_id]["message"] = "翻译完成！"
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        translation_tasks[task_id]["status"] = "failed"
        translation_tasks[task_id]["message"] = f"翻译失败: {str(e)}"


@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """查询翻译状态 API"""
    if task_id not in translation_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = translation_tasks[task_id]
    return TranslationStatus(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        message=task["message"],
        result_file=task.get("result_file")
    )


@app.get("/api/download/{task_id}")
async def download_result(task_id: str):
    """下载翻译结果 API"""
    if task_id not in translation_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = translation_tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="翻译尚未完成")
    
    result_file = task.get("result_file")
    if not result_file:
        raise HTTPException(status_code=404, detail="结果文件不存在")
    
    file_path = OUTPUT_DIR / result_file
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="结果文件不存在")
    
    # 根据文件类型设置 media_type
    media_type = task.get("media_type", "text/markdown")
    
    return FileResponse(
        path=file_path,
        filename=f"translated_{result_file}",
        media_type=media_type
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
