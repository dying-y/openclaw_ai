"""
向量搜索和混合搜索测试
"""
import sys
import os
sys.path.insert(0, '/vercel/share/v0-project')

from search.vector_search import VectorSearchEngine, HybridSearchEngine
from db import tool_store

def test_vector_search():
    """测试向量搜索"""
    print("\n=== 向量搜索测试 ===\n")
    
    # 初始化数据库
    tool_store._init_db()
    
    # 获取数据库中的工具数量
    tools = tool_store.query_all()
    tools_count = len(tools) if tools else 0
    print(f"数据库中已有 {tools_count} 个工具")
    
    if tools_count == 0:
        print("添加测试工具数据...")
        test_tools = [
            {
                'title': 'ChatGPT',
                'summary': '由OpenAI开发的大型语言模型，可进行对话交互',
                'url': 'https://chat.openai.com',
                'source': 'OpenAI官方',
                'tool_type': '大语言模型',
                'difficulty': '新手',
                'cost_level': '付费',
                'tech_requirement': '无特殊要求',
                'content': '多轮对话，代码生成，文本改写。功能强大，易于使用',
                'category': 'ChatGPT GPT-4 对话 文本生成',
                'tool_name': 'ChatGPT'
            },
            {
                'title': 'Claude 3',
                'summary': 'Anthropic开发的先进AI助手，具有更强的推理能力',
                'url': 'https://claude.ai',
                'source': 'Anthropic',
                'tool_type': '大语言模型',
                'difficulty': '新手',
                'cost_level': '付费',
                'tech_requirement': '无特殊要求',
                'content': '长文本处理，逻辑推理，代码分析。推理能力强，处理长文本',
                'category': 'Claude AI 助手 推理',
                'tool_name': 'Claude 3'
            },
            {
                'title': 'Midjourney',
                'summary': '专业的AI图像生成工具，支持高质量文生图',
                'url': 'https://www.midjourney.com',
                'source': 'Midjourney Inc',
                'tool_type': '图像生成',
                'difficulty': '新手',
                'cost_level': '付费',
                'tech_requirement': 'Discord账号',
                'content': '文生图，风格迁移，图像变体。图像质量高，风格多样',
                'category': 'Midjourney 生成 艺术 绘画',
                'tool_name': 'Midjourney'
            }
        ]
        
        for tool in test_tools:
            if not tool_store.is_url_exists(tool['url']):
                tool_store.insert_tool(tool)
        print(f"✓ 添加了 {len(test_tools)} 个测试工具")
    
    # 创建向量搜索引擎
    engine = VectorSearchEngine()
    
    # 构建索引
    print("\n构建向量索引...")
    engine.build_index(rebuild=True)
    
    # 测试搜索
    test_queries = [
        '大语言模型对话',
        '图像生成工具',
        'AI编程助手',
        '文本处理'
    ]
    
    print("\n执行向量搜索测试:")
    for query in test_queries:
        print(f"\n查询: '{query}'")
        results = engine.search_with_details(query, top_k=3)
        
        if results:
            for result in results:
                print(f"  [{result['rank']}] {result['tool']['title']} "
                      f"(相似度: {result['similarity']:.2%})")
        else:
            print("  没有结果")
    
    print("\n✓ 向量搜索测试完成")


def test_hybrid_search():
    """测试混合搜索"""
    print("\n=== 混合搜索测试 ===\n")
    
    engine = HybridSearchEngine()
    
    test_queries = [
        'ChatGPT对话',
        '图像生成',
        'AI工具',
        '编程辅助'
    ]
    
    print("执行混合搜索测试:")
    for query in test_queries:
        print(f"\n查询: '{query}'")
        results = engine.hybrid_search(query, top_k=3)
        
        if results:
            for result in results:
                print(f"  [{result['rank']}] {result['tool']['title']}")
                print(f"       关键词分数: {result['keyword_score']:.2f}, "
                      f"向量分数: {result['vector_score']:.2f}, "
                      f"综合分数: {result['combined_score']:.2f}")
        else:
            print("  没有结果")
    
    print("\n✓ 混合搜索测试完成")


def test_search_save():
    """测试搜索历史保存"""
    print("\n=== 搜索历史测试 ===\n")
    
    engine = HybridSearchEngine()
    
    queries = ['GPT-4', 'Midjourney', '编程工具']
    
    print("保存搜索历史:")
    for query in queries:
        results = engine.hybrid_search(query, top_k=3)
        engine.save_search_stats(query, results, 'hybrid')
        print(f"  ✓ 已保存: '{query}' ({len(results)} 个结果)")
    
    print("\n✓ 搜索历史保存完成")


if __name__ == '__main__':
    try:
        test_vector_search()
        test_hybrid_search()
        test_search_save()
        
        print("\n" + "="*50)
        print("✓ 所有搜索测试通过!")
        print("="*50)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
