"""统一API客户端"""
import requests
import json
import time
from typing import Dict, List, Optional
from config import API_BASE_URL, API_KEY, MODELS, REQUEST_TIMEOUT, MAX_RETRIES

class UnifiedLLMClient:
    """统一的LLM API客户端"""
    
    def __init__(self, model_type: str):
        """
        初始化客户端
        
        Args:
            model_type: 模型类型 ('qwen', 'doubao', 'deepseek')
        """
        if model_type not in MODELS:
            raise ValueError(f"不支持的模型类型: {model_type}")
        
        self.model_config = MODELS[model_type]
        self.model_name = self.model_config['model_name']
        self.temperature = self.model_config['temperature']
        self.max_tokens = self.model_config['max_tokens']
        
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    
    def call(self, messages: List[Dict[str, str]], 
             temperature: Optional[float] = None,
             max_tokens: Optional[int] = None,
             stream: bool = False) -> str:
        """
        调用LLM API
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数（可选）
            max_tokens: 最大token数（可选）
            stream: 是否流式返回
            
        Returns:
            模型响应内容
        """
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "stream": stream
        }
        
        # 重试机制
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    API_BASE_URL,
                    headers=self.headers,
                    json=data,
                    timeout=REQUEST_TIMEOUT
                )
                
                # 检查响应状态
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    return content
                else:
                    error_msg = f"API请求失败 (状态码: {response.status_code}): {response.text}"
                    print(f"   ⚠️  {error_msg}")
                    
                    if attempt < MAX_RETRIES - 1:
                        wait_time = 2 ** attempt  # 指数退避
                        print(f"   ⏳ 等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    else:
                        raise Exception(error_msg)
            
            except requests.exceptions.Timeout:
                error_msg = f"请求超时（尝试 {attempt + 1}/{MAX_RETRIES}）"
                print(f"   ⚠️  {error_msg}")
                
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise Exception("请求超时：服务器无响应")
            
            except requests.exceptions.RequestException as e:
                error_msg = f"请求错误: {str(e)}"
                print(f"   ⚠️  {error_msg}")
                
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise Exception(error_msg)
        
        raise Exception("达到最大重试次数")
    
    def call_stream(self, messages: List[Dict[str, str]]) -> str:
        """
        流式调用（如需要）
        
        Args:
            messages: 对话消息列表
            
        Returns:
            完整的模型响应
        """
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True
        }
        
        try:
            response = requests.post(
                API_BASE_URL,
                headers=self.headers,
                json=data,
                timeout=REQUEST_TIMEOUT,
                stream=True
            )
            
            if response.status_code == 200:
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]
                            if data_str.strip() != '[DONE]':
                                try:
                                    chunk = json.loads(data_str)
                                    delta = chunk['choices'][0]['delta']
                                    if 'content' in delta:
                                        full_content += delta['content']
                                except json.JSONDecodeError:
                                    continue
                return full_content
            else:
                raise Exception(f"流式请求失败: {response.status_code}")
        
        except Exception as e:
            raise Exception(f"流式请求错误: {str(e)}")


class LLMClientFactory:
    """LLM客户端工厂"""
    
    _clients = {}
    
    @classmethod
    def get_client(cls, model_type: str) -> UnifiedLLMClient:
        """
        获取或创建客户端实例（单例模式）
        
        Args:
            model_type: 模型类型
            
        Returns:
            LLM客户端实例
        """
        if model_type not in cls._clients:
            cls._clients[model_type] = UnifiedLLMClient(model_type)
        return cls._clients[model_type]