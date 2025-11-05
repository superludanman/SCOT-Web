<template>
  <div class="card">
    <h2 class="card-title">PRD文档生成</h2>
    
    <div v-if="!prdContent">
      <div v-if="referenceData">
        <div class="alert alert-info">
          <p><strong>参考信息:</strong></p>
          <p>标题: {{ referenceData.title }}</p>
          <p>文本块数量: {{ referenceData.text_blocks?.length || 0 }}</p>
        </div>
        
        <button 
          @click="generatePRDFromReference" 
          class="btn"
        >
          基于参考信息生成PRD文档
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
          @click="generatePRD" 
          :disabled="!referenceUrl && !uploadedFile" 
          class="btn"
        >
          生成PRD文档
        </button>
      </div>
      
      <div v-if="loading" class="mt-3 text-center">
        <div class="spinner"></div>
        <p class="mt-2">正在生成PRD文档...</p>
      </div>
    </div>
    
    <div v-else>
      <div class="alert alert-success">
        PRD文档生成成功！
      </div>
      
      <div class="form-group">
        <label for="prdTitle">PRD标题:</label>
        <input 
          type="text" 
          id="prdTitle" 
          v-model="prdTitle" 
          class="form-control" 
          placeholder="请输入PRD标题"
        />
      </div>
      
      <div class="form-group">
        <label>PRD内容:</label>
        <textarea 
          class="form-control" 
          rows="15" 
          v-model="prdContent"
          readonly
        ></textarea>
      </div>
      
      <div class="d-flex justify-content-between">
        <button @click="resetPRD" class="btn btn-secondary">重新生成</button>
        <button @click="savePRD" class="btn btn-success" :disabled="!prdTitle">保存PRD</button>
      </div>
    </div>
  </div>
</template>

<script>
import { prdAPI, uploadAPI } from '../api/index.js';

export default {
  name: 'PRDPanel',
  props: {
    referenceData: {
      type: Object,
      default: null
    },
    prdData: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      referenceUrl: '',
      uploadedFile: null,
      prdContent: '',
      prdTitle: '',
      loading: false
    };
  },
  watch: {
    prdData: {
      handler(newVal) {
        if (newVal) {
          this.prdContent = newVal.content;
          this.prdTitle = newVal.title;
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
    
    async generatePRDFromReference() {
      this.loading = true;
      
      try {
        // 基于参考数据生成PRD
        const response = await prdAPI.generatePRD({
          reference_info: this.referenceData
        });
        
        this.prdContent = response.prd_text;
        this.prdTitle = `PRD: ${this.referenceData.title}`;
        
        // 通知父组件PRD已生成
        this.$emit('prd-generated', {
          content: response.prd_text,
          title: `PRD: ${this.referenceData.title}`
        });
      } catch (error) {
        console.error('PRD生成失败:', error);
        alert('PRD生成失败: ' + (error.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    
    async generatePRD() {
      this.loading = true;
      
      try {
        let prdData;
        
        if (this.uploadedFile) {
          // 通过上传文件生成PRD
          const formData = new FormData();
          formData.append('file', this.uploadedFile);
          const response = await uploadAPI.generatePRDFromFile(formData);
          prdData = response.prd_text;
        } else if (this.referenceUrl) {
          // 通过URL生成PRD
          const requestData = { reference_url: this.referenceUrl };
          const response = await prdAPI.generatePRD(requestData);
          prdData = response.prd_text;
        } else {
          throw new Error('请选择一个文件或输入一个URL');
        }
        
        this.prdContent = prdData;
        this.prdTitle = this.referenceUrl ? `PRD: ${new URL(this.referenceUrl).hostname}` : `PRD: ${this.uploadedFile.name}`;
        
        // 通知父组件PRD已生成
        this.$emit('prd-generated', {
          content: prdData,
          title: this.prdTitle
        });
      } catch (error) {
        console.error('PRD生成失败:', error);
        if (error.message) {
          alert('PRD生成失败: ' + error.message);
        } else {
          alert('PRD生成失败: ' + JSON.stringify(error));
        }
      } finally {
        this.loading = false;
      }
    },
    
    async savePRD() {
      if (!this.prdTitle || !this.prdContent) {
        alert('请填写PRD标题和内容');
        return;
      }
      
      try {
        const requestData = {
          title: this.prdTitle,
          content: this.prdContent
        };
        
        await prdAPI.savePRD(requestData);
        alert('PRD保存成功！');
        this.$emit('prd-saved');
      } catch (error) {
        console.error('PRD保存失败:', error);
        alert('PRD保存失败: ' + (error.message || '未知错误'));
      }
    },
    
    resetPRD() {
      this.referenceUrl = '';
      this.uploadedFile = null;
      this.prdContent = '';
      this.prdTitle = '';
      const fileInput = document.getElementById('uploadedFile');
      if (fileInput) {
        fileInput.value = ''; // 清空文件输入
      }
    }
  }
};
</script>

<style scoped>
/* 组件特定样式 */
textarea {
  font-family: monospace;
  font-size: 14px;
}
</style>