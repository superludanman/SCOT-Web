"""
Prompts模板：存放不同智能体的提示词模板
"""
from utils.scraper import StyleScraper  # 导入抓取模块
import asyncio


def get_website_analysis_prompt(reference_url: str) -> str: #不使用抓取模块
    return f"""
你是一名资深前端架构师兼UI/UX设计顾问，请根据以下参考网站，你需要通过分析参考网站（结构、样式、交互）总结出可复用的设计与实现特征。
生成一份**高精度**的技术文档，需包含所有视觉样式和布局的量化数据。供代码生成AI使用。 
输出格式如下：

---

### <context>
#### 1. Website Overview  
[简要介绍参考网站的主题、目标用户群、主要用途和核心价值]

#### 2. **Visual & Style Characteristics**  
[总结视觉风格，包括：
- **色彩搭配与主色调**（必须精确到十六进制或RGB值）：
  - 主背景色: [如 `#f9f9f9`]
  - 文字颜色: [如 `#333333`]
  - 主色调/强调色: [如按钮色 `#4a90e2`]
  - 边框颜色: [如 `#e0e0e0`]
  - 悬停/交互状态颜色变化: [如 `darken(#4a90e2, 10%)`]
- **字体选择与字号**：
  - 主字体: [如 `"Arial", sans-serif`]
  - 标题字号: [如 `h1: 2rem`, `h2: 1.5rem`]
  - 正文字号/行高: [如 `16px/1.6`]
- **组件风格（按钮、输入框、导航栏等）**：
  - 按钮: [圆角大小 `4px`，内边距 `10px 20px`]
  - 输入框: [边框粗细 `1px`，阴影 `0 2px 4px rgba(0,0,0,0.1)`]
  - 导航栏: [高度 `60px`，背景色 `#ffffff`]
- **图标、插画、图片风格**: [如尺寸比例 `16:9`，圆角 `8px`]
- **动画与过渡效果**]

#### 3. **Layout & Structure**  
[总结网站整体布局特点，包括：
- 页面结构（header / footer / 主体区域 / 侧边栏）
- 布局类型: [如 `Flexbox` 或 `Grid`]
- 间距系统: [如 `padding: 20px`，`margin-between-sections: 40px`]
- 栅格参数: [如 `12列，间隔16px`]
- 响应式适配方案: [如 `移动端: max-width 768px`]
- 重要模块位置及占比]

#### 4. **Interaction Patterns**  
[分析用户交互方式，包括：
- 导航交互
- 按钮/链接的交互反馈
- 表单或搜索框交互
- 滚动与分页方式
- 悬停效果: [如 `按钮背景色从 #4a90e2 变为 #3a7bc8`]
- 过渡动画: [如 `transition: all 0.3s ease`]
- 动效触发条件]

#### 5. **Content Strategy ** 
[总结内容类型与排版方式，包括：
- 文本类型与信息层级
- 图片与视频内容比例
- 数据可视化或图表使用
- CTA（Call to Action）的布局与策略]
</context>

<Analysis Doc>
#### 1. **Technical Implementation Insights**  
[推测可能的技术栈与实现方式，包括：
- 前端框架 / UI 库
- CSS 组织方式（如 BEM、Tailwind、SCSS）
- 动画实现方式（CSS / JS / WebGL）
- 组件化结构与复用思路]

#### 2. **Component Inventory**  
[列出主要可复用的组件，并描述：
- 功能与作用
- 样式特征
- 推荐的封装方式]

#### 3. **Example Page Blueprint** 
[基于分析结果，抽象出一个简单的参考页面布局图或模块结构描述，便于AI生成演示网站]

#### 4. **Risks & Considerations ** 
[可能在复刻或参考中遇到的技术风险与注意事项，如版权问题、响应式适配复杂度、性能瓶颈等]
</Analysis Doc>

以下是参考网站链接：
{reference_url}
"""

