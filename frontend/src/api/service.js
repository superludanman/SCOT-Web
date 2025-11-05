// API服务封装
class APIService {
    constructor() {
        // 在开发环境中，API请求会被Vite代理到后端
        // 在生产环境中，API与前端在同一源下
        this.baseURL = import.meta.env.DEV ? '' : '';
    }

    async request(url, options = {}) {
        const response = await fetch(this.baseURL + url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async post(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async postForm(url, formData) {
        // For form data, we don't set Content-Type header
        // Browser will set it with boundary automatically
        return this.request(url, {
            method: 'POST',
            body: formData,
        });
    }

    async get(url) {
        return this.request(url, {
            method: 'GET',
        });
    }

    async delete(url) {
        return this.request(url, {
            method: 'DELETE',
        });
    }
}

export default new APIService();