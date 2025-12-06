"""统一API配置文件"""

# API基础配置
API_BASE_URL = "https://api.probex.top/v1/chat/completions"
API_KEY = "sk-cSdU0KTsMj3N28rEuxpXzWAXXQUTvLeodONvvSHacnlP1Wq3"  # 替换为你的API Key

# 模型配置
MODELS = {
    'ds3': {
        'model_name': 'deepseek-v3',
        'temperature': 0.4,
        'max_tokens': 4000
    }
}
'''
# 模型配置
MODELS = {
    'qwen': {
        'model_name': 'Qwen3-32B',
        'temperature': 0.4,
        'max_tokens': 4000
    },
    'doubao': {
        'model_name': 'deepseek-v3',
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
    'ner': 'qwen',       # NER使用Qwen
    're': 'doubao',      # RE使用Doubao
    'eval': 'qwen',      # 评估使用Qwen
    'classify': 'qwen'   # 分类使用Qwen
}
'''
# 任务-模型分配
TASK_MODEL_MAP = {
    'ner': 'ds3',       # NER使用Qwen
    're': 'ds3',      # RE使用Doubao
    'eval': 'ds3',      # 评估使用Qwen
    'classify': 'ds3'   # 分类使用Qwen
}

# Neo4j数据库配置
NEO4J_URI = "neo4j+s://fdd80838.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "E9dXvPhUioxv-XsF6g3TXeUQ3baICAXOrwRgFBLjgrc"
NEO4J_CONNECTION_TIMEOUT = 30
NEO4J_MAX_CONNECTION_LIFETIME = 3600
NEO4J_MAX_CONNECTION_POOL_SIZE = 50
