from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Todo API")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # 添加 Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TodoItem(BaseModel):
    id: Optional[str] = None
    title: str
    completed: bool = False
    description: Optional[str] = None

# 模拟数据库
todos_db = []

@app.get("/")
async def root():
    return {"message": "Todo API is running!"}

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_db

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    todo.id = str(uuid.uuid4())
    todos_db.append(todo)
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo_update: TodoItem):
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            # 更新现有待办事项
            todos_db[index] = todo_update
            todos_db[index].id = todo_id  # 保持 ID 不变
            return todos_db[index]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            del todos_db[index]
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
