"""\nCreated by 满仓干 on - 2025/03/10.\n"""

"""\n免责声明: \n本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用\n运行本程序即同意上述免责声明 \n"""

class NotConnectError(Exception):
    def __init__(self):
        msg = "未连接到交易终端"
        self.message = msg
        super().__init__(msg)


# 在现有 NotConnectError 后添加更多自定义异常

class TradingError(Exception):
    """交易相关错误基类"""
    def __init__(self, code: str, message: str, context: dict = None):
        self.code = code
        self.context = context or {}
        super().__init__(message)

class InsufficientFundsError(TradingError):
    """资金不足错误"""
    def __init__(self, required_amount: float, available_amount: float):
        super().__init__(
            code="INSUFFICIENT_FUNDS",
            message=f"资金不足：需要 {required_amount}，可用 {available_amount}",
            context={'required': required_amount, 'available': available_amount}
        )

class StockSuspendedError(TradingError):
    """股票停牌错误"""
    def __init__(self, symbol: str):
        super().__init__(
            code="STOCK_SUSPENDED",
            message=f"股票 {symbol} 已停牌",
            context={'symbol': symbol}
        )

class NetworkError(Exception):
    """网络错误"""
    def __init__(self, message: str, retry_count: int = 0):
        self.retry_count = retry_count
        super().__init__(message)

class OrderError(TradingError):
    """订单错误"""
    def __init__(self, message: str, order_id: str = None):
        super().__init__(
            code="ORDER_ERROR",
            message=message,
            context={'order_id': order_id} if order_id else {}
        )