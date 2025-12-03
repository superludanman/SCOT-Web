"""
Prompts模板：存放不同智能体的提示词模板
"""
import asyncio

def get_slow_mind_prompt_from_html(html_content: str, user_goal: str = ""):
    return f"""
你是一名资深前端架构师兼UI/UX设计顾问，请将用户上传的静态网页访问作为参考网站进行分析（结构、样式、交互）总结出可复用的设计与实现特征。
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
</Analysis Doc>文档。

🧱 用户上传的网页内容如下（HTML 原文）：
<webpage>
{html_content[:8000]}  # 控制长度，防止超长
</webpage>

🎯 用户的需求或目标说明（如果有）：
{user_goal or "（用户未补充）"}

"""

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

def get_knowledge_points_prompt_from_html(html_content: str, user_goal: str = "") -> str:
    return f"""
你是一位前端教学内容分析专家，请将用户上传的静态网页访问作为参考网站进行分析，总结该网站涉及的前端开发知识点，并输出成严格的 JSON 格式，结构如下（必须严格遵守）：
从中提炼出“模块（章节）”与“知识点（技能）”，  
并输出**严格符合以下 JSON 模板结构的知识图谱**。

输出 JSON 结构要求如下（必须严格遵守）：

{{
  "nodes": [
    {{ "data": {{ "id": "1_end", "label": "模块一: 文本与页面结构基础", "type": "chapter" }} }},
    {{ "data": {{ "id": "1_1", "label": "使用 h 元素和 p 元素体验标题与段落", "type": "knowledge","select_element": ["h1", "h2", "h3", "h4", "h5", "h6", "p"] }} }},
    {{ "data": {{ "id": "1_2", "label": "应用文本格式 (加粗、斜体)", "type": "knowledge","select_element": ["b", "i", "strong", "em", "u", "s", "mark", "small", "del", "ins", "sub", "sup"] }} }},
    ...
  ],
  "edges": [
    {{ "data": {{ "source": "1_end", "target": "2_end" }} }},
    {{ "data": {{ "source": "1_end", "target": "1_1" }} }}
    ...
  ],
  "dependent_edges": [
    {{ "data": {{ "source": "1_end", "target": "2_end" }} }},
    {{ "data": {{ "source": "1_end", "target": "1_1" }} }},
    {{ "data": {{ "source": "1_1", "target": "1_2" }} }}
    {{ "data": {{ "source": "2_end", "target": "2_1" }} }},
    ...
  ]
}}

字段定义说明：
- **nodes**：包含所有章节与知识点节点；
  - `id`：章节编号或知识点编号，如 “1_end”、“2_1”；
  - `label`：中文标题，清晰表达模块或技能名称；
  - `type`：章节节点用 `"chapter"`，知识点节点用 `"knowledge"`；
  - `select_element`：知识点相关的HTML 元素，如 `"h1"`、`"p"`、`"a"`。
- **edges**：表示章节之间、章节与其下知识点之间的层级关系；
- **dependent_edges**：表示知识点之间的逻辑依赖或学习顺序。

⚙️ 要求：
1. 所有章节应按知识主题分组，如“文本与结构”“样式与布局”“交互与脚本”等；
2. 每个章节下需包含 3~5 个具体知识点；
3. 知识点应从基础到进阶排列；
4. 输出结果必须是 **合法 JSON（仅英文双引号）**；
5. 严禁输出解释说明、注释或额外文本。

请基于参考网站的结构、布局、功能和样式推断可能的 HTML / CSS / JS 知识点，并完整输出 JSON。

🧱 用户上传的网页内容如下（HTML 原文）：
<webpage>
{html_content[:8000]}  # 控制长度，防止超长
</webpage>

🎯 用户的需求或目标说明（如果有）：
{user_goal or "（用户未补充）"}
    """

