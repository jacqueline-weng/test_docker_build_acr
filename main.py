"""
FC 简单测试服务
基于 FastAPI 的基础功能测试
"""

import os
import json
import logging
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 请求/响应模型
class HelloResponse(BaseModel):
    message: str
    status: str


class FileContentResponse(BaseModel):
    file_path: str
    content: Dict[str, Any]
    keys: list


# Lifespan 管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("=" * 50)
    logger.info("测试服务启动")
    logger.info("=" * 50)
    
    # 检查 /data 目录
    data_dir = "/data"
    if os.path.exists(data_dir):
        logger.info(f"/data 目录存在")
        # 列出 /data 目录内容
        try:
            files = os.listdir(data_dir)
            logger.info(f"/data 目录内容: {files}")
        except Exception as e:
            logger.warning(f"无法读取 /data 目录: {e}")
    else:
        logger.warning(f"/data 目录不存在")
    
    yield
    
    logger.info("测试服务关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="FC 简单测试服务",
    description="基于 FastAPI 的基础功能测试",
    version="1.0.0",
    lifespan=lifespan
)


# 健康检查端点（FC 必需）
@app.get("/", response_model=HelloResponse)
@app.get("/health", response_model=HelloResponse)
async def health_check():
    """健康检查端点"""
    return HelloResponse(
        message="Service is running",
        status="healthy"
    )


# 接口 1: 返回 "hello world"
@app.get("/hello", response_model=HelloResponse)
async def hello_world():
    """
    返回 Hello World 消息
    """
    logger.info("收到 /hello 请求")
    return HelloResponse(
        message="hello world",
        status="success"
    )


# 接口 2: 读取 /data/test.json 文件
@app.get("/read-file", response_model=FileContentResponse)
async def read_test_file():
    """
    读取 /data/test.json 文件并返回 key-value 信息
    """
    file_path = "/data/test.json"
    logger.info(f"收到 /read-file 请求，尝试读取: {file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        raise HTTPException(
            status_code=404,
            detail=f"文件不存在: {file_path}"
        )
    
    try:
        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        # 打印 key 和 value 到日志
        logger.info(f"成功读取文件: {file_path}")
        logger.info("文件内容:")
        for key, value in content.items():
            logger.info(f"  {key}: {value}")
        
        # 返回结果
        return FileContentResponse(
            file_path=file_path,
            content=content,
            keys=list(content.keys())
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析错误: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"文件内容不是有效的 JSON: {str(e)}"
        )
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"读取文件失败: {str(e)}"
        )


# 错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    logger.error(f"全局异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "9000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
