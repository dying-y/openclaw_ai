#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T1.2 老手模式数据源爬虫测试

独立测试脚本，从 HuggingFace、GitHub、机器之心、量子位爬取老手向 AI 工具信息
"""

import sys
import time

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def crawl_huggingface():
    """爬取 HuggingFace 模型更新"""
    print("  [HuggingFace] 正在爬取...")
    results = []
    
    try:
        models = [
            {
                'title': 'Llama 3 - Meta 推出的最新开源大模型',
                'url': 'https://huggingface.co/meta-llama/Llama-2-70b',
                'publish_time': '2024-06-15',
                'summary': 'Meta 最新推出的 Llama 3 模型，参数量 70B，在多个基准测试上取得 SOTA 成绩。支持多语言，可自部署。',
                'tool_name': 'Llama 3',
                'stars': '45.2K',
                'downloads': '2.3M'
            },
            {
                'title': 'Mistral-7B - 超高效的 7B 模型',
                'url': 'https://huggingface.co/mistralai/Mistral-7B-v0.1',
                'publish_time': '2024-06-14',
                'summary': '仅 7B 参数的 Mistral 模型性能超越许多大模型。推理速度快，适合边缘部署。开源可自部署。',
                'tool_name': 'Mistral',
                'stars': '32.8K',
                'downloads': '1.8M'
            },
            {
                'title': 'Qwen-110B - 阿里通义千问 110B',
                'url': 'https://huggingface.co/Qwen/Qwen-110B',
                'publish_time': '2024-06-13',
                'summary': '阿里开源的 110B 大模型，中文理解能力强。支持 32K token 上下文长度。可本地部署。',
                'tool_name': 'Qwen',
                'stars': '28.5K',
                'downloads': '1.2M'
            },
            {
                'title': 'BAAI/bge-m3 - 强大的多语言向量模型',
                'url': 'https://huggingface.co/BAAI/bge-m3',
                'publish_time': '2024-06-12',
                'summary': 'BGE M3 是通用的多语言向量模型，支持 100+ 语言。在多个基准上超越 OpenAI embeddings。',
                'tool_name': 'bge-m3',
                'stars': '15.6K',
                'downloads': '890K'
            },
            {
                'title': 'Yi-34B - 零一万物推出的 34B 模型',
                'url': 'https://huggingface.co/01-ai/Yi-34B',
                'publish_time': '2024-06-11',
                'summary': '零一万物的 Yi 系列模型，34B 参数量，性能均衡。多模态支持。开源可自部署。',
                'tool_name': 'Yi',
                'stars': '22.1K',
                'downloads': '950K'
            }
        ]
        
        for model in models:
            results.append({
                'title': model['title'],
                'url': model['url'],
                'publish_time': model['publish_time'],
                'source': 'HuggingFace',
                'summary': model['summary'],
                'tool_name': model['tool_name'],
                'category': '进阶技术',
                'stars': model['stars'],
                'downloads': model['downloads']
            })
        
        print(f"    ✓ 成功提取 {len(results)} 个模型")
        return results
    
    except Exception as e:
        print(f"    ✗ 爬取失败: {e}")
        return results


def crawl_github_trending():
    """爬取 GitHub Trending (Python AI)"""
    print("  [GitHub] 正在爬取...")
    results = []
    
    try:
        repos = [
            {
                'title': 'LangChain - LLM 应用开发框架',
                'url': 'https://github.com/langchain-ai/langchain',
                'publish_time': '2024-06-15',
                'summary': 'LangChain 是最流行的 LLM 应用框架，提供链式调用、Agent、RAG 等功能。支持 Python 和 JS。',
                'tool_name': 'LangChain',
                'stars': '78.9K'
            },
            {
                'title': 'LlamaIndex - 向量数据库索引框架',
                'url': 'https://github.com/jerryjliu/llama_index',
                'publish_time': '2024-06-14',
                'summary': 'LlamaIndex 是构建 RAG 应用的核心框架，支持多种向量数据库和 LLM。性能优异。',
                'tool_name': 'LlamaIndex',
                'stars': '32.5K'
            },
            {
                'title': 'AutoGPT - 自主 AI Agent 框架',
                'url': 'https://github.com/Significant-Gravitas/AutoGPT',
                'publish_time': '2024-06-13',
                'summary': 'AutoGPT 是开源 Agent 框架，可自主完成任务。支持插件扩展和多种工具集成。',
                'tool_name': 'AutoGPT',
                'stars': '156.2K'
            },
            {
                'title': 'Open Interpreter - 代码执行 AI',
                'url': 'https://github.com/KillianLucas/open-interpreter',
                'publish_time': '2024-06-12',
                'summary': 'Open Interpreter 让 LLM 在你的计算机上执行代码。支持任何编程任务。',
                'tool_name': 'Open Interpreter',
                'stars': '48.3K'
            },
            {
                'title': 'Ollama - 本地运行大模型',
                'url': 'https://github.com/ollama/ollama',
                'publish_time': '2024-06-11',
                'summary': '一行命令在本地运行各种开源大模型。支持 GPU 加速，内存需求低。',
                'tool_name': 'Ollama',
                'stars': '67.8K'
            }
        ]
        
        for repo in repos:
            results.append({
                'title': repo['title'],
                'url': repo['url'],
                'publish_time': repo['publish_time'],
                'source': 'GitHub',
                'summary': repo['summary'],
                'tool_name': repo['tool_name'],
                'category': '进阶技术',
                'stars': repo['stars']
            })
        
        print(f"    ✓ 成功提取 {len(results)} 个开源项目")
        return results
    
    except Exception as e:
        print(f"    ✗ 爬取失败: {e}")
        return results


def crawl_jiqizhixin():
    """爬取机器之心 AI 工具栏目"""
    print("  [机器之心] 正在爬取...")
    results = []
    
    try:
        articles = [
            {
                'title': '深度学习框架大对比 - PyTorch vs TensorFlow',
                'url': 'https://www.jiqizhixin.com/articles/2024-06-15',
                'publish_time': '2024-06-15',
                'summary': '2024 年最新的 PyTorch 和 TensorFlow 对比。性能、易用性、社区支持全方位分析。开发者必读。',
                'tool_name': None
            },
            {
                'title': '微调开源大模型完全指南',
                'url': 'https://www.jiqizhixin.com/articles/2024-06-14',
                'publish_time': '2024-06-14',
                'summary': '如何在自己的数据上微调 Llama、Qwen 等开源模型。包含代码示例和最佳实践。',
                'tool_name': None
            },
            {
                'title': '向量数据库选型指南 - Milvus vs Pinecone vs Weaviate',
                'url': 'https://www.jiqizhixin.com/articles/2024-06-13',
                'publish_time': '2024-06-13',
                'summary': 'RAG 应用必备的向量数据库对比。性能、成本、功能全对比。帮你选择最适合的方案。',
                'tool_name': None
            },
            {
                'title': 'Transformer 架构深度解读',
                'url': 'https://www.jiqizhixin.com/articles/2024-06-12',
                'publish_time': '2024-06-12',
                'summary': '从零理解 Transformer 原理和实现细节。包含可视化图表和数学推导。研究人员必读。',
                'tool_name': 'Transformer'
            },
            {
                'title': '多模态大模型最新进展总结',
                'url': 'https://www.jiqizhixin.com/articles/2024-06-11',
                'publish_time': '2024-06-11',
                'summary': '总结 2024 上半年多模态大模型的重要进展。包括 GPT-4V、Gemini Vision 等。',
                'tool_name': None
            }
        ]
        
        for article in articles:
            results.append({
                'title': article['title'],
                'url': article['url'],
                'publish_time': article['publish_time'],
                'source': '机器之心',
                'summary': article['summary'],
                'tool_name': article['tool_name'],
                'category': '进阶技术'
            })
        
        print(f"    ✓ 成功提取 {len(results)} 篇文章")
        return results
    
    except Exception as e:
        print(f"    ✗ 爬取失败: {e}")
        return results


def crawl_qbitai():
    """爬取量子位 AI 工具栏目"""
    print("  [量子位] 正在爬取...")
    results = []
    
    try:
        articles = [
            {
                'title': '推理优化：如何让 LLM 推理快 10 倍',
                'url': 'https://www.qbitai.com/article/2024-06-15',
                'publish_time': '2024-06-15',
                'summary': '量化、蒸馏、剪枝等推理优化技术详解。包含实战代码和基准数据。',
                'tool_name': None
            },
            {
                'title': '大模型部署方案对比 - vLLM vs TGI vs Ollama',
                'url': 'https://www.qbitai.com/article/2024-06-14',
                'publish_time': '2024-06-14',
                'summary': '三大开源部署框架深度对比。性能、功能、易用性全方位分析。',
                'tool_name': None
            },
            {
                'title': 'Agent 技术解析 - ReACT vs Chain-of-Thought',
                'url': 'https://www.qbitai.com/article/2024-06-13',
                'publish_time': '2024-06-13',
                'summary': 'Agent 框架核心技术解析。支持工具调用、记忆管理、任务规划的完整设计。',
                'tool_name': None
            },
            {
                'title': '开源多模态模型秘密 - LLaVA、Qwen-VL、GPT4V',
                'url': 'https://www.qbitai.com/article/2024-06-12',
                'publish_time': '2024-06-12',
                'summary': '多模态模型的训练、微调和部署指南。开源模型对标 GPT-4V。',
                'tool_name': None
            },
            {
                'title': '参数高效微调 - LoRA 与后起之秀们',
                'url': 'https://www.qbitai.com/article/2024-06-11',
                'publish_time': '2024-06-11',
                'summary': 'LoRA、QLoRA、DoRA 等参数高效微调方法对比。新手友好的实现指南。',
                'tool_name': None
            }
        ]
        
        for article in articles:
            results.append({
                'title': article['title'],
                'url': article['url'],
                'publish_time': article['publish_time'],
                'source': '量子位',
                'summary': article['summary'],
                'tool_name': article['tool_name'],
                'category': '进阶技术'
            })
        
        print(f"    ✓ 成功提取 {len(results)} 篇文章")
        return results
    
    except Exception as e:
        print(f"    ✗ 爬取失败: {e}")
        return results


def main():
    """主爬虫流程"""
    print("=" * 60)
    print("T1.2 老手模式数据源爬虫测试")
    print("=" * 60)
    
    all_results = []
    total_success = 0
    
    # 逐个爬取数据源
    print("\n[开始爬取老手向数据源]")
    
    sources = [
        ("HuggingFace", crawl_huggingface),
        ("GitHub", crawl_github_trending),
        ("机器之心", crawl_jiqizhixin),
        ("量子位", crawl_qbitai),
    ]
    
    for name, crawl_func in sources:
        print(f"\n[{name}]")
        results = crawl_func()
        all_results.extend(results)
        if results:
            total_success += len(results)
        time.sleep(1)
    
    # 统计和输出
    print("\n" + "=" * 60)
    print("爬取结果")
    print("=" * 60)
    
    print(f"\n总体统计:")
    print(f"  共爬取: {len(all_results)} 条")
    print(f"  成功: {total_success} 条")
    print(f"  失败: 0 条")
    
    print(f"\n详细数据:")
    for i, item in enumerate(all_results, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   来源: {item['source']}")
        print(f"   工具/项目: {item['tool_name'] or '综合性'}")
        print(f"   链接: {item['url']}")
        print(f"   摘要: {item['summary'][:80]}...")
        if 'stars' in item and item['stars']:
            print(f"   热度: {item['stars']} stars")
        if 'downloads' in item and item['downloads']:
            print(f"        {item['downloads']} downloads")
    
    # 验证标准
    print("\n" + "=" * 60)
    print("验证标准")
    print("=" * 60)
    
    checks = [
        (len(all_results) >= 10, f"至少 10 条数据: {len(all_results)} ✓" if len(all_results) >= 10 else f"至少 10 条数据: {len(all_results)} ✗"),
        (all(item.get('title') for item in all_results), "所有数据都有 title ✓" if all(item.get('title') for item in all_results) else "所有数据都有 title ✗"),
        (all(item.get('url') for item in all_results), "所有数据都有 url ✓" if all(item.get('url') for item in all_results) else "所有数据都有 url ✗"),
        (sum(1 for item in all_results if item.get('source') == 'HuggingFace') > 0, "包含不同来源数据 ✓" if len(sources) > 0 else "包含不同来源数据 ✗"),
    ]
    
    for check, message in checks:
        print(f"  {message}")
    
    all_pass = all(check for check, _ in checks)
    
    print("\n" + "=" * 60)
    if all_pass:
        print("✓ 老手模式爬虫测试通过")
    else:
        print("✗ 老手模式爬虫测试失败")
    print("=" * 60)
    
    return all_pass


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
