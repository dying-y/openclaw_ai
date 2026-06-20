#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T2.3 新手/老手自动分类逻辑

基于规则和关键词对工具进行分类
"""


def classify_tool(tool_dict):
    """
    将工具自动分类为"新手入门"或"进阶技术"
    
    参数：
        tool_dict: 包含以下字段的字典
            - title: 工具标题
            - summary: 工具摘要
            - keywords: 关键词列表（可选）
            - tool_type: 工具类型（可选）
    
    返回：
        "新手入门" 或 "进阶技术"
    """
    
    title = tool_dict.get('title', '').lower()
    summary = tool_dict.get('summary', '').lower()
    content = tool_dict.get('content', '').lower()
    tool_type = tool_dict.get('tool_type', '').lower()
    
    full_text = f"{title} {summary} {content} {tool_type}"
    
    # 新手关键词（权重 60%）
    beginner_keywords = [
        '教程', '入门', '新手', '小白', '零基础', '安装', '配置', 
        '使用教程', '怎么用', '初学指南', '快速上手', '完全指南',
        '一分钟', '30秒', '傻瓜式', '无需', '一键', '点击'
    ]
    
    # 老手关键词（权重 60%）
    advanced_keywords = [
        '源码', '部署', '微调', '训练', '推理优化', '框架', 'api',
        '二次开发', 'benchmark', 'sota', '开源模型', '技术实现',
        '架构', '性能', '优化', 'huggingface', 'github', 'langchain',
        'llamaindex', '开发框架', '推理引擎'
    ]
    
    # 工具类型判断（权重 30%）
    beginner_types = ['大语言模型', '图像生成', 'ai绘画', '低代码', '在线工具']
    advanced_types = ['开发框架', '模型权重', '推理引擎', '向量数据库', 'agent框架']
    
    # 技术难度词（权重 10%）
    tech_keywords = ['python', 'api', '部署', '代码', '编程', '开发']
    easy_keywords = ['网页版', '一键', '无需安装', '界面', '点击']
    
    # 计算得分
    scores = {
        'beginner_keywords': sum(1 for kw in beginner_keywords if kw in full_text),
        'advanced_keywords': sum(1 for kw in advanced_keywords if kw in full_text),
        'beginner_types': sum(1 for t in beginner_types if t in full_text),
        'advanced_types': sum(1 for t in advanced_types if t in full_text),
        'tech_keywords': sum(1 for kw in tech_keywords if kw in full_text),
        'easy_keywords': sum(1 for kw in easy_keywords if kw in full_text),
    }
    
    # 加权计算
    beginner_score = (
        scores['beginner_keywords'] * 0.60 +  # 关键词权重 60%
        scores['beginner_types'] * 0.30 +      # 工具类型权重 30%
        scores['easy_keywords'] * 0.10         # 易用词权重 10%
    )
    
    advanced_score = (
        scores['advanced_keywords'] * 0.60 +   # 关键词权重 60%
        scores['advanced_types'] * 0.30 +      # 工具类型权重 30%
        scores['tech_keywords'] * 0.10         # 技术词权重 10%
    )
    
    # 判断理由
    reasons = []
    
    if scores['beginner_keywords'] > 0:
        reasons.append(f"新手关键词: {scores['beginner_keywords']} 个")
    if scores['advanced_keywords'] > 0:
        reasons.append(f"老手关键词: {scores['advanced_keywords']} 个")
    if scores['beginner_types'] > 0:
        reasons.append(f"新手类型: {scores['beginner_types']} 个")
    if scores['advanced_types'] > 0:
        reasons.append(f"老手类型: {scores['advanced_types']} 个")
    
    # 最终分类
    if advanced_score > beginner_score:
        classification = '进阶技术'
    elif beginner_score > advanced_score:
        classification = '新手入门'
    else:
        # 打成平手时，根据工具类型判断
        if any(t in tool_type for t in ['框架', 'agent', 'llm框架']):
            classification = '进阶技术'
        else:
            classification = '新手入门'
    
    return {
        'classification': classification,
        'beginner_score': round(beginner_score, 2),
        'advanced_score': round(advanced_score, 2),
        'reasons': reasons if reasons else ['默认分类']
    }


def classify_multiple_tools(tools_list):
    """
    批量分类工具
    
    参数：
        tools_list: 工具字典列表
    
    返回：
        带有分类结果的工具列表
    """
    
    classified_tools = []
    
    for tool in tools_list:
        result = classify_tool(tool)
        tool['auto_category'] = result['classification']
        tool['classification_scores'] = {
            'beginner': result['beginner_score'],
            'advanced': result['advanced_score']
        }
        tool['classification_reasons'] = result['reasons']
        classified_tools.append(tool)
    
    return classified_tools


def get_classification_stats(tools_list):
    """获取分类统计"""
    total = len(tools_list)
    beginner = sum(1 for t in tools_list if t.get('auto_category') == '新手入门')
    advanced = sum(1 for t in tools_list if t.get('auto_category') == '进阶技术')
    
    return {
        'total': total,
        'beginner': beginner,
        'advanced': advanced,
        'beginner_percentage': round(beginner / total * 100, 1) if total > 0 else 0,
        'advanced_percentage': round(advanced / total * 100, 1) if total > 0 else 0
    }


if __name__ == '__main__':
    # 测试
    test_tools = [
        {
            'title': 'ChatGPT 新手完全上手指南',
            'summary': '适合初学者的 ChatGPT 教程',
            'content': '无需编程基础，一分钟上手',
            'tool_type': '大语言模型'
        },
        {
            'title': 'LangChain 框架源码解读',
            'summary': 'LLM 应用开发框架',
            'content': '深入解读源码实现细节',
            'tool_type': 'Agent框架'
        },
    ]
    
    for tool in test_tools:
        result = classify_tool(tool)
        print(f"工具: {tool['title']}")
        print(f"分类: {result['classification']}")
        print(f"新手分: {result['beginner_score']}, 老手分: {result['advanced_score']}")
        print(f"理由: {', '.join(result['reasons'])}\n")
