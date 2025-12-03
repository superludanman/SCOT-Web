<template>
  <div class="card">
    <h2 class="card-title">学习知识点</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner"></div>
      <p>正在生成学习内容...</p>
    </div>
    
    <div v-else-if="learningContent">
      <div class="content-header">
        <h3>{{ learningContent.title }}</h3>
        <button @click="goBack" class="btn btn-secondary">返回知识点图谱</button>
      </div>
      
      <div class="levels-container">
        <div 
          v-for="level in learningContent.levels" 
          :key="level.level" 
          class="level-card"
        >
          <div class="level-header">
            <h4>Level {{ level.level }}</h4>
          </div>
          <div class="level-content">
            <p>{{ level.description }}</p>
          </div>
        </div>
      </div>
      
      <!-- 添加查看测试题按钮 -->
      <div class="test-task-button-container">
        <button @click="viewTestTask" class="btn btn-primary">查看测试题</button>
      </div>
    </div>
    
    <div v-else class="no-content">
      <p>请选择一个知识点开始学习</p>
    </div>
  </div>
</template>

<script>
import { learningAPI } from '../api/index.js';

export default {
  name: 'LearningContent',
  props: {
    knowledgeNode: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      learningContent: null,
      loading: false
    };
  },
  watch: {
    knowledgeNode: {
      handler(newVal) {
        if (newVal) {
          this.generateLearningContent(newVal);
        }
      },
      immediate: true
    }
  },
  methods: {
    async generateLearningContent(nodeData) {
      this.loading = true;
      this.learningContent = null;
      
      try {
        // 调用后端API生成学习内容
        const response = await learningAPI.generateKnowledgeContent(nodeData);
        this.learningContent = response;
      } catch (error) {
        console.error('生成学习内容失败:', error);
        alert('生成学习内容失败: ' + (error.message || '未知错误'));
      } finally {
        this.loading = false;
      }
    },
    
    goBack() {
      this.$emit('back-to-graph');
    },
    
    viewTestTask() {
      // 通知父组件跳转到测试题模块
      this.$emit('view-test-task', {
        knowledgeNode: this.knowledgeNode,
        learningContent: this.learningContent
      });
    }
  }
};
</script>

<style scoped>
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-header h3 {
  margin: 0;
}

.levels-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.level-card {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 20px;
  background-color: #f9f9f9;
}

.level-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.level-header h4 {
  margin: 0;
  color: var(--primary-color);
}

.level-content p {
  margin: 0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.no-content {
  text-align: center;
  padding: 40px;
  color: #666;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: var(--primary-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.test-task-button-container {
  margin-top: 20px;
  text-align: center;
}

.test-task-content {
  margin-top: 20px;
}

</style>