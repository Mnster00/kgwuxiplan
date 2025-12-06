"""评估提示词"""
import json

EVAL_SYSTEM_PROMPT = """你是专业的城市规划文本质量评估专家，负责评价知识三元组的准确性和可靠性。"""

EVAL_DIMENSIONS = """
评分维度（1-5分）：

1. 语义准确性(Semantically): 三元组是否准确表达原句语义
2. 一致性(Consistency): 三元组是否与原文逻辑一致
3. 事实性(Factuality): 三元组是否保留了原文的事实陈述
4. 准确性(Accuracy): 是否存在不准确、遗漏或虚假信息
5. 可理解性(Understandability): 对非专家是否易于理解

评分标准：
5分 - 完全准确，无任何问题
4分 - 基本准确，有轻微瑕疵
3分 - 部分准确，存在一些问题
2分 - 较多错误或不准确
1分 - 严重错误，不可用
"""

def get_eval_prompt(triplets: list, sentence: str, context: str = "") -> str:
    """生成评估提示"""
    
    triplets_str = '\n'.join([f"<{h}, {r}, {t}>" for h, r, t in triplets])
    
    prompt = f"""{EVAL_DIMENSIONS}

任务：对以下三元组进行质量评分

原句子：
"{sentence}"

"""
    
    if context:
        prompt += f"""上下文：
{context[:150]}...

"""
    
    prompt += f"""待评估三元组：
{triplets_str}

要求：
1. 对每个三元组给出综合评分（1-5分）
2. 输出格式：<h, r, t>: 分数
3. 只输出评分结果，每行一个

示例：
<广州, 建设, 美丽宜居花城>: 4.5
<广州, 保护, 白云山>: 4.0
"""
    
    return prompt