<template>
  <div class="card">
    <h2 class="card-title">知识点图谱</h2>
    
    <div v-if="!knowledgeGraph">
      <div class="form-group">
        <label for="referenceUrl">参考网站URL:</label>
        <input 
          type="url" 
          id="referenceUrl" 
          v-model="referenceUrl" 
          class="form-control" 
          placeholder="https://example.com"
        />
      </div>
      
      <div class="form-group">
        <label for="uploadedFile">或上传HTML文件:</label>
        <input 
          type="file" 
          id="uploadedFile" 
          @change="handleFileUpload" 
          class="form-control" 
          accept=".html,.htm"
        />
      </div>
      
      <button 
        @click="extractKnowledge" 
        :disabled="!referenceUrl && !uploadedFile" 
        class="btn"
      >
        提取知识点
      </button>
      
      <div v-if="loading" class="mt-3 text-center">
        <div class="spinner"></div>
        <p class="mt-2">正在提取知识点...</p>
      </div>
    </div>
    
    <div v-else>
      <div class="alert alert-success">
        知识点提取成功！共 {{ knowledgeGraph.nodes.length }} 个知识点。
      </div>
      
      <div class="form-group">
        <label for="graphName">图谱名称:</label>
        <input 
          type="text" 
          id="graphName" 
          v-model="graphName" 
          class="form-control" 
          placeholder="请输入知识点图谱名称"
        />
      </div>
      
      <div class="form-group">
        <label>知识点列表:</label>
        <div class="knowledge-list">
          <div 
            v-for="(node, index) in knowledgeGraph.nodes" 
            :key="node.data.id"
            class="knowledge-item"
          >
            <span class="knowledge-id">{{ index + 1 }}.</span>
            <span class="knowledge-label">{{ node.data.label }}</span>
          </div>
        </div>
      </div>
      
      <div class="d-flex justify-content-between">
        <button @click="resetKnowledge" class="btn btn-secondary">重新提取</button>
        <button @click="saveKnowledgeGraph" class="btn btn-success" :disabled="!graphName">保存图谱</button>
      </div>
    </div>
  </div>
</template>

<script>
import { knowledgeAPI } from '../api/index.js';

export default {
  name: 'KnowledgeGraph',
  data() {
    return {
      referenceUrl: '',
      uploadedFile: null,
      knowledgeGraph: null,
      graphName: '',
      loading: false
    };
  },
  methods: {
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.uploadedFile = files[0];
        this.referenceUrl = ''; // 清除URL输入
      }
    },
    
    async extractKnowledge() {
      this.loading = true;
      
      try {
        let knowledgeData;
        
        if (this.uploadedFile) {
          // 通过上传文件提取知识点
          const formData = new FormData();
          formData.append('file', this.uploadedFile);
          const response = await knowledgeAPI.extractKnowledgeFromFile(formData);
          knowledgeData = response.graph;
        } else if (this.referenceUrl) {
          // 通过URL提取知识点
          const requestData = { reference_url: this.referenceUrl };
          const response = await knowledgeAPI.extractKnowledge(requestData);
          knowledgeData = response.graph;
        }
        
        this.knowledgeGraph = knowledgeData;
        this.graphName = this.referenceUrl ? `知识点: ${new URL(this.referenceUrl).hostname}` : `知识点: ${this.uploadedFile.name}`;
      } catch (error) {
        console.error('知识点提取失败:', error);
        alert('知识点提取失败: ' + (error.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    
    async saveKnowledgeGraph() {
      if (!this.graphName || !this.knowledgeGraph) {
        alert('请填写图谱名称并确保已提取知识点');
        return;
      }
      
      try {
        const requestData = {
          name: this.graphName,
          graph: this.knowledgeGraph
        };
        
        await knowledgeAPI.saveKnowledgeGraph(requestData);
        alert('知识点图谱保存成功！');
        this.$emit('knowledge-saved');
      } catch (error) {
        console.error('知识点图谱保存失败:', error);
        alert('知识点图谱保存失败: ' + (error.message || '未知错误'));
      }
    },
    
    resetKnowledge() {
      this.referenceUrl = '';
      this.uploadedFile = null;
      this.knowledgeGraph = null;
      this.graphName = '';
      document.getElementById('uploadedFile').value = ''; // 清空文件输入
    }
  }
};
</script>

<style scoped>
.knowledge-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 1rem;
}

.knowledge-item {
  padding: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.knowledge-item:last-child {
  border-bottom: none;
}

.knowledge-id {
  font-weight: bold;
  color: var(--primary-color);
  margin-right: 0.5rem;
}

.knowledge-label {
  color: var(--dark-color);
}
</style>