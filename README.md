# 🚀 LLM面试模拟系统 - Enhanced版

> 基于DeepSeek + BGE + Qdrant的智能面试系统
> 
> 🇨🇳 **完全国产化方案，成本极低，中文支持优秀**

## 📋 项目概述

这是一个基于大语言模型的智能面试模拟系统，帮助求职者进行技术面试练习。系统采用DeepSeek作为核心LLM，BGE作为嵌入模型，支持多种面试模式。

### 🌟 核心特性

- **🇨🇳 国产化技术栈**: DeepSeek + BGE + Qdrant，支持中文对话
- **💰 极低成本**: 比OpenAI方案节省95%以上成本
- **🎯 多模式面试**: 基础/JD解析/CV搜索三种面试模式
- **🧠 智能记忆**: 支持多轮对话和上下文记忆
- **📊 详细反馈**: 生成完整的面试评估报告
- **🔧 灵活配置**: 支持本地模型和云端API灵活切换

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                     LLM面试模拟系统                          │
├─────────────────────────────────────────────────────────────┤
│  🧠 核心LLM      │  DeepSeek-Chat (国产大模型)               │
│  🔍 嵌入模型      │  BGE-small-zh-v1.5 (百度开源)            │
│  💾 向量数据库    │  Qdrant / FAISS (可选)                   │
│  🛠️ 开发框架      │  LangChain + Python 3.11                │
├─────────────────────────────────────────────────────────────┤
│  📝 面试模式      │  v1: 基础面试 │ v2: JD解析 │ v3: CV搜索   │
│  🎯 教学模块      │  Agent教程 │ Function Calling │ 路由链   │
└─────────────────────────────────────────────────────────────┘
```

## 📂 项目结构

```
llm-developing-mock-interview/
├── 📚 教程文件
│   ├── Learn-Agent-Enhanced.ipynb          # 🌟 Agent入门教程
│   ├── Learn-Function-calling-Enhanced.ipynb  # Function Calling教程
│   └── 补充-路由链-Enhanced.ipynb           # 路由链教程
├── 🎯 面试系统
│   ├── v1-Create-Custom-Agent-Enhanced.ipynb  # 基础面试模式
│   ├── v2-Create-Custom-Agent-Enhanced.ipynb  # JD解析面试模式
│   └── v3-Create-Custom-Agent-Enhanced.ipynb  # CV搜索面试模式
├── 🔧 工具文件
│   ├── utils_enhanced.py                   # 工具函数库
│   ├── check_config.py                     # 配置验证脚本
│   └── requirements.txt                    # 依赖包
├── ⚙️ 配置文件
│   ├── .env.example.enhanced               # 环境变量模板
│   └── DEPLOYMENT_GUIDE.md                 # 部署指南
└── 📊 数据目录
    ├── data/                               # 简历和职位数据
    └── chat_history/                       # 面试记录
```

## 🚀 快速开始

### 1. 环境准备

#### 1.1 克隆项目



#### 1.2 安装依赖
```bash
pip install -r requirements.txt
```

#### 1.3 配置环境变量
```bash
# 复制配置模板
copy .env.example.enhanced .env

# 编辑.env文件，填入你的配置
notepad .env
```

**必要配置**：
```bash
# DeepSeek API Key (必填)
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# 可选配置
BGE_MODEL_PATH="./models--BAAI--bge-small-zh-v1.5"
QDRANT_HOST=localhost
QDRANT_PORT=6333

# 代理配置 (如果需要)
# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

### 2. 验证配置

运行配置检查脚本：
```bash
python check_config.py
```

如果看到 `🎉 恭喜！所有配置检查通过`，说明环境配置正确。

### 3. 开始使用

#### 🌟 推荐学习路径：

1. **入门教程** (`Learn-Agent-Enhanced.ipynb`)
   - Agent基础概念
   - DeepSeek + BGE集成
   - 实际案例演练

2. **面试实战** (选择一个模式开始)
   - `v1`: 基础技术面试
   - `v2`: 基于职位描述的面试
   - `v3`: 基于简历内容的面试

## 📖 详细使用指南

### 🎯 面试模式说明

