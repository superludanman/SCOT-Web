<template>
  <div class="card">
    <h2 class="card-title">知识点图谱</h2>
    
    <div v-if="!knowledgeGraph">
      <div v-if="referenceData">
        <div class="alert alert-info">
          <p><strong>参考信息:</strong></p>
          <p>标题: {{ referenceData.title }}</p>
          <p>文本块数量: {{ referenceData.text_blocks?.length || 0 }}</p>
        </div>
        
        <button 
          @click="extractKnowledgeFromReference" 
          class="btn"
        >
          基于参考信息提取知识点
        </button>
      </div>
      
      <div v-else>
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
      </div>
      
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
import { knowledgeAPI, uploadAPI } from '../api/index.js';

export default {
  name: 'KnowledgeGraph',
  props: {
    referenceData: {
      type: Object,
      default: null
    },
    knowledgeData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      referenceUrl: '',
      uploadedFile: null,
      knowledgeGraph: null,
      graphName: '',
      loading: false
    };
  },
  watch: {
    knowledgeData: {
      handler(newVal) {
        if (newVal) {
          this.knowledgeGraph = newVal.graph;
          this.graphName = newVal.name;
        }
      },
      immediate: true
    }
  },
  methods: {
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.uploadedFile = files[0];
        this.referenceUrl = ''; // 清除URL输入
      }
    },
    
    async extractKnowledgeFromReference() {
      this.loading = true;
      
      try {
        // 基于参考数据提取知识点
        const response = await knowledgeAPI.extractKnowledge({
          reference_info: this.referenceData
        });
        
        this.knowledgeGraph = response.graph;
        this.graphName = `知识点: ${this.referenceData.title}`;
        
        // 通知父组件知识点已提取
        this.$emit('knowledge-extracted', {
          graph: response.graph,
          name: `知识点: ${this.referenceData.title}`
        });
      } catch (error) {
        console.error('知识点提取失败:', error);
        alert('知识点提取失败: ' + (error.message || '未知错误'));
      } finally {
        this.loading = false;
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
          const response = await uploadAPI.extractKnowledgeFromFile(formData);
          knowledgeData = response.graph;
        } else if (this.referenceUrl) {
          // 通过URL提取知识点
          const requestData = { reference_url: this.referenceUrl };
          const response = await knowledgeAPI.extractKnowledge(requestData);
          knowledgeData = response.graph;
        } else {
          throw new Error('请选择一个文件或输入一个URL');
        }
        
        this.knowledgeGraph = knowledgeData;
        this.graphName = this.referenceUrl ? `知识点: ${new URL(this.referenceUrl).hostname}` : `知识点: ${this.uploadedFile.name}`;
        
        // 通知父组件知识点已提取
        this.$emit('knowledge-extracted', {
          graph: knowledgeData,
          name: this.graphName
        });
      } catch (error) {
        console.error('知识点提取失败:', error);
        if (error.message) {
          alert('知识点提取失败: ' + error.message);
        } else {
          alert('知识点提取失败: ' + JSON.stringify(error));
        }
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
      const fileInput = document.getElementById('uploadedFile');
      if (fileInput) {
        fileInput.value = ''; // 清空文件输入
      }
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