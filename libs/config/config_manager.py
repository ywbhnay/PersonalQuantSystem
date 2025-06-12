"""\n统一配置管理器 - 管理应用程序的所有配置参数\n"""
from typing import Dict, Any, Optional  # 导入类型提示工具，用于函数参数和返回值的类型声明
from dataclasses import dataclass, field  # 导入数据类装饰器，简化类的定义
from pathlib import Path  # 导入路径处理模块，用于文件路径操作
import json  # 导入JSON处理模块，用于JSON格式配置文件的读写
import yaml  # 导入YAML处理模块，用于YAML格式配置文件的读写
from libs.output.output_manager import output_manager  # 导入输出管理器

# 这些默认值应该保留在数据类中，但可以从配置文件覆盖
@dataclass
class RiskConfig:
    max_single_position: float = 0.1 #  单只股票最大持仓比例
    max_total_positions: float = 0.8 #  总持仓比例
    stop_loss: float = 0.05 #  止损比例
    max_positions_count: int = 5 #  最大持仓数量
    max_daily_loss: float = 0.02 #  最大单日亏损比例
    max_drawdown: float = 0.1 #  最大回撤比例
    position_risk_pct: float = 0.02 #   单笔交易风险比例

@dataclass
class BacktestConfig:
    """回测配置 - 定义回测模式下的参数设置"""
    initial_cash: float = 1000000  # 初始资金，默认100万
    commission: float = 0.0003  # 交易佣金比例，默认万分之三
    data_source: str = 'qmt_historical'  # 数据源，默认使用QMT历史数据
    debug_mode: bool = False  # 调试模式开关，默认关闭
    error_output_interval: int = 30  # 错误输出间隔(秒)，默认30秒
    risk_management: RiskConfig = field(default_factory=RiskConfig)  # 风险管理配置，使用默认工厂函数创建

@dataclass
class LiveConfig:
    """实盘配置 - 定义实盘交易模式下的参数设置"""
    mini_qmt_path: str = r'D:\国金证券QMT交易端\userdata_mini'  # QMT交易端路径
    account_id: str = '8886281695'  # 交易账户ID
    account_type: str = 'STOCK'  # 账户类型，默认股票账户
    data_source: str = 'qmt_realtime'  # 数据源，默认使用QMT实时数据
    debug_mode: bool = False  # 调试模式开关，默认关闭
    error_output_interval: int = 30  # 错误输出间隔(秒)，默认30秒
    risk_management: RiskConfig = field(default_factory=RiskConfig)  # 风险管理配置

@dataclass
class AppConfig:
    """应用配置 - 整合所有配置，定义应用运行模式和配置"""
    mode: str = 'backtest'  # 运行模式，'backtest'为回测模式，'live'为实盘模式
    backtest: BacktestConfig = field(default_factory=BacktestConfig)  # 回测配置
    live: LiveConfig = field(default_factory=LiveConfig)  # 实盘配置
    
