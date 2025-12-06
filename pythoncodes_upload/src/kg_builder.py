"""知识图谱构建模块 - 改进版"""
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager
import json
from typing import List, Tuple, Dict

class KnowledgeGraphBuilder:
    """知识图谱构建器"""
    
    # 实体类型规则
    ENTITY_TYPE_RULES = {
        'location': ['市', '区', '县', '镇', '街道', '村', '路', '街', '广场', '园区',
                     '江', '河', '湖', '山', '丘陵', '平原', '地区', '流域', '水域'],
        'land_use': ['用地', '空间', '农田', '耕地', '林地', '绿地', '建设用地', '国土', '土地'],
        'concept': ['发展', '建设', '保护', '管理', '规划', '战略', '目标', '定位', '格局', 
                    '体系', '网络', '布局', '结构', '模式', '生态', '文化', '经济'],
        'facility': ['设施', '基础设施', '公共服务', '交通', '道路', '桥梁', '管网', '系统'],
        'indicator': ['率', '量', '度', '指标', '标准', '比例', '规模', '密度', '强度']
    }
    
    # 关系类型规则
    RELATION_TYPE_RULES = {
        'development': ['建设', '推进', '发展', '打造', '实施', '开展', '加快', '促进'],
        'conservation': ['保护', '维护', '保留', '守护', '控制', '严守'],
        'restriction': ['限制', '禁止', '不得', '严禁', '防止'],
        'regulation': ['协调', '统筹', '整合', '引导', '优化', '提升', '改善'],
        'explanation': ['位于', '包含', '属于', '是', '为', '有', '达到']
    }
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entity_types = {}
        self.relation_types = {}
    
    def _auto_classify_entity(self, entity: str) -> str:
        """自动分类实体"""
        for entity_type, keywords in self.ENTITY_TYPE_RULES.items():
            if any(kw in entity for kw in keywords):
                return entity_type
        return 'concept'
    
    def _auto_classify_relation(self, relation: str) -> str:
        """自动分类关系"""
        for rel_type, keywords in self.RELATION_TYPE_RULES.items():
            if any(kw in relation for kw in keywords):
                return rel_type
        return 'explanation'
    
    def add_triplet(self, head: str, relation: str, tail: str, 
                   head_type: str = None, tail_type: str = None, rel_type: str = None):
        """添加三元组到图（自动分类）"""
        # 自动分类实体类型
        if not head_type:
            head_type = self._auto_classify_entity(head)
        if not tail_type:
            tail_type = self._auto_classify_entity(tail)
        if not rel_type:
            rel_type = self._auto_classify_relation(relation)
        
        # 添加节点
        if not self.graph.has_node(head):
            self.graph.add_node(head, type=head_type)
            self.entity_types[head] = head_type
        
        if not self.graph.has_node(tail):
            self.graph.add_node(tail, type=tail_type)
            self.entity_types[tail] = tail_type
        
        # 添加边
        self.graph.add_edge(head, tail, relation=relation, type=rel_type)
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
            'facility': '#98D8C8',
            'indicator': '#FFD93D'
        }
        
        for node in subgraph.nodes():
            node_type = self.entity_types.get(node, 'concept')
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
                    'type': self.entity_types.get(node, 'concept')
                }
                for node in self.graph.nodes()
            ],
            'edges': [
                {
                    'source': u,
                    'target': v,
                    'relation': data.get('relation', ''),
                    'type': self.relation_types.get(data.get('relation', ''), 'explanation')
                }
                for u, v, data in self.graph.edges(data=True)
            ],
            'stats': self.get_stats()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)