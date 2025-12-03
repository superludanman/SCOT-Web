<template>
  <div class="dashboard card">
    <h1 class="text-center mb-4">SCOT-Web 控制面板</h1>
    
    <div class="steps-container">
      <div class="step" :class="{ 'active': currentStep === 1 }" @click="goToStep(1)">
        <div class="step-number">1</div>
        <div class="step-title">上传参考网页</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 2 }" @click="goToStep(2)">
        <div class="step-number">2</div>
        <div class="step-title">生成设计文档</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3 }" @click="goToStep(3)">
        <div class="step-number">3</div>
        <div class="step-title">生成学习路径</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3.5 }" @click="goToStep(3.5)" v-if="showLearningStep">
        <div class="step-number">-</div>
        <div class="step-title">渐进式知识展示</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3.7 }" @click="goToStep(3.7)" v-if="showTestTaskStep">
        <div class="step-number">-</div>
        <div class="step-title">生成实践案例</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 4 }" @click="goToStep(4)">
        <div class="step-number">4</div>
        <div class="step-title">生成网页</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 5 }" @click="goToStep(5)">
        <div class="step-number">5</div>
        <div class="step-title">预览结果</div>
      </div>
    </div>
    
    <div class="panels-container mt-4">
      <UploadPanel 
        v-if="currentStep === 1" 
        :initial-data="uploadData"
        @upload-complete="onUploadComplete"
        @proceed-to-prd="proceedToPRD"
        @proceed-to-knowledge="proceedToKnowledge"
        @upload-cleared="onUploadCleared"
      />
      
      <PRDPanel 
        v-if="currentStep === 2" 
        ref="prdPanel"
        :reference-data="referenceData"
        :upload-type="uploadType"
        :prd-data="prdData"
        @prd-saved="onPRDSaved"
        @prd-generated="onPRDGenerated"
      />
      
      <KnowledgeGraph 
        v-if="currentStep === 3" 
        ref="knowledgeGraph"
        :reference-data="referenceData"
        :upload-type="uploadType"
        :knowledge-data="knowledgeData"
        @knowledge-saved="onKnowledgeSaved"
        @knowledge-extracted="onKnowledgeExtracted"
        @learn-knowledge="onLearnKnowledge"
      />
      
      <LearningContent
        v-else-if="currentStep === 3.5"
        :knowledge-node="learningNode"
        @back-to-graph="backToKnowledgeGraph"
        @view-test-task="onViewTestTask"
      />
      
      <TestTaskDisplay
        v-else-if="currentStep === 3.7"
        :test-task="testTask"
        :loading="testTaskLoading"
        @back-to-learning="backToLearningContent"
      />
      
      <GeneratePanel 
        v-else-if="currentStep === 4" 
        ref="generatePanel"
        :prd-data="prdData"
        :knowledge-data="knowledgeData"
        @website-generated="onWebsiteGenerated"
      />
      
      <PreviewPane 
        v-if="currentStep === 5" 
        :initial-task-id="generatedTaskId"
      />
    </div>
    
    <div class="navigation mt-4" v-if="currentStep > 1 && currentStep !== 3.5 && currentStep !== 3.7">
      <button @click="prevStep" class="btn btn-secondary">上一步</button>
      <button 
        v-if="currentStep < 5" 
        @click="nextStep" 
        class="btn btn-primary ml-2"
        :disabled="!canProceed"
      >
        下一步
      </button>
    </div>
    
    <div class="navigation mt-4" v-else-if="currentStep === 3.5">
      <button @click="backToKnowledgeGraph" class="btn btn-secondary">返回知识点图谱</button>
    </div>
    
    <div class="navigation mt-4" v-else-if="currentStep === 3.7">
      <button @click="backToLearningContent" class="btn btn-secondary">返回学习内容</button>
    </div>
  </div>
</template>

<script>
import UploadPanel from './UploadPanel.vue';
import PRDPanel from './PRDPanel.vue';
import KnowledgeGraph from './KnowledgeGraph.vue';
import LearningContent from './LearningContent.vue';
import TestTaskDisplay from './TestTaskDisplay.vue';
import GeneratePanel from './GeneratePanel.vue';
import PreviewPane from './PreviewPane.vue';
import { testGenerationAPI } from '../api/index.js';