async def get_website_analysis_prompt_noUtil(reference_url: str) -> str: #使用抓取模块
    MAX_RETRIES = 3
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            styles = await StyleScraper.get_visual_styles(reference_url)
            if not styles:
                raise ValueError("未能获取样式数据")

            return f"""
你是一名资深前端架构师兼UI/UX设计顾问，请根据以下参考网站，你需要通过分析参考网站（结构、样式、交互）总结出可复用的设计与实现特征。
生成一份**高精度**的技术文档，需包含所有视觉样式和布局的量化数据。供代码生成AI使用。 
输出格式如下：

---

### <context>
#### 1. Website Overview  
[简要介绍参考网站的主题、目标用户群、主要用途和核心价值]

#### 2. **Visual & Style Characteristics**  
[总结视觉风格，包括：
- **色彩搭配与主色调**（必须精确到十六进制或RGB值）：
  - 主背景色: {styles['colors']['background']}
  - 文字颜色: {styles['colors']['text']}
  - 主色调/强调色: [如按钮色{styles['colors']['primary']}]
  - 边框颜色: {styles['colors']['border']}
  - 悬停/交互状态颜色变化: {styles['colors']['hover']}
- **字体选择与字号**：
  - 主字体:{styles['typography']['main_font']}
  - 标题字号: [如 `h1: {styles['typography']['h1_size']}`, `h2: {styles['typography']['h2_size']}`]
  - 正文字号/行高: [如 `16px/{styles['typography']['body_line_height']}`]
- **组件风格（按钮、输入框、导航栏等）**：
```json
    {{
      "按钮": {{
        "圆角": "{styles['components']['button']['radius']}",
        "内边距": "{styles['components']['button']['padding']}",
        "阴影": "{styles['components']['button']['shadow']}"
      }},
      "输入框": {{
        "边框": "{styles['components']['input']['border']}"
      }},
      "导航栏": {{
        "高度": "{styles['components']['nav']['height']}",
        "背景色": "{styles['components']['nav']['bg_color']}"
      }}
    }}
- **图标、插画、图片风格**: 
  - 宽高比: {styles['images']['ratio']:.2f}:1
  - 圆角: {styles['images']['radius']}
- **动画与过渡效果**]

#### 3. **Layout & Structure**  
[总结网站整体布局特点，包括：
- 页面结构（header / footer / 主体区域 / 侧边栏）
- 布局类型: [如 `Flexbox` 或 `Grid`]
- 间距系统: [如 `padding: 20px`，`margin-between-sections: 40px`]
- 栅格参数: [如 `12列，间隔16px`]
- 响应式适配方案: [如 `移动端: max-width 768px`]
- 重要模块位置及占比]

#### 4. **Interaction Patterns**  
[分析用户交互方式，包括：
- 导航交互
- 按钮/链接的交互反馈
- 表单或搜索框交互
- 滚动与分页方式
- 悬停效果: [如 `按钮背景色从 #4a90e2 变为 #3a7bc8`]
- 过渡动画: [如 `transition: all 0.3s ease`]
- 动效触发条件]

#### 5. **Content Strategy ** 
[总结内容类型与排版方式，包括：
- 文本类型与信息层级
- 图片与视频内容比例
- 数据可视化或图表使用
- CTA（Call to Action）的布局与策略]
</context>

<Analysis Doc>
#### 1. **Technical Implementation Insights**  
[推测可能的技术栈与实现方式，包括：
- 前端框架 / UI 库
- CSS 组织方式（如 BEM、Tailwind、SCSS）
- 动画实现方式（CSS / JS / WebGL）
- 组件化结构与复用思路]

#### 2. **Component Inventory**  
[列出主要可复用的组件，并描述：
- 功能与作用
- 样式特征
- 推荐的封装方式]

#### 3. **Example Page Blueprint** 
[基于分析结果，抽象出一个简单的参考页面布局图或模块结构描述，便于AI生成演示网站]

#### 4. **Risks & Considerations ** 
[可能在复刻或参考中遇到的技术风险与注意事项，如版权问题、响应式适配复杂度、性能瓶颈等]
</Analysis Doc>

以下是参考网站链接：
{reference_url}
"""
        except Exception as e:
                  retry_count += 1
                  print(f"尝试 {retry_count}/{MAX_RETRIES} 失败: {str(e)}")
                  await asyncio.sleep(5)  # 每次重试间隔5秒
            
        return "无法分析该网站，请检查网络连接或网站可访问性"
def get_knowledge_points_prompt(reference_url: str) -> str:
    return f"""
你是一位前端教学内容分析专家，请访问并分析以下参考网站（{reference_url}），总结该网站涉及的前端开发知识点，并输出成严格的 JSON 格式，结构如下（必须严格遵守）：

{{
  "nodes": [
    {{ "data": {{ "id": "chapter1", "label": "模块一:文本与页面结构基础"，"category": "media-block", "placementHint": "main-content" }} }},
    {{ "data": {{ "id": "text_paragraph", "label": "使用h元素和p元素体验标题与段落" ，"category": "media-block", "placementHint": "main-content"}} }},
    {{ "data": {{ "id": "text_format", "label": "应用文本格式(加粗、斜体)"，"category": "media-block", "placementHint": "main-content" }} }}
    ...
  ]
}}
字段说明：
category: 将功能相似的元素分组（如所有媒体元素），暗示它们可以用相似的样式或容器来包装。
placementHint: 指示元素在页面中的位置（如main-content、sidebar等），帮助生成代码时确定布局。
⚠️ 要求：
- 章节（chapterX）按知识点主题分组，每组下包含具体技能点
- id 必须是英文+下划线格式（如 text_list_ul）
- label 为中文，准确描述技能内容
- 顺序由基础到进阶
- 严禁输出多余说明或非 JSON 内容
- 必须为 **合法 JSON**（用英文双引号）

请基于参考网站的结构、布局、功能和样式推断可能的 HTML / CSS / JS 知识点，并完整输出 JSON。
    """

