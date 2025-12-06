"""知识图谱构建模块"""
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager
import json
from typing import List, Tuple, Dict

class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entity_types = {}
        self.relation_types = {}
    
    def add_triplet(self, head: str, relation: str, tail: str, 
                   head_type: str = None, tail_type: str = None, rel_type: str = None):
        """添加三元组到图"""
        # 添加节点
        if not self.graph.has_node(head):
            self.graph.add_node(head, type=head_type)
            if head_type:
                self.entity_types[head] = head_type
        
        if not self.graph.has_node(tail):
            self.graph.add_node(tail, type=tail_type)
            if tail_type:
                self.entity_types[tail] = tail_type
        
        # 添加边
        self.graph.add_edge(head, tail, relation=relation, type=rel_type)
        if rel_type:
            self.relation_types[relation] = rel_type
    
    def get_stats(self) -> Dict:
        """获取图谱统计信息"""
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'entity_types': dict(sorted({t: list(self.entity_types.values()).count(t) 
                                        for t in set(self.entity_types.values())}.items())),
            'relation_types': dict(sorted({t: list(self.relation_types.values()).count(t) 
                                          for t in set(self.relation_types.values())}.items()))
        }
    
    def visualize(self, output_path: str = 'kg_visualization.png', sample_size: int = 50):
        """可视化知识图谱（采样）"""
        # 采样节点
        if self.graph.number_of_nodes() > sample_size:
            central_nodes = sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)[:sample_size]
            sampled_nodes = [n[0] for n in central_nodes]
            subgraph = self.graph.subgraph(sampled_nodes)
        else:
            subgraph = self.graph
        
        plt.figure(figsize=(20, 15))
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 布局
        pos = nx.spring_layout(subgraph, k=2, iterations=50)
        
        # 绘制节点
        node_colors = []
        color_map = {
            'location': '#FF6B6B',
            'land_use': '#4ECDC4',
            'concept': '#45B7D1',
            'planned_activity': '#FFA07A',
            'direction': '#98D8C8'
        }
        
        for node in subgraph.nodes():
            node_type = self.entity_types.get(node, 'unknown')
            node_colors.append(color_map.get(node_type, '#CCCCCC'))
        
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, 
                              node_size=1000, alpha=0.8)
        nx.draw_networkx_labels(subgraph, pos, font_size=8)
        
        # 绘制边
        nx.draw_networkx_edges(subgraph, pos, edge_color='gray', 
                              arrows=True, arrowsize=15, alpha=0.5)
        
        plt.title(f'Planning Knowledge Graph (Sampled {len(subgraph.nodes())} nodes)', 
                 fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
    
    def save(self, output_path: str = 'knowledge_graph.json'):
        """保存知识图谱"""
        data = {
            'nodes': [
                {
                    'id': node,
                    'type': self.entity_types.get(node, 'unknown')
                }
                for node in self.graph.nodes()
            ],
            'edges': [
                {
                    'source': u,
                    'target': v,
                    'relation': data.get('relation', ''),
                    'type': self.relation_types.get(data.get('relation', ''), 'unknown')
                }
                for u, v, data in self.graph.edges(data=True)
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)