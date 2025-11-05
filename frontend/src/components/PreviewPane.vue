<template>
  <div class="card">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="card-title">网页预览</h2>
      <button 
        v-if="taskId" 
        @click="refreshPreview" 
        class="btn btn-secondary btn-sm"
      >
        刷新预览
      </button>
    </div>
    
    <div v-if="!taskId">
      <div class="alert alert-warning">
        请先生成网页以进行预览
      </div>
      
      <div class="form-group">
        <label for="taskIdInput">任务ID:</label>
        <input 
          type="text" 
          id="taskIdInput" 
          v-model="taskIdInput" 
          class="form-control" 
          placeholder="请输入任务ID"
        />
      </div>
      
      <button 
        @click="loadPreview" 
        :disabled="!taskIdInput" 
        class="btn"
      >
        加载预览
      </button>
    </div>
    
    <div v-else>
      <div class="preview-container">
        <iframe 
          :src="previewUrl" 
          class="preview-frame"
          frameborder="0"
        ></iframe>
      </div>
      
      <div class="mt-3">
        <button @click="resetPreview" class="btn btn-secondary">关闭预览</button>
      </div>
    </div>
  </div>
</template>

<script>
import { previewAPI } from '../api/index.js';

export default {
  name: 'PreviewPane',
  data() {
    return {
      taskId: '',
      taskIdInput: '',
      previewUrl: ''
    };
  },
  methods: {
    loadPreview() {
      if (this.taskIdInput) {
        this.taskId = this.taskIdInput;
        this.previewUrl = `/api/preview/${this.taskId}`;
      }
    },
    
    refreshPreview() {
      // 通过添加时间戳来强制刷新iframe
      this.previewUrl = `/api/preview/${this.taskId}?t=${new Date().getTime()}`;
    },
    
    resetPreview() {
      this.taskId = '';
      this.taskIdInput = '';
      this.previewUrl = '';
    }
  },
  props: {
    initialTaskId: {
      type: String,
      default: ''
    }
  },
  mounted() {
    if (this.initialTaskId) {
      this.taskId = this.initialTaskId;
      this.previewUrl = `/api/preview/${this.taskId}`;
    }
  }
};
</script>

<style scoped>
.preview-container {
  width: 100%;
  height: 500px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  overflow: hidden;
}

.preview-frame {
  width: 100%;
  height: 100%;
}
</style>