#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T3.2 历史搜索记录功能测试

独立测试脚本，验证搜索历史的所有功能
"""

import sys
import time
from db import search_history


def test_add_search():
    """测试添加搜索记录"""
    print("\n[测试1] 添加 15 条搜索记录...")
    
    # 测试数据（包含重复关键词）
    searches = [
        ('大模型', 12),
        ('AI绘画', 8),
        ('大模型', 15),  # 重复
        ('Agent框架', 5),
        ('LangChain', 3),
        ('大模型', 18),  # 重复
        ('Midjourney', 10),
        ('GPT-4', 7),
        ('向量数据库', 4),
        ('AI绘画', 9),  # 重复
        ('Prompt工程', 6),
        ('微调模型', 2),
        ('多模态AI', 11),
        ('代码生成', 8),
        ('AI分类', 5)
    ]
    
    success_count = 0
    for keyword, result_count in searches:
        if search_history.add_search(keyword, result_count):
            success_count += 1
        time.sleep(0.1)  # 稍微延迟以确保时间差异
    
    print(f"  成功添加 {success_count}/{len(searches)} 条记录")
    return success_count == len(searches)


def test_recent_searches():
    """测试最近搜索（去重）"""
    print("\n[测试2] 获取最近 10 条搜索（去重）...")
    
    recent = search_history.get_recent_searches(10)
    print(f"  共获取 {len(recent)} 条（去重后）:")
    
    for i, item in enumerate(recent, 1):
        print(f"  {i}. {item['keyword']} (时间: {item['search_time']}, 结果数: {item['result_count']})")
    
    # 验证去重
    keywords = [item['keyword'] for item in recent]
    unique_keywords = set(keywords)
    
    if len(keywords) == len(unique_keywords):
        print(f"  ✓ 去重成功，无重复关键词")
        return True
    else:
        print(f"  ✗ 去重失败，仍有重复关键词")
        return False


def test_hot_searches():
    """测试热门搜索"""
    print("\n[测试3] 获取热门搜索 Top 5...")
    
    hot = search_history.get_hot_searches(5)
    print(f"  共获取 {len(hot)} 条热门搜索:")
    
    for i, item in enumerate(hot, 1):
        print(f"  {i}. {item['keyword']} (搜索次数: {item['count']})")
    
    # 验证排序
    if len(hot) > 1:
        for i in range(len(hot) - 1):
            if hot[i]['count'] < hot[i+1]['count']:
                print(f"  ✗ 排序错误")
                return False
    
    print(f"  ✓ 排序正确")
    return len(hot) > 0


def test_delete_search():
    """测试删除搜索记录"""
    print("\n[测试4] 测试删除功能...")
    
    # 删除 "大模型" 的所有记录
    if search_history.delete_search('大模型'):
        print(f"  ✓ 成功删除 '大模型' 的所有记录")
        
        # 验证删除
        recent = search_history.get_recent_searches(20)
        keywords = [item['keyword'] for item in recent]
        
        if '大模型' not in keywords:
            print(f"  ✓ 验证成功，'大模型' 已从记录中移除")
            return True
        else:
            print(f"  ✗ 验证失败，'大模型' 仍在记录中")
            return False
    else:
        return False


def test_clear_history():
    """测试清空历史"""
    print("\n[测试5] 测试清空历史...")
    
    # 先添加一些记录
    search_history.add_search('测试关键词', 5)
    
    # 清空
    if search_history.clear_history():
        print(f"  ✓ 成功清空历史")
        
        # 验证
        recent = search_history.get_recent_searches(10)
        if len(recent) == 0:
            print(f"  ✓ 验证成功，历史已完全清空")
            return True
        else:
            print(f"  ✗ 验证失败，还有 {len(recent)} 条记录")
            return False
    else:
        return False


def verify_database_file():
    """验证数据库文件"""
    print("\n[验证] 检查搜索历史数据库文件...")
    from pathlib import Path
    
    db_path = Path(__file__).parent / "data" / "search_history.db"
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
    print("T3.2 历史搜索记录功能测试")
    print("=" * 60)
    
    # 清空历史数据
    print("\n[准备] 清空旧数据...")
    search_history.clear_history()
    print("  ✓ 旧数据已清空")
    
    # 执行所有测试
    tests = [
        ("添加记录", test_add_search),
        ("最近搜索", test_recent_searches),
        ("热门搜索", test_hot_searches),
        ("删除记录", test_delete_search),
        ("清空历史", test_clear_history),
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