def get_knowledge_points_prompt(reference_url: str) -> str:
    return f"""
你是一位专业的前端教学知识图谱构建专家。  
请分析以下网站的内容、结构、样式和交互功能（{reference_url}），  
从中提炼出“模块（章节）”与“知识点（技能）”，  
并输出**严格符合以下 JSON 模板结构的知识图谱**。

输出 JSON 结构要求如下（必须严格遵守）：

{{
  "nodes": [
    {{ "data": {{ "id": "1_end", "label": "模块一: 文本与页面结构基础", "type": "chapter" }} }},
    {{ "data": {{ "id": "1_1", "label": "使用 h 元素和 p 元素体验标题与段落", "type": "knowledge","select_element": ["h1", "h2", "h3", "h4", "h5", "h6", "p"] }} }},
    {{ "data": {{ "id": "1_2", "label": "应用文本格式 (加粗、斜体)", "type": "knowledge","select_element": ["b", "i", "strong", "em", "u", "s", "mark", "small", "del", "ins", "sub", "sup"] }} }},
    ...
  ],
  "edges": [
    {{ "data": {{ "source": "1_end", "target": "2_end" }} }},
    {{ "data": {{ "source": "1_end", "target": "1_1" }} }}
    ...
  ],
  "dependent_edges": [
    {{ "data": {{ "source": "1_end", "target": "2_end" }} }},
    {{ "data": {{ "source": "1_end", "target": "1_1" }} }},
    {{ "data": {{ "source": "1_1", "target": "1_2" }} }}
    {{ "data": {{ "source": "2_end", "target": "2_1" }} }},
    ...
  ]
}}

字段定义说明：
- **nodes**：包含所有章节与知识点节点；
  - `id`：章节编号或知识点编号，如 “1_end”、“2_1”；
  - `label`：中文标题，清晰表达模块或技能名称；
  - `type`：章节节点用 `"chapter"`，知识点节点用 `"knowledge"`；
  - `select_element`：知识点相关的HTML 元素，如 `"h1"`、`"p"`、`"a"`。
- **edges**：表示章节之间、章节与其下知识点之间的层级关系；
- **dependent_edges**：表示知识点之间的逻辑依赖或学习顺序。

⚙️ 要求：
1. 所有章节应按知识主题分组，如“文本与结构”“样式与布局”“交互与脚本”等；
2. 每个章节下需包含 3~5 个具体知识点；
3. 知识点应从基础到进阶排列；
4. 输出结果必须是 **合法 JSON（仅英文双引号）**；
5. 严禁输出解释说明、注释或额外文本。

请你基于网站内容分析输出完整的 JSON 知识图谱结构。
    """

def generate_demo_site_prompt(dependency_context=None, existing_code_context=None, user_goal: str = ""):
    return f"""
你是一个资深的 Web 全栈开发专家，请根据以下任务说明、参考网页风格和前端技术知识点，生成结构清晰、可运行的 HTML 网站代码项目。最终效果应与用户提供的网站风格一致，并正确运用指定的前端技术点构建页面结构、样式与交互。




---

🎯 你必须实现以下关键点（不可遗漏）：

1. 页面整体风格、结构布局、配色等尽量贴近参考网站。
2. 使用要求的前端技术点（基于知识点图谱自动选取合适位置嵌入）：
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
🎯 用户的需求或目标说明（如果有）：
{user_goal or "（用户未补充）"}

---

✍️ 请你完成以下两部分输出（严格格式化）：

### 第一部分：项目主页面代码（嵌入所有 HTML、CSS、JS）

``html filename=public/index.html
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

def generate_learning_content_prompt(topic_info: dict) -> str:
    """
    生成学习内容提示词，适配知识图谱 data 结构
    """

    topic_id = topic_info.get("id", "")
    title = topic_info.get("label", "未命名知识点")
    select_elements = topic_info.get("select_element", [])

    prompt = f"""
您是一位专业的前端开发导师，擅长为零基础学习者讲解前端知识。现在需要根据传入的知识点信息，为学生生成系统化的学习内容。

请根据以下知识点信息生成内容：

知识点ID：{topic_id}
知识点标题：{title}
涉及的HTML/CSS/JS元素或属性：{", ".join(select_elements) if select_elements else "无特别指定"}

请编写适合零基础的学习内容，并严格按照以下 JSON 结构返回（不要添加任何额外说明、前后缀或解释文本）：

{{
  "topic_id": "{topic_id}",
  "title": "{title}",
  "levels": [
    {{
      "level": 1,
      "description": "适合零基础入门，掌握核心概念与基本语法。不少于300字。"
    }},
    {{
      "level": 2,
      "description": "理解知识点常见的场景与组合用法，提升实践能力。不少于300字。"
    }},
    {{
      "level": 3,
      "description": "深入知识点的机制与性能优化，形成系统化认知。不少于300字。"
    }},
    {{
      "level": 4,
      "description": "综合实战与拓展题，必须包含示例代码，不少于300字。"
    }}
  ]
}}

生成要求：
1. 必须返回纯 JSON，不要包含任何额外文本。
2. description 字段中不允许出现标题格式（如“概念：”“说明：”等）。
3. 每个 description 必须直接以正文开头。
4. 专业术语必须解释清楚，让零基础也能理解。
5. 所有内容必须与前端开发及本知识点相关。
6. Level 4 必须包含完整且可运行的代码示例（HTML/CSS/JS 均可）。
7. 全部内容必须使用中文。
"""

    return prompt
