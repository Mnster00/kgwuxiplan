"""关系抽取模块"""
import re
from typing import Dict, List, Tuple
from .llm_client import LLMClientFactory
from config import TASK_MODEL_MAP
from prompts.re_prompt import (
    RE_SYSTEM_PROMPT,
    get_re_user_prompt,
    get_re_second_prompt
)

class RelationExtractor:
    """关系抽取器"""
    
    def __init__(self):
        # 从配置获取模型类型
        model_type = TASK_MODEL_MAP['re']
        self.llm = LLMClientFactory.get_client(model_type)
    
    def extract(self, sentence: str, entities: Dict, context: str = "") -> List[Tuple[str, str, str]]:
        """提取三元组"""
        try:
            # 过滤空实体
            if sum(len(v) for v in entities.values()) == 0:
                return []
            
            # 第一阶段
            messages_1 = [
                {"role": "system", "content": RE_SYSTEM_PROMPT},
                {"role": "user", "content": get_re_user_prompt(sentence, entities, context=context)}
            ]
            
            response_1 = self.llm.call(messages_1)
            triplets_1 = self._parse_triplets(response_1)
            
            if not triplets_1:
                return []
            
            # 第二阶段验证
            messages_2 = messages_1 + [
                {"role": "assistant", "content": response_1},
                {"role": "user", "content": get_re_second_prompt(triplets_1)}
            ]
            
            response_2 = self.llm.call(messages_2)
            triplets_2 = self._parse_triplets(response_2)
            
            return triplets_2
        
        except Exception as e:
            print(f"      ❌ RE提取错误: {str(e)}")
            return []
    
    def _parse_triplets(self, response: str) -> List[Tuple[str, str, str]]:
        """解析三元组"""
        triplets = []
        
        # 支持多种格式
        patterns = [
            r'<\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^>]+?)\s*>',  # <h, r, t>
            r'\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)',  # (h, r, t)
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response)
            if matches:
                break
        
        for h, r, t in matches:
            h, r, t = h.strip(), r.strip(), t.strip()
            # 过滤null和过短的实体
            if all(x.lower() != 'null' and len(x) > 1 for x in [h, r, t]):
                triplets.append((h, r, t))
        
        return triplets