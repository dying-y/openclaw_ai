#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T2.2 工具评分与推荐度计算

实现多维度加权打分算法
"""

from datetime import datetime, timedelta


def calculate_final_score(tool_dict):
    """
    计算最终综合评分
    
    参数：
        tool_dict: 包含以下字段的字典
            - source: 来源（官方博客/头部媒体/社区/自媒体）
            - search_count: 搜索次数
            - overall_score: LLM 评分（0-10）
            - publish_time: 发布时间（YYYY-MM-DD）
            - use_cases_count: 使用场景数量
            - target_users: 适用人群
    
    返回：
        0-10 分的最终综合评分（保留 1 位小数）
    """
    
    score = 0.0
    
    # 1. 来源权重（20%）
    source_weight = 0.2
    source = tool_dict.get('source', '社区')
    source_scores = {
        '官方博客': 1.2,
        '头部媒体': 1.0,
        '社区': 0.8,
        '自媒体': 0.6,
        '知乎': 0.85,
        'CSDN': 0.80,
        '简书': 0.75,
        'HuggingFace': 1.0,
        'GitHub': 1.1,
        '机器之心': 1.0,
        '量子位': 0.95,
    }
    source_score = source_scores.get(source, 0.8)
    source_final = min(2.0, source_score)  # 最多贡献 2 分
    score += source_final * source_weight
    
    # 2. 热度权重（20%）
    heat_weight = 0.2
    search_count = tool_dict.get('search_count', 0)
    # 搜索次数映射到 0-10 分
    heat_score = min(10.0, (search_count / 100.0) * 10)
    score += heat_score * heat_weight
    
    # 3. LLM 评分（60%）
    llm_weight = 0.6
    overall_score = tool_dict.get('overall_score', 5.0)
    llm_final = min(10.0, overall_score)
    score += llm_final * llm_weight
    
    # 4. 新鲜度权重（10%）
    freshness_weight = 0.1
    publish_time_str = tool_dict.get('publish_time')
    if publish_time_str:
        try:
            pub_date = datetime.strptime(publish_time_str, '%Y-%m-%d')
            days_old = (datetime.now() - pub_date).days
            
            if days_old <= 7:
                freshness_score = 10.0
            elif days_old <= 30:
                # 7-30 天内线性衰减
                freshness_score = 10.0 - (days_old - 7) / 23 * 5  # 从 10 衰减到 5
            else:
                # 超过 30 天衰减 50%
                freshness_score = 5.0
        except:
            freshness_score = 7.0
    else:
        freshness_score = 7.0
    
    score += freshness_score * freshness_weight
    
    # 实用性加分（最多 1 分）
    use_cases_count = tool_dict.get('use_cases_count', 0)
    target_users = tool_dict.get('target_users')
    practicality_bonus = 0.0
    
    if use_cases_count >= 3:
        practicality_bonus += 0.5
    if target_users and target_users != '其他':
        practicality_bonus += 0.5
    
    score += practicality_bonus
    
    # 确保分数在 0-10 之间
    final_score = min(10.0, max(0.0, score))
    
    return round(final_score, 1)


def get_recommend_level(score):
    """
    根据分数返回推荐等级
    
    参数：
        score: 综合评分（0-10）
    
    返回：
        推荐等级字符串
    """
    if score >= 8.5:
        return '强烈推荐'
    elif score >= 7.0:
        return '推荐'
    elif score >= 5.0:
        return '一般'
    else:
        return '不推荐'


def rank_tools(tools_list):
    """
    对工具列表进行排序和评分
    
    参数：
        tools_list: 工具字典列表
    
    返回：
        按最终评分降序排列的工具列表
    """
    
    for tool in tools_list:
        # 计算最终评分
        tool['final_score'] = calculate_final_score(tool)
        tool['recommend_level'] = get_recommend_level(tool['final_score'])
    
    # 按最终评分降序排列
    ranked_tools = sorted(tools_list, key=lambda x: x['final_score'], reverse=True)
    
    return ranked_tools


if __name__ == '__main__':
    # 测试
    test_tools = [
        {
            'source': 'HuggingFace',
            'search_count': 150,
            'overall_score': 8.5,
            'publish_time': '2024-06-15',
            'use_cases_count': 5,
            'target_users': '专业开发者'
        },
        {
            'source': '知乎',
            'search_count': 50,
            'overall_score': 7.0,
            'publish_time': '2024-06-01',
            'use_cases_count': 3,
            'target_users': '零基础新手'
        },
    ]
    
    for tool in test_tools:
        score = calculate_final_score(tool)
        level = get_recommend_level(score)
        print(f"评分: {score}, 等级: {level}")
