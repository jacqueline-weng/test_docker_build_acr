# =============================================================================
# FC 简单测试服务 - Dockerfile
# 基于阿里云 ACR Python 基础镜像
# =============================================================================

# 使用阿里云 ACR 官方 Python 基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/acs/alpine:3.18

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装 Python 3.10 和 pip
RUN yum install -y python3 python3-pip && \
    yum clean all

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY main.py .

# 创建 /data 目录（用于挂载测试文件）
RUN mkdir -p /data

# 暴露端口（与 FC 配置一致）
EXPOSE 9000

# 启动命令
CMD ["python3", "main.py"]
