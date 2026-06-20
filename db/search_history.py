import sqlite3
from datetime import datetime
from pathlib import Path
from collections import Counter

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "search_history.db"

# 确保 data 文件夹存在
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    """初始化数据库表"""
    conn = _get_connection()
    cursor = conn.cursor()
    
    # 创建 search_history 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            search_time TEXT DEFAULT (datetime('now','localtime')),
            result_count INTEGER DEFAULT 0,
            click_tool_id INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()


# 初始化数据库
_init_db()


def add_search(keyword, result_count=0, click_tool_id=0):
    """
    添加一条搜索记录
    
    参数：
        keyword: 搜索关键词
        result_count: 搜索结果数量
        click_tool_id: 用户点击的工具 ID
    
    返回：
        True if 成功, False if 失败
    """
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO search_history (keyword, result_count, click_tool_id)
            VALUES (?, ?, ?)
        """, (keyword, result_count, click_tool_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 添加搜索记录失败: {e}")
        return False


def get_recent_searches(limit=10):
    """
    获取最近 N 条搜索记录（去重，相同关键词只保留最新一条）
    
    参数：
        limit: 返回条数
    
    返回：
        list of dict
    """
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # 按关键词分组，取每组最新的记录
        cursor.execute("""
            SELECT keyword, search_time, result_count, click_tool_id
            FROM search_history
            WHERE id IN (
                SELECT MAX(id) FROM search_history 
                GROUP BY keyword
            )
            ORDER BY search_time DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 获取最近搜索失败: {e}")
        return []


def get_hot_searches(limit=10):
    """
    获取热门搜索 Top N（按搜索次数排序）
    
    参数：
        limit: 返回条数
    
    返回：
        list of dict，每条包含 keyword 和 count
    """
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT keyword, COUNT(*) as count, MAX(search_time) as latest_time
            FROM search_history
            GROUP BY keyword
            ORDER BY count DESC, latest_time DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 获取热门搜索失败: {e}")
        return []


def delete_search(keyword):
    """删除某条关键词的所有搜索记录"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM search_history WHERE keyword = ?", (keyword,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 删除搜索记录失败: {e}")
        return False


def clear_history():
    """清空所有搜索记录"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM search_history")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 清空搜索历史失败: {e}")
        return False


def get_search_stats():
    """获取搜索统计信息"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # 总搜索次数
        cursor.execute("SELECT COUNT(*) as total FROM search_history")
        total = cursor.fetchone()['total']
        
        # 唯一关键词数
        cursor.execute("SELECT COUNT(DISTINCT keyword) as unique_count FROM search_history")
        unique_count = cursor.fetchone()['unique_count']
        
        conn.close()
        return {
            'total_searches': total,
            'unique_keywords': unique_count
        }
    except Exception as e:
        print(f"[错误] 获取搜索统计失败: {e}")
        return {'total_searches': 0, 'unique_keywords': 0}
