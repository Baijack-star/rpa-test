# 贡献指南

🎉 感谢您对RPA自动化测试项目的关注！我们欢迎所有形式的贡献，包括但不限于代码、文档、测试、问题报告和功能建议。

## 📋 目录

- [开发环境搭建](#开发环境搭建)
- [Git工作流程](#git工作流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request流程](#pull-request流程)
- [测试指南](#测试指南)
- [文档贡献](#文档贡献)
- [问题报告](#问题报告)
- [社区准则](#社区准则)
- [联系方式](#联系方式)

## 🛠️ 开发环境搭建

### 前置要求

- Python 3.8 或更高版本
- Git
- Chrome 或 Edge 浏览器
- 推荐使用 VS Code 或 PyCharm

### 环境配置

1. **Fork 并克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rpa-test.git
   cd rpa-test
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements_rpa.txt
   pip install -r requirements-dev.txt  # 开发依赖
   ```

4. **配置Git**
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

## 🌿 Git工作流程

我们采用 **Git Flow** 工作流程：

### 分支说明

- `master`: 生产环境分支，包含稳定的发布版本
- `develop`: 开发主分支，包含最新的开发进度
- `feature/*`: 功能开发分支
- `bugfix/*`: Bug修复分支
- `hotfix/*`: 紧急修复分支
- `release/*`: 发布准备分支

### 开发流程

1. **从develop分支创建功能分支**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **进行开发工作**
   ```bash
   # 进行代码修改
   git add .
   git commit -m "feat: add new feature"
   ```

3. **推送分支并创建Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # 在GitHub上创建Pull Request
   ```

### 分支命名规范

- `feature/功能描述`: 新功能开发
- `bugfix/问题描述`: Bug修复
- `hotfix/紧急修复描述`: 紧急修复
- `docs/文档更新描述`: 文档更新
- `test/测试相关描述`: 测试相关

## 📝 代码规范

### Python代码规范

我们遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格指南：

```python
# 好的示例
class WebAutomation:
    """Web自动化核心类。"""
    
    def __init__(self, browser_type: str = "chrome"):
        """初始化Web自动化实例。
        
        Args:
            browser_type: 浏览器类型，默认为chrome
        """
        self.browser_type = browser_type
        self.driver = None
    
    def open_browser(self) -> None:
        """打开浏览器。"""
        if self.browser_type == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser_type == "edge":
            self.driver = webdriver.Edge()
        else:
            raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
```

### 命名规范

- **类名**: 使用 PascalCase (如 `WebAutomation`)
- **函数名**: 使用 snake_case (如 `open_browser`)
- **变量名**: 使用 snake_case (如 `browser_type`)
- **常量名**: 使用 UPPER_SNAKE_CASE (如 `DEFAULT_TIMEOUT`)
- **私有成员**: 以单下划线开头 (如 `_private_method`)

### 代码质量工具

我们使用以下工具确保代码质量：

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy src/

# 导入排序
isort .
```

## 📋 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交消息格式

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式化（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修复bug的代码变动）
- `test`: 增加测试
- `chore`: 构建过程或辅助工具的变动
- `perf`: 性能优化
- `ci`: CI配置文件和脚本的变动

### 提交示例

```bash
# 新功能
git commit -m "feat: 添加Chrome浏览器自动化支持"

# Bug修复
git commit -m "fix: 修复元素定位超时问题"

# 文档更新
git commit -m "docs: 更新API文档"

# 重构
git commit -m "refactor: 重构浏览器驱动管理模块"
```

## 🔄 Pull Request流程

### 创建Pull Request

1. **确保代码质量**
   ```bash
   # 运行测试
   pytest
   
   # 代码检查
   flake8 .
   black --check .
   ```

2. **填写PR模板**
   - 使用提供的PR模板
   - 详细描述变更内容
   - 关联相关Issue
   - 添加测试说明

3. **请求代码审查**
   - 指定合适的审查者
   - 响应审查意见
   - 及时更新代码

### 代码审查标准

- ✅ 代码功能正确
- ✅ 遵循代码规范
- ✅ 包含适当的测试
- ✅ 文档完整
- ✅ 性能合理
- ✅ 安全性考虑

## 🧪 测试指南

### 测试类型

1. **单元测试**: 测试单个函数或方法
2. **集成测试**: 测试模块间的交互
3. **端到端测试**: 测试完整的用户场景

### 测试编写

```python
import pytest
from src.automation import WebAutomation

class TestWebAutomation:
    """Web自动化测试类。"""
    
    def setup_method(self):
        """测试前置设置。"""
        self.automation = WebAutomation()
    
    def teardown_method(self):
        """测试后置清理。"""
        if self.automation.driver:
            self.automation.close_browser()
    
    def test_open_browser_chrome(self):
        """测试打开Chrome浏览器。"""
        self.automation.open_browser()
        assert self.automation.driver is not None
        assert "chrome" in self.automation.driver.name.lower()
    
    def test_navigate_to_url(self):
        """测试导航到指定URL。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://example.com")
        assert "example.com" in self.automation.driver.current_url
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_automation.py

# 运行特定测试方法
pytest tests/test_automation.py::TestWebAutomation::test_open_browser_chrome

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

## 📚 文档贡献

### 文档类型

- **API文档**: 代码中的docstring
- **用户指南**: 使用说明和教程
- **开发文档**: 架构设计和开发指南
- **README**: 项目概述和快速开始

### 文档规范

```python
def click_element(self, selector: str, timeout: int = 10) -> None:
    """点击页面元素。
    
    Args:
        selector: CSS选择器或XPath
        timeout: 等待超时时间（秒），默认10秒
    
    Raises:
        TimeoutException: 元素在指定时间内未找到
        ElementNotInteractableException: 元素不可交互
    
    Example:
        >>> automation = WebAutomation()
        >>> automation.open_browser()
        >>> automation.navigate_to("https://example.com")
        >>> automation.click_element("#submit-button")
    """
    pass
```

## 🐛 问题报告

### 报告Bug

使用 [Bug报告模板](../../issues/new?template=bug_report.md) 创建Issue，包含：

- 🐛 **Bug描述**: 简洁明了的问题描述
- 🔄 **复现步骤**: 详细的重现步骤
- ✅ **预期行为**: 期望的正确行为
- 🖥️ **环境信息**: 操作系统、Python版本等
- 📸 **截图**: 如果适用
- 🔍 **错误日志**: 相关的错误信息

### 功能请求

使用 [功能请求模板](../../issues/new?template=feature_request.md) 创建Issue，包含：

- 🚀 **功能描述**: 清晰的功能说明
- 💡 **动机和背景**: 为什么需要这个功能
- 📋 **详细设计**: 具体的实现想法
- 🎯 **用户故事**: 用户使用场景
- 📝 **验收标准**: 功能完成的标准

## 🤝 社区准则

请阅读我们的 [行为准则](CODE_OF_CONDUCT.md) 了解社区标准。

### 核心原则

- 🤝 **尊重**: 尊重所有贡献者
- 🌟 **包容**: 欢迎不同背景的参与者
- 📚 **学习**: 保持开放的学习心态
- 🔄 **协作**: 积极参与讨论和协作
- 🎯 **专注**: 专注于项目目标

## 📞 联系方式

- 💬 **讨论**: [GitHub Discussions](../../discussions)
- 🐛 **问题**: [GitHub Issues](../../issues)
- 📧 **邮件**: [项目邮箱]
- 💬 **即时通讯**: [Discord/Slack链接]

## 🙏 致谢

感谢所有为项目做出贡献的开发者！您的贡献让这个项目变得更好。

---

**再次感谢您的贡献！** 🎉

如果您有任何问题或建议，请随时通过上述方式联系我们。