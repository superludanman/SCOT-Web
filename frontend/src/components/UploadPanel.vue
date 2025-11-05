<template>
  <div class="upload-panel">
    <h2>上传参考网页</h2>
    <div class="upload-area">
      <div class="upload-box" @dragover.prevent @drop.prevent="handleDrop">
        <div class="upload-content" @click="triggerFileInput">
          <i class="upload-icon">📁</i>
          <p>拖拽HTML文件到此处或点击选择文件</p>
          <p class="hint">支持 .html, .htm 格式</p>
          <input 
            type="file" 
            ref="fileInput" 
            accept=".html,.htm" 
            @change="handleFileSelect" 
            style="display: none;"
          />
        </div>
      </div>
      
      <div class="url-input">
        <label for="url">或输入网页链接:</label>
        <div class="input-group">
          <input 
            type="url" 
            id="url" 
            v-model="url" 
            placeholder="https://example.com" 
          />
          <button @click="handleUrlSubmit" :disabled="!url">解析</button>
        </div>
      </div>
    </div>
    
    <div v-if="uploadResult" class="result">
      <h3>解析结果</h3>
      <div class="result-content">
        <p><strong>页面标题:</strong> {{ uploadResult.title }}</p>
        <p><strong>文本块数量:</strong> {{ uploadResult.text_blocks?.length || 0 }}</p>
        <div class="actions">
          <button @click="proceedToPRD">生成PRD文档</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadAPI } from '../api/index.js';

export default {
  name: 'UploadPanel',
  props: {
    initialData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      url: '',
      uploadResult: null
    };
  },
  watch: {
    initialData: {
      handler(newVal) {
        if (newVal) {
          this.uploadResult = newVal;
        }
      },
      immediate: true
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    
    handleDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.processFile(files[0]);
      }
    },
    
    handleFileSelect(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.processFile(files[0]);
      }
    },
    
    async processFile(file) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const result = await uploadAPI.uploadHTML(formData);
        this.uploadResult = result;
        this.$emit('upload-complete', result);
      } catch (error) {
        console.error('文件上传失败:', error);
        if (error.response && error.response.status === 422) {
          alert('文件上传失败: 请求参数错误，请检查文件格式');
        } else {
          alert('文件上传失败: ' + (error.message || '未知错误'));
        }
      }
    },
    
    async handleUrlSubmit() {
      try {
        const formData = new FormData();
        formData.append('url', this.url);
        
        const result = await uploadAPI.uploadHTML(formData);
        this.uploadResult = result;
        this.$emit('upload-complete', result);
      } catch (error) {
        console.error('URL解析失败:', error);
        if (error.response && error.response.status === 422) {
          alert('URL解析失败: 请求参数错误');
        } else {
          alert('URL解析失败: ' + (error.message || '未知错误'));
        }
      }
    },
    
    proceedToPRD() {
      if (this.uploadResult) {
        this.$emit('proceed-to-prd', this.uploadResult);
      }
    }
  }
};
</script>

<style scoped>
.upload-panel {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.upload-area {
  margin-bottom: 20px;
}

.upload-box {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-box:hover {
  border-color: #4a90e2;
}

.upload-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 10px;
}

.hint {
  color: #666;
  font-size: 14px;
}

.url-input {
  margin-top: 20px;
}

.url-input label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
}

.input-group {
  display: flex;
  gap: 10px;
}

.input-group input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.input-group button {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.input-group button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.result-content {
  margin-top: 10px;
}

.actions {
  margin-top: 20px;
}

.actions button {
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>