# LLM4KG-Planning: 基于大语言模型的城市规划知识图谱构建

## 项目简介

本项目复现了论文《A large language model-based approach to building the knowledge graph for master plan》的核心方法，使用阿里云Qwen和字节跳动Doubao两个中文大模型，从城市规划文本中自动构建知识图谱。

## 核心功能

1. **命名实体识别 (NER)**: 使用Qwen-Max识别5类规划实体
2. **关系抽取 (RE)**: 使用Doubao-Pro提取实体间关系
3. **三元组评估**: 基于LLM-as-Judge机制筛选高质量三元组
4. **知识图谱构建**: 自动构建并可视化规划知识图谱

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置API Key

编辑 `config.py`，填入你的API密钥：
```python
QWEN_CONFIG = {
    'api_key': 'YOUR_DASHSCOPE_API_KEY',
    ...
}

DOUBAO_CONFIG = {
    'api_key': 'YOUR_VOLCENGINE_API_KEY',
    'endpoint_id': 'YOUR_ENDPOINT_ID',
    ...
}
```

### 3. 准备数据

将规划文本放入 `data/guangzhou_plan.txt`

### 4. 运行
```bash
python main.py
```

## 输出结果

- `results/extraction_results.json`: 实体和三元组抽取结果
- `results/knowledge_graph.json`: 知识图谱数据
- `results/kg_sample.png`: 知识图谱可视化（采样）

## 方法论概述

### 两阶段对话策略

1. **第一轮**: 初步提取实体/关系
2. **第二轮**: 验证并补全结果

### LLM分工

| 任务 | 使用模型 | 原因 |
|------|---------|------|
| NER | Qwen-Max | 论文中性能最佳 |
| RE | Doubao-Pro | 在中文RE任务上表现优异 |
| 评估 | Qwen-Max | 作为Judge更可靠 |

## 局限性

- 为节省成本，简化了评估机制
- 未实现完整的RAG分类
- 处理句子数量受限

## 扩展方向

1. 添加HanLP进行句法分析
2. 实现完整的五维评分机制
3. 接入Neo4j图数据库
4. 支持多文档联合构图

## 参考文献

Zhang, W., Chen, Y., Liu, X., & Zhang, H. (2025). A large language model-based approach to building the knowledge graph for master plan: A case study in Guangzhou, China. *Land Use Policy*, 159, 107807.