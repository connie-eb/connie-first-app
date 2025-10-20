## Project Setup

### 安装依赖
```sh
npm install
```

### 启动项目

```sh
npm run dev
```

### 打包项目

```sh
npm run build
```

# backend

## Project Setup

### 创建 requirements.txt
```shell
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic==2.5.0
python-multipart==0.0.6
```

### 安装后端依赖
```shell
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 启动后端服务
```shell
python app.py
```
后端将在 http://localhost:8000 运行
