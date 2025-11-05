<template>
  <div class="dashboard">
    <h1 class="text-center mb-4">SCOT-Web 控制面板</h1>
    
    <div class="steps-container">
      <div class="step" :class="{ 'active': currentStep === 1 }">
        <div class="step-number">1</div>
        <div class="step-title">上传参考网页</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 2 }">
        <div class="step-number">2</div>
        <div class="step-title">生成PRD文档</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3 }">
        <div class="step-number">3</div>
        <div class="step-title">提取知识点</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 4 }">
        <div class="step-number">4</div>
        <div class="step-title">生成网页</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 5 }">
        <div class="step-number">5</div>
        <div class="step-title">预览结果</div>
      </div>
    </div>
    
    <div class="panels-container mt-4">
      <UploadPanel 
        v-if="currentStep === 1" 
        @upload-complete="onUploadComplete"
        @proceed-to-prd="proceedToPRD"
      />
      
      <PRDPanel 
        v-if="currentStep === 2" 
        ref="prdPanel"
        @prd-saved="onPRDSaved"
      />
      
      <KnowledgeGraph 
        v-if="currentStep === 3" 
        ref="knowledgeGraph"
        @knowledge-saved="onKnowledgeSaved"
      />
      
      <GeneratePanel 
        v-if="currentStep === 4" 
        ref="generatePanel"
        @website-generated="onWebsiteGenerated"
      />
      
      <PreviewPane 
        v-if="currentStep === 5" 
        :initial-task-id="generatedTaskId"
      />
    </div>
    
    <div class="navigation mt-4" v-if="currentStep > 1">
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
  </div>
</template>

<script>
import UploadPanel from './UploadPanel.vue';
import PRDPanel from './PRDPanel.vue';
import KnowledgeGraph from './KnowledgeGraph.vue';
import GeneratePanel from './GeneratePanel.vue';
import PreviewPane from './PreviewPane.vue';

export default {
  name: 'Dashboard',
  components: {
    UploadPanel,
    PRDPanel,
    KnowledgeGraph,
    GeneratePanel,
    PreviewPane
  },
  data() {
    return {
      currentStep: 1,
      referenceData: null,
      generatedTaskId: '',
      canProceed: false
    };
  },
  methods: {
    onUploadComplete(data) {
      this.referenceData = data;
      this.canProceed = true;
    },
    
    proceedToPRD(data) {
      this.referenceData = data;
      this.currentStep = 2;
      this.canProceed = false;
      
      // 将参考数据传递给PRD面板
      if (this.$refs.prdPanel) {
        // 这里可以设置PRD面板的初始数据
      }
    },
    
    onPRDSaved() {
      this.canProceed = true;
    },
    
    onKnowledgeSaved() {
      this.canProceed = true;
    },
    
    onWebsiteGenerated(data) {
      this.generatedTaskId = data.taskId;
      this.canProceed = true;
    },
    
    nextStep() {
      if (this.currentStep < 5) {
        this.currentStep++;
        this.canProceed = false;
      }
    },
    
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.canProceed = false;
      }
    }
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.steps-container {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.steps-container::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: var(--border-color);
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--light-color);
  border: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.step-title {
  font-size: 0.9rem;
  text-align: center;
  color: var(--secondary-color);
}

.step.active .step-number {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.step.active .step-title {
  color: var(--primary-color);
  font-weight: bold;
}

.panels-container {
  min-height: 400px;
}

.navigation {
  display: flex;
  justify-content: center;
}

.ml-2 {
  margin-left: 1rem;
}
</style>