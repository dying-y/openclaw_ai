import sqlite3
import json
from datetime import datetime
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent.parent / "data" / "tools.db"

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
    
    # 创建 tools 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            publish_time TEXT,
            source TEXT,
            tool_name TEXT,
            category TEXT DEFAULT '',
            summary TEXT DEFAULT '',
            content TEXT DEFAULT '',
            tool_type TEXT DEFAULT '',
            difficulty TEXT DEFAULT '',
            cost_level TEXT DEFAULT '',
            tech_requirement TEXT DEFAULT '',
            target_users TEXT DEFAULT '',
            score REAL DEFAULT 0.0,
            recommend_level TEXT DEFAULT '',
            analysis_json TEXT DEFAULT '',
            search_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    
    conn.commit()
    conn.close()


# 初始化数据库
_init_db()


def insert_tool(tool_dict):
    """
    插入工具数据
    
    参数：
        tool_dict: 包含工具信息的字典
    
    返回：
        True if 成功, False if 失败
    """
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # 检查 URL 是否已存在
        cursor.execute("SELECT id FROM tools WHERE url = ?", (tool_dict.get('url'),))
        if cursor.fetchone():
            conn.close()
            return False
        
        # 插入数据
        cursor.execute("""
            INSERT INTO tools (
                title, url, publish_time, source, tool_name, category, 
                summary, content, tool_type, difficulty, cost_level, 
                tech_requirement, target_users, score, recommend_level, 
                analysis_json, search_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tool_dict.get('title'),
            tool_dict.get('url'),
            tool_dict.get('publish_time'),
            tool_dict.get('source'),
            tool_dict.get('tool_name'),
            tool_dict.get('category'),
            tool_dict.get('summary'),
            tool_dict.get('content'),
            tool_dict.get('tool_type'),
            tool_dict.get('difficulty'),
            tool_dict.get('cost_level'),
            tool_dict.get('tech_requirement'),
            tool_dict.get('target_users'),
            tool_dict.get('score', 0.0),
            tool_dict.get('recommend_level'),
            tool_dict.get('analysis_json', ''),
            tool_dict.get('search_count', 0)
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 插入工具失败: {e}")
        return False


def query_all():
    """查询所有工具，返回 list[dict]"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tools ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 查询所有工具失败: {e}")
        return []


def query_by_category(category):
    """按分类查询工具"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tools WHERE category = ? ORDER BY created_at DESC",
            (category,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 按分类查询失败: {e}")
        return []


def query_by_date(date_str):
    """按日期查询工具（date_str 格式: YYYY-MM-DD）"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM tools 
            WHERE DATE(created_at) = ? 
            ORDER BY created_at DESC
        """, (date_str,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 按日期查询失败: {e}")
        return []


def query_by_keyword(keyword):
    """按关键词模糊搜索（标题+工具名）"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        query_pattern = f"%{keyword}%"
        cursor.execute("""
            SELECT * FROM tools 
            WHERE title LIKE ? OR tool_name LIKE ? 
            ORDER BY created_at DESC
        """, (query_pattern, query_pattern))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 按关键词查询失败: {e}")
        return []


def is_url_exists(url):
    """检查 URL 是否已存在"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tools WHERE url = ?", (url,))
        result = cursor.fetchone() is not None
        conn.close()
        return result
    except Exception as e:
        print(f"[错误] 检查 URL 存在失败: {e}")
        return False


def update_analysis(tool_id, analysis_dict):
    """更新分析结果和评分"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        # 将分析结果转为 JSON
        analysis_json = json.dumps(analysis_dict, ensure_ascii=False)
        
        cursor.execute("""
            UPDATE tools 
            SET analysis_json = ?, 
                score = ?,
                recommend_level = ?,
                tool_type = ?,
                difficulty = ?,
                cost_level = ?,
                tech_requirement = ?,
                target_users = ?,
                updated_at = datetime('now','localtime')
            WHERE id = ?
        """, (
            analysis_json,
            analysis_dict.get('overall_score', 0.0),
            analysis_dict.get('recommend_level'),
            analysis_dict.get('tool_type'),
            analysis_dict.get('difficulty'),
            analysis_dict.get('cost_level'),
            analysis_dict.get('tech_requirement'),
            analysis_dict.get('target_users'),
            tool_id
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 更新分析结果失败: {e}")
        return False


def increment_search_count(tool_id):
    """搜索次数+1"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tools SET search_count = search_count + 1 WHERE id = ?",
            (tool_id,)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 更新搜索次数失败: {e}")
        return False


def get_top_tools(limit=10):
    """获取热门工具（按搜索次数+评分排序）"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        # 综合排序：搜索次数 * 0.4 + 评分 * 0.6
        cursor.execute("""
            SELECT * FROM tools 
            ORDER BY (search_count * 0.4 + score * 0.6) DESC 
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[错误] 获取热门工具失败: {e}")
        return []


def clear_all():
    """清空所有数据（仅用于测试）"""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tools")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[错误] 清空数据失败: {e}")
        return False
