"""
定时任务调度器 - 使用APScheduler实现自动爬取和报告生成
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from pytz import utc
import logging

# 导入业务模块
from crawler import tool_crawler
from report.report_generator import ReportGenerator
from db import tool_store

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.scheduler = BackgroundScheduler(timezone=utc)
        self.report_gen = ReportGenerator()
        
    def start(self):
        """启动调度器"""
        logger.info("启动定时任务调度器...")
        
        # 每日早8点执行爬虫
        self.scheduler.add_job(
            self.daily_crawl_task,
            'cron',
            hour=8,
            minute=0,
            id='daily_crawl',
            name='每日爬虫任务'
        )
        
        # 每日晚11点生成日报
        self.scheduler.add_job(
            self.daily_report_task,
            'cron',
            hour=23,
            minute=0,
            id='daily_report',
            name='每日报告生成'
        )
        
        # 每周一早8点生成周报
        self.scheduler.add_job(
            self.weekly_report_task,
            'cron',
            day_of_week='0',
            hour=8,
            minute=0,
            id='weekly_report',
            name='周报生成'
        )
        
        # 每小时更新一次搜索热度
        self.scheduler.add_job(
            self.update_search_stats,
            'interval',
            hours=1,
            id='update_search_stats',
            name='更新搜索统计'
        )
        
        # 每天凌晨2点清理过期缓存
        self.scheduler.add_job(
            self.cleanup_cache,
            'cron',
            hour=2,
            minute=0,
            id='cleanup_cache',
            name='缓存清理'
        )
        
        self.scheduler.start()
        logger.info("定时任务调度器已启动!")
        self.print_jobs()
    
    def stop(self):
        """停止调度器"""
        if self.scheduler.running:
            logger.info("停止定时任务调度器...")
            self.scheduler.shutdown()
    
    def print_jobs(self):
        """打印所有定时任务"""
        logger.info("已配置的定时任务:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  - [{job.id}] {job.name}")
    
    def daily_crawl_task(self):
        """每日爬虫任务"""
        logger.info("=" * 50)
        logger.info("[爬虫] 开始执行每日爬虫任务...")
        
        try:
            # 初始化数据库
            tool_store._init_db()
            
            # 执行新手爬虫
            logger.info("[爬虫] 执行新手模式爬虫...")
            beginner_tools = tool_crawler.crawl_beginner_tools()
            logger.info(f"[爬虫] 新手模式: 获取 {len(beginner_tools)} 个工具")
            
            # 执行老手爬虫
            logger.info("[爬虫] 执行老手模式爬虫...")
            advanced_tools = tool_crawler.crawl_advanced_tools()
            logger.info(f"[爬虫] 老手模式: 获取 {len(advanced_tools)} 个工具")
            
            # 去重入库
            total_new = len(beginner_tools) + len(advanced_tools)
            logger.info(f"[爬虫] 共获取 {total_new} 个工具，正在进行去重...")
            
            logger.info(f"[爬虫] 每日爬虫任务完成! 新增工具数: {total_new}")
            
        except Exception as e:
            logger.error(f"[爬虫] 爬虫任务失败: {e}", exc_info=True)
    
    def daily_report_task(self):
        """每日报告生成任务"""
        logger.info("=" * 50)
        logger.info("[报告] 开始生成每日报告...")
        
        try:
            # 生成报告
            report = self.report_gen.generate_daily_report()
            
            # 保存JSON和HTML
            json_path = self.report_gen.save_report_json(report, 'daily')
            html_path = self.report_gen.save_report_html(report, 'daily')
            
            logger.info(f"[报告] 每日报告生成完成!")
            logger.info(f"[报告]   JSON: {json_path}")
            logger.info(f"[报告]   HTML: {html_path}")
            
            # 记录统计
            summary = report['summary']
            logger.info(f"[报告] 统计信息:")
            logger.info(f"        工具总数: {summary['total_tools']}")
            logger.info(f"        搜索总数: {summary['total_searches']}")
            logger.info(f"        平均评分: {summary['average_score']:.2f}")
            
        except Exception as e:
            logger.error(f"[报告] 报告生成失败: {e}", exc_info=True)
    
    def weekly_report_task(self):
        """周报生成任务"""
        logger.info("=" * 50)
        logger.info("[周报] 开始生成周报告...")
        
        try:
            # 生成周报
            report = self.report_gen.generate_weekly_report()
            
            # 保存报告
            json_path = self.report_gen.save_report_json(report, 'weekly')
            html_path = self.report_gen.save_report_html(report, 'weekly')
            
            logger.info(f"[周报] 周报告生成完成!")
            logger.info(f"[周报]   JSON: {json_path}")
            logger.info(f"[周报]   HTML: {html_path}")
            
        except Exception as e:
            logger.error(f"[周报] 周报生成失败: {e}", exc_info=True)
    
    def update_search_stats(self):
        """更新搜索统计"""
        try:
            # 这是一个占位符任务，可以用于定期更新搜索热度
            conn = tool_store._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) as count FROM tools')
            total = cursor.fetchone()['count']
            
            cursor.execute('SELECT SUM(search_count) as total FROM tools')
            searches = cursor.fetchone()['total'] or 0
            
            conn.close()
            
            logger.debug(f"[搜索] 当前统计: {total} 个工具, {searches} 次搜索")
            
        except Exception as e:
            logger.error(f"[搜索] 搜索统计更新失败: {e}")
    
    def cleanup_cache(self):
        """清理过期缓存"""
        try:
            logger.info("[清理] 开始清理过期缓存...")
            
            # 清理超过30天的数据（可选）
            # 这里可以添加数据库优化等操作
            
            logger.info("[清理] 缓存清理完成")
            
        except Exception as e:
            logger.error(f"[清理] 缓存清理失败: {e}")
    
    def get_job_stats(self):
        """获取所有定时任务的统计"""
        stats = {
            'scheduler_running': self.scheduler.running,
            'job_count': len(self.scheduler.get_jobs()),
            'jobs': []
        }
        
        for job in self.scheduler.get_jobs():
            next_run = job.next_run_time
            next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else '未安排'
            
            stats['jobs'].append({
                'id': job.id,
                'name': job.name,
                'next_run': next_run_str,
                'trigger': str(job.trigger)
            })
        
        return stats


# 全局调度器实例
_scheduler_instance = None


def get_scheduler():
    """获取全局调度器实例"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = TaskScheduler()
    return _scheduler_instance


def start_scheduler():
    """启动调度器"""
    scheduler = get_scheduler()
    scheduler.start()


def stop_scheduler():
    """停止调度器"""
    scheduler = get_scheduler()
    scheduler.stop()


if __name__ == '__main__':
    # 测试模式：立即运行所有任务
    print("=" * 50)
    print("定时任务调度器 - 测试模式")
    print("=" * 50)
    
    scheduler = TaskScheduler()
    
    print("\n执行每日爬虫任务...")
    scheduler.daily_crawl_task()
    
    print("\n执行每日报告任务...")
    scheduler.daily_report_task()
    
    print("\n执行周报告任务...")
    scheduler.weekly_report_task()
    
    print("\n更新搜索统计...")
    scheduler.update_search_stats()
    
    print("\n清理缓存...")
    scheduler.cleanup_cache()
    
    print("\n=" * 50)
    print("✓ 测试完成!")
    print("=" * 50)
