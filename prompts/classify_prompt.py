"""分类提示词"""
import json

CLASSIFY_SYSTEM_PROMPT = """你是城市规划领域的文本分类专家，擅长对规划实体和关系进行精确分类。"""

# 实体分类
ENTITY_COARSE_CATEGORIES = """
实体粗分类：
1. LOC (Location): 地理位置
2. FUNC (Function): 功能区域
3. CONC (Concept): 规划概念
"""

ENTITY_FINE_CATEGORIES = """
位置实体细分类：
1. 科教 (Sci-tech & Education)
2. 商业 (Commercial & Business)
3. 工业 (Industry)
4. 居住 (Residential)
5. 绿地 (Green & Open Space)
6. 交通 (Transportation)
7. 历史保护 (Historic Preservation)
8. 生态保护 (Ecological Preservation)
9. 行政公服 (Administration & Public Services)
10. 市政设施 (Municipal Utilities)
11. 特殊区域 (Specially-designated Areas)
12. 水系 (Water)
13. 行政区划 (Administrative Regions)
"""

# 关系分类
RELATION_CATEGORIES = """
关系类型分类：
1. development (发展): 建设、推进、发展、优化等
2. conservation (保护): 保护、维护、保留等
3. restriction (限制): 限制、控制、禁止等
4. regulation (调控): 协调、整合、引导等
5. explanation (说明): 位于、包含、属于等
"""

def get_entity_coarse_classify_prompt(entity: str, context: str = "") -> str:
    """粗分类提示"""
    prompt = f"""{ENTITY_COARSE_CATEGORIES}

任务：对实体进行粗分类

实体：{entity}
"""
    
    if context:
        prompt += f"上下文：{context}\n"
    
    prompt += """
输出格式：只输出类别名称（LOC/FUNC/CONC），不要其他内容。
"""
    
    return prompt

def get_entity_fine_classify_prompt(entity: str, context: str = "") -> str:
    """细分类提示"""
    prompt = f"""{ENTITY_FINE_CATEGORIES}

任务：对位置实体进行功能细分类

实体：{entity}
"""
    
    if context:
        prompt += f"上下文：{context[:100]}...\n"
    
    prompt += """
要求：
1. 可以输出1-3个最可能的类别
2. 按可能性从高到低排序
3. 输出格式：类别1, 类别2, 类别3

示例：
Commercial & Business, Historic Preservation
"""
    
    return prompt

def get_relation_classify_prompt(relation: str, head: str, tail: str) -> str:
    """关系分类提示"""
    prompt = f"""{RELATION_CATEGORIES}

任务：对规划关系进行分类

三元组：<{head}, {relation}, {tail}>

输出格式：只输出类别名称（development/conservation/restriction/regulation/explanation），不要其他内容。
"""
    
    return prompt
```

## 修复后的完整项目文件列表

确保你的项目包含以下所有文件：
```
llm4kg_planning/
├── README.md
├── requirements.txt
├── config.py
├── data/
│   └── guangzhou_plan.txt
├── prompts/
│   ├── __init__.py          ✓ 新增
│   ├── ner_prompt.py        ✓ 修复（加入json import）
│   ├── re_prompt.py         ✓ 修复（加入json import）
│   ├── eval_prompt.py       ✓ 新增
│   └── classify_prompt.py   ✓ 新增
├── src/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── ner_extractor.py
│   ├── relation_extractor.py
│   ├── evaluator.py
│   ├── classifier.py         （可选）
│   ├── preprocessor.py       （可选）
│   └── kg_builder.py
├── results/                   （运行后自动创建）
└── main.py