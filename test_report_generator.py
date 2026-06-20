"""
报告生成模块测试
"""
import sys
import os
sys.path.insert(0, '/vercel/share/v0-project')

from report.report_generator import ReportGenerator

def test_daily_ranking():
    """测试每日排行"""
    print("\n=== 每日排行榜测试 ===\n")
    
    gen = ReportGenerator()
    ranking = gen.get_daily_ranking()
    
    print(f"获取到 {len(ranking)} 个工具的排行:")
    for item in ranking[:5]:
        print(f"  #{item['rank']} {item['title']}")
        print(f"       评分: {item['score']:.2f}, 搜索: {item['search_count']}")
    
    print("\n✓ 每日排行测试完成")


def test_hot_ranking():
    """测试热门榜单"""
    print("\n=== 热门榜单测试 ===\n")
    
    gen = ReportGenerator()
    hot = gen.get_hot_ranking(days=7, limit=10)
    
    print(f"最近7天热门工具 ({len(hot)} 个):")
    for item in hot[:5]:
        print(f"  #{item['rank']} {item['title']}")
        print(f"       搜索数: {item['search_count']}, 评分: {item['score']:.2f}")
    
    print("\n✓ 热门榜单测试完成")


def test_score_ranking():
    """测试评分排行"""
    print("\n=== 评分排行榜测试 ===\n")
    
    gen = ReportGenerator()
    scores = gen.get_score_ranking(limit=10)
    
    print(f"高评分工具 ({len(scores)} 个):")
    for item in scores[:5]:
        print(f"  #{item['rank']} {item['title']}")
        print(f"       评分: {item['score']:.2f}, 推荐: {item['recommend_level']}")
    
    print("\n✓ 评分排行测试完成")


def test_category_ranking():
    """测试分类排行"""
    print("\n=== 分类排行榜测试 ===\n")
    
    gen = ReportGenerator()
    categories = gen.get_category_ranking(limit=10)
    
    print(f"各类别排行 ({len(categories)} 个工具):")
    for item in categories[:8]:
        print(f"  [{item['category']}] #{item['rank']} {item['title']}")
        print(f"       评分: {item['score']:.2f}")
    
    print("\n✓ 分类排行测试完成")


def test_daily_report():
    """测试每日报告生成"""
    print("\n=== 每日报告生成测试 ===\n")
    
    gen = ReportGenerator()
    
    # 生成报告
    report = gen.generate_daily_report()
    
    print(f"报告类型: {report['type']}")
    print(f"报告日期: {report['date']}")
    print(f"工具总数: {report['summary']['total_tools']}")
    print(f"总搜索数: {report['summary']['total_searches']}")
    print(f"平均评分: {report['summary']['average_score']:.2f}")
    
    print(f"\n综合排行前3:")
    for item in report['rankings']['overall'][:3]:
        print(f"  #{item['rank']} {item['title']} - 评分: {item['score']:.2f}")
    
    # 保存JSON报告
    json_path = gen.save_report_json(report, 'daily_test')
    print(f"\n✓ JSON报告已保存: {json_path}")
    
    # 保存HTML报告
    html_path = gen.save_report_html(report, 'daily_test')
    print(f"✓ HTML报告已保存: {html_path}")


def test_weekly_report():
    """测试周报告生成"""
    print("\n=== 周报告生成测试 ===\n")
    
    gen = ReportGenerator()
    
    # 生成周报告
    report = gen.generate_weekly_report()
    
    print(f"报告类型: {report['type']}")
    print(f"周期: {report['week_start']} 到 {report['week_end']}")
    print(f"工具总数: {report['summary']['total_tools']}")
    print(f"热门工具数: {len(report['rankings']['hot'])}")
    
    print(f"\n热门工具前3:")
    for item in report['rankings']['hot'][:3]:
        print(f"  #{item['rank']} {item['title']} - 搜索: {item['search_count']}")


def test_trend_data():
    """测试趋势数据"""
    print("\n=== 趋势数据测试 ===\n")
    
    gen = ReportGenerator()
    trends = gen.get_trend_data(days=30)
    
    print(f"30天趋势数据 ({len(trends['trend_data'])} 天):")
    for item in trends['trend_data'][-5:]:
        print(f"  {item['date']}: 工具数 {item['tool_count']}, 搜索数 {item['search_total']}")
    
    print("\n✓ 趋势数据测试完成")


if __name__ == '__main__':
    try:
        test_daily_ranking()
        test_hot_ranking()
        test_score_ranking()
        test_category_ranking()
        test_daily_report()
        test_weekly_report()
        test_trend_data()
        
        print("\n" + "="*50)
        print("✓ 所有报告生成测试通过!")
        print("="*50)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
