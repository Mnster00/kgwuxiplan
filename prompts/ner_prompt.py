"""命名实体识别提示词"""
import json

ENTITY_DEFINITIONS = """
实体类型定义：
1. 地理位置(location): 可在地图上识别的地理实体，如省、市、区、街道、景点等
   示例：广州市、白云山风景名胜区、珠江

2. 土地使用功能(land_use): 土地用途、功能区描述、产业布局
   示例：先进制造业、商业办公区、生态网络、住宅用地

3. 方位(direction): 方向指示词及相关短语
   示例：东部、南部、中心区、周边

4. 规划概念(concept): 宏观、抽象的规划理念和目标
   示例：美丽宜居花城、国家重要中心城市、创新驱动

5. 规划活动(planned_activity): 描述规划行动的动词和短语
   示例：加强、保护、建设、推进、优化
"""

NER_SYSTEM_PROMPT = """你是一位经验丰富的城市规划学者，擅长从规划文本中识别各类地理规划知识实体。你的任务是准确识别实体并分类。"""

def get_ner_user_prompt(sentence: str, examples: list = None) -> str:
    """生成NER用户提示"""
    prompt = f"""{ENTITY_DEFINITIONS}

任务要求：
1. 从输入句子中提取上述5类实体
2. 严格按照JSON格式输出
3. 每个实体分类准确
4. 避免额外解释和描述

"""
    
    if examples:
        prompt += "参考示例：\n"
        for i, ex in enumerate(examples[:3], 1):
            prompt += f"\n示例{i}：\n"
            prompt += f"输入：{ex['input']}\n"
            prompt += f"输出：{ex['output']}\n"
    
    prompt += f"""\n现在请提取以下句子的实体：
"{sentence}"

要求：
- 仅输出JSON格式结果
- 不要任何额外说明
- 格式示例：{{"location": [...], "land_use": [...], "direction": [...], "concept": [...], "planned_activity": [...]}}
"""
    
    return prompt

def get_ner_second_prompt(sentence: str, first_result: dict) -> str:
    """第二轮对话提示"""
    return f"""第一次提取的实体可能不完整或不准确。请重新审视并完善。

原句子："{sentence}"

首次提取结果：
{json.dumps(first_result, ensure_ascii=False, indent=2)}

请检查：
1. 是否有遗漏的实体
2. 实体分类是否准确
3. 是否有错误识别的实体

仅输出最终的JSON结果，不要其他内容。"""