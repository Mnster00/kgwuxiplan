# LLM4KG-Planning: LLM-Based Urban Planning Knowledge Graph Construction

# LLM-Driven Relation Extraction for Complex Knowledge Graph: A Land Plan Study in Wuxi

## Project Overview

This project implements an urban planning knowledge graph construction system based on large language models (LLMs). It can automatically identify entities, extract relationships, and build knowledge graphs from urban planning texts. The project supports multi-city planning text processing and provides visualization functionality.

## Core Features

1. **Named Entity Recognition (NER)**：Identify planning-related entities from planning texts
2. **Relationship Extraction (RE)**：Extract semantic relationships between entities
3. **Triple Evaluation**：Filter high-quality triples using LLM-based judgment mechanisms
4. **Knowledge Graph Construction**：Automatically build urban planning knowledge graphs
5. **Visualization Display**：Provide knowledge graph visualization and word cloud generation functions

## Project Structure

```
├── config.py                # API configuration file
├── data/                    # Data directory
│   └── wuxi_plan.txt        # Wuxi planning text example
├── main_wuxi.py             # Wuxi planning processing program
├── prompts/                 # Prompt template directory
│   ├── classify_prompt.py   # Classification prompt
│   ├── eval_prompt.py       # Evaluation prompt
│   ├── init.py
│   ├── ner_prompt.py        # NER prompt
│   └── re_prompt.py         # Relationship extraction prompt
├── results/                 # Results output directory
│   ├── extraction_results.json  # Entity and relationship extraction results
│   ├── knowledge_graph.json     # Knowledge graph data
│   └── kg_sample.png            # Knowledge graph visualization
├── src/                     # Source code directory
│   ├── evaluator.py         # Triple evaluator
│   ├── kg_builder.py        # Knowledge graph builder
│   ├── llm_client.py        # LLM client
│   ├── ner_extractor.py     # Named entity recognizer
│   └── relation_extractor.py # Relationship extractor
├── visualize_wuxi_policy_kawa.py  # Visualization tool
├── wuxi_policy_wordcloud.py       # Word cloud generation tool
├── requirements.txt         # Dependencies list
└── readme.md                # Project documentation
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` and fill in your API keys:

```python
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
```

### 3. Prepare Data

Place urban planning texts in the `data/` directory with filenames in the format `city_name_plan.txt` (e.g., `wuxi_plan.txt`).

### 4. Run the Program

Run the corresponding main program based on the city you need to process:

```bash
# Process Wuxi planning
python main_wuxi.py
```

## Output Results

After the program runs, results will be saved in the `results/` directory:

- `extraction_results.json`: Contains identified entities and extracted relationship information
- `knowledge_graph.json`: Completed knowledge graph data
- `kg_sample.png`: Visualization of the knowledge graph (sample display)

## Visualization Features

### Knowledge Graph Visualization

Use the following command to generate knowledge graph visualization:

```bash
python visualize_wuxi_policy_kawa.py
```

### Word Cloud Generation

Use the following command to generate a word cloud from planning texts:

```bash
python wuxi_policy_wordcloud.py
```


### Model Division

| Task | Model Used |
|------|---------|
| Named Entity Recognition | DeepSeek | 
| Relationship Extraction | Glm-4.5 + DeepSeek + Qwen| 
| Triple Evaluation | Qwen | 





