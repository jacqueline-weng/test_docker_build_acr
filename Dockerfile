# =============================================================================
# FC 简单测试服务 - Dockerfile
# 基于阿里云 ACR Python 基础镜像
# =============================================================================

# 使用企业版 ACR 中的基础镜像，或本地构建
# 方案：使用 alpine 基础镜像，手动安装 Python
FROM alpine:3.18

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装 Python 和 pip
RUN apk add --no-cache python3 py3-pip

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# 复制应用代码
COPY main.py .

# 创建 /data 目录（用于挂载测试文件）
RUN mkdir -p /data

# 暴露端口（与 FC 配置一致）
EXPOSE 9000

# 启动命令
CMD ["python3", "main.py"]
