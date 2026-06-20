#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
T1.4 工具爬虫管理器测试

测试爬虫去重入库功能
"""

import sys
from crawler import tool_crawler
from db import tool_store


def test_first_crawl():
    """第一次爬取（全新）"""
    print("\n[测试1] 第一次爬取（应该全部成功）")
    
    # 清空数据库
    print("  清空数据库...")
    tool_store.clear_all()
    
    # 执行爬取
    stats = tool_crawler.crawl_all_tools()
    
    # 验证结果
    print(f"\n  验证结果:")
    print(f"    新增数量: {stats['new_count']}")
    print(f"    重复数量: {stats['duplicate_count']}")
    print(f"    失败数量: {stats['failed_count']}")
    
    # 检查数据库
    all_tools = tool_store.query_all()
    print(f"    数据库中的工具数: {len(all_tools)}")
    
    success = (stats['new_count'] == stats['total'] and 
               stats['duplicate_count'] == 0 and 
               len(all_tools) == stats['total'])
    
    if success:
        print("  ✓ 第一次爬取测试通过")
    else:
        print("  ✗ 第一次爬取测试失败")
    
    return success


def test_second_crawl():
    """第二次爬取（应该全部去重）"""
    print("\n[测试2] 第二次爬取（应该全部去重）")
    
    # 执行爬取
    stats = tool_crawler.crawl_all_tools()
    
    # 验证结果
    print(f"\n  验证结果:")
    print(f"    新增数量: {stats['new_count']}")
    print(f"    重复数量: {stats['duplicate_count']}")
    print(f"    失败数量: {stats['failed_count']}")
    
    success = (stats['new_count'] == 0 and 
               stats['duplicate_count'] == stats['total'])
    
    if success:
        print("  ✓ 第二次爬取去重测试通过")
    else:
        print("  ✗ 第二次爬取去重测试失败")
    
    return success


def test_category_split():
    """验证分类正确"""
    print("\n[测试3] 验证分类分布")
    
    beginner_tools = tool_store.query_by_category('新手入门')
    advanced_tools = tool_store.query_by_category('进阶技术')
    
    print(f"  新手入门: {len(beginner_tools)} 条")
    for tool in beginner_tools:
        print(f"    - {tool['tool_name']}")
    
    print(f"  进阶技术: {len(advanced_tools)} 条")
    for tool in advanced_tools:
        print(f"    - {tool['tool_name']}")
    
    success = len(beginner_tools) > 0 and len(advanced_tools) > 0
    
    if success:
        print("  ✓ 分类验证通过")
    else:
        print("  ✗ 分类验证失败")
    
    return success


def test_data_integrity():
    """验证数据完整性"""
    print("\n[测试4] 验证数据完整性")
    
    all_tools = tool_store.query_all()
    
    required_fields = ['title', 'url', 'source', 'tool_name', 'category']
    
    incomplete = 0
    for tool in all_tools:
        for field in required_fields:
            if not tool.get(field):
                print(f"  ✗ {tool.get('tool_name', 'Unknown')} 缺少字段: {field}")
                incomplete += 1
    
    if incomplete == 0:
        print(f"  ✓ 所有 {len(all_tools)} 条工具数据完整")
        return True
    else:
        print(f"  ✗ 发现 {incomplete} 条数据不完整")
        return False


def test_duplicate_detection():
    """验证去重机制"""
    print("\n[测试5] 验证去重机制")
    
    all_tools = tool_store.query_all()
    urls = [tool['url'] for tool in all_tools]
    unique_urls = set(urls)
    
    if len(urls) == len(unique_urls):
        print(f"  ✓ 没有重复的 URL，共 {len(urls)} 条唯一工具")
        return True
    else:
        duplicate_count = len(urls) - len(unique_urls)
        print(f"  ✗ 发现 {duplicate_count} 条重复 URL")
        return False


def print_sample_data():
    """打印示例数据"""
    print("\n[示例] 数据库中的工具样本")
    
    all_tools = tool_store.query_all()
    
    print(f"\n总共 {len(all_tools)} 条工具")
    print("\n前 5 条工具信息:")
    
    for i, tool in enumerate(all_tools[:5], 1):
        print(f"\n{i}. {tool['title']}")
        print(f"   工具: {tool['tool_name']}")
        print(f"   来源: {tool['source']}")
        print(f"   分类: {tool['category']}")
        print(f"   URL: {tool['url']}")


def main():
    """主测试流程"""
    print("=" * 60)
    print("T1.4 工具爬虫管理器全链路测试")
    print("=" * 60)
    
    tests = [
        ("第一次爬取", test_first_crawl),
        ("第二次爬取去重", test_second_crawl),
        ("分类分布验证", test_category_split),
        ("数据完整性验证", test_data_integrity),
        ("去重机制验证", test_duplicate_detection),
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
    
    # 打印示例数据
    print_sample_data()
    
    # 总结
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{len(tests)} 通过")
    print("=" * 60)
    
    return passed == len(tests)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
