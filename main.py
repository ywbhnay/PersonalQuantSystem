#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一量化交易系统 - 主入口文件 (重构版)

高性能量化交易系统，融合miniQMT实盘交易和BackTrader回测框架
支持每秒10,000条数据处理的专业量化交易解决方案

Author: AlphaBot
Version: 2.0
"""

# OPTIMIZED: 优化导入语句，移除未使用的导入
import argparse
import sys
from pathlib import Path

from libs.core.strategies.base_strategy import BaseStrategy
from libs.utils.container import container
from libs.config.consts import DEFAULT_TRADE_SIZE
from trading_engine import TradingEngine


# OPTIMIZED: 示例策略类 - 使用常量替代魔术数字
class MyStrategy(BaseStrategy):
    """示例交易策略
    
    简单的趋势跟踪策略，基于价格变化进行买卖决策
    """
    
    def next(self):
        """策略主逻辑
        
        每个数据周期调用一次，实现具体的交易逻辑
        """
        # 策略逻辑
        if not self.position:
            if self.data.close[0] > self.data.close[-1]:  # 简单上涨信号
                self.buy_stock(self.data, size=DEFAULT_TRADE_SIZE)
        else:
            if self.data.close[0] < self.data.close[-1]:  # 简单下跌信号
                self.sell_stock(self.data, size=self.position.size)


def parse_arguments():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的命令行参数
    """
    parser = argparse.ArgumentParser(
        description='统一量化交易系统 - 高性能量化交易解决方案',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --mode backtest --debug
  python main.py --mode live --config custom_config.yaml
        """
    )
    
    parser.add_argument('--mode', choices=['backtest', 'live'], default='live',
                       help='运行模式: backtest(回测) 或 live(实盘)')
    parser.add_argument('--debug', action='store_true',
                       help='启用调试模式，显示完整错误堆栈信息')
    parser.add_argument('--config', type=str,
                       help='指定配置文件路径（可选）')
    
    return parser.parse_args()


def setup_error_handling():
    """设置全局错误处理
    
    OPTIMIZED: 简化错误处理逻辑，提升性能
    """
    # 从依赖注入容器中获取管理器
    error_manager = container.get('error_manager')
    output_manager = container.get('output_manager')
    
    # OPTIMIZED: 简化错误回调函数
    def error_callback(error_info):
        """错误回调处理函数
        
        Args:
            error_info: 错误信息对象
        """
        output_manager.error(f"[{error_info.code}] {error_info.message}")
        if error_info.suggestion:
            output_manager.info(f"建议: {error_info.suggestion}")
    
    error_manager.register_callback(error_callback)


def main():
    """主函数
    
    程序入口点，负责初始化系统并启动交易引擎
    """
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 设置错误处理
        setup_error_handling()
        
        # 获取输出管理器
        output_manager = container.get('output_manager')
        
        # 显示启动信息
        output_manager.success("=" * 60)
        output_manager.success("    统一量化交易系统 v2.0 启动中...")
        output_manager.success("=" * 60)
        output_manager.info(f"运行模式: {args.mode}")
        output_manager.info(f"调试模式: {'开启' if args.debug else '关闭'}")
        
        if args.config:
            output_manager.info(f"配置文件: {args.config}")
        
        # 创建并启动交易引擎
        engine = TradingEngine()
        
        # 添加策略
        engine.add_strategy(MyStrategy)
        
        # 根据模式运行
        if args.mode == 'backtest':
            output_manager.info("开始回测...")
            engine.run_backtest()
        else:
            output_manager.info("开始实盘交易...")
            engine.run_live()
            
        output_manager.success("系统运行完成")
        
    except KeyboardInterrupt:
        output_manager.warning("用户中断程序")
        sys.exit(0)
    except Exception as e:
        if args.debug if 'args' in locals() else False:
            import traceback
            print(f"系统错误: {e}")
            print("详细错误信息:")
            traceback.print_exc()
        else:
            print(f"系统错误: {e}")
            print("使用 --debug 参数查看详细错误信息")
        sys.exit(1)


if __name__ == '__main__':
    main()