class ConfigManager:
    """配置管理器 - 负责加载、管理和更新应用配置"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器
        
        Args:
            config_path: 配置文件路径，如果为None则自动查找
        """
        self._config = AppConfig()  # 创建默认应用配置
        
        # 如果没有指定配置文件，自动查找默认配置文件
        if not config_path:
            default_paths = ['config.yaml', 'config.yml', 'config.json']  # 默认配置文件列表
            for path in default_paths:
                if Path(path).exists():  # 检查文件是否存在
                    config_path = path  # 如果存在则使用该路径
                    break
        
        if config_path:
            self.load_from_file(config_path)  # 从指定路径加载配置
            output_manager.success(f"✅ 已找到配置文件: {config_path}",logger_type='info')  # 打印成功消息
        else:
            output_manager.error(f"⚠️  未找到配置文件，使用默认配置")  # 打印警告消息
    
    def load_from_file(self, config_path: str):
        """从文件加载配置
        
        Args:
            config_path: 配置文件路径
        """
        path = Path(config_path)  # 创建Path对象
        if not path.exists():  # 检查文件是否存在
            raise FileNotFoundError(f"Config file not found: {config_path}")  # 抛出文件不存在异常
        
        output_manager.info(f"📖 正在加载配置文件: {config_path}")  # 打印加载消息
        
        try:
            if path.suffix.lower() == '.json':  # 如果是JSON文件
                with open(path, 'r', encoding='utf-8') as f:  # 以UTF-8编码打开文件
                    data = json.load(f)  # 加载JSON数据
            elif path.suffix.lower() in ['.yml', '.yaml']:  # 如果是YAML文件
                # 尝试多种编码方式，提高兼容性
                encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'cp1252']  # 支持的编码列表
                data = None  # 初始化数据变量
                
                for encoding in encodings:  # 尝试每种编码
                    try:
                        with open(path, 'r', encoding=encoding) as f:  # 以当前编码打开文件
                            data = yaml.safe_load(f)  # 安全加载YAML数据
                        output_manager.success(f"✅ 使用 {encoding} 编码成功加载配置文件")  # 打印成功消息
                        break  # 成功加载后跳出循环
                    except UnicodeDecodeError:
                        continue  # 编码错误则尝试下一种编码
                    except Exception as e:
                        output_manager.error(f"❌ 使用 {encoding} 编码加载失败: {e}")
                        continue
                
                if data is None:
                    raise ValueError(f"无法使用任何编码方式读取配置文件: {config_path}")
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
            
            self._update_config_from_dict(data)
            output_manager.success(f"✅ 配置文件加载成功")
            
        except Exception as e:
            output_manager.error(f"❌ 配置文件加载失败: {e}")
            raise
    
    def _update_config_from_dict(self, data: Dict[str, Any]):
        """从字典更新配置"""
        # 更新运行模式
        if 'mode' in data:
            self._config.mode = data['mode']
        
        # 更新回测配置
        if 'backtest' in data:
            backtest_data = data['backtest']
            for key, value in backtest_data.items():
                if hasattr(self._config.backtest, key):
                    setattr(self._config.backtest, key, value)
        
        # 更新实盘配置
        if 'live' in data:
            live_data = data['live']
            for key, value in live_data.items():
                if hasattr(self._config.live, key):
                    setattr(self._config.live, key, value)
    
    @property
    def config(self) -> AppConfig:
        """获取当前配置"""
        return self._config
    
    @property
    def mode(self) -> str:
        """获取运行模式"""
        return self._config.mode
    
    @property
    def is_backtest(self) -> bool:
        """是否为回测模式"""
        return self._config.mode == 'backtest'
    
    @property
    def is_live(self) -> bool:
        """是否为实盘模式"""
        return self._config.mode == 'live'
    
    @property
    def current_config(self):
        """获取当前模式的配置"""
        if self.is_backtest:
            return self._config.backtest
        else:
            return self._config.live
    
    def get_risk_config(self) -> RiskConfig:
        """获取风险管理配置"""
        return self.current_config.risk_management
    
    def update_config(self, **kwargs):
        """动态更新配置"""
        current = self.current_config
        for key, value in kwargs.items():
            if hasattr(current, key):
                setattr(current, key, value)
                output_manager.info(f"📝 配置已更新: {key} = {value}")
            else:
                output_manager.warning(f"⚠️  未知配置项: {key}")
    
    def save_to_file(self, config_path: str):
        """保存配置到文件"""
        path = Path(config_path)
        
        # 将配置转换为字典
        config_dict = {
            'mode': self._config.mode,
            'backtest': {
                'initial_cash': self._config.backtest.initial_cash,
                'commission': self._config.backtest.commission,
                'data_source': self._config.backtest.data_source,
                'debug_mode': self._config.backtest.debug_mode,
                'error_output_interval': self._config.backtest.error_output_interval,
            },
            'live': {
                'mini_qmt_path': self._config.live.mini_qmt_path,
                'account_id': self._config.live.account_id,
                'account_type': self._config.live.account_type,
                'data_source': self._config.live.data_source,
                'debug_mode': self._config.live.debug_mode,
                'error_output_interval': self._config.live.error_output_interval,
            }
        }
        
        try:
            if path.suffix.lower() == '.json':
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
            elif path.suffix.lower() in ['.yml', '.yaml']:
                with open(path, 'w', encoding='utf-8') as f:
                    yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
            
            output_manager.success(f"✅ 配置已保存到: {config_path}")
            
        except Exception as e:
            output_manager.error(f"❌ 配置保存失败: {e}")
            raise
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"ConfigManager(mode={self.mode}, config={self.current_config})"