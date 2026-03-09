# FC 简单测试服务

基于 FastAPI 的基础功能测试服务，用于验证 FC 自定义容器部署流程。

## 功能

- `GET /hello` - 返回 "hello world"
- `GET /read-file` - 读取 `/data/test.json` 文件并打印 key-value

## 快速开始

### 1. 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py

# 测试
python test_api.py
```

### 2. 构建镜像

```bash
# 修改 build.sh 中的 NAMESPACE
chmod +x build.sh
./build.sh
```

### 3. 部署到 FC

```bash
# 安装 Serverless Devs
npm install @serverless-devs/s -g

# 配置密钥
s config add

# 修改 s.yaml 中的镜像地址
# 部署
s deploy
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `main.py` | FastAPI 主服务 |
| `requirements.txt` | Python 依赖 |
| `Dockerfile` | 容器镜像配置 |
| `build.sh` | 镜像构建脚本 |
| `s.yaml` | FC 部署配置 |
| `test_api.py` | API 测试脚本 |
