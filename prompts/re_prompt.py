"""关系抽取提示词"""
import json

RE_SYSTEM_PROMPT = """你是城市规划领域的自然语言处理专家，专注于从规划文本中抽取实体间的关系，构建结构化的知识三元组。"""

RELATION_DEFINITIONS = """
关系类型说明：
规划文本中的关系主要由"规划活动"来表达，常见关系包括：

1. belongTo（归属）: 表示"A属于B"、"A是B的一部分"
   示例：<南沙, 属于, 广州>

2. consistOf（包含）: 表示"A由B组成"、"A包含B"
   示例：<生态网络, 包含, 公园体系>

3. is/is_a（定义）: 表示"A是B"，用于定义概念
   示例：<广州, 是, 国家重要中心城市>

4. 发展关系: 由"建设"、"推进"、"发展"等词表达
   示例：<广州, 建设, 美丽宜居花城>

5. 保护关系: 由"保护"、"维护"、"保留"等词表达
   示例：<广州, 保护, 白云山>
"""

def get_re_user_prompt(sentence: str, entities: dict, syntax_info: str = "", context: str = "") -> str:
    """生成关系抽取提示"""
    
    # 格式化实体列表
    entity_str = json.dumps(entities, ensure_ascii=False, indent=2)
    
    prompt = f"""{RELATION_DEFINITIONS}

任务说明：
从句子中提取关系三元组，格式为 <头实体, 关系, 尾实体>

已识别实体：
{entity_str}

"""
    
    if context:
        prompt += f"""上下文信息（用于补全省略成分）：
{context[:200]}...

"""
    
    prompt += f"""输入句子：
"{sentence}"

提取要求：
1. 头实体和尾实体必须来自已识别的实体列表
2. 关系词通常是 planned_activity 中的词，或者是 belongTo/consistOf/is 等
3. 如果句子中省略了主语，根据上下文补全
4. 每个三元组占一行
5. 格式严格为：<头实体, 关系, 尾实体>

只输出三元组，不要解释。如果某个位置无法确定，用 <null> 标记。

示例输出格式：
<广州, 建设, 美丽宜居花城>
<广州, 是, 国家重要中心城市>
"""
    
    return prompt

def get_re_second_prompt(initial_triplets: list) -> str:
    """第二轮验证提示"""
    triplets_str = '\n'.join([f"<{h}, {r}, {t}>" for h, r, t in initial_triplets])
    
    return f"""请验证并完善以下三元组：

{triplets_str}

检查要点：
1. 关系是否准确表达了原句语义
2. 是否遗漏了重要关系
3. 头尾实体是否正确
4. 省略的主语是否已补全

仅输出最终的三元组列表，每行一个，格式：<h, r, t>"""