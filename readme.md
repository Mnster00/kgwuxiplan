# LLM4KG-Planning: 基于大语言模型的城市规划知识图谱构建

## 项目简介

本项目实现了基于大语言模型的城市规划知识图谱构建系统，能够从城市规划文本中自动识别实体、提取关系并构建知识图谱。项目支持多城市的规划文本处理，并提供了可视化功能。

## 核心功能

1. **命名实体识别 (NER)**：从规划文本中识别规划实体
2. **关系抽取 (RE)**：提取实体之间的语义关系
3. **三元组评估**：基于大语言模型的判断机制筛选高质量三元组
4. **知识图谱构建**：自动构建城市规划知识图谱
5. **可视化展示**：提供知识图谱可视化和词云生成功能

## 项目结构

```
├── config.py                # API配置文件
├── data/                    # 数据目录
│   └── wuxi_plan.txt        # 无锡规划文本示例
├── main.py                  # 主程序（广州）
├── main_suzhou.py           # 苏州规划处理程序
├── main_wuxi.py             # 无锡规划处理程序
├── prompts/                 # 提示词模板目录
│   ├── classify_prompt.py   # 分类提示词
│   ├── eval_prompt.py       # 评估提示词
│   ├── init.py
│   ├── ner_prompt.py        # NER提示词
│   └── re_prompt.py         # 关系抽取提示词
├── results/                 # 结果输出目录
│   ├── extraction_results.json  # 实体和关系抽取结果
│   ├── knowledge_graph.json     # 知识图谱数据
│   └── kg_sample.png            # 知识图谱可视化图
├── src/                     # 源代码目录
│   ├── evaluator.py         # 三元组评估器
│   ├── kg_builder.py        # 知识图谱构建器
│   ├── llm_client.py        # LLM客户端
│   ├── ner_extractor.py     # 命名实体识别器
│   └── relation_extractor.py # 关系抽取器
├── visualize_wuxi_policy_kawa.py  # 可视化工具
├── wuxi_policy_wordcloud.py       # 词云生成工具
├── requirements.txt         # 依赖列表
└── readme.md                # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API Key

编辑 `config.py`，填入你的API密钥：

```python
QWEN_CONFIG = {
    'api_key': 'YOUR_DASHSCOPE_API_KEY',  # 阿里云Qwen API密钥
    'model': 'qwen-max',
    'temperature': 0.7
}

DOUBAO_CONFIG = {
    'api_key': 'YOUR_VOLCENGINE_API_KEY',  # 字节跳动Doubao API密钥
    'endpoint_id': 'YOUR_ENDPOINT_ID',
    'model': 'doubao-pro',
    'temperature': 0.7
}
```

### 3. 准备数据

将城市规划文本放入 `data/` 目录下，文件命名格式为 `城市名称_plan.txt`（例如：`wuxi_plan.txt`）。

### 4. 运行程序

根据需要处理的城市，运行相应的主程序：

```bash
# 处理无锡规划
python main_wuxi.py
```

## 输出结果

程序运行完成后，结果将保存在 `results/` 目录下：

- `extraction_results.json`: 包含识别出的实体和抽取的关系信息
- `knowledge_graph.json`: 构建完成的知识图谱数据
- `kg_sample.png`: 知识图谱的可视化图像（采样展示）

## 可视化功能

### 知识图谱可视化

使用以下命令生成知识图谱可视化：

```bash
python visualize_wuxi_policy_kawa.py
```

### 词云生成

使用以下命令生成规划文本的词云：

```bash
python wuxi_policy_wordcloud.py
```


### 模型分工

| 任务 | 使用模型 |
|------|---------|
| 命名实体识别 | DeepSeek | 
| 关系抽取 | Glm-4.5 + DeepSeek + Qwen| 
| 三元组评估 | Qwen | 



