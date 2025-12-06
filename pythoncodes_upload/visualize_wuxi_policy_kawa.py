"""Wuxi Policy Multi-dimensional Knowledge Graph Visualization Tool"""
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from collections import Counter
import community as community_louvain  # 用于社区检测
from typing import Dict, List, Set, Tuple

from matplotlib.patches import PathPatch
from matplotlib.patheffects import PathPatchEffect, Stroke

# 设置中文字体和期刊级样式，确保清晰可读
# 设置中文字体，确保中文正常显示
plt.rcParams['font.family'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'DejaVu Sans', 'Times New Roman']
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']  # 确保中文显示
plt.rcParams['font.size'] = 12  # 基础字体大小
plt.rcParams['axes.titlesize'] = 16  # 标题字体大小
plt.rcParams['axes.labelsize'] = 14  # 坐标轴标签字体大小
plt.rcParams['xtick.labelsize'] = 12  # X轴刻度字体大小
plt.rcParams['ytick.labelsize'] = 12  # Y轴刻度字体大小
plt.rcParams['legend.fontsize'] = 12  # 图例字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
plt.rcParams['figure.dpi'] = 300  # 设置默认DPI



class WuxiPolicyVisualizer:
    """Wuxi Policy Knowledge Graph Visualization Class"""
    
    # 实体类型颜色映射 - 精心设计的配色方案
    ENTITY_COLOR_MAP = {
        'location': '#FF6B6B',      # Red - Geographic Location
        'land_use': '#4ECDC4',      # Cyan - Land Use
        'concept': '#45B7D1',       # Blue - Planning Concept
        'facility': '#98D8C8',      # Green - Facility
        'indicator': '#FFD93D',     # Yellow - Indicator
        'planned_activity': '#FFA07A', # Orange - Planned Activity
        'direction': '#C9A0DC'      # Purple - Direction
    }
    
    # 关系类型颜色映射
    RELATION_COLOR_MAP = {
        'development': '#388E3C',    # Forest Green - Development Relation
        'conservation': '#1976D2',   # Deep Blue - Conservation Relation
        'restriction': '#D32F2F',    # Deep Red - Restriction Relation
        'regulation': '#7B1FA2',     # Deep Purple - Regulation Relation
        'explanation': '#616161'     # Dark Grey - Explanation Relation
    }
    
    # 布局类型字典
    LAYOUTS = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'spectral': nx.spectral_layout,
        'random': nx.random_layout
    }
    
    def __init__(self, kg_file: str):
        """Initialize Visualizer"""
        self.kg_file = kg_file
        self.G = nx.MultiDiGraph()
        self.entity_types = {}
        self.relation_types = {}
        self.load_data()
        # 创建输出目录
        self.output_dir = os.path.abspath('results_wuxi_visualizations0')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_data(self):
        """Load Knowledge Graph Data"""
        print(f"加载知识图谱数据: {self.kg_file}")
        with open(self.kg_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 添加节点
        for node in data['nodes']:
            self.G.add_node(node['id'], type=node['type'])
            self.entity_types[node['id']] = node['type']
        
        # 添加边
        for edge in data['edges']:
            self.G.add_edge(edge['source'], edge['target'], 
                           relation=edge['relation'], 
                           type=edge['type'])
            self.relation_types[edge['relation']] = edge['type']
        
        print(f"成功加载知识图谱: {len(self.G.nodes())} 个节点, {len(self.G.edges())} 条边")
    
    def get_stats(self) -> Dict:
        """Get Statistics"""
        entity_counts = Counter(self.entity_types.values())
        relation_counts = Counter(self.relation_types.values())
        
        return {
            'nodes': len(self.G.nodes()),
            'edges': len(self.G.edges()),
            'entity_types': dict(entity_counts),
            'relation_types': dict(relation_counts)
        }
    
    def plot_entity_type_distribution(self):
        """Plot Entity Type Distribution - Basic Statistical Analysis"""
        plt.figure(figsize=(4, 4))
        stats = self.get_stats()
        
        types = list(stats['entity_types'].keys())
        counts = list(stats['entity_types'].values())
        colors = [self.ENTITY_COLOR_MAP.get(t, '#CCCCCC') for t in types]
        
        # 按数量排序，使图表更清晰
        sorted_data = sorted(zip(types, counts, colors), key=lambda x: x[1], reverse=True)
        types, counts, colors = zip(*sorted_data)
        
        bars = plt.bar(types, counts, color=colors, alpha=0.8)
        plt.xlabel('Entity Type')
        plt.ylabel('Count')
        #plt.title('Wuxi Policy Knowledge Graph Entity Type Distribution')
        plt.xticks(rotation=0, ha='center')
        
        # 添加数值标签，提高可读性
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'entity_type_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Entity type distribution chart saved: {output_path}")
    
    def plot_relation_type_distribution(self):
        """Plot Relation Type Distribution - Basic Statistical Analysis"""
        plt.figure(figsize=(10, 4))
        stats = self.get_stats()
        
        types = list(stats['relation_types'].keys())
        counts = list(stats['relation_types'].values())
        colors = [self.RELATION_COLOR_MAP.get(t, '#CCCCCC') for t in types]
        
        # 按数量排序
        sorted_data = sorted(zip(types, counts, colors), key=lambda x: x[1], reverse=True)
        types, counts, colors = zip(*sorted_data)
        
        bars = plt.bar(types, counts, color=colors, alpha=0.8)
        plt.xlabel('Relation Type')
        plt.ylabel('Count')
        #plt.title('Wuxi Policy Knowledge Graph Relation Type Distribution')
        plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'relation_type_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Relation type distribution chart saved: {output_path}")
    
    def plot_knowledge_graph_by_entity_type(self, entity_type: str, sample_size: int = 50):
        """Plot Knowledge Graph by Entity Type - Focus on Specific Entity Type"""
        # 筛选指定类型的节点及其邻居
        target_nodes = [n for n, attr in self.G.nodes(data=True) if attr.get('type') == entity_type]
        
        if not target_nodes:
            print(f"Entity type not found: {entity_type}")
            return
        
        # 构建子图（包含目标节点及其邻居）
        nodes_to_include = set(target_nodes)
        for node in target_nodes:
            nodes_to_include.update(list(self.G.neighbors(node)))
            nodes_to_include.update([n for n in self.G.predecessors(node)])
        
        # 如果节点太多，采样中心性最高的节点
        if len(nodes_to_include) > sample_size:
            # 计算度中心性
            centrality = nx.degree_centrality(self.G.subgraph(nodes_to_include))
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            nodes_to_include = [n for n, c in sorted_nodes[:sample_size]]
        
        subgraph = self.G.subgraph(nodes_to_include)
        
        plt.figure(figsize=(8, 6))  # 增加图形大小
        # 使用kamada_kawai布局，增加scale参数值以增加节点间距
        pos = self.LAYOUTS['kamada_kawai'](subgraph, dist=None, scale=50.0)  # 增加scale值
        
        # 绘制节点，目标类型的节点更大更突出，但减小整体大小避免重叠
        node_colors = []
        node_sizes = []
        for node in subgraph.nodes():
            # 设置颜色
            node_type = self.entity_types.get(node, 'concept')
            node_colors.append(self.ENTITY_COLOR_MAP.get(node_type, '#CCCCCC'))
            # 设置大小（目标类型的节点更大，但整体减小）
            size = 1200 if node_type == entity_type else 500  # 减小节点大小
            node_sizes.append(size)
        
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                             node_size=700, alpha=0.8, linewidths=1.0, edgecolors='k')  # 使用动态节点大小
        
        # 绘制边（根据关系类型着色）
        edge_colors = []
        for u, v, data in subgraph.edges(data=True):
            rel_type = data.get('type', 'explanation')
            edge_colors.append(self.RELATION_COLOR_MAP.get(rel_type, '#CCCCCC'))
        
        nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors, 
                             arrows=True, arrowsize=6, alpha=0.7, width=1.0)  # 调整箭头大小和边的宽度
        
        # 绘制标签，减小字体大小并添加字体白边效果
        text_objects = nx.draw_networkx_labels(subgraph, pos, font_size=7, font_weight='bold')
        for _, text in text_objects.items():
            text.set_path_effects([PathPatchEffect(offset=(0, 0), facecolor='black', edgecolor='white', linewidth=0.12)])

        plt.axis('off')
        
        output_path = os.path.join(self.output_dir, f'kg_by_entity_type_{entity_type}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Knowledge graph by entity type {entity_type} saved: {output_path}")
    
    def plot_knowledge_graph_by_relation_type(self, relation_type: str, sample_size: int = 50):
        """Plot Knowledge Graph by Relation Type - Focus on Specific Relation Type"""
        # 筛选指定类型的边
        target_edges = [(u, v, data) for u, v, data in self.G.edges(data=True) 
                       if data.get('type') == relation_type]
        
        if not target_edges:
            print(f"Relation type not found: {relation_type}")
            return
        
        # 构建子图
        nodes_to_include = set()
        for u, v, _ in target_edges:
            nodes_to_include.add(u)
            nodes_to_include.add(v)
        
        # 如果节点太多，采样
        if len(nodes_to_include) > sample_size:
            # 计算在目标关系中的度
            relation_degree = {}
            for u, v, _ in target_edges:
                relation_degree[u] = relation_degree.get(u, 0) + 1
                relation_degree[v] = relation_degree.get(v, 0) + 1
            
            sorted_nodes = sorted(relation_degree.items(), key=lambda x: x[1], reverse=True)
            nodes_to_include = [n for n, d in sorted_nodes[:sample_size]]
            target_edges = [(u, v, data) for u, v, data in target_edges 
                          if u in nodes_to_include and v in nodes_to_include]
        
        # 创建只包含目标边的图
        subgraph = nx.DiGraph()
        subgraph.add_nodes_from(nodes_to_include)
        for u, v, data in target_edges:
            subgraph.add_edge(u, v, relation=data.get('relation', ''))
        
        plt.figure(figsize=(8, 6), dpi=300)  # 增加图形大小
        pos = self.LAYOUTS['kamada_kawai'](subgraph, dist=None, scale=50.0)  # 增加scale值以增加节点间距
        
        # 绘制节点，减小节点大小避免重叠
        node_colors = []
        for node in subgraph.nodes():
            node_type = self.entity_types.get(node, 'concept')
            node_colors.append(self.ENTITY_COLOR_MAP.get(node_type, '#CCCCCC'))
        
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                             node_size=700, alpha=0.8, linewidths=1.0, edgecolors='k')  # 减小节点大小
        
        # 绘制边（统一使用关系类型颜色）
        edge_color = self.RELATION_COLOR_MAP.get(relation_type, '#FF6B6B')
        nx.draw_networkx_edges(subgraph, pos, edge_color=edge_color, 
                             arrows=True, arrowsize=6, alpha=0.7, width=1.0)  # 调整箭头大小和边的宽度
        
        # 绘制标签，减小字体大小并添加字体白边效果
        text_objects = nx.draw_networkx_labels(subgraph, pos, font_size=7, font_weight='bold')
        for _, text in text_objects.items():
            text.set_path_effects([PathPatchEffect(offset=(0, 0), facecolor='black', edgecolor='white', linewidth=0.12)])

        plt.axis('off')

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, f'kg_by_relation_type_{relation_type}.png')
        try:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Knowledge graph by relation type {relation_type} saved: {output_path}")
        except Exception as e:
            print(f"Error saving image: {e}")
        finally:
            plt.close()  # 确保关闭图形，释放资源
    
    def plot_communities(self, sample_size: int = 100):
        """Plot Community Structure - Advanced Network Analysis"""
        # 为了社区检测，转换为无向图
        undirected_G = self.G.to_undirected()
        
        # 采样
        if undirected_G.number_of_nodes() > sample_size:
            centrality = nx.degree_centrality(undirected_G)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            sampled_nodes = [n for n, c in sorted_nodes[:sample_size]]
            undirected_G = undirected_G.subgraph(sampled_nodes)
        
        # 社区检测 - 使用Louvain算法
        partition = community_louvain.best_partition(undirected_G)
        n_communities = max(partition.values()) + 1
        
        plt.figure(figsize=(20, 15), dpi=300)
        pos = self.LAYOUTS['kamada_kawai'](undirected_G, dist=None, scale=15.0)  # 使用kamada_kawai布局并设置合适的缩放参数
        
        # 为每个社区分配颜色
        cmap = cm.get_cmap('viridis', n_communities)
        colors = [cmap(partition[node]) for node in undirected_G.nodes()]
        
        # 绘制节点
        nx.draw_networkx_nodes(undirected_G, pos, node_color=colors, 
                             node_size=2000, alpha=0.8, linewidths=1, edgecolors='k')  # 增加边框
        
        # 绘制边
        nx.draw_networkx_edges(undirected_G, pos, edge_color='gray', 
                             alpha=0.5, arrows=False, width=1.5)  # 调整边的透明度和宽度
        
        # 绘制标签
        nx.draw_networkx_labels(subgraph, pos, font_size=10, font_weight='bold', bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))  # 增加背景和加粗字体
        
        #plt.title(f'Wuxi Policy Knowledge Graph - Community Structure Analysis ({n_communities} Communities)', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'kg_communities.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Community structure diagram saved: {output_path}")
    
    def plot_centrality_analysis(self):
        """Plot Centrality Analysis - Identify Key Nodes"""
        # 计算中心性 - 只保留度中心性（Degree Centrality）
        degree_centrality = nx.degree_centrality(self.G)
        
        # 排序并取前20个
        sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # 创建单个子图
        fig, ax = plt.subplots(1, 1, figsize=(5, 6))
        
        # 度中心性（Degree Centrality）
        nodes, centrality_values = zip(*sorted_degree)
        colors = [self.ENTITY_COLOR_MAP.get(self.entity_types.get(n, 'concept'), '#CCCCCC') for n in nodes]
        bars = ax.barh(range(len(nodes)), centrality_values, color=colors, alpha=0.8)
        ax.set_yticks(range(len(nodes)))
        ax.set_yticklabels(nodes)
        ax.invert_yaxis()
        ax.set_xlabel('Degree Centrality')
        ax.set_title('Urban Policy Knowledge Graph - Degree Centrality Analysis (Top 20)', fontweight='bold')
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'centrality_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Centrality analysis chart saved: {output_path}")
    
    def plot_full_knowledge_graph(self, sample_size: int = 150):
        """Plot Full Knowledge Graph with All Nodes and Edges"""
        # 采样，避免图形过于复杂
        if self.G.number_of_nodes() > sample_size:
            centrality = nx.degree_centrality(self.G)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            sampled_nodes = [n for n, c in sorted_nodes[:sample_size]]
            subgraph = self.G.subgraph(sampled_nodes)
            print(f"Sampling {sample_size} nodes from {self.G.number_of_nodes()} total nodes")
        else:
            subgraph = self.G
            print(f"Plotting all {subgraph.number_of_nodes()} nodes and {subgraph.number_of_edges()} edges")
        
        plt.figure(figsize=(12, 6), dpi=300)
        # 使用kamada_kawai布局，优化参数使图形更美观且节点分布更均匀
        pos = self.LAYOUTS['kamada_kawai'](subgraph, dist=None, scale=3.0)
        
        # 节点颜色根据实体类型
        node_colors = []
        node_sizes = []
        for node in subgraph.nodes():
            node_type = self.entity_types.get(node, 'concept')
            node_colors.append(self.ENTITY_COLOR_MAP.get(node_type, '#CCCCCC'))
            # 根据节点类型设置不同大小
            size = 400
            node_sizes.append(size)
        
        # 绘制节点
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors,
                             node_size=node_sizes, alpha=0.8, linewidths=0.2, edgecolors='k')
        
        # 绘制边（根据关系类型着色）
        edge_colors = []
        for u, v, data in subgraph.edges(data=True):
            rel_type = data.get('type', 'explanation')
            edge_colors.append(self.RELATION_COLOR_MAP.get(rel_type, '#CCCCCC'))
        
        nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors,
                             arrows=True, arrowsize=5, alpha=0.2, width=0.7)
        
        # 绘制标签
        # nx.draw_networkx_labels(subgraph, pos, font_size=7, font_weight='bold')
        # 绘制标签，减小字体大小并添加字体白边效果
        text_objects = nx.draw_networkx_labels(subgraph, pos, font_size=6, font_weight='bold')
        for _, text in text_objects.items():
            text.set_path_effects([PathPatchEffect(offset=(0, 0), facecolor='black', edgecolor='white', linewidth=0.1)])
        
        #plt.title('Wuxi Policy Complete Knowledge Graph', fontsize=20, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        output_path = os.path.join(self.output_dir, 'full_knowledge_graph.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Full knowledge graph saved: {output_path}")
    
    def plot_multiple_layouts(self, sample_size: int = 70):
        """Plot Knowledge Graph with Multiple Layouts - Multi-angle Display"""
        # 采样
        if self.G.number_of_nodes() > sample_size:
            centrality = nx.degree_centrality(self.G)
            sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
            sampled_nodes = [n for n, c in sorted_nodes[:sample_size]]
            subgraph = self.G.subgraph(sampled_nodes)
        else:
            subgraph = self.G
        
        # 只使用kamada_kawai布局
        selected_layouts = ['kamada_kawai']
        
        # 创建图形和坐标轴，处理只有一个布局的情况
        if len(selected_layouts) == 1:
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            layout_name = selected_layouts[0]
            
            # 为布局函数设置合适的参数
            if layout_name == 'kamada_kawai':
                pos = self.LAYOUTS[layout_name](subgraph, dist=None, scale=15.0)  # 增加scale参数扩大布局范围
            else:  # 其他布局
                pos = self.LAYOUTS[layout_name](subgraph)
            
            # 节点颜色
            node_colors = []
            for node in subgraph.nodes():
                node_type = self.entity_types.get(node, 'concept')
                node_colors.append(self.ENTITY_COLOR_MAP.get(node_type, '#CCCCCC'))
            
            # 绘制
            nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                                 node_size=600, alpha=0.8, linewidths=1, edgecolors='k', ax=ax)  # 调整节点大小减少重叠
            nx.draw_networkx_edges(subgraph, pos, edge_color='gray', 
                                 alpha=0.7, ax=ax, width=1.2)  # 调整边的透明度和宽度
            nx.draw_networkx_labels(subgraph, pos, font_size=6, font_weight='bold', ax=ax, bbox=dict(facecolor='white', alpha=0.3, edgecolor='none', boxstyle='round,pad=0.1'))  # 减小字体大小避免重叠
            
            #ax.set_title(f'{layout_name}布局')
            ax.axis('off')
        else:
            # 多个布局的情况（保留原逻辑）
            fig, axes = plt.subplots(1, len(selected_layouts), figsize=(10*len(selected_layouts), 10))
            
            for i, layout_name in enumerate(selected_layouts):
                # 为不同布局函数设置合适的参数
                if layout_name == 'kamada_kawai':
                    pos = self.LAYOUTS[layout_name](subgraph, dist=None, scale=15.0)  # 增加scale参数扩大布局范围
                else:  # 其他布局
                    pos = self.LAYOUTS[layout_name](subgraph)
                
                # 节点颜色
                node_colors = []
                for node in subgraph.nodes():
                    node_type = self.entity_types.get(node, 'concept')
                    node_colors.append(self.ENTITY_COLOR_MAP.get(node_type, '#CCCCCC'))
                
                # 绘制
                ax = axes[i]
                nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                                     node_size=600, alpha=0.8, linewidths=1, edgecolors='k', ax=ax)  # 调整节点大小减少重叠
                nx.draw_networkx_edges(subgraph, pos, edge_color='gray', 
                                     alpha=0.7, ax=ax, width=1.2)  # 调整边的透明度和宽度
                nx.draw_networkx_labels(subgraph, pos, font_size=6, font_weight='bold', ax=ax, bbox=dict(facecolor='white', alpha=0.3, edgecolor='none', boxstyle='round,pad=0.1'))  # 减小字体大小避免重叠
                
                #ax.set_title(f'{layout_name}布局')
                ax.axis('off')
        
        #('Wuxi Policy Knowledge Graph - Different Layouts Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'multiple_layouts.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Multiple layouts comparison chart saved: {output_path}")
    
    def run_all_visualizations(self):
        """Run All Visualizations - One-click Generate Complete Analysis"""
        print("="*80)
        print("Starting Wuxi Policy Knowledge Graph Multi-dimensional Visualization")
        print("="*80)
        
        # 基本统计
        stats = self.get_stats()
        print(f"\nKnowledge Graph Statistics:")
        print(f"Total Nodes: {stats['nodes']}")
        print(f"Total Edges: {stats['edges']}")
        print(f"Entity Types: {stats['entity_types']}")
        print(f"Relation Types: {stats['relation_types']}")
        
        # 1. Plot Distribution Charts
        self.plot_entity_type_distribution()
        self.plot_relation_type_distribution()
        
        # 2. Plot Knowledge Graph by Entity Types
        print("\nPlotting knowledge graphs by entity types:")
        for entity_type in stats['entity_types'].keys():
            if stats['entity_types'][entity_type] > 5:  # Only plot types with sufficient count
                self.plot_knowledge_graph_by_entity_type(entity_type, sample_size=50)
        
        # 3. Plot Knowledge Graph by Relation Types
        print("\nPlotting knowledge graphs by relation types:")
        for relation_type in stats['relation_types'].keys():
            if stats['relation_types'][relation_type] > 5:  # Only plot types with sufficient count
                self.plot_knowledge_graph_by_relation_type(relation_type, sample_size=50)
        
        # 4. Full Knowledge Graph Visualization
        print("\nGenerating full knowledge graph visualization:")
        self.plot_full_knowledge_graph(sample_size=170)
        
        # 5. Advanced Analysis Visualization
        print("\nGenerating advanced analysis visualizations:")
        try:
            self.plot_communities(sample_size=300)
        except Exception as e:
            print(f"Community detection failed: {str(e)}")
            print("Please install python-louvain library: pip install python-louvain")
        
        self.plot_centrality_analysis()
        self.plot_multiple_layouts(sample_size=100)
        
        print("\n" + "="*80)
        print(f"All visualization results saved to: {self.output_dir}")
        print("="*80)

if __name__ == '__main__':
    # Main function
    kg_file = 'results/knowledge_graph_enhanced.json'
    
    if not os.path.exists(kg_file):
        print(f"Error: Knowledge graph file {kg_file} not found")
        print("Please run main_wuxi.py first to generate knowledge graph data")
    else:
        visualizer = WuxiPolicyVisualizer(kg_file)
        visualizer.run_all_visualizations()