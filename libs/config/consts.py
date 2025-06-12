"""\n常量定义模块 - 简化版本，只保留常量定义\n"""

import os
import sys
import traceback
from enum import Enum
from typing import Optional


# ==================== 系统常量定义 ====================
# OPTIMIZED: 提取魔术数字为常量，提高代码可维护性
MAX_RETRY_ATTEMPTS = 3  # 最大重试次数
DEFAULT_RISK_PCT = 0.02  # 默认风险百分比
MAX_POSITIONS = 10  # 最大持仓数量
DEFAULT_PRICE_PRECISION = 2  # 默认价格精度
DEFAULT_VOLUME_UNIT = 100  # 默认交易单位（手）
DEFAULT_TRADE_SIZE = 100  # 默认交易数量
RISK_FREE_RATE = 0.03  # 无风险利率
TRADING_DAYS_PER_YEAR = 252  # 年交易日数

# 涨跌停限制常量
LIMIT_UP_RATIO = {
    'MAIN_BOARD': 0.1,      # 主板10%
    'STAR_MARKET': 0.2,     # 科创板20%
    'GROWTH_BOARD': 0.2,    # 创业板20%
    'BEIJING_BOARD': 0.3,   # 北交所30%
    'ST_STOCK': 0.05        # ST股5%
}


# ==================== 枚举类定义 ====================
class PriceType(Enum):
    """价格类型枚举"""
    LIMIT = 'LIMIT'        # 限价
    MARKET = 'MARKET'      # 市价
    STOP = 'STOP'          # 止损
    STOP_LIMIT = 'STOP_LIMIT'  # 止损限价


class OrderError(Enum):
    """订单错误类型枚举"""
    INSUFFICIENT_FUNDS = 'INSUFFICIENT_FUNDS'  # 资金不足
    INVALID_STOCK = 'INVALID_STOCK'            # 无效股票
    MARKET_CLOSED = 'MARKET_CLOSED'            # 市场关闭
    PRICE_LIMIT = 'PRICE_LIMIT'                # 价格限制
    VOLUME_LIMIT = 'VOLUME_LIMIT'              # 数量限制
    NETWORK = 'NETWORK'                        # 网络错误
    SYSTEM = 'SYSTEM'                          # 系统错误
    ACCOUNT = 'ACCOUNT'                        # 账户问题
    UNKNOWN = 'UNKNOWN'                        # 未知错误


class ErrorStrategy(Enum):
    """错误处理策略枚举"""
    RETRY = 'RETRY'                    # 重试
    REJECT = 'REJECT'                  # 拒绝
    ALLOW_BROKER_HANDLE = 'ALLOW_BROKER_HANDLE'  # 允许券商处理


class OrderStatus(Enum):
    """订单状态枚举"""
    SUBMITTED = 'SUBMITTED' #   提交   
    ACCEPTED = 'ACCEPTED'#  已提交
    PARTIAL = 'PARTIAL' #    部分成交
    COMPLETED = 'COMPLETED' #  全部成交
    CANCELED = 'CANCELED'   #  已撤销
    REJECTED = 'REJECTED'   #  已拒绝
    EXPIRED = 'EXPIRED'     #  已过期


class TradeDirection(Enum):
    """交易方向枚举"""
    BUY = 'BUY'  # 买入
    SELL = 'SELL'    #  卖出


class MarketType(Enum):
    """市场类型枚举"""
    STOCK = 'STOCK'
    FUND = 'FUND' #  基金
    BOND = 'BOND'#  债券
    OPTION = 'OPTION' #  期权
    FUTURE = 'FUTURE' #  期货


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class OrderType(Enum):
    """订单类型枚举"""
    MARKET = 'MARKET'      # 市价单
    LIMIT = 'LIMIT'        # 限价单
    STOP = 'STOP'          # 止损单
    STOP_LIMIT = 'STOP_LIMIT'  # 止损限价单


class PositionDirection(Enum):
    """持仓方向枚举"""
    LONG = 'LONG'   # 多头
    SHORT = 'SHORT' # 空头
    NET = 'NET'     # 净头寸


# ==================== 错误处理相关常量 ====================
CONNECTION_MESSAGES = {
    'connecting': '正在连接交易终端...',
    'connected': '✅ 交易终端连接成功',
    'disconnected': '❌ 交易终端连接断开',
    'reconnecting': '🔄 正在重新连接...',
    'failed': '❌ 连接失败'
}

ERROR_KEYWORDS_MAPPING = {
    '资金不足': OrderError.INSUFFICIENT_FUNDS,
    '余额不足': OrderError.INSUFFICIENT_FUNDS,
    '可用资金不足': OrderError.INSUFFICIENT_FUNDS,
    '股票代码错误': OrderError.INVALID_STOCK,
    '证券代码不存在': OrderError.INVALID_STOCK,
    '非交易时间': OrderError.MARKET_CLOSED,
    '市场未开放': OrderError.MARKET_CLOSED,
    '价格超出涨跌停': OrderError.PRICE_LIMIT,
    '委托价格不合理': OrderError.PRICE_LIMIT,
    '委托数量错误': OrderError.VOLUME_LIMIT,
    '数量必须是100的整数倍': OrderError.VOLUME_LIMIT,
    '网络连接失败': OrderError.NETWORK,
    '连接超时': OrderError.NETWORK,
    '系统繁忙': OrderError.SYSTEM,
    '服务器错误': OrderError.SYSTEM,
    '账户状态异常': OrderError.ACCOUNT,
    '账户被冻结': OrderError.ACCOUNT,
}

