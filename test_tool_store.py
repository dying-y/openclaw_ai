#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T1.3 AI 工具数据库表设计与测试

独立测试脚本，验证工具数据库的所有功能
"""

import sys
from pathlib import Path
from db import tool_store

# 测试数据
TEST_TOOLS = [
    {
        'title': 'ChatGPT 新手入门教程',
        'url': 'https://example.com/chatgpt-beginner',
        'publish_time': '2024-06-15',
        'source': '知乎',
        'tool_name': 'ChatGPT',
        'category': '新手入门',
        'summary': 'ChatGPT 是 OpenAI 推出的强大对话式 AI，适合所有人使用。本教程从零开始教你如何使用 ChatGPT。',
        'tool_type': '大语言模型',
        'difficulty': '新手友好',
        'cost_level': '免费增值',
        'tech_requirement': '无需技术',
        'target_users': '零基础新手'
    },
    {
        'title': '文心一言使用指南',
        'url': 'https://example.com/wenxin-guide',
        'publish_time': '2024-06-14',
        'source': 'CSDN',
        'tool_name': '文心一言',
        'category': '新手入门',
        'summary': '百度推出的国产对话 AI，完全免费。本文介绍如何快速上手文心一言。',
        'tool_type': '大语言模型',
        'difficulty': '新手友好',
        'cost_level': '完全免费',
        'tech_requirement': '无需技术',
        'target_users': '零基础新手'
    },
    {
        'title': '豆包 AI 助手入门手册',
        'url': 'https://example.com/doubao-handbook',
        'publish_time': '2024-06-13',
        'source': '简书',
        'tool_name': '豆包',
        'category': '新手入门',
        'summary': '字节跳动出品的 AI 助手，功能强大易用。新手必读指南。',
        'tool_type': '大语言模型',
        'difficulty': '新手友好',
        'cost_level': '完全免费',
        'tech_requirement': '无需技术',
        'target_users': '零基础新手'
    },
    {
        'title': 'LangChain 框架源码解读',
        'url': 'https://example.com/langchain-source',
        'publish_time': '2024-06-12',
        'source': 'GitHub',
        'tool_name': 'LangChain',
        'category': '进阶技术',
        'summary': 'LangChain 是最流行的 LLM 应用框架，本文深入解读源码实现细节和扩展方案。',
        'tool_type': 'Agent框架',
        'difficulty': '专业级',
        'cost_level': '开源可自部署',
        'tech_requirement': '需要深度学习背景',
        'target_users': '专业开发者'
    },
    {
        'title': 'LlamaIndex 向量检索优化指南',
        'url': 'https://example.com/llamaindex-optimize',
        'publish_time': '2024-06-11',
        'source': '机器之心',
        'tool_name': 'LlamaIndex',
        'category': '进阶技术',
        'summary': '如何在生产环境中优化 LlamaIndex 的检索速度和准确性。包含基准测试和最佳实践。',
        'tool_type': 'Agent框架',
        'difficulty': '专业级',
        'cost_level': '开源可自部署',
        'tech_requirement': '需要深度学习背景',
        'target_users': '专业开发者'
    }
]


def test_insert():
    """测试插入功能"""
    print("\n[测试1] 插入 5 条工具数据...")
    success_count = 0
    for tool in TEST_TOOLS:
        if tool_store.insert_tool(tool):
            success_count += 1
            print(f"  ✓ 插入: {tool['tool_name']}")
        else:
            print(f"  ✗ 插入失败: {tool['tool_name']}")
    print(f"  结果: {success_count}/5 插入成功")
    return success_count == 5


def test_query_all():
    """测试查询所有工具"""
    print("\n[测试2] 查询所有工具...")
    tools = tool_store.query_all()
    print(f"  共查询到 {len(tools)} 条工具")
    for tool in tools:
        print(f"  - {tool['tool_name']} ({tool['category']})")
    return len(tools) == 5


def test_query_by_category():
    """测试按分类查询"""
    print("\n[测试3] 按分类查询工具...")
    
    beginner_tools = tool_store.query_by_category('新手入门')
    print(f"  新手入门: {len(beginner_tools)} 条")
    for tool in beginner_tools:
        print(f"    - {tool['tool_name']}")
    
    advanced_tools = tool_store.query_by_category('进阶技术')
    print(f"  进阶技术: {len(advanced_tools)} 条")
    for tool in advanced_tools:
        print(f"    - {tool['tool_name']}")
    
    return len(beginner_tools) == 3 and len(advanced_tools) == 2


def test_is_url_exists():
    """测试 URL 去重"""
    print("\n[测试4] 检查 URL 存在...")
    exists = tool_store.is_url_exists('https://example.com/chatgpt-beginner')
    print(f"  ChatGPT URL 存在: {exists}")
    
    not_exists = tool_store.is_url_exists('https://example.com/nonexistent')
    print(f"  不存在的 URL: {not_exists}")
    
    return exists and not not_exists


def test_update_analysis():
    """测试更新分析结果"""
    print("\n[测试5] 更新分析结果...")
    
    # 获取第一个工具
    tools = tool_store.query_all()
    if not tools:
        print("  ✗ 没有工具可更新")
        return False
    
    tool_id = tools[0]['id']
    tool_name = tools[0]['tool_name']
    
    analysis = {
        'tool_type': '大语言模型',
        'target_users': '零基础新手',
        'cost_level': '免费增值',
        'tech_requirement': '无需技术',
        'capability_directions': ['日常对话', '文本生成'],
        'highlights': ['易用友好', '功能强大', '免费试用'],
        'limitations': ['中文理解稍弱', '响应速度不稳定'],
        'overall_score': 8.5,
        'recommend_level': '强烈推荐',
        'use_cases': ['学生学习', '工作辅助', '创意写作'],
        'difficulty': '新手友好'
    }
    
    if tool_store.update_analysis(tool_id, analysis):
        print(f"  ✓ 成功更新 {tool_name} 的分析结果")
        print(f"    评分: {analysis['overall_score']}")
        print(f"    推荐等级: {analysis['recommend_level']}")
        return True
    else:
        print(f"  ✗ 更新失败")
        return False


def test_increment_search_count():
    """测试搜索计数"""
    print("\n[测试6] 测试搜索计数...")
    
    tools = tool_store.query_all()
    if not tools:
        print("  ✗ 没有工具可更新")
        return False
    
    tool_id = tools[0]['id']
    tool_name = tools[0]['tool_name']
    
    initial_count = tools[0]['search_count']
    
    for _ in range(3):
        tool_store.increment_search_count(tool_id)
    
    updated_tools = tool_store.query_all()
    updated_tool = next((t for t in updated_tools if t['id'] == tool_id), None)
    
    if updated_tool:
        new_count = updated_tool['search_count']
        print(f"  {tool_name}: {initial_count} -> {new_count} (增加 3 次)")
        return new_count == initial_count + 3
    
    return False


def test_get_top_tools():
    """测试热门榜单"""
    print("\n[测试7] 获取热门工具（前 3 名）...")
    
    top_tools = tool_store.get_top_tools(3)
    print(f"  共获取 {len(top_tools)} 条热门工具:")
    for i, tool in enumerate(top_tools, 1):
        print(f"  {i}. {tool['tool_name']} (评分: {tool['score']}, 搜索次数: {tool['search_count']})")
    
    return len(top_tools) > 0


def verify_database_file():
    """验证数据库文件"""
    print("\n[验证] 检查数据库文件...")
    db_path = Path(__file__).parent / "data" / "tools.db"
    if db_path.exists():
        size = db_path.stat().st_size
        print(f"  ✓ 数据库文件存在: {db_path}")
        print(f"    文件大小: {size} bytes")
        return True
    else:
        print(f"  ✗ 数据库文件不存在: {db_path}")
        return False


def main():
    """主测试流程"""
    print("=" * 60)
    print("T1.3 AI 工具数据库表设计与测试")
    print("=" * 60)
    
    # 清空旧数据
    print("\n[准备] 清空历史数据...")
    tool_store.clear_all()
    print("  ✓ 历史数据已清空")
    
    # 执行所有测试
    tests = [
        ("插入工具", test_insert),
        ("查询所有", test_query_all),
        ("分类查询", test_query_by_category),
        ("URL去重", test_is_url_exists),
        ("更新分析", test_update_analysis),
        ("搜索计数", test_increment_search_count),
        ("热门榜单", test_get_top_tools),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ 测试异常: {e}")
    
    # 验证数据库文件
    verify_database_file()
    
    # 总结
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{len(tests)} 通过")
    print("=" * 60)
    
    return passed == len(tests)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
