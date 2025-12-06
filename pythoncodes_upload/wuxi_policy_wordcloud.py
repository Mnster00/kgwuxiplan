"""无锡政策知识图谱词云可视化工具

此脚本用于生成无锡政策知识图谱中实体和关系的词云可视化，
按不同属性切面展示，适用于顶级期刊论文发表。
"""
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from typing import Dict, List, Set, Tuple
from wordcloud import WordCloud, STOPWORDS
from matplotlib.colors import LinearSegmentedColormap

# 设置中文字体，确保中文正常显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 常用中文字体路径列表（Windows系统）
COMMON_CHINESE_FONTS = [
    'C:\\Windows\\Fonts\\simhei.ttf',  # 黑体
    'C:\\Windows\\Fonts\\msyh.ttc',  # 微软雅黑
    'C:\\Windows\\Fonts\\simsun.ttc',  # 宋体
    'C:\\Windows\\Fonts\\simkai.ttf',  # 楷体
]

class WuxiPolicyWordCloudGenerator:
    """无锡政策词云生成器类"""
    
    # 实体类型颜色映射 - 精心设计的配色方案
    ENTITY_COLOR_MAP = {
        'location': '#FF6B6B',      # 红色 - 地理位置
        'land_use': '#4ECDC4',      # 青色 - 土地使用
        'concept': '#45B7D1',       # 蓝色 - 规划概念
        'facility': '#98D8C8',      # 绿色 - 设施
        'indicator': '#A64C14',     # 黄色 - 指标
        'planned_activity': '#FFA07A', # 橙色 - 规划活动
        'direction': '#C9A0DC'      # 紫色 - 方位指示
    }
    
    # 关系类型颜色映射
    RELATION_COLOR_MAP = {
        'development': '#FF6B6B',    # 红色 - 发展关系
        'conservation': '#4ECDC4',   # 青色 - 保护关系
        'restriction': '#A64C14',    # 黄色 - 限制关系
        'regulation': '#45B7D1',     # 蓝色 - 调控关系
        'explanation': '#98D8C8'     # 绿色 - 说明关系
    }
    
    def __init__(self, kg_file: str, output_dir: str = 'results_wuxi_visualizations'):
        """初始化词云生成器
        
        Args:
            kg_file: 知识图谱JSON文件路径
            output_dir: 输出目录路径
        """
        self.kg_file = kg_file
        self.output_dir = output_dir
        self.G = None  # 知识图谱
        self.entity_types = {}  # 实体类型映射
        self.relation_types = {}  # 关系类型映射
        self.entity_frequencies = Counter()  # 实体频率
        self.relation_frequencies = Counter()  # 关系频率
        self.entity_by_type = {}  # 按类型分组的实体
        self.relation_by_type = {}  # 按类型分组的关系
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_data(self):
        """加载知识图谱数据并提取实体和关系信息"""
        print(f"正在加载知识图谱数据: {self.kg_file}")
        
        try:
            with open(self.kg_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取节点信息
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            
            print(f"加载完成: {len(nodes)} 个实体, {len(edges)} 个关系")
            
            # 构建实体类型映射和频率统计
            for node in nodes:
                entity_id = node.get('id', '')
                entity_type = node.get('type', 'unknown')
                
                # 存储实体类型
                self.entity_types[entity_id] = entity_type
                
                # 更新实体频率
                self.entity_frequencies[entity_id] += 1
                
                # 按类型分组实体
                if entity_type not in self.entity_by_type:
                    self.entity_by_type[entity_type] = []
                self.entity_by_type[entity_type].append(entity_id)
            
            # 构建关系类型映射和频率统计
            for edge in edges:
                relation_type = edge.get('type', 'unknown')
                source = edge.get('source', '')
                target = edge.get('target', '')
                
                # 存储关系类型（以source->target为键）
                relation_key = f"{source}->{relation_type}->{target}"
                self.relation_types[relation_key] = relation_type
                
                # 更新关系类型频率
                self.relation_frequencies[relation_type] += 1
                
                # 按类型分组关系
                if relation_type not in self.relation_by_type:
                    self.relation_by_type[relation_type] = []
                self.relation_by_type[relation_type].append(relation_key)
            
            print("数据预处理完成")
            
        except Exception as e:
            print(f"加载数据时出错: {e}")
            raise
    
    def create_custom_colormap(self, base_color: str) -> LinearSegmentedColormap:
        """基于基础颜色创建词云渐变色图
        
        Args:
            base_color: 基础颜色的十六进制值
            
        Returns:
            自定义的渐变色图
        """
        # 将十六进制颜色转换为RGB
        r, g, b = int(base_color[1:3], 16)/255, int(base_color[3:5], 16)/255, int(base_color[5:7], 16)/255
        
        # 创建从白色到基础颜色的渐变
        colors = [(0.5*r, 0.5*g, 0.5*b), (r, g, b)]
        return LinearSegmentedColormap.from_list('custom_cmap', colors, N=256)
    
    def generate_entity_wordcloud_by_type(self, entity_type: str, max_words: int = 100):
        """按实体类型生成词云
        
        Args:
            entity_type: 实体类型
            max_words: 词云中显示的最大词数
        """
        if entity_type not in self.entity_by_type:
            print(f"警告: 未找到实体类型 {entity_type} 的数据")
            return
        
        # 准备词频数据
        words = self.entity_by_type[entity_type]
        word_freq = {word: self.entity_frequencies.get(word, 1) for word in words}
        
        # 获取对应的颜色
        base_color = self.ENTITY_COLOR_MAP.get(entity_type, '#CCCCCC')
        cmap = self.create_custom_colormap(base_color)
        
        # 选择可用的中文字体
        font_path = None
        for f in COMMON_CHINESE_FONTS:
            if os.path.exists(f):
                font_path = f
                break
        
        # 创建词云
        wc = WordCloud(
            font_path=font_path,  # 指定中文字体
            width=500, 
            height=500,
            background_color='white',
            colormap=cmap,
            max_words=max_words,
            max_font_size=100,  # 限制最大字体大小
            min_font_size=10,   # 设置最小字体大小
            relative_scaling=0.3,  # 控制字体大小相对于词频的缩放程度
            contour_width=2,
            contour_color=base_color,
            prefer_horizontal=0.9,
            random_state=42,
            stopwords=set(STOPWORDS)
        )
        
        # 生成词云
        wc.generate_from_frequencies(word_freq)
        
        # 绘制和保存
        plt.figure(figsize=(7, 7))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        #plt.title(f'无锡政策知识图谱 - {entity_type} 实体词云', fontsize=16, pad=20)
        
        output_path = os.path.join(self.output_dir, f'wordcloud_entity_{entity_type}.png')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"实体词云已保存: {output_path}")
    
    def generate_relation_wordcloud(self, max_words: int = 50):
        """生成关系类型词云
        
        Args:
            max_words: 词云中显示的最大词数
        """
        # 准备词频数据
        word_freq = {rel_type: count for rel_type, count in self.relation_frequencies.items()}
        
        # 选择可用的中文字体
        font_path = None
        for f in COMMON_CHINESE_FONTS:
            if os.path.exists(f):
                font_path = f
                break
        
        # 创建多色词云
        wc = WordCloud(
            font_path=font_path,
            width=800,
            height=400,
            background_color='white',
            max_words=max_words,
            max_font_size=100,  # 限制最大字体大小
            min_font_size=10,   # 设置最小字体大小
            relative_scaling=0.3,  # 控制字体大小相对于词频的缩放程度
            prefer_horizontal=0.9,
            random_state=42,
            stopwords=set(STOPWORDS)
        )
        
        # 生成词云
        wc.generate_from_frequencies(word_freq)
        
        # 修改词云颜色以匹配关系类型颜色
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            return self.RELATION_COLOR_MAP.get(word, '#333333')
        
        wc.recolor(color_func=color_func, random_state=42)
        
        # 绘制和保存
        plt.figure(figsize=(12, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title('无锡政策知识图谱 - 关系类型词云', fontsize=16, pad=20)
        
        output_path = os.path.join(self.output_dir, 'wordcloud_relations.png')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"关系类型词云已保存: {output_path}")
    
    def generate_combined_wordcloud(self, max_words: int = 200):
        """生成综合词云（所有实体）
        
        Args:
            max_words: 词云中显示的最大词数
        """
        # 准备词频数据
        word_freq = dict(self.entity_frequencies)
        
        # 选择可用的中文字体
        font_path = None
        for f in COMMON_CHINESE_FONTS:
            if os.path.exists(f):
                font_path = f
                break
        
        # 创建多彩词云
        wc = WordCloud(
            font_path=font_path,
            width=1200,
            height=600,
            background_color='white',
            max_words=max_words,
            max_font_size=100,  # 限制最大字体大小
            min_font_size=10,   # 设置最小字体大小
            relative_scaling=0.3,  # 控制字体大小相对于词频的缩放程度
            prefer_horizontal=0.9,
            random_state=42,
            stopwords=set(STOPWORDS)
        )
        
        # 生成词云
        wc.generate_from_frequencies(word_freq)
        
        # 修改词云颜色以匹配实体类型颜色
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            entity_type = self.entity_types.get(word, 'concept')
            return self.ENTITY_COLOR_MAP.get(entity_type, '#333333')
        
        wc.recolor(color_func=color_func, random_state=42)
        
        # 绘制和保存
        plt.figure(figsize=(15, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title('无锡政策知识图谱 - 实体综合词云', fontsize=18, pad=20)
        
        output_path = os.path.join(self.output_dir, 'wordcloud_combined_entities.png')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"综合词云已保存: {output_path}")
    
    def generate_co_occurrence_wordcloud(self, entity_type1: str, entity_type2: str, max_words: int = 100):
        """生成两种实体类型共同出现的词云
        
        Args:
            entity_type1: 第一种实体类型
            entity_type2: 第二种实体类型
            max_words: 词云中显示的最大词数
        """
        # 检查类型是否存在
        if entity_type1 not in self.entity_by_type or entity_type2 not in self.entity_by_type:
            print(f"警告: 未找到实体类型 {entity_type1} 或 {entity_type2} 的数据")
            return
        
        # 选择可用的中文字体
        font_path = None
        for f in COMMON_CHINESE_FONTS:
            if os.path.exists(f):
                font_path = f
                break
        
        # 创建混合颜色的词云
        wc = WordCloud(
            font_path=font_path,
            width=1000,
            height=500,
            background_color='white',
            max_words=max_words,
            max_font_size=100,  # 限制最大字体大小
            min_font_size=10,   # 设置最小字体大小
            relative_scaling=0.3,  # 控制字体大小相对于词频的缩放程度
            prefer_horizontal=0.9,
            random_state=42,
            stopwords=set(STOPWORDS)
        )
        
        # 准备混合词频数据
        entities1 = self.entity_by_type[entity_type1]
        entities2 = self.entity_by_type[entity_type2]
        
        # 合并词频
        word_freq = {}
        for entity in entities1:
            word_freq[entity] = self.entity_frequencies.get(entity, 1)
        for entity in entities2:
            word_freq[entity] = self.entity_frequencies.get(entity, 1)
        
        # 生成词云
        wc.generate_from_frequencies(word_freq)
        
        # 修改词云颜色以区分不同类型的实体
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            entity_type = self.entity_types.get(word, None)
            if entity_type == entity_type1:
                return self.ENTITY_COLOR_MAP.get(entity_type1, '#FF6B6B')
            elif entity_type == entity_type2:
                return self.ENTITY_COLOR_MAP.get(entity_type2, '#4ECDC4')
            else:
                return '#333333'
        
        wc.recolor(color_func=color_func, random_state=42)
        
        # 绘制和保存
        plt.figure(figsize=(14, 7))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title(f'无锡政策知识图谱 - {entity_type1} 与 {entity_type2} 实体共现词云', fontsize=16, pad=20)
        
        output_path = os.path.join(self.output_dir, f'wordcloud_cooccurrence_{entity_type1}_{entity_type2}.png')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"实体共现词云已保存: {output_path}")
    
    def run_all_wordclouds(self):
        """生成所有词云可视化"""
        print("开始生成词云可视化...")
        
        # 生成各类型实体词云
        for entity_type in self.ENTITY_COLOR_MAP.keys():
            if entity_type in self.entity_by_type:
                self.generate_entity_wordcloud_by_type(entity_type)
        
        # 生成关系类型词云
        self.generate_relation_wordcloud()
        
        # 生成综合实体词云
        self.generate_combined_wordcloud()
        
        # 生成实体共现词云（选择数据中实际存在的类型组合）
        important_pairs = [
            ('location', 'land_use'),
            ('concept', 'indicator')
        ]
        
        # 只使用数据中实际存在的类型组合
        valid_pairs = []
        for type1, type2 in important_pairs:
            if type1 in self.entity_by_type and type2 in self.entity_by_type:
                valid_pairs.append((type1, type2))
        
        if valid_pairs:
            for type1, type2 in valid_pairs:
                self.generate_co_occurrence_wordcloud(type1, type2)
        else:
            print("警告: 没有找到有效的实体类型组合用于共现词云")
        
        print("所有词云可视化生成完成！")

def main():
    """主函数"""
    # 设置文件路径
    kg_file = 'results/knowledge_graph_enhanced.json'
    
    # 检查文件是否存在
    if not os.path.exists(kg_file):
        print(f"错误: 未找到知识图谱文件 {kg_file}")
        print("请先运行 main_wuxi.py 生成知识图谱数据")
        return
    
    # 创建词云生成器实例
    wordcloud_gen = WuxiPolicyWordCloudGenerator(kg_file)
    
    # 加载数据
    wordcloud_gen.load_data()
    
    # 生成所有词云
    wordcloud_gen.run_all_wordclouds()

if __name__ == '__main__':
    # 显示使用说明
    print("="*80)
    print("无锡政策知识图谱词云可视化工具")
    print("用于生成不同属性切面的词云，适用于顶级期刊论文")
    print("="*80)
    
    # 运行主函数
    main()