ERROR_HANDLING_STRATEGY = {
    OrderError.INSUFFICIENT_FUNDS: ErrorStrategy.REJECT,
    OrderError.INVALID_STOCK: ErrorStrategy.REJECT,
    OrderError.MARKET_CLOSED: ErrorStrategy.REJECT,
    OrderError.PRICE_LIMIT: ErrorStrategy.ALLOW_BROKER_HANDLE,
    OrderError.VOLUME_LIMIT: ErrorStrategy.REJECT,
    OrderError.NETWORK: ErrorStrategy.RETRY,
    OrderError.SYSTEM: ErrorStrategy.RETRY,
    OrderError.ACCOUNT: ErrorStrategy.REJECT,
    OrderError.UNKNOWN: ErrorStrategy.RETRY,
}

ERROR_USER_MESSAGES = {
    OrderError.INSUFFICIENT_FUNDS: '资金不足，请检查账户余额',
    OrderError.INVALID_STOCK: '股票代码无效，请检查输入',
    OrderError.MARKET_CLOSED: '当前非交易时间',
    OrderError.PRICE_LIMIT: '价格超出限制，系统将自动调整',
    OrderError.VOLUME_LIMIT: '交易数量不符合要求',
    OrderError.NETWORK: '网络连接问题，正在重试',
    OrderError.SYSTEM: '系统繁忙，正在重试',
    OrderError.ACCOUNT: '账户状态异常，请联系客服',
    OrderError.UNKNOWN: '未知错误，正在重试',
}


# ==================== 工具函数 ====================
def get_error_type(error_message: str) -> OrderError:
    """根据错误消息获取错误类型"""
    for keyword, error_type in ERROR_KEYWORDS_MAPPING.items():
        if keyword in error_message:
            return error_type
    return OrderError.UNKNOWN


def is_retryable_error(error_type: OrderError) -> bool:
    """判断错误是否可重试"""
    return ERROR_HANDLING_STRATEGY.get(error_type) == ErrorStrategy.RETRY


def format_error_message(error_type: OrderError, original_message: str = '') -> str:
    """格式化错误消息"""
    user_message = ERROR_USER_MESSAGES.get(error_type, '未知错误')
    if original_message:
        return f"{user_message} (原始错误: {original_message})"
    return user_message


def get_error_suggestion(error_type: OrderError) -> str:
    """获取错误处理建议"""
    suggestions = {
        OrderError.INSUFFICIENT_FUNDS: '建议: 1) 检查账户余额 2) 减少交易数量 3) 充值资金',
        OrderError.INVALID_STOCK: '建议: 1) 检查股票代码格式 2) 确认股票是否存在 3) 检查市场类型',
        OrderError.MARKET_CLOSED: '建议: 1) 等待市场开盘 2) 检查交易时间 3) 确认节假日安排',
        OrderError.PRICE_LIMIT: '建议: 1) 调整委托价格 2) 使用市价单 3) 等待价格回调',
        OrderError.VOLUME_LIMIT: '建议: 1) 调整为100的整数倍 2) 检查最小交易单位 3) 确认持仓限制',
        OrderError.NETWORK: '建议: 1) 检查网络连接 2) 重启交易软件 3) 联系网络服务商',
        OrderError.SYSTEM: '建议: 1) 稍后重试 2) 联系券商客服 3) 检查系统公告',
        OrderError.ACCOUNT: '建议: 1) 联系券商客服 2) 检查账户状态 3) 确认资金账户',
        OrderError.UNKNOWN: '建议: 1) 记录错误信息 2) 联系技术支持 3) 稍后重试',
    }
    return suggestions.get(error_type, '建议联系技术支持')


def format_order_status(status: OrderStatus) -> str:
    """格式化订单状态显示"""
    status_map = {
        OrderStatus.SUBMITTED: '📝 已提交',
        OrderStatus.ACCEPTED: '✅ 已接受',
        OrderStatus.PARTIAL: '🔄 部分成交',
        OrderStatus.COMPLETED: '✅ 全部成交',
        OrderStatus.CANCELED: '❌ 已撤销',
        OrderStatus.REJECTED: '❌ 已拒绝',
        OrderStatus.EXPIRED: '⏰ 已过期',
    }
    return status_map.get(status, str(status.value))


def format_trade_action(direction: TradeDirection) -> str:
    """格式化交易动作显示"""
    action_map = {
        TradeDirection.BUY: '🟢 买入',
        TradeDirection.SELL: '🔴 卖出',
    }
    return action_map.get(direction, str(direction.value))


# ==================== 导出列表 ====================
__all__ = [
    # 常量
    'MAX_RETRY_ATTEMPTS', 'DEFAULT_RISK_PCT', 'MAX_POSITIONS',
    'DEFAULT_PRICE_PRECISION', 'DEFAULT_VOLUME_UNIT', 'DEFAULT_TRADE_SIZE',
    'RISK_FREE_RATE', 'TRADING_DAYS_PER_YEAR', 'LIMIT_UP_RATIO',
    
    # 枚举类
    'PriceType', 'OrderError', 'ErrorStrategy', 'OrderStatus',
    'TradeDirection', 'MarketType', 'LogLevel', 'OrderType', 'PositionDirection',
    
    # 错误处理常量
    'CONNECTION_MESSAGES', 'ERROR_KEYWORDS_MAPPING', 'ERROR_HANDLING_STRATEGY',
    'ERROR_USER_MESSAGES',
    
    # 工具函数
    'get_error_type', 'is_retryable_error', 'format_error_message',
    'get_error_suggestion', 'format_order_status', 'format_trade_action',
]