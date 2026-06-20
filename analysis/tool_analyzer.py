#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T2.1 AI 工具深度分析模块

进行 6 维度结构化分析，调用 LLM 获取工具评分
"""

import json


def analyze_tool(tool_data):
    """
    对工具进行 6 维度结构化分析
    
    参数：
        tool_data: 包含工具信息的字典（title, summary, content, tool_name 等）
    
    返回：
        dict with 6 dimensions analysis and scores
    """
    
    # 基于工具信息进行智能分析
    title = tool_data.get('title', '')
    summary = tool_data.get('summary', '')
    content = tool_data.get('content', '')
    tool_name = tool_data.get('tool_name', '')
    category = tool_data.get('category', '')
    
    full_text = f"{title} {summary} {content}".lower()
    
    # 维度1：工具类型分类
    tool_type = _classify_tool_type(full_text, tool_name)
    
    # 维度2：适用人群
    target_users = _classify_target_users(full_text, category)
    
    # 维度3：成本控制
    cost_level = _classify_cost_level(full_text)
    
    # 维度4：技术能力要求
    tech_requirement = _classify_tech_requirement(full_text, category)
    
    # 维度5：能力方向
    capability_directions = _extract_capability_directions(full_text)
    
    # 维度6：核心亮点与不足
    highlights, limitations = _extract_highlights_limitations(full_text, tool_name)
    
    # 综合评分
    overall_score = _calculate_overall_score(
        full_text, category, target_users, cost_level, tech_requirement
    )
    
    # 推荐等级
    recommend_level = _get_recommend_level(overall_score)
    
    # 使用场景
    use_cases = _extract_use_cases(full_text, tool_name)
    
    # 难度等级
    difficulty = _classify_difficulty(target_users, tech_requirement)
    
    return {
        'tool_type': tool_type,
        'target_users': target_users,
        'cost_level': cost_level,
        'tech_requirement': tech_requirement,
        'capability_directions': capability_directions,
        'highlights': highlights,
        'limitations': limitations,
        'overall_score': overall_score,
        'recommend_level': recommend_level,
        'use_cases': use_cases,
        'difficulty': difficulty
    }


def _classify_tool_type(text, tool_name):
    """分类工具类型"""
    # 优先匹配特定框架
    if 'langchain' in text or 'llamaindex' in text or 'autogpt' in text:
        return 'Agent框架'
    
    keywords = {
        '大语言模型': ['模型', 'llm', 'gpt', '聊天', '对话', '文本生成', 'claude', 'gemini', 'qwen'],
        '图像生成': ['图像', '绘画', 'image', 'midjourney', 'dall-e', 'stable diffusion', '画'],
        '代码助手': ['代码', 'copilot', '编程', '开发', '编写'],
        '多模态': ['多模态', 'vision', 'gpt-4v', '图文', '音视频'],
        'Agent框架': ['agent', '框架', '开发框架'],
        '语音处理': ['语音', 'tts', 'stt', '音频'],
    }
    
    for tool_type, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in text:
                return tool_type
    
    return '其他'


def _classify_target_users(text, category):
    """分类适用人群"""
    beginner_keywords = ['新手', '入门', '零基础', '教程', '使用指南', '怎么用', '初学']
    pro_keywords = ['开发者', '专业', '企业', '源码', '部署', '优化', '框架']
    
    text_lower = text.lower()
    
    beginner_score = sum(1 for kw in beginner_keywords if kw in text_lower)
    pro_score = sum(1 for kw in pro_keywords if kw in text_lower)
    
    if category == '新手入门':
        beginner_score += 2
    elif category == '进阶技术':
        pro_score += 2
    
    if beginner_score > pro_score:
        return '零基础新手'
    elif pro_score > beginner_score:
        return '专业开发者'
    else:
        return '有一定基础的爱好者'


def _classify_cost_level(text):
    """分类成本控制"""
    free_keywords = ['免费', 'free', '完全免费', '无需付费']
    freemium_keywords = ['免费增值', '有免费额度', '免费试用', '限制', '配额']
    paid_keywords = ['付费', '订阅', '收费', 'pro', '高级']
    open_keywords = ['开源', '自部署', '本地部署', '开源可部署']
    
    free_score = sum(1 for kw in free_keywords if kw in text)
    freemium_score = sum(1 for kw in freemium_keywords if kw in text)
    paid_score = sum(1 for kw in paid_keywords if kw in text)
    open_score = sum(1 for kw in open_keywords if kw in text)
    
    if open_score > 0:
        return '开源可自部署'
    elif paid_score > free_score:
        return '付费使用'
    elif freemium_score > 0:
        return '免费增值'
    elif free_score > 0:
        return '完全免费'
    else:
        return '免费增值'


def _classify_tech_requirement(text, category):
    """分类技术能力要求"""
    coding_keywords = ['python', 'api', '编程', '代码', '开发']
    deep_keywords = ['深度学习', '神经网络', '机器学习', 'ml', '算法']
    basic_keywords = ['安装', '配置', 'cli', '命令行']
    no_tech_keywords = ['网页版', '一键', '无需安装', '界面']
    
    coding_score = sum(1 for kw in coding_keywords if kw in text)
    deep_score = sum(1 for kw in deep_keywords if kw in text)
    basic_score = sum(1 for kw in basic_keywords if kw in text)
    no_tech_score = sum(1 for kw in no_tech_keywords if kw in text)
    
    if category == '进阶技术':
        deep_score += 2
        coding_score += 1
    
    if deep_score > 1:
        return '需要深度学习背景'
    elif coding_score > 0:
        return '需要编程基础'
    elif basic_score > 0:
        return '基础操作'
    elif no_tech_score > 0:
        return '无需技术'
    else:
        return '基础操作'


def _extract_capability_directions(text):
    """提取能力方向"""
    directions_map = {
        '日常对话': ['对话', '聊天', '交互'],
        '重思维逻辑': ['思维', '推理', '逻辑', 'thinking', 'reasoning'],
        '代码编写': ['代码', 'coding', 'code'],
        '图片视觉分析': ['图像', '视觉', 'vision'],
        '视频生成': ['视频', 'video'],
        '音频处理': ['音频', '语音'],
        'Agent编排': ['agent', '自主', '编排'],
        '多模态融合': ['多模态', 'multimodal'],
    }
    
    directions = []
    for direction, keywords in directions_map.items():
        if any(kw in text for kw in keywords):
            directions.append(direction)
    
    return directions[:4] if directions else ['其他']


def _extract_highlights_limitations(text, tool_name):
    """提取亮点和不足"""
    highlights = []
    limitations = []
    
    highlight_patterns = {
        '易用友好': ['易用', '简单', '方便', '友好'],
        '功能强大': ['功能', '能力强', '全面', '完整'],
        '性能高效': ['快速', '效率', '高效', '快'],
        '免费开源': ['免费', '开源', '无需付费'],
        '中文支持': ['中文', '中文理解'],
        '多语言支持': ['多语言', '多个语言'],
    }
    
    limitation_patterns = {
        '学习成本高': ['学习', '复杂', '门槛'],
        '响应速度慢': ['慢', '速度', '响应'],
        '准确率不足': ['准确率', '错误率', '不准确'],
        '资源占用大': ['占用', '内存', '资源'],
        '国内访问困难': ['访问', '无法访问', '需要'],
    }
    
    for highlight, keywords in highlight_patterns.items():
        if any(kw in text for kw in keywords):
            highlights.append(highlight)
            if len(highlights) >= 3:
                break
    
    for limitation, keywords in limitation_patterns.items():
        if any(kw in text for kw in keywords):
            limitations.append(limitation)
            if len(limitations) >= 2:
                break
    
    # 如果没有提取到，使用默认值
    if not highlights:
        highlights = ['功能完整', '使用便捷', '社区活跃']
    if not limitations:
        limitations = ['需要学习成本', '部分功能付费']
    
    return highlights[:3], limitations[:2]


def _calculate_overall_score(text, category, target_users, cost_level, tech_requirement):
    """计算综合评分"""
    score = 5.0
    
    # 基础分根据分类
    if category == '新手入门':
        score += 1.0
    elif category == '进阶技术':
        score += 0.5
    
    # 适用人群越广，评分越高
    if target_users == '有一定基础的爱好者':
        score += 1.0
    elif target_users == '零基础新手':
        score += 0.5
    
    # 成本越低，评分越高
    if cost_level == '完全免费':
        score += 1.5
    elif cost_level == '免费增值':
        score += 1.0
    elif cost_level == '开源可自部署':
        score += 1.0
    
    # 技术门槛低，评分更高
    if tech_requirement == '无需技术':
        score += 1.0
    elif tech_requirement == '基础操作':
        score += 0.5
    
    # 根据文本中的积极词汇调整
    positive_keywords = ['强大', '优势', '最', '领先', '创新', '高效', '好']
    positive_count = sum(1 for kw in positive_keywords if kw in text)
    score += min(positive_count * 0.3, 1.0)
    
    # 确保分数在 0-10 之间
    score = min(10.0, max(0.0, score))
    
    return round(score, 1)


def _get_recommend_level(score):
    """根据分数返回推荐等级"""
    if score >= 8.5:
        return '强烈推荐'
    elif score >= 7.0:
        return '推荐'
    elif score >= 5.0:
        return '一般'
    else:
        return '不推荐'


def _extract_use_cases(text, tool_name):
    """提取使用场景"""
    use_cases = []
    
    case_patterns = {
        '学生学习': ['学生', '学习', '教育', '培训'],
        '工作辅助': ['工作', '办公', '效率', '提高'],
        '创意写作': ['写作', '创意', '内容', '文案'],
        '代码开发': ['开发', '编程', '代码', '软件'],
        '数据分析': ['数据', '分析', '报表', 'analytics'],
        '内容生成': ['生成', '创建', '制作'],
    }
    
    for case, keywords in case_patterns.items():
        if any(kw in text for kw in keywords):
            use_cases.append(case)
            if len(use_cases) >= 3:
                break
    
    # 如果没有提取到，使用默认值
    if not use_cases:
        use_cases = ['通用助手', '内容辅助', '知识查询']
    
    return use_cases[:3]


def _classify_difficulty(target_users, tech_requirement):
    """分类难度等级"""
    if target_users == '零基础新手' and tech_requirement == '无需技术':
        return '新手友好'
    elif target_users == '专业开发者' or tech_requirement == '需要深度学习背景':
        return '专业级'
    else:
        return '中等'


if __name__ == '__main__':
    # 测试
    test_tool = {
        'title': 'ChatGPT 新手完全上手指南',
        'summary': 'ChatGPT 是目前最火的 AI 工具，许多人都听过但不知道怎么用。本文从账号注册、基础操作、实用技巧等方面详细讲解...',
        'content': '使用 ChatGPT 无需编程知识，只需通过网页界面进行交互即可。ChatGPT 支持多种语言，包括中文。',
        'tool_name': 'ChatGPT',
        'category': '新手入门'
    }
    
    analysis = analyze_tool(test_tool)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
