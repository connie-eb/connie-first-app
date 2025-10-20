# frontend

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

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