#!/usr/bin/env python3
"""
OpenClaw AI 项目初始化脚本
"""
import os
import sys

def init_project():
    """初始化项目环境"""
    print("=" * 60)
    print("OpenClaw AI 项目初始化")
    print("=" * 60)
    
    # 创建必要的目录
    directories = [
        'data',
        'outputs',
        'web/templates',
        'web/static',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ 创建目录: {directory}")
    
    # 初始化数据库
    print("\n初始化数据库...")
    from db import tool_store, search_history
    tool_store._init_db()
    search_history._init_db()
    print("✓ 数据库初始化完成")
    
    # 创建示例数据
    print("\n创建示例数据...")
    sample_tools = [
        {
            'title': 'ChatGPT',
            'tool_name': 'ChatGPT',
            'summary': 'OpenAI开发的大型语言模型',
            'url': 'https://chat.openai.com',
            'source': 'OpenAI',
            'content': 'ChatGPT是一个AI助手，可以进行对话、写代码、解答问题等',
            'category': 'ChatGPT GPT-4',
            'tool_type': '大语言模型'
        },
        {
            'title': 'Claude',
            'tool_name': 'Claude',
            'summary': 'Anthropic开发的AI助手',
            'url': 'https://claude.ai',
            'source': 'Anthropic',
            'content': 'Claude是一个功能强大的AI助手，擅长长文本分析和推理',
            'category': 'Claude AI',
            'tool_type': '大语言模型'
        },
        {
            'title': 'Midjourney',
            'tool_name': 'Midjourney',
            'summary': 'AI图像生成工具',
            'url': 'https://midjourney.com',
            'source': 'Midjourney',
            'content': '使用文字描述生成高质量的AI艺术图像',
            'category': 'Midjourney 图像生成',
            'tool_type': '图像生成'
        }
    ]
    
    for tool in sample_tools:
        if not tool_store.is_url_exists(tool['url']):
            tool_store.insert_tool(tool)
            print(f"✓ 添加工具: {tool['title']}")
    
    print("\n" + "=" * 60)
    print("✓ 项目初始化完成!")
    print("=" * 60)
    print("\n快速开始:")
    print("1. 启动Web服务器: python web/app.py")
    print("2. 访问应用: http://localhost:5000")
    print("3. 启动定时任务: python scheduler/task_scheduler.py")
    print("\n项目结构:")
    print("  - db/: 数据库模块")
    print("  - crawler/: 爬虫模块")
    print("  - analysis/: 分析模块")
    print("  - search/: 搜索模块")
    print("  - report/: 报告生成模块")
    print("  - web/: Web应用")
    print("  - scheduler/: 定时任务")


if __name__ == '__main__':
    try:
        init_project()
    except Exception as e:
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
