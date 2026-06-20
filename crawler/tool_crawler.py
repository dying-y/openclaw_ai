#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T1.4 工具爬虫管理器

整合新手和老手模式的爬虫，实现去重入库功能
"""

import time
from db import tool_store


# 模拟新手模式爬虫数据
def _get_beginner_tools():
    """获取新手模式工具数据"""
    articles = [
        {
            'title': 'ChatGPT 新手完全上手指南',
            'url': 'https://zhuanlan.zhihu.com/p/example1',
            'publish_time': '2024-06-15',
            'source': '知乎',
            'summary': 'ChatGPT 是目前最火的 AI 工具，许多人都听过但不知道怎么用。本文从账号注册、基础操作、实用技巧等方面详细讲解...',
            'tool_name': 'ChatGPT',
            'category': '新手入门'
        },
        {
            'title': 'AI 绘画工具 Midjourney 使用教程',
            'url': 'https://zhuanlan.zhihu.com/p/example2',
            'publish_time': '2024-06-14',
            'source': '知乎',
            'summary': 'Midjourney 是一款革命性的 AI 绘画工具。本文介绍如何通过 Discord 使用 Midjourney...',
            'tool_name': 'Midjourney',
            'category': '新手入门'
        },
        {
            'title': '文心一言和 ChatGPT 对比测评',
            'url': 'https://zhuanlan.zhihu.com/p/example4',
            'publish_time': '2024-06-12',
            'source': '知乎',
            'summary': '百度推出的文心一言在中文处理上有优势。本文详细对比文心一言和 ChatGPT...',
            'tool_name': '文心一言',
            'category': '新手入门'
        },
        {
            'title': 'Copilot 在代码编写中的应用',
            'url': 'https://blog.csdn.net/example2',
            'publish_time': '2024-06-14',
            'source': 'CSDN',
            'summary': 'GitHub Copilot 是微软推出的 AI 编程助手，如何在 VS Code 中配置使用？',
            'tool_name': 'Copilot',
            'category': '新手入门'
        },
        {
            'title': '豆包 - 字节跳动的 AI 助手',
            'url': 'https://www.jianshu.com/p/example3',
            'publish_time': '2024-06-13',
            'source': '简书',
            'summary': '豆包是字节跳动推出的新一代 AI 助手。不知道怎么用？看这篇就够了...',
            'tool_name': '豆包',
            'category': '新手入门'
        },
    ]
    return articles


# 模拟老手模式爬虫数据
def _get_advanced_tools():
    """获取老手模式工具数据"""
    articles = [
        {
            'title': 'Llama 3 - Meta 推出的最新开源大模型',
            'url': 'https://huggingface.co/meta-llama/Llama-2-70b',
            'publish_time': '2024-06-15',
            'source': 'HuggingFace',
            'summary': 'Meta 最新推出的 Llama 3 模型，参数量 70B，在多个基准测试上取得 SOTA 成绩。支持多语言，可自部署。',
            'tool_name': 'Llama 3',
            'category': '进阶技术'
        },
        {
            'title': 'LangChain - LLM 应用开发框架',
            'url': 'https://github.com/langchain-ai/langchain',
            'publish_time': '2024-06-15',
            'source': 'GitHub',
            'summary': 'LangChain 是最流行的 LLM 应用框架，提供链式调用、Agent、RAG 等功能。支持 Python 和 JS。',
            'tool_name': 'LangChain',
            'category': '进阶技术'
        },
        {
            'title': 'LlamaIndex - 向量数据库索引框架',
            'url': 'https://github.com/jerryjliu/llama_index',
            'publish_time': '2024-06-14',
            'source': 'GitHub',
            'summary': 'LlamaIndex 是构建 RAG 应用的核心框架，支持多种向量数据库和 LLM。性能优异。',
            'tool_name': 'LlamaIndex',
            'category': '进阶技术'
        },
        {
            'title': 'AutoGPT - 自主 AI Agent 框架',
            'url': 'https://github.com/Significant-Gravitas/AutoGPT',
            'publish_time': '2024-06-13',
            'source': 'GitHub',
            'summary': 'AutoGPT 是开源 Agent 框架，可自主完成任务。支持插件扩展和多种工具集成。',
            'tool_name': 'AutoGPT',
            'category': '进阶技术'
        },
        {
            'title': 'Mistral-7B - 超高效的 7B 模型',
            'url': 'https://huggingface.co/mistralai/Mistral-7B-v0.1',
            'publish_time': '2024-06-14',
            'source': 'HuggingFace',
            'summary': '仅 7B 参数的 Mistral 模型性能超越许多大模型。推理速度快，适合边缘部署。开源可自部署。',
            'tool_name': 'Mistral',
            'category': '进阶技术'
        },
    ]
    return articles


def crawl_beginner_tools():
    """
    爬取新手模式所有数据源
    
    返回：
        dict with keys: 'total', 'success', 'failed', 'results'
    """
    print("[爬虫] 开始爬取新手模式数据...")
    
    try:
        results = _get_beginner_tools()
        print(f"[爬虫] 新手模式爬取完成，共 {len(results)} 条")
        
        return {
            'total': len(results),
            'success': len(results),
            'failed': 0,
            'results': results,
            'category': '新手入门'
        }
    
    except Exception as e:
        print(f"[错误] 新手模式爬虫异常: {e}")
        return {
            'total': 0,
            'success': 0,
            'failed': 0,
            'results': [],
            'category': '新手入门'
        }


def crawl_advanced_tools():
    """
    爬取老手模式所有数据源
    
    返回：
        dict with keys: 'total', 'success', 'failed', 'results'
    """
    print("[爬虫] 开始爬取老手模式数据...")
    
    try:
        results = _get_advanced_tools()
        print(f"[爬虫] 老手模式爬取完成，共 {len(results)} 条")
        
        return {
            'total': len(results),
            'success': len(results),
            'failed': 0,
            'results': results,
            'category': '进阶技术'
        }
    
    except Exception as e:
        print(f"[错误] 老手模式爬虫异常: {e}")
        return {
            'total': 0,
            'success': 0,
            'failed': 0,
            'results': [],
            'category': '进阶技术'
        }


def crawl_all_tools():
    """
    完整的爬虫流程：新手 + 老手 + 去重入库
    
    返回：
        dict with stats: 'total', 'new_count', 'duplicate_count', 'failed_count', 
                        'beginner_count', 'advanced_count'
    """
    print("\n" + "=" * 60)
    print("开始全量爬取工具数据")
    print("=" * 60)
    
    stats = {
        'total': 0,
        'new_count': 0,
        'duplicate_count': 0,
        'failed_count': 0,
        'beginner_count': 0,
        'advanced_count': 0
    }
    
    # 爬取新手模式
    beginner_result = crawl_beginner_tools()
    time.sleep(1)
    
    # 爬取老手模式
    advanced_result = crawl_advanced_tools()
    
    # 合并所有结果
    all_tools = beginner_result['results'] + advanced_result['results']
    stats['total'] = len(all_tools)
    stats['beginner_count'] = len(beginner_result['results'])
    stats['advanced_count'] = len(advanced_result['results'])
    
    # 去重入库
    print("\n[入库] 开始去重入库...")
    for tool in all_tools:
        try:
            # 检查是否已存在
            if tool_store.is_url_exists(tool['url']):
                stats['duplicate_count'] += 1
                print(f"  [重复] {tool['tool_name']} (URL 已存在)")
            else:
                # 插入新数据
                if tool_store.insert_tool(tool):
                    stats['new_count'] += 1
                    print(f"  [新增] {tool['tool_name']} - {tool['source']}")
                else:
                    stats['failed_count'] += 1
                    print(f"  [失败] {tool['tool_name']}")
        
        except Exception as e:
            stats['failed_count'] += 1
            print(f"  [异常] {tool.get('tool_name', 'Unknown')}: {e}")
    
    # 统计结果
    print("\n" + "=" * 60)
    print("爬取统计结果")
    print("=" * 60)
    print(f"总计: {stats['total']} 条")
    print(f"  - 新增: {stats['new_count']} 条")
    print(f"  - 重复: {stats['duplicate_count']} 条")
    print(f"  - 失败: {stats['failed_count']} 条")
    print(f"分类: 新手入门 {stats['beginner_count']} 条，进阶技术 {stats['advanced_count']} 条")
    print("=" * 60)
    
    return stats


if __name__ == '__main__':
    # 用于独立测试
    result = crawl_all_tools()