#### **v1 - 基础面试模式**
- **适用场景**: 通用技术面试练习
- **特点**: 
  - 基础技术问题
  - 循序渐进的提问策略
  - 完整的面试流程管理

#### **v2 - JD解析面试模式**
- **适用场景**: 针对特定职位的面试准备
- **特点**:
  - 解析职位描述(JD)文件
  - 针对性技术提问
  - 匹配度评估

#### **v3 - CV搜索面试模式**
- **适用场景**: 基于个人简历的深度面试
- **特点**:
  - 向量化简历内容
  - 智能简历搜索
  - 个性化问题生成

### 🔧 高级配置

#### **本地BGE模型配置**
```bash
# 下载BGE模型到本地
git lfs clone https://huggingface.co/BAAI/bge-small-zh-v1.5

# 在.env中配置路径
BGE_MODEL_PATH="/path/to/your/bge-model"
```

#### **Qdrant向量数据库**
```bash
# Docker运行Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 或使用本地安装
pip install qdrant-client
```

## 💡 使用技巧

### 🎪 面试技巧
1. **回答策略**: 
   - 先回答核心要点
   - 提供具体代码示例
   - 说明实际应用场景

2. **互动优化**:
   - 主动询问澄清问题
   - 展示思考过程
   - 承认不懂并表达学习意愿

### 🔍 系统优化
1. **成本控制**:
   - 使用本地BGE模型减少API调用
   - 合理设置temperature参数
   - 控制对话轮数

2. **性能提升**:
   - 使用GPU加速BGE模型
   - 启用Qdrant向量缓存
   - 优化提示模板长度

## 🆚 技术方案对比

| 组件 | OpenAI方案 | 本项目方案 | 优势 |
|------|------------|------------|------|
| **LLM** | GPT-4 | DeepSeek-Chat | 🇨🇳 中文理解更好<br>💰 成本降低95% |
| **嵌入模型** | text-embedding-ada-002 | BGE-small-zh-v1.5 | 📱 完全免费<br>🚀 本地运行 |
| **向量数据库** | Pinecone | Qdrant/FAISS | 🔒 数据私有<br>💾 无额外费用 |
| **月成本** | $200+ | <$10 | 💵 节省95%+ |

## 🐛 常见问题

### Q: DeepSeek API Key如何获取？
A: 访问 [https://platform.deepseek.com](https://platform.deepseek.com) 注册账号，在API Keys页面创建新的Key。

### Q: 为什么选择DeepSeek而不是OpenAI？
A: 
- 🇨🇳 中文理解和生成能力更强
- 💰 成本仅为OpenAI的1/50
- 🔒 数据更安全，支持私有部署
- 🚀 响应速度快，延迟低

### Q: BGE模型下载慢怎么办？
A: 可以使用镜像站点：
```bash
export HF_ENDPOINT=https://hf-mirror.com
# 然后正常下载模型
```

### Q: Qdrant连接失败怎么办？
A: 
1. 确保Docker中的Qdrant正在运行
2. 检查端口6333是否被占用
3. 如果不需要向量搜索，可以跳过Qdrant配置

### Q: 面试问题太简单或太难？
A: 可以修改`system_prompt`中的难度设置，或者在对话中要求面试官调整问题难度。

## 🔄 更新日志

### v2.0 (当前版本)
- ✅ 完全迁移到DeepSeek API
- ✅ 集成BGE本地嵌入模型
- ✅ 添加Qdrant向量数据库支持
- ✅ 优化中文对话效果
- ✅ 大幅降低使用成本

### v1.0 (原版)
- OpenAI GPT-4 + Embeddings
- 基础面试功能
- 简历和JD解析

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境
```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python check_config.py

# 代码格式化
black *.py
```

## 📄 许可证

MIT License - 可自由使用和修改

## 🔗 相关链接

- [DeepSeek官网](https://platform.deepseek.com)
- [BGE模型](https://huggingface.co/BAAI/bge-small-zh-v1.5)
- [Qdrant文档](https://qdrant.tech/documentation/)
- [LangChain文档](https://python.langchain.com/)

## 📞 联系方式

- 项目作者: [qq:2969844692]
- 技术支持: 通过GitHub Issues

---

🎉 **开始你的AI面试练习之旅吧！使用国产技术栈，享受极低成本的智能面试体验！**
