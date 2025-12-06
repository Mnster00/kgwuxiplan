"""三元组评估模块"""
import re
from typing import List, Tuple, Dict
from .llm_client import LLMClientFactory
from config import TASK_MODEL_MAP

class TripletEvaluator:
    """LLM-as-Judge评估器"""
    
    def __init__(self):
        model_type = TASK_MODEL_MAP['eval']
        self.judge = LLMClientFactory.get_client(model_type)
    
    def evaluate(self, triplets: List[Tuple], sentence: str, context: str = "") -> List[Tuple]:
        """
        评估并筛选三元组（简化版）
        
        Args:
            triplets: 三元组列表
            sentence: 原句子
            context: 上下文
            
        Returns:
            筛选后的三元组
        """
        if not triplets:
            return []
        
        try:
            # 简化评估：只做基本筛选
            scored = self._score_triplets(triplets, sentence, context)
            
            # 过滤低分三元组
            threshold = 3.0
            filtered = [t for t, score in scored if score >= threshold]
            
            return filtered
        
        except Exception as e:
            print(f"      ⚠️  评估错误: {str(e)}，返回原始结果")
            return triplets
    
    def _score_triplets(self, triplets: List[Tuple], sentence: str, context: str) -> List[Tuple]:
        """对三元组评分"""
        triplet_str = '\n'.join([f"<{h}, {r}, {t}>" for h, r, t in triplets])
        
        prompt = f"""请对以下三元组的质量进行评分(1-5分)。

原句子：{sentence}

三元组：
{triplet_str}

评分标准：
- 5分: 完全准确，语义清晰
- 4分: 基本准确，有小瑕疵
- 3分: 部分准确，存在一些问题
- 2分: 较多错误
- 1分: 严重错误

对每个三元组输出评分，格式：
<h, r, t>: 分数

仅输出评分结果，每行一个。"""
        
        messages = [
            {"role": "system", "content": "你是专业的城市规划文本评估专家。"},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.judge.call(messages, temperature=0.3)
            
            # 解析评分
            scored_triplets = []
            for line in response.split('\n'):
                if '<' in line and '>' in line and ':' in line:
                    try:
                        # 提取三元组和分数
                        match = re.search(r'<([^,]+),\s*([^,]+),\s*([^>]+)>\s*:\s*([\d.]+)', line)
                        if match:
                            h, r, t = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
                            score = float(match.group(4))
                            scored_triplets.append(((h, r, t), score))
                    except:
                        continue
            
            # 如果解析失败，给所有三元组默认分数
            if not scored_triplets:
                scored_triplets = [(t, 3.5) for t in triplets]
            
            return scored_triplets
        
        except Exception as e:
            print(f"      ⚠️  评分失败: {str(e)}")
            return [(t, 3.5) for t in triplets]