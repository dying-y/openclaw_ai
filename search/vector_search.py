"""
向量搜索模块 - 使用FAISS和句子向量实现语义搜索
"""
import os
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import sqlite3
from datetime import datetime

class VectorSearchEngine:
    """向量搜索引擎 - 支持语义搜索"""
    
    def __init__(self, db_path: str = 'data/tools.db', model_name: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化向量搜索引擎
        
        Args:
            db_path: 数据库路径
            model_name: 句子变换模型名称
        """
        self.db_path = db_path
        self.model_name = model_name
        self.model = None
        self.index = None
        self.tool_ids = []
        self.embeddings_path = 'data/embeddings.pkl'
        self.index_path = 'data/faiss.index'
        
    def load_model(self):
        """加载句子转换模型"""
        if self.model is None:
            print(f"[VectorSearch] 加载模型: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
    
    def build_index(self, rebuild: bool = False):
        """
        构建FAISS索引
        
        Args:
            rebuild: 是否重新构建索引
        """
        self.load_model()
        
        # 如果索引已存在且不需要重建，加载现有索引
        if os.path.exists(self.index_path) and os.path.exists(self.embeddings_path) and not rebuild:
            print("[VectorSearch] 加载现有索引...")
            self.index = faiss.read_index(self.index_path)
            with open(self.embeddings_path, 'rb') as f:
                data = pickle.load(f)
                self.tool_ids = data['tool_ids']
            return
        
        print("[VectorSearch] 构建新索引...")
        
        # 从数据库获取所有工具
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, tool_name, summary, content, tool_type, category, target_users 
            FROM tools
        ''')
        tools = cursor.fetchall()
        conn.close()
        
        if not tools:
            print("[VectorSearch] 数据库中没有工具数据")
            return
        
        # 构建索引文本 - 综合多个字段
        documents = []
        self.tool_ids = []
        
        for tool in tools:
            doc = f"{tool['title']} {tool['tool_name']} {tool['summary']} {tool['content']} {tool['tool_type']} {tool['category']}"
            documents.append(doc)
            self.tool_ids.append(tool['id'])
        
        print(f"[VectorSearch] 为 {len(documents)} 个工具生成向量...")
        
        # 生成向量
        embeddings = self.model.encode(documents, show_progress_bar=True, convert_to_numpy=True)
        
        # 创建FAISS索引
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        # 保存索引
        os.makedirs('data', exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump({'tool_ids': self.tool_ids}, f)
        
        print(f"[VectorSearch] 索引构建完成, 维度={dimension}, 工具数={len(self.tool_ids)}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        执行向量搜索
        
        Args:
            query: 搜索查询文本
            top_k: 返回前k个结果
            
        Returns:
            搜索结果列表，包含ID和相似度
        """
        if self.model is None or self.index is None:
            raise ValueError("索引未初始化，请先调用 build_index()")
        
        # 编码查询
        query_vector = self.model.encode([query], convert_to_numpy=True)
        
        # 搜索
        distances, indices = self.index.search(query_vector.astype('float32'), top_k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx >= 0:  # 有效的索引
                tool_id = self.tool_ids[idx]
                # L2距离转换为相似度分数 (0-1)
                similarity = 1 / (1 + dist)
                
                results.append({
                    'rank': i + 1,
                    'tool_id': tool_id,
                    'distance': float(dist),
                    'similarity': float(similarity)
                })
        
        return results
    
    def get_tool_details(self, tool_id: str) -> Dict:
        """获取工具详细信息"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tools WHERE id = ?', (tool_id,))
        tool = cursor.fetchone()
        conn.close()
        
        if tool:
            return dict(tool)
        return None
    
    def search_with_details(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索并返回完整的工具详情"""
        search_results = self.search(query, top_k)
        
        results_with_details = []
        for result in search_results:
            tool_details = self.get_tool_details(result['tool_id'])
            if tool_details:
                result['tool'] = tool_details
                results_with_details.append(result)
        
        return results_with_details


class HybridSearchEngine:
    """混合搜索引擎 - 融合关键词搜索和向量搜索"""
    
    def __init__(self, db_path: str = 'data/tools.db'):
        """初始化混合搜索引擎"""
        self.db_path = db_path
        self.vector_engine = VectorSearchEngine(db_path)
        
    def keyword_search(self, keyword: str, top_k: int = 5) -> List[Dict]:
        """关键词搜索"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 多字段搜索
        search_term = f'%{keyword}%'
        cursor.execute('''
            SELECT * FROM tools 
            WHERE title LIKE ? 
               OR tool_name LIKE ? 
               OR summary LIKE ?
               OR content LIKE ?
               OR category LIKE ?
            LIMIT ?
        ''', (search_term, search_term, search_term, search_term, search_term, top_k))
        
        tools = cursor.fetchall()
        conn.close()
        
        results = []
        for i, tool in enumerate(tools):
            results.append({
                'rank': i + 1,
                'tool': dict(tool),
                'search_type': 'keyword',
                'score': 0.0  # 将在混合搜索中计算
            })
        
        return results
    
    def hybrid_search(self, query: str, top_k: int = 5, 
                     keyword_weight: float = 0.3, 
                     vector_weight: float = 0.7) -> List[Dict]:
        """
        混合搜索 - 融合关键词和向量搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数
            keyword_weight: 关键词搜索权重
            vector_weight: 向量搜索权重
            
        Returns:
            融合后的搜索结果
        """
        # 初始化向量引擎
        if self.vector_engine.index is None:
            self.vector_engine.build_index()
        
        # 执行两种搜索
        keyword_results = self.keyword_search(query, top_k * 2)
        vector_results = self.vector_engine.search_with_details(query, top_k * 2)
        
        # 构建结果字典，基于tool_id去重
        combined_results = {}
        
        # 处理关键词搜索结果
        for result in keyword_results:
            tool_id = result['tool']['id']
            score = keyword_weight * 1.0  # 关键词匹配得1分
            combined_results[tool_id] = {
                'tool': result['tool'],
                'keyword_score': score,
                'vector_score': 0.0,
                'combined_score': 0.0
            }
        
        # 处理向量搜索结果
        for i, result in enumerate(vector_results):
            tool_id = result['tool_id']
            vector_score = vector_weight * result['similarity']
            
            if tool_id not in combined_results:
                combined_results[tool_id] = {
                    'tool': result['tool'],
                    'keyword_score': 0.0,
                    'vector_score': vector_score,
                    'combined_score': 0.0
                }
            else:
                combined_results[tool_id]['vector_score'] = vector_score
            
            combined_results[tool_id]['combined_score'] = (
                combined_results[tool_id]['keyword_score'] + 
                combined_results[tool_id]['vector_score']
            )
        
        # 按综合分数排序
        sorted_results = sorted(
            combined_results.items(),
            key=lambda x: x[1]['combined_score'],
            reverse=True
        )[:top_k]
        
        # 构建最终结果
        final_results = []
        for rank, (tool_id, scores) in enumerate(sorted_results, 1):
            final_results.append({
                'rank': rank,
                'tool_id': tool_id,
                'tool': scores['tool'],
                'keyword_score': float(scores['keyword_score']),
                'vector_score': float(scores['vector_score']),
                'combined_score': float(scores['combined_score']),
                'search_type': 'hybrid'
            })
        
        return final_results
    
    def save_search_stats(self, query: str, results: List[Dict], search_type: str):
        """保存搜索统计信息"""
        from db import search_history
        
        search_history._init_db()
        search_history.add_search(query, len(results))
