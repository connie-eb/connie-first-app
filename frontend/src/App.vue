<template>
  <div class="app">
    <header class="app-header">
      <h1>📝 Todo App (Vue 3)</h1>
      <p>一个简单的全栈待办事项应用</p>
    </header>

    <main class="main-content">
      <!-- 添加待办表单 -->
      <div class="add-todo-section">
        <form @submit.prevent="addTodo" class="todo-form">
          <div class="form-group">
            <input
                v-model="newTodo.title"
                type="text"
                placeholder="输入待办事项标题..."
                required
                class="title-input"
            >
          </div>

          <div class="form-group">
            <textarea
                v-model="newTodo.description"
                placeholder="描述（可选）..."
                class="description-textarea"
                rows="3"
            ></textarea>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? '添加中...' : '添加待办' }}
          </button>
        </form>
      </div>

      <!-- 统计信息 -->
      <div class="stats-card">
        <div class="stat-item">
          <span class="stat-number">{{ todos.length }}</span>
          <span class="stat-label">总计</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ completedCount }}</span>
          <span class="stat-label">已完成</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ pendingCount }}</span>
          <span class="stat-label">待完成</span>
        </div>
      </div>

      <!-- 待办列表 -->
      <div class="todos-section">
        <div v-if="loading" class="loading">加载中...</div>

        <div v-else-if="todos.length === 0" class="empty-state">
          <p>暂无待办事项</p>
          <p class="empty-hint">添加你的第一个待办事项吧！</p>
        </div>

        <div v-else class="todo-list">
          <div
              v-for="todo in todos"
              :key="todo.id"
              :class="['todo-item', { 'todo-completed': todo.completed }]"
          >
            <div class="todo-main">
              <input
                  type="checkbox"
                  :id="`todo-${todo.id}`"
                  v-model="todo.completed"
                  @change="updateTodo(todo)"
                  class="todo-checkbox"
              >

              <div class="todo-content">
                <label :for="`todo-${todo.id}`" class="todo-title">
                  {{ todo.title }}
                </label>
                <p v-if="todo.description" class="todo-description">
                  {{ todo.description }}
                </p>
                <span class="todo-date">创建时间: {{ formatDate(todo.id) }}</span>
              </div>
            </div>

            <button
                @click="deleteTodo(todo.id)"
                class="delete-btn"
                title="删除"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      {{ error }}
      <button @click="error = ''" class="close-error">×</button>
    </div>
  </div>
</template>

<script setup name="App" lang="js">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

// 响应式数据
const todos = ref([])
const loading = ref(false)
const error = ref('')

const newTodo = ref({
  title: '',
  description: ''
})

// 计算属性
const completedCount = computed(() =>
    todos.value.filter(todo => todo.completed).length
)

const pendingCount = computed(() =>
    todos.value.filter(todo => !todo.completed).length
)

// 方法
const loadTodos = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get(`${API_BASE}/todos`)
    todos.value = response.data
  } catch (err) {
    error.value = '加载待办事项失败: ' + (err.response?.data?.detail || err.message)
    console.error('加载失败:', err)
  } finally {
    loading.value = false
  }
}

const addTodo = async () => {
  if (!newTodo.value.title.trim()) return

  loading.value = true
  error.value = ''
  try {
    const todoData = {
      title: newTodo.value.title.trim(),
      description: newTodo.value.description.trim(),
      completed: false
    }

    const response = await axios.post(`${API_BASE}/todos`, todoData)
    todos.value.push(response.data)

    // 重置表单
    newTodo.value = {
      title: '',
      description: ''
    }
  } catch (err) {
    error.value = '添加待办事项失败: ' + (err.response?.data?.detail || err.message)
    console.error('添加失败:', err)
  } finally {
    loading.value = false
  }
}

const updateTodo = async (todo) => {
  error.value = ''
  try {
    await axios.put(`${API_BASE}/todos/${todo.id}`, todo)
  } catch (err) {
    error.value = '更新待办事项失败: ' + (err.response?.data?.detail || err.message)
    console.error('更新失败:', err)
    // 回滚状态
    todo.completed = !todo.completed
  }
}

const deleteTodo = async (todoId) => {
  error.value = ''
  try {
    await axios.delete(`${API_BASE}/todos/${todoId}`)
    todos.value = todos.value.filter(todo => todo.id !== todoId)
  } catch (err) {
    error.value = '删除待办事项失败: ' + (err.response?.data?.detail || err.message)
    console.error('删除失败:', err)
  }
}

const formatDate = (todoId) => {
  // 简单的时间格式化，实际项目中可以使用 dayjs 或 date-fns
  const date = new Date()
  return date.toLocaleTimeString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadTodos()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-600: #4b5563;
  --gray-800: #1f2937;
  --white: #ffffff;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: var(--gray-800);
}

.app {
  min-height: 100vh;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 40px;
  color: var(--white);
}

.app-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.app-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.main-content {
  max-width: 600px;
  margin: 0 auto;
}

/* 添加待办表单 */
.add-todo-section {
  background: var(--white);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.todo-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.title-input,
.description-textarea {
  padding: 12px 16px;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.2s;
}

.title-input:focus,
.description-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.description-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.submit-btn {
  background: var(--primary-color);
  color: var(--white);
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-1px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* 统计卡片 */
.stats-card {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-item {
  background: var(--white);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--gray-600);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 待办列表 */
.todos-section {
  background: var(--white);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.loading,
.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--gray-600);
}

.empty-hint {
  font-size: 0.9rem;
  opacity: 0.7;
  margin-top: 8px;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 16px;
  border: 2px solid var(--gray-200);
  border-radius: 12px;
  transition: all 0.2s;
}

.todo-item:hover {
  border-color: var(--gray-300);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.todo-completed {
  opacity: 0.7;
  background: var(--gray-100);
}

.todo-main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.todo-checkbox {
  margin-top: 4px;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.todo-content {
  flex: 1;
}

.todo-title {
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: block;
  margin-bottom: 4px;
}

.todo-completed .todo-title {
  text-decoration: line-through;
  color: var(--gray-600);
}

.todo-description {
  color: var(--gray-600);
  margin-bottom: 8px;
  line-height: 1.4;
}

.todo-date {
  font-size: 0.75rem;
  color: var(--gray-600);
}

.delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: var(--gray-100);
  transform: scale(1.1);
}

/* 错误提示 */
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--danger-color);
  color: var(--white);
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 400px;
}

.close-error {
  background: none;
  border: none;
  color: var(--white);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .app {
    padding: 16px;
  }

  .app-header h1 {
    font-size: 2rem;
  }

  .stats-card {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .add-todo-section,
  .todos-section {
    padding: 20px;
  }

  .error-message {
    left: 16px;
    right: 16px;
    top: 16px;
  }
}
</style>
