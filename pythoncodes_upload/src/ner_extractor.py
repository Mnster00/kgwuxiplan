"""命名实体识别模块"""
import json
import re
from typing import Dict, List
from .llm_client import LLMClientFactory
from config import TASK_MODEL_MAP
from prompts.ner_prompt import (
    NER_SYSTEM_PROMPT, 
    get_ner_user_prompt, 
    get_ner_second_prompt
)

class NERExtractor:
    """命名实体识别器"""
    
    def __init__(self):
        # 从配置获取模型类型
        model_type = TASK_MODEL_MAP['ner']
        self.llm = LLMClientFactory.get_client(model_type)
        self.examples = self._load_examples()
    
    def _load_examples(self) -> List[Dict]:
        """加载少样本示例"""
        return [
            {
                "input": "优先保障先进制造业、战略性新兴产业发展空间，推进价值创新园建设。",
                "output": '''{
                    "location": [],
                    "land_use": ["先进制造业", "战略性新兴产业", "价值创新园"],
                    "direction": [],
                    "concept": [],
                    "planned_activity": ["优先保障", "推进"]
                }'''
            },
            {
                "input": "增加绿地开敞空间供给，完善城市生态网络和公园体系。",
                "output": '''{
                    "location": [],
                    "land_use": ["绿地开敞空间", "生态网络", "公园体系"],
                    "direction": [],
                    "concept": [],
                    "planned_activity": ["增加", "完善"]
                }'''
            },
            {
                "input": "加强白云山风景名胜区、南湖国家旅游度假区等生态资源保护。",
                "output": '''{
                    "location": ["白云山风景名胜区", "南湖国家旅游度假区"],
                    "land_use": ["生态资源"],
                    "direction": [],
                    "concept": [],
                    "planned_activity": ["加强", "保护"]
                }'''
            }
        ]
    
    def extract(self, sentence: str) -> Dict[str, List[str]]:
        """提取实体（两阶段对话）"""
        try:
            # 第一阶段
            messages_1 = [
                {"role": "system", "content": NER_SYSTEM_PROMPT},
                {"role": "user", "content": get_ner_user_prompt(sentence, self.examples)}
            ]
            
            response_1 = self.llm.call(messages_1)
            result_1 = self._parse_json(response_1)
            
            # 第二阶段
            messages_2 = [
                {"role": "system", "content": NER_SYSTEM_PROMPT},
                {"role": "user", "content": get_ner_user_prompt(sentence, self.examples)},
                {"role": "assistant", "content": response_1},
                {"role": "user", "content": get_ner_second_prompt(sentence, result_1)}
            ]
            
            response_2 = self.llm.call(messages_2)
            result_2 = self._parse_json(response_2)
            
            return result_2
        
        except Exception as e:
            print(f"NER提取错误: {str(e)}")
            return self._empty_result()
    
    def _parse_json(self, response: str) -> Dict[str, List[str]]:
        """解析JSON响应"""
        # 清理markdown代码块
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*', '', response)
        response = response.strip()
        
        try:
            result = json.loads(response)
            # 确保所有字段存在
            for key in ['location', 'land_use', 'direction', 'concept', 'planned_activity']:
                if key not in result:
                    result[key] = []
            return result
        except json.JSONDecodeError as e:
            print(f"      ⚠️  JSON解析错误: {str(e)}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, List[str]]:
        """返回空结果"""
        return {
            "location": [],
            "land_use": [],
            "direction": [],
            "concept": [],
            "planned_activity": []
        }