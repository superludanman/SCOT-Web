import apiService from './service.js';

// 上传相关API
export const uploadAPI = {
    // 上传HTML文件
    uploadHTML: (formData) => {
        return apiService.postForm('/api/upload/html', formData);
    },

    // 从文件生成PRD
    generatePRDFromFile: (formData) => {
        return apiService.postForm('/api/upload/generate-prd', formData);
    },

    // 从文件提取知识点
    extractKnowledgeFromFile: (formData) => {
        return apiService.postForm('/api/upload/extract-knowledge', formData);
    },

    // 获取上传文件列表
    listFiles: () => {
        return apiService.get('/api/upload/list');
    }
};

// PRD相关API
export const prdAPI = {
    // 生成PRD
    generatePRD: (data) => {
        return apiService.post('/api/prd/generate', data);
    },

    // 保存PRD
    savePRD: (data) => {
        return apiService.post('/api/prd/save', data);
    },

    // 获取PRD列表
    listPRDs: () => {
        return apiService.get('/api/prd');
    },

    // 获取PRD详情
    getPRD: (id) => {
        return apiService.get(`/api/prd/${id}`);
    },

    // 删除PRD
    deletePRD: (id) => {
        return apiService.delete(`/api/prd/${id}`);
    },

    // 下载PRD
    downloadPRD: (id) => {
        return apiService.download(`/api/prd/download/${id}`);
    }
};

// 知识图谱相关API
export const knowledgeAPI = {
    // 提取知识点
    extractKnowledge: (data) => {
        return apiService.post('/api/knowledge/extract', data);
    },

    // 保存知识图谱
    saveKnowledgeGraph: (data) => {
        return apiService.post('/api/knowledge/save', data);
    },

    // 获取知识图谱列表
    listKnowledgeGraphs: () => {
        return apiService.get('/api/knowledge');
    },

    // 获取知识图谱详情
    getKnowledgeGraph: (id) => {
        return apiService.get(`/api/knowledge/${id}`);
    },

    // 删除知识图谱
    deleteKnowledgeGraph: (id) => {
        return apiService.delete(`/api/knowledge/${id}`);
    },

    // 下载知识图谱
    downloadKnowledgeGraph: (id) => {
        return apiService.download(`/api/knowledge/download/${id}`);
    }
};

// 学习知识点相关API
export const learningAPI = {
    // 生成知识点学习内容
    generateKnowledgeContent: (data) => {
        return apiService.post('/api/learning/generate-knowledge-point', data);
    }
};

// 测试题生成相关API
export const testGenerationAPI = {
    // 生成测试题
    generateTestTask: (data) => {
        return apiService.post('/api/test/generate-test-task', data);
    }
};

// 执行器相关API
export const executorAPI = {
    // 执行任务
    executeTask: (data) => {
        return apiService.post('/api/execute', data);
    },

    // 获取任务状态
    getTaskStatus: (taskId) => {
        return apiService.get(`/api/execute/status/${taskId}`);
    },

    // 下载生成的文件
    downloadGeneratedFiles: (taskId) => {
        return apiService.download(`/api/execute/download/${taskId}`);
    }
};

// 预览相关API
export const previewAPI = {
    // 预览网站
    previewWebsite: (taskId) => {
        return apiService.get(`/api/preview/${taskId}`);
    },

    // 获取预览文件
    getPreviewFile: (taskId, filePath) => {
        return apiService.get(`/api/preview/file/${taskId}/${filePath}`);
    }
};

// 日志相关API
export const logsAPI = {
    // 获取日志列表
    listLogs: () => {
        return apiService.get('/api/logs');
    },

    // 获取日志详情
    getLogDetail: (taskId) => {
        return apiService.get(`/api/logs/${taskId}`);
    }
};