export default {
  name: 'Dashboard',
  components: {
    UploadPanel,
    PRDPanel,
    KnowledgeGraph,
    LearningContent,
    TestTaskDisplay,
    GeneratePanel,
    PreviewPane
  },
  data() {
    return {
      currentStep: 1,
      uploadData: null,       // 上传的数据
      referenceData: null,    // 参考数据（用于PRD和知识点提取）
      prdData: null,          // PRD数据
      knowledgeData: null,    // 知识点数据
      generatedTaskId: '',    // 生成任务ID
      canProceed: false,
      showLearningStep: false, // 是否显示学习步骤
      showTestTaskStep: false, // 是否显示测试题步骤
      learningNode: null,     // 当前学习的知识点节点
      testTask: null,         // 当前测试题
      testTaskLoading: false  // 测试题加载状态
    };
  },
  methods: {
    goToStep(step) {
      // 允许用户点击步骤标题导航到对应步骤
      if ((step <= 5 && step >= 1) || step === 3.5 || step === 3.7) {
        this.currentStep = step;
        this.canProceed = false;
      }
    },
    
    onUploadComplete(data) {
      this.uploadData = data.data;
      this.referenceData = data.data;
      this.uploadType = data.type;
      this.canProceed = true;
      console.log('上传完成，可以进行下一步');
    },
    
    proceedToPRD(data) {
      this.uploadData = data.data;
      this.referenceData = data.data;
      this.currentStep = 2;
      this.canProceed = false;
      console.log('进入PRD生成步骤');
    },

    proceedToKnowledge(data) {
      this.uploadData = data.data;
      this.referenceData = data.data;
      this.currentStep = 3;
      this.canProceed = false;
      console.log('进入知识点提取步骤');
    },
    
    onPRDGenerated(data) {
      this.prdData = data;
      console.log('PRD已生成');
    },
    
    onPRDSaved() {
      this.canProceed = true;
      console.log('PRD已保存，可以进行下一步');
    },
    
    onKnowledgeExtracted(data) {
      this.knowledgeData = data;
      console.log('知识点已提取');
    },
    
    onKnowledgeSaved() {
      this.canProceed = true;
      console.log('知识点已保存，可以进行下一步');
    },
    
    onLearnKnowledge(nodeData) {
      this.learningNode = nodeData;
      this.showLearningStep = true;
      this.currentStep = 3.5; // 跳转到学习知识点模块
      console.log('进入学习知识点模块');
    },
    
    onViewTestTask(data) {
      // 生成测试题并跳转到测试题显示模块
      this.showTestTaskStep = true;
      this.currentStep = 3.7;
      this.testTask = null;
      this.testTaskLoading = true;
      
      // 调用后端API生成测试题
      this.generateTestTask(data);
    },
    
    async generateTestTask(data) {
      try {
        const requestData = {
          topic_id: data.knowledgeNode.id,
          knowledge_node: data.knowledgeNode,
          learning_content: data.learningContent
        };
        
        const response = await testGenerationAPI.generateTestTask(requestData);
        this.testTask = response;
      } catch (error) {
        console.error('生成测试题失败:', error);
        alert('生成测试题失败: ' + (error.message || '未知错误'));
      } finally {
        this.testTaskLoading = false;
      }
    },
    
    backToKnowledgeGraph() {
      this.currentStep = 3;
      this.learningNode = null;
      this.showLearningStep = false;
      console.log('返回知识点图谱');
    },
    
    backToLearningContent() {
      this.currentStep = 3.5;
      this.testTask = null;
      this.showTestTaskStep = false;
      console.log('返回学习内容');
    },
    
    onWebsiteGenerated(data) {
      this.generatedTaskId = data.taskId;
      this.canProceed = true;
      console.log('网页生成完成，可以进行下一步');
    },
    
    nextStep() {
      if (this.currentStep < 5) {
        this.currentStep++;
        this.canProceed = false;
        console.log('进入步骤:', this.currentStep);
      }
    },
    
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.canProceed = false;
        console.log('返回步骤:', this.currentStep);
      }
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-top: 20px;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  position: relative;
  cursor: pointer;
}

.steps-container::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e0e0e0;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  flex: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #e0e0e0;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-bottom: 5px;
}

.step-title {
  font-size: 14px;
  color: #666;
  text-align: center;
}

.step.active .step-number {
  background-color: #4a90e2;
  color: white;
}

.step.active .step-title {
  color: #4a90e2;
  font-weight: bold;
}

.panels-container {
  min-height: 400px;
}

.navigation {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.ml-2 {
  margin-left: 0.5rem;
}
</style>