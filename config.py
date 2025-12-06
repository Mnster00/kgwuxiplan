"""统一API配置文件"""

# API基础配置
API_BASE_URL = "https://api.probex.top/v1/chat/completions"
API_KEY = "sk-cSdUxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 替换为你的API Key

# 模型配置
MODELS = {
    'ds3': {
        'model_name': 'deepseek-v3',
        'temperature': 0.4,
        'max_tokens': 4000
    }
    'qwen': {
        'model_name': 'Qwen3-32B',
        'temperature': 0.4,
        'max_tokens': 4000
    },
    'GLM': {
        'model_name': 'GLM-4.5',
        'temperature':0.4,
        'max_tokens': 4000
    }
}
'''

# 请求配置
REQUEST_TIMEOUT = 300  # 超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数

# 实体类型定义
ENTITY_TYPES = {
    'location': '地理位置实体',
    'land_use': '土地使用功能',
    'direction': '方位指示',
    'concept': '规划概念',
    'planned_activity': '规划活动'
}

# 关系类型定义
RELATION_TYPES = {
    'development': '发展',
    'conservation': '保护',
    'restriction': '限制',
    'regulation': '调控',
    'explanation': '说明'
}
'''
# 任务-模型分配
TASK_MODEL_MAP = {
    'ner': 'qwen',      
    're': 'qwen',      
    'eval': 'qwen',      
    'classify': 'GLM'   
}


