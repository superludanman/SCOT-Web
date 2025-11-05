<template>
  <div class="card">
    <h2 class="card-title">网页生成</h2>
    
    <div v-if="!generatedFiles">
      <div class="form-group">
        <label for="referenceInfo">参考网站信息:</label>
        <textarea 
          id="referenceInfo" 
          v-model="referenceInfo" 
          class="form-control" 
          rows="4" 
          placeholder="请输入参考网站的相关信息"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label>知识点信息:</label>
        <textarea 
          v-model="knowledgePoints" 
          class="form-control" 
          rows="6" 
          placeholder="请输入知识点信息（JSON格式）"
        ></textarea>
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
        :disabled="!referenceInfo || !knowledgePoints" 
        class="btn"
      >
        生成网页
      </button>
      
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
        <button @click="resetGeneration" class="btn btn-secondary">重新生成</button>
        <button @click="previewWebsite" class="btn btn-info">预览网页</button>
      </div>
    </div>
  </div>
</template>

<script>
import { executorAPI, previewAPI } from '../api/index.js';

export default {
  name: 'GeneratePanel',
  data() {
    return {
      referenceInfo: '',
      knowledgePoints: '',
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
        // 验证知识点信息是否为有效的JSON
        let knowledgeData;
        try {
          knowledgeData = JSON.parse(this.knowledgePoints);
        } catch (e) {
          throw new Error('知识点信息必须是有效的JSON格式');
        }
        
        const requestData = {
          reference_info: this.referenceInfo,
          knowledge_points: knowledgeData,
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
        alert('网页生成失败: ' + (error.message || '未知错误'));
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
    
    resetGeneration() {
      this.referenceInfo = '';
      this.knowledgePoints = '';
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
</style>