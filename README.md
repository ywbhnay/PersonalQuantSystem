# PersonalQuantSystem

高性能量化交易系统 - 融合miniQMT实盘交易和BackTrader回测框架

## 🚀 项目特性

- **高性能处理**: 支持每秒10,000条数据处理
- **双引擎支持**: 融合miniQMT实盘交易和BackTrader回测框架
- **模块化架构**: 易于扩展和维护的设计
- **完善错误处理**: 统一的异常管理和日志系统
- **安全保护**: 完整的敏感数据保护机制

## 📁 项目结构

```
PersonalQuantSystem/
├── libs/                 # 核心库文件
│   ├── config/          # 配置管理
│   ├── core/            # 核心功能
│   ├── errors/          # 错误处理
│   ├── output/          # 输出管理
│   ├── trader/          # 交易模块
│   └── utils/           # 工具函数
├── docs/                # 文档和指南
├── examples/            # 示例代码
├── tests/               # 单元测试
└── main.py              # 主程序入口
```

## 🛠️ 技术栈

- **Python 3.8+**: 主要开发语言
- **miniQMT**: 实盘交易接口
- **BackTrader**: 回测框架
- **simple_chalk**: 命令行颜色输出
- **terminaltables3**: 表格格式化
- **pytest**: 单元测试框架

## 🚀 快速开始

1. **克隆项目**
```bash
git clone https://github.com/ywbhnay/PersonalQuantSystem.git
cd PersonalQuantSystem
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置系统**
```bash
cp config.yaml.template config.yaml
# 编辑 config.yaml 配置文件
```

4. **运行系统**
```bash
python main.py
```

## 📖 文档

- [错误处理指南](docs/error_handling_guide.md)
- [API文档](docs/api_reference.md)
- [开发规范](docs/development_guide.md)

## 🔒 安全说明

本项目已配置完善的`.gitignore`规则，自动屏蔽：
- 日志文件和敏感配置
- 交易账户信息和API密钥
- 个人数据和临时文件

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

⭐ 如果这个项目对您有帮助，请给个星标支持！