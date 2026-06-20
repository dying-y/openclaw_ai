#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T2.1 工具多维度结构化分析测试

测试工具深度分析功能
"""

import sys
import json
from analysis import tool_analyzer


def test_beginner_tool():
    """测试新手向工具分析"""
    print("\n[测试1] 新手向工具分析（ChatGPT）")
    
    tool_data = {
        'title': 'ChatGPT 新手完全上手指南',
        'summary': 'ChatGPT 是目前最火的 AI 工具，许多人都听过但不知道怎么用。本文从账号注册、基础操作、实用技巧等方面详细讲解...',
        'content': '使用 ChatGPT 无需编程知识，只需通过网页界面进行交互即可。完全免费使用。支持中文。',
        'tool_name': 'ChatGPT',
        'category': '新手入门'
    }
    
    analysis = tool_analyzer.analyze_tool(tool_data)
    
    print(f"  工具类型: {analysis['tool_type']}")
    print(f"  适用人群: {analysis['target_users']}")
    print(f"  成本控制: {analysis['cost_level']}")
    print(f"  技术要求: {analysis['tech_requirement']}")
    print(f"  能力方向: {', '.join(analysis['capability_directions'])}")
    print(f"  核心亮点: {', '.join(analysis['highlights'])}")
    print(f"  主要不足: {', '.join(analysis['limitations'])}")
    print(f"  综合评分: {analysis['overall_score']}")
    print(f"  推荐等级: {analysis['recommend_level']}")
    print(f"  使用场景: {', '.join(analysis['use_cases'])}")
    print(f"  难度等级: {analysis['difficulty']}")
    
    # 验证
    success = (
        analysis['tool_type'] == '大语言模型' and
        analysis['overall_score'] >= 5.0 and
        analysis['overall_score'] <= 10.0 and
        analysis['recommend_level'] in ['强烈推荐', '推荐', '一般', '不推荐']
    )
    
    if success:
        print("  ✓ 新手工具分析通过")
    else:
        print("  ✗ 新手工具分析失败")
    
    return success


def test_advanced_tool():
    """测试老手向工具分析"""
    print("\n[测试2] 老手向工具分析（LangChain）")
    
    tool_data = {
        'title': 'LangChain - LLM 应用开发框架',
        'summary': 'LangChain 是最流行的 LLM 应用框架，提供链式调用、Agent、RAG 等功能。支持 Python 和 JavaScript。',
        'content': '使用 LangChain 需要 Python 编程基础。支持多种 LLM，包括 OpenAI、Anthropic 等。开源项目，可自由部署。',
        'tool_name': 'LangChain',
        'category': '进阶技术'
    }
    
    analysis = tool_analyzer.analyze_tool(tool_data)
    
    print(f"  工具类型: {analysis['tool_type']}")
    print(f"  适用人群: {analysis['target_users']}")
    print(f"  成本控制: {analysis['cost_level']}")
    print(f"  技术要求: {analysis['tech_requirement']}")
    print(f"  能力方向: {', '.join(analysis['capability_directions'])}")
    print(f"  核心亮点: {', '.join(analysis['highlights'])}")
    print(f"  主要不足: {', '.join(analysis['limitations'])}")
    print(f"  综合评分: {analysis['overall_score']}")
    print(f"  推荐等级: {analysis['recommend_level']}")
    print(f"  使用场景: {', '.join(analysis['use_cases'])}")
    print(f"  难度等级: {analysis['difficulty']}")
    
    # 验证
    success = (
        analysis['tool_type'] == 'Agent框架' and
        analysis['overall_score'] >= 5.0 and
        analysis['overall_score'] <= 10.0 and
        analysis['recommend_level'] in ['强烈推荐', '推荐', '一般', '不推荐']
    )
    
    if success:
        print("  ✓ 老手工具分析通过")
    else:
        print("  ✗ 老手工具分析失败")
    
    return success


def test_multiple_tools():
    """测试多个工具分析"""
    print("\n[测试3] 多个工具分析验证")
    
    tools = [
        {
            'title': 'Midjourney - AI 绘画工具',
            'summary': '强大的 AI 绘画工具',
            'content': '使用 Discord 界面',
            'tool_name': 'Midjourney',
            'category': '新手入门'
        },
        {
            'title': 'Llama 3 - 开源大模型',
            'summary': 'Meta 推出的开源模型',
            'content': '支持本地部署，需要 GPU',
            'tool_name': 'Llama 3',
            'category': '进阶技术'
        },
        {
            'title': 'GitHub Copilot',
            'summary': '代码编写助手',
            'content': '提高编程效率',
            'tool_name': 'Copilot',
            'category': '新手入门'
        },
    ]
    
    all_success = True
    for tool in tools:
        analysis = tool_analyzer.analyze_tool(tool)
        print(f"\n  {tool['tool_name']}:")
        print(f"    类型: {analysis['tool_type']}, 评分: {analysis['overall_score']}, 等级: {analysis['recommend_level']}")
        
        # 验证分数范围
        if not (0 <= analysis['overall_score'] <= 10):
            all_success = False
            print(f"    ✗ 评分不在 0-10 范围内")
        else:
            print(f"    ✓")
    
    if all_success:
        print("\n  ✓ 多工具分析通过")
    else:
        print("\n  ✗ 多工具分析失败")
    
    return all_success


def test_dimension_coverage():
    """测试 6 维度覆盖"""
    print("\n[测试4] 6 维度覆盖验证")
    
    tool_data = {
        'title': '测试工具',
        'summary': '一个测试工具',
        'content': '内容',
        'tool_name': '测试',
        'category': '新手入门'
    }
    
    analysis = tool_analyzer.analyze_tool(tool_data)
    
    required_dims = [
        'tool_type',
        'target_users',
        'cost_level',
        'tech_requirement',
        'capability_directions',
        'highlights',
        'limitations'
    ]
    
    missing = []
    for dim in required_dims:
        if dim not in analysis or not analysis[dim]:
            missing.append(dim)
            print(f"  ✗ 缺少维度: {dim}")
        else:
            print(f"  ✓ {dim}: {analysis[dim]}")
    
    # 验证评分字段
    required_scores = ['overall_score', 'recommend_level', 'use_cases', 'difficulty']
    for score in required_scores:
        if score not in analysis:
            missing.append(score)
            print(f"  ✗ 缺少评分字段: {score}")
        else:
            print(f"  ✓ {score}: {analysis[score]}")
    
    success = len(missing) == 0
    
    if success:
        print("\n  ✓ 6 维度覆盖完整")
    else:
        print(f"\n  ✗ 缺少 {len(missing)} 项")
    
    return success


def test_output_format():
    """测试输出 JSON 格式"""
    print("\n[测试5] 输出 JSON 格式验证")
    
    tool_data = {
        'title': '格式测试工具',
        'summary': '测试',
        'content': '内容',
        'tool_name': '测试',
        'category': '新手入门'
    }
    
    analysis = tool_analyzer.analyze_tool(tool_data)
    
    try:
        json_str = json.dumps(analysis, ensure_ascii=False, indent=2)
        print(f"  JSON 长度: {len(json_str)} 字符")
        print(f"\n  示例 JSON:")
        print(f"  {json_str[:200]}...")
        print(f"\n  ✓ JSON 格式正确")
        return True
    except Exception as e:
        print(f"  ✗ JSON 序列化失败: {e}")
        return False


def main():
    """主测试流程"""
    print("=" * 60)
    print("T2.1 工具多维度结构化分析测试")
    print("=" * 60)
    
    tests = [
        ("新手工具分析", test_beginner_tool),
        ("老手工具分析", test_advanced_tool),
        ("多工具分析", test_multiple_tools),
        ("6维度覆盖", test_dimension_coverage),
        ("JSON格式", test_output_format),
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
    
    # 总结
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{len(tests)} 通过")
    print("=" * 60)
    
    return passed == len(tests)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
