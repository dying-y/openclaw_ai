#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T2 阶段综合集成测试

测试分析、评分、分类模块的完整流程
"""

import sys
from analysis import tool_analyzer, tool_scoring, tool_classifier


def test_complete_workflow():
    """完整工作流测试"""
    print("\n[综合测试] 完整工作流")
    
    # 1. 分析工具
    tool_data = {
        'title': 'ChatGPT 新手完全上手指南',
        'summary': '适合初学者的 ChatGPT 使用教程',
        'content': '无需编程基础，通过网页界面即可使用',
        'tool_name': 'ChatGPT',
        'category': '新手入门'
    }
    
    print("  [步骤1] 工具分析...")
    analysis = tool_analyzer.analyze_tool(tool_data)
    print(f"    ✓ 分析完成，评分: {analysis['overall_score']}")
    
    # 2. 计算最终评分
    print("  [步骤2] 评分计算...")
    score_dict = {
        'source': '知乎',
        'search_count': 100,
        'overall_score': analysis['overall_score'],
        'publish_time': '2024-06-15',
        'use_cases_count': len(analysis['use_cases']),
        'target_users': analysis['target_users']
    }
    final_score = tool_scoring.calculate_final_score(score_dict)
    recommend = tool_scoring.get_recommend_level(final_score)
    print(f"    ✓ 最终评分: {final_score}, 推荐等级: {recommend}")
    
    # 3. 自动分类
    print("  [步骤3] 自动分类...")
    classification = tool_classifier.classify_tool(tool_data)
    print(f"    ✓ 分类: {classification['classification']}")
    print(f"      新手分: {classification['beginner_score']}, 老手分: {classification['advanced_score']}")
    print(f"      理由: {', '.join(classification['reasons'])}")
    
    return True


def test_multiple_tools_workflow():
    """多工具工作流"""
    print("\n[综合测试] 多工具工作流")
    
    tools = [
        {
            'title': 'ChatGPT 使用指南',
            'summary': '新手教程',
            'content': '无需编程',
            'tool_name': 'ChatGPT',
            'category': '新手入门'
        },
        {
            'title': 'LangChain 框架开发',
            'summary': '开发框架',
            'content': '需要 Python 基础',
            'tool_name': 'LangChain',
            'category': '进阶技术'
        },
        {
            'title': 'Midjourney AI 绘画',
            'summary': '图像生成工具',
            'content': '点击即用',
            'tool_name': 'Midjourney',
            'category': '新手入门'
        }
    ]
    
    print(f"  分析 {len(tools)} 个工具...")
    
    analyzed_tools = []
    for tool in tools:
        analysis = tool_analyzer.analyze_tool(tool)
        
        score_dict = {
            'source': '多渠道',
            'search_count': 50 + len(analyzed_tools) * 30,
            'overall_score': analysis['overall_score'],
            'publish_time': '2024-06-15',
            'use_cases_count': len(analysis['use_cases']),
            'target_users': analysis['target_users']
        }
        final_score = tool_scoring.calculate_final_score(score_dict)
        recommend = tool_scoring.get_recommend_level(final_score)
        
        classification = tool_classifier.classify_tool(tool)
        
        analyzed_tools.append({
            'name': tool['tool_name'],
            'analysis_score': analysis['overall_score'],
            'final_score': final_score,
            'recommend': recommend,
            'category': classification['classification']
        })
    
    print(f"  ✓ 分析完成\n")
    
    # 排序
    ranked = sorted(analyzed_tools, key=lambda x: x['final_score'], reverse=True)
    
    print(f"  工具排名:")
    for i, tool in enumerate(ranked, 1):
        print(f"    {i}. {tool['name']}: {tool['final_score']} 分 ({tool['recommend']})")
        print(f"       分析分: {tool['analysis_score']}, 分类: {tool['category']}")
    
    return len(analyzed_tools) == len(tools)


def main():
    """主测试"""
    print("=" * 60)
    print("T2 阶段综合集成测试")
    print("=" * 60)
    
    tests = [
        ("完整工作流", test_complete_workflow),
        ("多工具工作流", test_multiple_tools_workflow),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  ✗ 测试异常: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"综合测试结果: {passed}/{len(tests)} 通过")
    print("=" * 60)
    
    return passed == len(tests)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
