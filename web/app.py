"""
OpenClaw AI 工具库 - Flask Web应用主程序
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from datetime import datetime
import json

# 导入业务模块
from search.vector_search import HybridSearchEngine
from report.report_generator import ReportGenerator
from db import tool_store, search_history

# 创建Flask应用
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# 缓存配置
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}
cache = Cache(app, config=cache_config)

# 初始化业务模块
search_engine = HybridSearchEngine()
report_gen = ReportGenerator()

# 初始化数据库
tool_store._init_db()
search_history._init_db()


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """搜索API"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        search_type = data.get('type', 'hybrid')  # hybrid 或 keyword
        top_k = data.get('top_k', 10)
        
        if not query:
            return jsonify({'error': '查询不能为空'}), 400
        
        # 执行搜索
        if search_type == 'keyword':
            results = search_engine.keyword_search(query, top_k)
        else:
            results = search_engine.hybrid_search(query, top_k)
        
        # 保存搜索历史
        search_history.add_search(query, len(results))
        
        return jsonify({
            'success': True,
            'query': query,
            'search_type': search_type,
            'count': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools', methods=['GET'])
@cache.cached(timeout=600)
def get_tools():
    """获取所有工具"""
    try:
        tools = tool_store.query_all()
        
        if tools:
            result = [dict(tool) for tool in tools]
        else:
            result = []
        
        return jsonify({
            'success': True,
            'count': len(result),
            'tools': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tools/<int:tool_id>', methods=['GET'])
def get_tool_detail(tool_id):
    """获取工具详情"""
    try:
        conn = tool_store._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tools WHERE id = ?', (tool_id,))
        tool = cursor.fetchone()
        conn.close()
        
        if tool:
            return jsonify({
                'success': True,
                'tool': dict(tool)
            })
        else:
            return jsonify({'error': '工具不存在'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rankings/daily', methods=['GET'])
@cache.cached(timeout=3600)
def get_daily_ranking():
    """获取每日排行"""
    try:
        ranking = report_gen.get_daily_ranking()
        
        return jsonify({
            'success': True,
            'type': 'daily_ranking',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'count': len(ranking),
            'ranking': ranking
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rankings/hot', methods=['GET'])
@cache.cached(timeout=3600)
def get_hot_ranking():
    """获取热门排行"""
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        ranking = report_gen.get_hot_ranking(days=days, limit=limit)
        
        return jsonify({
            'success': True,
            'type': 'hot_ranking',
            'days': days,
            'count': len(ranking),
            'ranking': ranking
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rankings/score', methods=['GET'])
@cache.cached(timeout=3600)
def get_score_ranking():
    """获取评分排行"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        ranking = report_gen.get_score_ranking(limit=limit)
        
        return jsonify({
            'success': True,
            'type': 'score_ranking',
            'count': len(ranking),
            'ranking': ranking
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rankings/category', methods=['GET'])
@cache.cached(timeout=3600)
def get_category_ranking():
    """获取分类排行"""
    try:
        category = request.args.get('category', None)
        limit = request.args.get('limit', 10, type=int)
        
        ranking = report_gen.get_category_ranking(category_filter=category, limit=limit)
        
        return jsonify({
            'success': True,
            'type': 'category_ranking',
            'category': category,
            'count': len(ranking),
            'ranking': ranking
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/daily', methods=['GET'])
def get_daily_report():
    """获取每日报告"""
    try:
        date_str = request.args.get('date', None)
        report = report_gen.generate_daily_report(date_str)
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/weekly', methods=['GET'])
def get_weekly_report():
    """获取周报告"""
    try:
        report = report_gen.generate_weekly_report()
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trends', methods=['GET'])
@cache.cached(timeout=3600)
def get_trends():
    """获取趋势数据"""
    try:
        days = request.args.get('days', 30, type=int)
        trends = report_gen.get_trend_data(days=days)
        
        return jsonify({
            'success': True,
            'type': 'trends',
            'periods': trends['period_days'],
            'data_points': len(trends['trend_data']),
            'data': trends['trend_data']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search-history', methods=['GET'])
def get_search_history():
    """获取搜索历史"""
    try:
        limit = request.args.get('limit', 10, type=int)
        histories = search_history.get_recent_searches(limit=limit)
        
        result = [dict(h) for h in histories] if histories else []
        
        return jsonify({
            'success': True,
            'count': len(result),
            'history': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hot-searches', methods=['GET'])
def get_hot_searches():
    """获取热门搜索"""
    try:
        limit = request.args.get('limit', 10, type=int)
        hot = search_history.get_hot_searches(limit=limit)
        
        result = [dict(h) for h in hot] if hot else []
        
        return jsonify({
            'success': True,
            'count': len(result),
            'hot_searches': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
@cache.cached(timeout=3600)
def get_stats():
    """获取系统统计信息"""
    try:
        conn = tool_store._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM tools')
        total_tools = cursor.fetchone()['count']
        
        cursor.execute('SELECT SUM(search_count) as total FROM tools')
        total_searches = cursor.fetchone()['total'] or 0
        
        cursor.execute('SELECT COUNT(DISTINCT tool_type) as count FROM tools')
        categories = cursor.fetchone()['count']
        
        cursor.execute('SELECT AVG(score) as avg FROM tools WHERE score > 0')
        avg_score = cursor.fetchone()['avg'] or 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_tools': total_tools,
                'total_searches': total_searches,
                'categories': categories,
                'average_score': round(avg_score, 2)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.errorhandler(404)
def not_found(error):
    """404处理"""
    return jsonify({'error': '资源不存在'}), 404


@app.errorhandler(500)
def server_error(error):
    """500处理"""
    return jsonify({'error': '服务器错误'}), 500


if __name__ == '__main__':
    print("启动 OpenClaw AI 工具库 Web 服务器...")
    print("访问地址: http://localhost:5000")
    print("API文档: http://localhost:5000/api/docs")
    app.run(debug=True, host='0.0.0.0', port=5000)
