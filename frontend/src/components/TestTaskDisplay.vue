<template>
  <div class="card">
    <h2 class="card-title">测试题</h2>
    
    <div v-if="loading" class="text-center">
      <div class="spinner"></div>
      <p>正在生成测试题...</p>
    </div>
    
    <div v-else-if="testTask" class="test-task-content">
      <div class="content-header">
        <h3>{{ testTask.title }}</h3>
        <button @click="goBack" class="btn btn-secondary">返回学习内容</button>
      </div>
      
      <div class="task-description">
        <h4>任务描述</h4>
        <div v-html="renderMarkdown(testTask.description_md)" class="markdown-content"></div>
      </div>
      
      <div class="task-start-code">
        <h4>起始代码</h4>
        <div class="code-block">
          <pre><code class="language-html">{{ testTask.start_code.html }}</code></pre>
          <pre><code class="language-css">{{ testTask.start_code.css }}</code></pre>
          <pre><code class="language-javascript">{{ testTask.start_code.js }}</code></pre>
        </div>
      </div>
      
      <div class="task-checkpoints">
        <h4>检查点</h4>
        <ul>
          <li v-for="(checkpoint, index) in testTask.checkpoints" :key="index">
            {{ checkpoint.name }}: {{ checkpoint.feedback }}
          </li>
        </ul>
      </div>
      
      <div class="task-answer">
        <h4>参考答案</h4>
        <div class="code-block">
          <pre><code class="language-html">{{ testTask.answer.html }}</code></pre>
          <pre><code class="language-css">{{ testTask.answer.css }}</code></pre>
          <pre><code class="language-javascript">{{ testTask.answer.js }}</code></pre>
        </div>
      </div>
    </div>
    
    <div v-else class="no-content">
      <p>暂无测试题内容</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestTaskDisplay',
  props: {
    testTask: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goBack() {
      this.$emit('back-to-learning');
    },
    
    renderMarkdown(mdText) {
      // 简单的markdown渲染实现
      if (!mdText) return '';
      
      // 替换标题
      let html = mdText.replace(/^# (.*$)/gm, '<h1>$1</h1>');
      html = html.replace(/^## (.*$)/gm, '<h2>$1</h2>');
      html = html.replace(/^### (.*$)/gm, '<h3>$1</h3>');
      
      // 替换列表
      html = html.replace(/^\- (.*$)/gm, '<li>$1</li>');
      html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
      
      // 替换段落
      html = html.replace(/\n\n([^<])/g, '</p><p>$1');
      html = '<p>' + html + '</p>';
      
      return html;
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

.test-task-content {
  margin-top: 20px;
}

.task-description,
.task-start-code,
.task-checkpoints,
.task-answer {
  margin-bottom: 30px;
}

.task-description h4,
.task-start-code h4,
.task-checkpoints h4,
.task-answer h4 {
  color: var(--primary-color);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 5px;
  margin-top: 0;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 1em;
  margin-bottom: 0.5em;
}

.markdown-content ul {
  padding-left: 20px;
}

.markdown-content li {
  margin-bottom: 5px;
}

.markdown-content p {
  line-height: 1.6;
  margin: 0 0 1em 0;
}

.code-block {
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.code-block pre {
  margin: 0;
  padding: 15px;
  overflow-x: auto;
}

.code-block pre code {
  font-family: 'Courier New', monospace;
  font-size: 14px;
}

.task-checkpoints ul {
  padding-left: 20px;
}

.task-checkpoints li {
  margin-bottom: 5px;
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
</style>