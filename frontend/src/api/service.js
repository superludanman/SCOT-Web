import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '',  // 移除baseURL，让请求使用相对路径
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 确保所有请求都以/api开头
    if (!config.url.startsWith('/api')) {
      config.url = '/api' + config.url;
    }
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  error => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.config.url);
    return response.data;
  },
  error => {
    console.error('API Response Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

// API服务类
class APIService {
  // GET请求
  async get(url) {
    try {
      const response = await apiClient.get(url);
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // POST请求
  async post(url, data) {
    try {
      const response = await apiClient.post(url, data);
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // POST表单请求
  async postForm(url, formData) {
    try {
      const response = await apiClient.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // PUT请求
  async put(url, data) {
    try {
      const response = await apiClient.put(url, data);
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // DELETE请求
  async delete(url) {
    try {
      const response = await apiClient.delete(url);
      return response;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  // 错误处理
  handleError(error) {
    if (error.response) {
      // 服务器响应了错误状态码
      const { status, data } = error.response;
      console.error(`API Error ${status}:`, data);
      return new Error(`HTTP ${status}: ${data?.detail || '请求失败'}`);
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('API Network Error:', error.request);
      return new Error('网络错误: 无法连接到服务器');
    } else {
      // 其他错误
      console.error('API Error:', error.message);
      return new Error(`请求错误: ${error.message}`);
    }
  }
}

// 导出API服务实例
export default new APIService();