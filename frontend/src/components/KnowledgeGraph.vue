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
          @click="extractKnowledge" 
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
            :value="referenceUrlInput" 
            @input="referenceUrlInput = $event.target.value"
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
          :disabled="!referenceUrlInput && !uploadedFileInput" 
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
      
      <!-- 切换视图 -->
      <div class="view-toggle">
        <button 
          @click="currentView = 'list'" 
          :class="['btn', 'btn-small', { 'btn-primary': currentView === 'list' }]"
        >
          列表视图
        </button>
        <button 
          @click="currentView = 'graph'" 
          :class="['btn', 'btn-small', { 'btn-primary': currentView === 'graph' }]"
        >
          图谱视图
        </button>
      </div>
      
      <!-- 列表视图 -->
      <div v-if="currentView === 'list'" class="form-group">
        <label>知识点列表:</label>
        <div class="knowledge-list">
          <div 
            v-for="(node, index) in knowledgeGraph.nodes" 
            :key="node.data.id"
            class="knowledge-item"
          >
            <span class="knowledge-id">{{ index + 1 }}.</span>
            <span class="knowledge-label">{{ node.data.label }}</span>
            <button 
              v-if="node.data.type !== 'chapter'"
              @click="learnKnowledge(node.data)"
              class="btn btn-small btn-primary ml-auto"
            >
              学习
            </button>
          </div>
        </div>
      </div>
      
      <!-- 图谱视图 -->
      <div v-else-if="currentView === 'graph'">
        <KnowledgeGraphVisualization 
          :graph-data="knowledgeGraph"
          @save-graph="handleSaveGraph"
          @learn-knowledge="learnKnowledge"
        />
      </div>
      
      <div class="d-flex justify-content-between">
        <div>
          <button @click="resetKnowledge" class="btn btn-secondary">重新提取</button>
          <button 
            v-if="savedKnowledgeId" 
            @click="downloadKnowledgeGraph" 
            class="btn btn-info ml-2"
          >
            下载图谱
          </button>
        </div>
        <button @click="saveKnowledgeGraph" class="btn btn-success" :disabled="!graphName">保存图谱</button>
      </div>
    </div>
  </div>
</template>

<script>
import { knowledgeAPI, uploadAPI } from '../api/index.js';
import KnowledgeGraphVisualization from './KnowledgeGraphVisualization.vue';

export default {
  name: 'KnowledgeGraph',
  components: {
    KnowledgeGraphVisualization
  },
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
      referenceUrlInput: '',
      uploadedFileInput: null,
      knowledgeGraph: null,
      graphName: '',
      loading: false,
      savedKnowledgeId: null,
      currentView: 'list' // 'list' 或 'graph'
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
    },
    referenceData: {
      handler(newVal) {
        if (newVal && newVal.url) {
          this.referenceUrlInput = newVal.url;
        }
      },
      immediate: true
    }
  },
  methods: {
    handleFileUpload(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.uploadedFileInput = files[0];
        this.referenceUrlInput = ''; // 清除URL输入
      }
    },
    
    async extractKnowledge() {
      this.loading = true;
      
      try {
        let knowledgeData;
        
        // 根据参考数据中的type属性调用不同的接口
        if (this.referenceData && this.referenceData.type === 'file') {
          // 通过上传文件提取知识点
          console.log("通过上传文件提取知识点");
          const formData = new FormData();
          formData.append('file', this.referenceData.file);
          const response = await uploadAPI.extractKnowledgeFromFile(formData);
          knowledgeData = response.graph;
          this.graphName = `知识点: ${this.referenceData.file.name}`;
        } else if (this.referenceData && this.referenceData.type === 'url') {
          // 通过URL提取知识点
          console.log("通过上传的URL提取知识点");
          const requestData = { reference_url: this.referenceData.url };
          const response = await knowledgeAPI.extractKnowledge(requestData);
          knowledgeData = response.graph;
          this.graphName = `知识点: ${new URL(this.referenceData.url).hostname}`;
        } else if (this.uploadedFileInput) {
          // 通过当前选择的文件提取知识点
          console.log("通过当前选择的文件提取知识点");
          const formData = new FormData();
          formData.append('file', this.uploadedFileInput);
          const response = await uploadAPI.extractKnowledgeFromFile(formData);
          knowledgeData = response.graph;
          this.graphName = `知识点: ${this.uploadedFileInput.name}`;
        } else if (this.referenceUrlInput) {
          // 通过当前输入的URL提取知识点
          console.log("通过当前输入的URL提取知识点");
          const requestData = { reference_url: this.referenceUrlInput };
          const response = await knowledgeAPI.extractKnowledge(requestData);
          knowledgeData = response.graph;
          this.graphName = `知识点: ${new URL(this.referenceUrlInput).hostname}`;
        } else if (this.referenceData) {
          // 基于参考数据提取知识点（当没有明确的上传类型时）
          console.log("基于参考数据提取知识点（没有明确的上传类型）");
          const requestData = { reference_info: this.referenceData };
          const response = await knowledgeAPI.extractKnowledge(requestData);
          knowledgeData = response.graph;
          this.graphName = `知识点: ${this.referenceData.title}`;
        } else {
          throw new Error('请选择一个文件或输入一个URL');
        }
        
        this.knowledgeGraph = knowledgeData;
        
        // 通知父组件知识点已提取
        this.$emit('knowledge-extracted', {
          graph: knowledgeData,
          name: this.graphName
        });
      } catch (error) {
        console.error('知识点提取失败:', error);
        if (error.response && error.response.status) {
          alert('知识点提取失败: HTTP错误 ' + error.response.status);
        } else if (error.message) {
          alert('知识点提取失败: ' + error.message);
        } else {
          alert('知识点提取失败: ' + JSON.stringify(error));
        }
      } finally {
        this.loading = false;
      }
    },
    
    handleSaveGraph(graph) {
      // 更新当前知识图谱数据
      this.knowledgeGraph = graph;
      alert('图谱修改已保存到本地');
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
        
        const response = await knowledgeAPI.saveKnowledgeGraph(requestData);
        this.savedKnowledgeId = response.id;
        alert('知识点图谱保存成功！');
        this.$emit('knowledge-saved');
      } catch (error) {
        console.error('知识点图谱保存失败:', error);
        alert('知识点图谱保存失败: ' + (error.message || '未知错误'));
      }
    },
    
    async downloadKnowledgeGraph() {
      if (this.savedKnowledgeId) {
        try {
          await knowledgeAPI.downloadKnowledgeGraph(this.savedKnowledgeId);
        } catch (error) {
          console.error('知识点图谱下载失败:', error);
          alert('知识点图谱下载失败: ' + (error.message || '未知错误'));
        }
      }
    },
    
    resetKnowledge() {
      this.referenceUrlInput = '';
      this.uploadedFileInput = null;
      this.knowledgeGraph = null;
      this.graphName = '';
      this.savedKnowledgeId = null;
      this.currentView = 'list';
      const fileInput = document.getElementById('uploadedFile');
      if (fileInput) {
        fileInput.value = ''; // 清空文件输入
      }
    },
    
    learnKnowledge(nodeData) {
      // 通知父组件跳转到学习知识点模块
      this.$emit('learn-knowledge', nodeData);
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
  display: flex;
  align-items: center;
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
  flex: 1;
}

.ml-2 {
  margin-left: 0.5rem;
}

.ml-auto {
  margin-left: auto;
}

.view-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn-small {
  padding: 5px 10px;
  font-size: 14px;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}
</style>