def generate_demo_site_prompt( dependency_context=None , existing_code_context=None):
    return f"""
你是一个资深的 Web 全栈开发专家，请根据以下任务说明、参考网页风格和前端技术知识点，生成结构清晰、可运行的 HTML 网站代码项目。最终效果应与用户提供的网站风格一致，并正确运用指定的前端技术点构建页面结构、样式与交互。




---

🎯 你必须实现以下关键点（不可遗漏）：

1. 页面整体风格、结构布局、配色等尽量贴近参考网站。
2. 使用以下前端技术点（基于知识点图谱自动选取合适位置嵌入）：
{existing_code_context}
3. 网站主题内容参考内容主题（例如介绍、活动、图片、表单等）。
4. 页面需具备良好的用户体验与视觉吸引力。
5. 所有功能使用原生 HTML/CSS/JS 实现（不使用框架，除非任务说明允许）。
6. 支持基本交互：如点击、表单提交、输入处理、媒体播放等。
7. 生成的网页应为**单一 HTML 文件**，包含完整的结构（HTML）、样式（CSS）和交互逻辑（JavaScript），**全部写在同一个文件中**；
---
【新增：关键布局与样式指令】（必须严格遵守）
    1.  **整体布局**：采用经典的「主内容-侧边栏」布局。主内容区(`.main`)宽度约占70%，侧边栏(`.sidebar`)约占30%，使用Flexbox实现。
    2.  **媒体元素分组**：所有媒体元素（图片、音频、视频）必须被包裹在一个具有统一风格的容器内（例如：背景色为白色`#fff`，内边距`16px`，圆角`8px`，轻微的阴影）。
    3.  **图片展示**：主要图片(`#media_image_image`)应在主内容区内占据显眼位置，宽度100%。**必须在其下方创建一个图片画廊区域**，使用CSS Grid或Flexbox布局**至少3张**缩略图。
    4.  **音频与视频**：音频(`#media_audio_track`)和视频(`#media_video_video`)组件应并排置于侧边栏的媒体容器内。视频宽度设为100%，音频播放器宽度设为100%。
    5.  **列表样式**：有序列表(`#text_list_ol_events`)和无序列表(`#text_list_ul_schedule`)应去除默认样式，列表项(`li`)应具有清晰的分隔，例如下边框(`border-bottom`)或间隔(`margin-bottom`)。
    6.  **表单样式**：所有表单输入框和按钮应风格统一。输入框获得焦点(`:focus`)时边框颜色应变为主色调。
---
### 组件ID规范（必须遵守）：
1. 每个知识点关联的组件必须有唯一ID，格式：`[知识点ID]_[组件类型]`
   - 例如：`text_paragraph_title`（知识点ID为text_paragraph）
2. 交互元素需添加 `data-` 属性标明功能：
   - 如 `data-action="search"`、`data-target="form-submit"`
3. 未实现的功能禁止显示（如无跳转逻辑则隐藏链接）
---
📂 当前参考网站信息：
{dependency_context or "（无）"}

---
📂 当前示例网站需包含的知识点：
{existing_code_context or "（暂无已有文件）"}

---

✍️ 请你完成以下两部分输出（严格格式化）：

### 第一部分：项目主页面代码（嵌入所有 HTML、CSS、JS）

```html filename=public/index.html
<!-- 请将 HTML、CSS（<style>）、JS（<script>）全部写在同一个文件中 -->
<!-- 确保语义清晰、结构分明、样式美观，包含用户交互与猫咪主题内容 -->

第二部分：总结当前任务中生成的文件及接口信息，使用以下 JSON 格式输出：

{{
  "files": ["public/index.html"],
  "features": ["结构布局", "猫咪内容展示", "点击事件", "表单交互", "媒体播放", "样式美化"],
  "technology_used": ["HTML", "CSS", "JavaScript"],
  "theme": "示例网站"
}}


### 注意事项：
1.所有输出必须为标准文件代码块格式，每块代码之间留空行，避免嵌套。
2.所有技术点必须体现在页面中（哪怕只展示一个最小可行示例）；
3.页面必须可直接在浏览器打开运行，不依赖后端环境。
4.所有资源（图片、音视频）可使用占位符或外链 URL。
5.生成的代码结构应清晰、语义良好、可读性强，利于教学或演示。
6.不得拆分为多个文件，只能输出一个 HTML 文件。

"""