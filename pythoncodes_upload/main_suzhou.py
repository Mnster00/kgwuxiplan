"""主程序"""
import os
import json
from config import TASK_MODEL_MAP
from src.ner_extractor import NERExtractor
from src.relation_extractor import RelationExtractor
from src.evaluator import TripletEvaluator
from src.kg_builder import KnowledgeGraphBuilder

def load_text(file_path: str) -> list:
    """加载规划文本并分句"""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 简单分句
    import re
    sentences = re.split(r'[。！？]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    return sentences

def print_banner():
    """打印标题"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║  LLM-based Knowledge Graph Construction for Urban Planning  ║
║                    基于大模型的规划知识图谱构建                    ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """主流程"""
    print_banner()
    
    # 初始化模块
    print("\n[1/6] 初始化NLP模块...")
    print(f"   使用模型配置: NER={TASK_MODEL_MAP['ner']}, RE={TASK_MODEL_MAP['re']}, Eval={TASK_MODEL_MAP['eval']}")
    
    ner = NERExtractor()
    re_extractor = RelationExtractor()
    evaluator = TripletEvaluator()
    kg_builder = KnowledgeGraphBuilder()
    
    # 加载规划文本
    print("\n[2/6] 加载规划文本...")
    if not os.path.exists('data/suzhou_plan.txt'):
        print("错误: data/wuxi_plan.txt 不存在")
        return
    
    sentences = load_text('data/suzhou_plan.txt')
    print(f"共加载 {len(sentences)} 个句子")
    
    # 处理句子
    print("\n[3/6] 开始知识抽取...")
    max_sentences = min(15, len(sentences))  # 限制数量
    max_sentences = len(sentences)
    print(f"处理前 {max_sentences} 个句子（可修改config.py调整）\n")
    
    all_results = []
    total_entities = 0
    total_triplets = 0
    
    for i, sent in enumerate(sentences[:max_sentences], 1):
        print(f"   [{i}/{max_sentences}] {sent[:]}...")
        
        try:
            # NER
            entities = ner.extract(sent)
            entity_count = sum(len(v) for v in entities.values())
            total_entities += entity_count
            print(f"提取实体: {entity_count} 个")
            
            # RE
            context = ' '.join(sentences[max(0, i-2):min(len(sentences), i+1)])
            triplets = re_extractor.extract(sent, entities, context)
            print(f"提取三元组: {len(triplets)} 个")
            
            # 评估
            if triplets:
                filtered_triplets = evaluator.evaluate(triplets, sent, context)
                print(f"评估后保留: {len(filtered_triplets)} 个")
            else:
                filtered_triplets = []
            
            total_triplets += len(filtered_triplets)
            
            # 添加到知识图谱
            for h, r, t in filtered_triplets:
                kg_builder.add_triplet(h, r, t)
            
            all_results.append({
                'sentence': sent,
                'entities': entities,
                'triplets': [f"<{h}, {r}, {t}>" for h, r, t in filtered_triplets]
            })
            
            print()
        
        except Exception as e:
            print(f"处理错误: {str(e)}\n")
            continue
    
    # 保存结果
    print("[4/6] 保存结果...")
    os.makedirs('results', exist_ok=True)
    
    with open('results_sz/extraction_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print("抽取结果已保存: results/extraction_results.json")
    
    kg_builder.save('results_sz/knowledge_graph.json')
    print("知识图谱已保存: results/knowledge_graph.json")
    
    # 统计
    print("\n[5/6]生成统计...")
    stats = kg_builder.get_stats()
    print(f"""
   知识图谱统计:
   ├─ 节点数: {stats['nodes']}
   ├─ 边数: {stats['edges']}
   ├─ 总实体数: {total_entities}
   └─ 总三元组数: {total_triplets}
""")
    
    if stats['entity_types']:
        print("   实体类型分布:")
        for etype, count in stats['entity_types'].items():
            print(f"   ├─ {etype}: {count}")
    
    # 可视化
    print("\n[6/6]生成可视化...")
    try:
        kg_builder.visualize('results_sz/kg_sample.png', sample_size=30)
        print("知识图谱已可视化: results/kg_sample.png")
    except Exception as e:
        print(f"可视化失败: {str(e)}")
    
    print("\n" + "="*60)
    print("完成！所有结果已保存到 results/ 目录")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
    except Exception as e:
        print(f"\n\n程序错误: {str(e)}")