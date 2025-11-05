// 前端主入口文件
import axios from 'axios';
import { createApp } from 'vue';
import Dashboard from './components/Dashboard.vue';
import './styles/main.css';

// 创建Vue应用并挂载到正确的元素
const app = createApp({
  components: {
    Dashboard
  },
  template: `
    <Dashboard />
  `
});

// 挂载应用到新的挂载点
app.mount('#vue-app');
console.log('SCOT-Web前端应用已启动');

// 创建API实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// PRD相关API
export const prdAPI = {
  // 创建PRD
  createPRD: (data) => api.post('/prd', data),
  
  // 获取PRD列表
  listPRDs: () => api.get('/prd'),
  
  // 获取单个PRD
  getPRD: (id) => api.get(`/prd/${id}`),
  
  // 删除PRD
  deletePRD: (id) => api.delete(`/prd/${id}`),
};

// 知识点相关API
export const knowledgeAPI = {
  // 创建知识点图谱
  createKnowledgeGraph: (name, graph) => api.post('/knowledge', graph, { params: { name } }),
  
  // 获取知识点图谱列表
  listKnowledgeGraphs: () => api.get('/knowledge'),
  
  // 获取单个知识点图谱
  getKnowledgeGraph: (id) => api.get(`/knowledge/${id}`),
  
  // 删除知识点图谱
  deleteKnowledgeGraph: (id) => api.delete(`/knowledge/${id}`),
};

// 执行器相关API
export const executorAPI = {
  // 执行任务
  executeTask: (data) => api.post('/executor/execute', data),
  
  // 获取任务状态
  getTaskStatus: (taskId) => api.get(`/executor/status/${taskId}`),
  
  // 获取任务结果
  getTaskResult: (taskId) => api.get(`/executor/result/${taskId}`),
};

// 日志相关API
export const logsAPI = {
  // 获取日志列表
  listLogs: (params) => api.get('/logs', { params }),
  
  // 获取日志详情
  getLogDetail: (taskId) => api.get(`/logs/${taskId}`),
  
  // 删除日志
  deleteLog: (taskId) => api.delete(`/logs/${taskId}`),
};

// 预览相关API
export const previewAPI = {
  // 预览网站
  previewWebsite: (taskId) => api.get(`/preview/${taskId}`),
  
  // 获取网站文件
  getWebsiteFile: (taskId, filePath) => api.get(`/preview/file/${taskId}/${filePath}`),
};

// 上传相关API
export const uploadAPI = {
  // 上传图片
  uploadImage: (formData) => api.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // 上传文档
  uploadDocument: (formData) => api.post('/upload/document', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // 获取上传文件列表
  listUploadedFiles: () => api.get('/upload/list'),
};

// 默认导出API实例
export default api;