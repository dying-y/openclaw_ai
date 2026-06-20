"""
报告生成模块 - 生成日报、热门榜单、趋势分析
"""
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import os

class ReportGenerator:
    """报告生成器 - 生成各种报告"""
    
    def __init__(self, db_path: str = 'data/tools.db', output_dir: str = 'outputs'):
        """初始化报告生成器"""
        self.db_path = db_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_daily_ranking(self, date_str: Optional[str] = None) -> List[Dict]:
        """
        获取日排行榜 - 基于当日搜索热度和评分
        
        Args:
            date_str: 日期字符串，格式 'YYYY-MM-DD'，默认为今天
            
        Returns:
            排序后的工具列表
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 获取今日及之前的数据，计算综合热度
        cursor.execute('''
            SELECT 
                id, title, tool_name, url, source, tool_type,
                summary, score, recommend_level, search_count,
                created_at, updated_at
            FROM tools
            WHERE date(created_at) <= ?
            ORDER BY score DESC, search_count DESC
            LIMIT 20
        ''', (date_str,))
        
        tools = cursor.fetchall()
        conn.close()
        
        results = []
        for rank, tool in enumerate(tools, 1):
            results.append({
                'rank': rank,
                'id': tool['id'],
                'title': tool['title'],
                'tool_name': tool['tool_name'],
                'url': tool['url'],
                'source': tool['source'],
                'tool_type': tool['tool_type'],
                'summary': tool['summary'],
                'score': tool['score'],
                'search_count': tool['search_count'],
                'recommend_level': tool['recommend_level']
            })
        
        return results
    
    def get_hot_ranking(self, days: int = 7, limit: int = 20) -> List[Dict]:
        """
        获取热门榜单 - 基于最近N天的搜索热度
        
        Args:
            days: 统计天数
            limit: 返回数量
            
        Returns:
            热门工具列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # 获取最近N天搜索量最多的工具
        cursor.execute('''
            SELECT 
                id, title, tool_name, url, source, tool_type,
                summary, score, recommend_level, search_count,
                created_at
            FROM tools
            WHERE date(created_at) >= ?
            ORDER BY search_count DESC, score DESC
            LIMIT ?
        ''', (start_date, limit))
        
        tools = cursor.fetchall()
        conn.close()
        
        results = []
        for rank, tool in enumerate(tools, 1):
            results.append({
                'rank': rank,
                'id': tool['id'],
                'title': tool['title'],
                'tool_name': tool['tool_name'],
                'url': tool['url'],
                'source': tool['source'],
                'tool_type': tool['tool_type'],
                'summary': tool['summary'],
                'score': tool['score'],
                'search_count': tool['search_count'],
                'recommend_level': tool['recommend_level'],
                'created_at': tool['created_at']
            })
        
        return results
    
    def get_score_ranking(self, limit: int = 20) -> List[Dict]:
        """
        获取评分榜单 - 基于工具综合评分
        
        Args:
            limit: 返回数量
            
        Returns:
            高评分工具列表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                id, title, tool_name, url, source, tool_type,
                summary, score, recommend_level, search_count
            FROM tools
            WHERE score > 0
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        
        tools = cursor.fetchall()
        conn.close()
        
        results = []
        for rank, tool in enumerate(tools, 1):
            results.append({
                'rank': rank,
                'id': tool['id'],
                'title': tool['title'],
                'tool_name': tool['tool_name'],
                'url': tool['url'],
                'source': tool['source'],
                'tool_type': tool['tool_type'],
                'summary': tool['summary'],
                'score': tool['score'],
                'recommend_level': tool['recommend_level'],
                'search_count': tool['search_count']
            })
        
        return results
    
    def get_category_ranking(self, category_filter: str = None, limit: int = 10) -> List[Dict]:
        """
        获取分类排行榜
        
        Args:
            category_filter: 类别过滤，如 'GPT', 'Claude', '图像生成' 等
            limit: 每个类别返回的数量
            
        Returns:
            分类排行结果
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if category_filter:
            cursor.execute('''
                SELECT 
                    id, title, tool_name, url, source, tool_type,
                    summary, score, recommend_level, search_count, category
                FROM tools
                WHERE tool_type LIKE ?
                ORDER BY score DESC, search_count DESC
                LIMIT ?
            ''', (f'%{category_filter}%', limit))
        else:
            cursor.execute('''
                SELECT 
                    id, title, tool_name, url, source, tool_type,
                    summary, score, recommend_level, search_count, category
                FROM tools
                ORDER BY score DESC, search_count DESC
                LIMIT ?
            ''', (limit,))
        
        tools = cursor.fetchall()
        
        # 按tool_type分组
        grouped = {}
        for tool in tools:
            tool_type = tool['tool_type'] if tool['tool_type'] else '未分类'
            if tool_type not in grouped:
                grouped[tool_type] = []
            grouped[tool_type].append({
                'id': tool['id'],
                'title': tool['title'],
                'tool_name': tool['tool_name'],
                'score': tool['score'],
                'search_count': tool['search_count']
            })
        
        conn.close()
        
        results = []
        for tool_type, items in grouped.items():
            for rank, item in enumerate(items[:limit], 1):
                results.append({
                    'category': tool_type,
                    'rank': rank,
                    **item
                })
        
        return results
    
    def generate_daily_report(self, date_str: Optional[str] = None) -> Dict:
        """
        生成每日报告
        
        Args:
            date_str: 日期字符串
            
        Returns:
            报告数据
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        report = {
            'type': 'daily_report',
            'date': date_str,
            'generated_at': datetime.now().isoformat(),
            'rankings': {
                'overall': self.get_daily_ranking(date_str),
                'by_score': self.get_score_ranking(limit=10),
                'by_category': self.get_category_ranking(limit=10)
            },
            'summary': self._generate_summary()
        }
        
        return report
    
    def generate_weekly_report(self) -> Dict:
        """生成周报告"""
        report = {
            'type': 'weekly_report',
            'week_start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'week_end': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'rankings': {
                'hot': self.get_hot_ranking(days=7, limit=15),
                'by_score': self.get_score_ranking(limit=15),
                'by_category': self.get_category_ranking(limit=15)
            },
            'summary': self._generate_summary()
        }
        
        return report
    
    def _generate_summary(self) -> Dict:
        """生成报告摘要"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 统计基本信息
        cursor.execute('SELECT COUNT(*) FROM tools')
        total_tools = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(search_count) FROM tools')
        total_searches = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT COUNT(DISTINCT tool_type) FROM tools')
        total_categories = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(score) FROM tools WHERE score > 0')
        avg_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_tools': total_tools,
            'total_searches': total_searches,
            'total_categories': total_categories,
            'average_score': round(avg_score, 2)
        }
    
    def save_report_json(self, report: Dict, report_type: str = 'daily') -> str:
        """保存报告为JSON文件"""
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Path(self.output_dir) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"[Report] 报告已保存: {filepath}")
        return str(filepath)
    
    def save_report_html(self, report: Dict, report_type: str = 'daily') -> str:
        """保存报告为HTML文件"""
        filename = f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = Path(self.output_dir) / filename
        
        html_content = self._generate_html(report, report_type)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[Report] HTML报告已保存: {filepath}")
        return str(filepath)
    
    def _generate_html(self, report: Dict, report_type: str) -> str:
        """生成HTML内容"""
        title = f"{'每日' if report_type == 'daily' else '周'} AI工具报告"
        
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{
                    font-family: 'Microsoft YaHei', Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    background: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #555;
                    margin-top: 30px;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin: 20px 0;
                }}
                .summary-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .summary-card h3 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .summary-card p {{
                    margin: 5px 0 0 0;
                    opacity: 0.9;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background-color: #007bff;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }}
                td {{
                    padding: 10px 12px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f8f9fa;
                }}
                .rank {{
                    font-weight: bold;
                    color: #007bff;
                    font-size: 18px;
                }}
                .score {{
                    color: #28a745;
                    font-weight: bold;
                }}
                .meta {{
                    color: #666;
                    font-size: 12px;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <p>生成时间: {report['generated_at']}</p>
                
                <h2>数据摘要</h2>
                <div class="summary">
                    <div class="summary-card">
                        <h3>{report['summary']['total_tools']}</h3>
                        <p>总工具数</p>
                    </div>
                    <div class="summary-card">
                        <h3>{report['summary']['total_searches']}</h3>
                        <p>总搜索数</p>
                    </div>
                    <div class="summary-card">
                        <h3>{report['summary']['total_categories']}</h3>
                        <p>类别数</p>
                    </div>
                    <div class="summary-card">
                        <h3>{report['summary']['average_score']:.2f}</h3>
                        <p>平均评分</p>
                    </div>
                </div>
                
                <h2>综合排行</h2>
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>工具名称</th>
                            <th>来源</th>
                            <th>类型</th>
                            <th>评分</th>
                            <th>搜索次数</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # 处理不同报告类型的数据结构
        ranking_data = report['rankings'].get('overall') or report['rankings'].get('hot', [])
        
        for item in ranking_data[:10]:
            html += f"""
                        <tr>
                            <td class="rank">#{item['rank']}</td>
                            <td><strong>{item['title']}</strong></td>
                            <td>{item['source']}</td>
                            <td>{item['tool_type']}</td>
                            <td class="score">{item['score']:.2f}</td>
                            <td>{item['search_count']}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
                
                <div class="meta">
                    <p>本报告由 OpenClaw AI 系统自动生成</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def get_trend_data(self, days: int = 30) -> Dict:
        """
        获取趋势数据 - 按天统计工具数和搜索量变化
        
        Args:
            days: 统计天数
            
        Returns:
            趋势数据
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 按日期统计
        cursor.execute('''
            SELECT 
                date(created_at) as date,
                COUNT(*) as tool_count,
                SUM(search_count) as search_total
            FROM tools
            WHERE created_at >= datetime('now', '-' || ? || ' days')
            GROUP BY date(created_at)
            ORDER BY date
        ''', (days,))
        
        trends = cursor.fetchall()
        conn.close()
        
        data = {
            'period_days': days,
            'trend_data': []
        }
        
        for trend in trends:
            data['trend_data'].append({
                'date': trend['date'],
                'tool_count': trend['tool_count'],
                'search_total': trend['search_total'] or 0
            })
        
        return data
