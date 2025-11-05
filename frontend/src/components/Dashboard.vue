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
        <div class="step-title">生成PRD文档</div>
      </div>
      
      <div class="step" :class="{ 'active': currentStep === 3 }" @click="goToStep(3)">
        <div class="step-number">3</div>
        <div class="step-title">提取知识点</div>
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
      />
      
      <PRDPanel 
        v-if="currentStep === 2" 
        ref="prdPanel"
        :reference-data="referenceData"
        :prd-data="prdData"
        @prd-saved="onPRDSaved"
        @prd-generated="onPRDGenerated"
      />
      
      <KnowledgeGraph 
        v-if="currentStep === 3" 
        ref="knowledgeGraph"
        :reference-data="referenceData"
        :knowledge-data="knowledgeData"
        @knowledge-saved="onKnowledgeSaved"
        @knowledge-extracted="onKnowledgeExtracted"
      />
      
      <GeneratePanel 
        v-if="currentStep === 4" 
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
      uploadData: null,       // 上传的数据
      referenceData: null,    // 参考数据（用于PRD和知识点提取）
      prdData: null,          // PRD数据
      knowledgeData: null,    // 知识点数据
      generatedTaskId: '',    // 生成任务ID
      canProceed: false
    };
  },
  methods: {
    goToStep(step) {
      // 允许用户点击步骤标题导航到对应步骤
      if (step <= 5 && step >= 1) {
        this.currentStep = step;
        this.canProceed = false;
      }
    },
    
    onUploadComplete(data) {
      this.uploadData = data;
      this.referenceData = data;
      this.canProceed = true;
      console.log('上传完成，可以进行下一步');
    },
    
    proceedToPRD(data) {
      this.uploadData = data;
      this.referenceData = data;
      this.currentStep = 2;
      this.canProceed = false;
      console.log('进入PRD生成步骤');
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
  background-color: var(--border-color);
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  transition: all 0.3s ease;
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

.step:hover:not(.active) .step-number {
  background-color: #e9ecef;
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