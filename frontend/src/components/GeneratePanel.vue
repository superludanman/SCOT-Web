<template>
  <div class="card">
    <h2 class="card-title">网页生成</h2>
    
    <div v-if="!generatedFiles">
      <div v-if="!prdData || !knowledgeData">
        <div class="alert alert-warning">
          请先完成PRD文档和知识点图谱的生成与保存
        </div>
      </div>
      
      <div v-else>
        <div class="form-group">
          <label>PRD文档:</label>
          <div class="form-control">
            <p><strong>{{ prdData.title }}</strong></p>
            <p class="text-muted">内容长度: {{ prdData.content?.length || 0 }} 字符</p>
          </div>
        </div>
        
        <div class="form-group">
          <label>知识点图谱:</label>
          <div class="form-control">
            <p><strong>{{ knowledgeData.name }}</strong></p>
            <p class="text-muted">知识点数量: {{ knowledgeData.graph?.nodes?.length || 0 }} 个</p>
          </div>
        </div>
        
        <div class="form-group">
          <label for="userNote">用户备注:</label>
          <input 
            type="text" 
            id="userNote" 
            v-model="userNote" 
            class="form-control" 
            placeholder="可选：添加一些备注信息"
          />
        </div>
        
        <button 
          @click="generateWebsite" 
          class="btn"
        >
          生成网页
        </button>
      </div>
      
      <div v-if="loading" class="mt-3 text-center">
        <div class="spinner"></div>
        <p class="mt-2">正在生成网页...</p>
      </div>
    </div>
    
    <div v-else>
      <div class="alert alert-success">
        网页生成成功！
      </div>
      
      <div class="form-group">
        <label>任务ID:</label>
        <div class="form-control">
          {{ taskId }}
        </div>
      </div>
      
      <div class="form-group">
        <label>生成的文件:</label>
        <ul>
          <li v-for="file in generatedFiles" :key="file">{{ file }}</li>
        </ul>
      </div>
      
      <div class="d-flex justify-content-between">
        <div>
          <button @click="resetGeneration" class="btn btn-secondary">重新生成</button>
          <button 
            v-if="taskId" 
            @click="downloadGeneratedFiles" 
            class="btn btn-info ml-2"
          >
            下载网页文件
          </button>
        </div>
        <button @click="previewWebsite" class="btn btn-primary">预览网页</button>
      </div>
    </div>
  </div>
</template>

<script>
import { executorAPI } from '../api/index.js';

export default {
  name: 'GeneratePanel',
  props: {
    prdData: {
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
      userNote: '',
      generatedFiles: null,
      taskId: '',
      loading: false
    };
  },
  methods: {
    async generateWebsite() {
      this.loading = true;
      
      try {
        const requestData = {
          prd: {
            title: this.prdData.title,
            content: this.prdData.content
          },
          knowledge_graph: {
            name: this.knowledgeData.name,
            graph: this.knowledgeData.graph
          },
          user_note: this.userNote
        };
        
        const response = await executorAPI.executeTask(requestData);
        
        this.generatedFiles = response.files;
        this.taskId = response.task_id;
        
        this.$emit('website-generated', {
          taskId: this.taskId,
          files: this.generatedFiles
        });
      } catch (error) {
        console.error('网页生成失败:', error);
        if (error.response && error.response.status) {
          alert('网页生成失败: HTTP错误 ' + error.response.status);
        } else {
          alert('网页生成失败: ' + (error.message || '未知错误'));
        }
      } finally {
        this.loading = false;
      }
    },
    
    previewWebsite() {
      if (this.taskId) {
        // 打开新窗口预览网页
        window.open(`/api/preview/${this.taskId}`, '_blank');
      }
    },
    
    async downloadGeneratedFiles() {
      if (this.taskId) {
        try {
          await executorAPI.downloadGeneratedFiles(this.taskId);
        } catch (error) {
          console.error('网页文件下载失败:', error);
          alert('网页文件下载失败: ' + (error.message || '未知错误'));
        }
      }
    },
    
    resetGeneration() {
      this.userNote = '';
      this.generatedFiles = null;
      this.taskId = '';
    }
  }
};
</script>

<style scoped>
ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

ul li {
  margin-bottom: 0.25rem;
}

.ml-2 {
  margin-left: 0.5rem;
}
</style>