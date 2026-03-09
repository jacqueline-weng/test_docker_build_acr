# =============================================================================
# FC 简单测试服务 - Dockerfile
# 使用 Ubuntu 22.04 基础镜像
# =============================================================================

# 使用 Ubuntu 22.04 基础镜像
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装 Python 3.10
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python 3.10 为默认 python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# 升级 pip
RUN pip install --upgrade pip

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY main.py .

# 创建 /data 目录（用于挂载测试文件）
RUN mkdir -p /data

# 暴露端口（与 FC 配置一致）
EXPOSE 9000

# 启动命令
CMD ["python", "main.py"]
