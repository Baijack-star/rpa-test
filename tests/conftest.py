#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest配置文件

定义测试的全局配置、fixtures和标记。
"""

import pytest
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """pytest配置函数。"""
    # 注册自定义标记
    config.addinivalue_line(
        "markers", "integration: 标记集成测试（需要真实浏览器）"
    )
    config.addinivalue_line(
        "markers", "unit: 标记单元测试（不需要外部依赖）"
    )
    config.addinivalue_line(
        "markers", "slow: 标记慢速测试"
    )
    config.addinivalue_line(
        "markers", "network: 标记需要网络连接的测试"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集项。"""
    # 为没有标记的测试添加默认标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)


@pytest.fixture(scope="session")
def test_data_dir():
    """测试数据目录fixture。"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope="session")
def temp_dir():
    """临时目录fixture。"""
    import tempfile
    import shutil
    
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    
    # 清理临时目录
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_html():
    """示例HTML内容fixture。"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试页面</title>
    </head>
    <body>
        <h1 id="title">测试标题</h1>
        <form id="test-form">
            <input type="text" id="username" name="username" placeholder="用户名">
            <input type="password" id="password" name="password" placeholder="密码">
            <button type="submit" id="submit-btn">提交</button>
        </form>
        <div class="content">
            <p class="text">这是第一段文本</p>
            <p class="text">这是第二段文本</p>
        </div>
        <ul id="list">
            <li>项目1</li>
            <li>项目2</li>
            <li>项目3</li>
        </ul>
    </body>
    </html>
    """


@pytest.fixture
def mock_web_automation():
    """Mock的WebAutomation实例fixture。"""
    from unittest.mock import Mock
    
    mock_automation = Mock()
    mock_automation.driver = Mock()
    mock_automation.wait = Mock()
    mock_automation.actions = Mock()
    
    return mock_automation


@pytest.fixture(scope="function")
def cleanup_screenshots():
    """清理测试截图文件的fixture。"""
    screenshots = []
    
    def add_screenshot(filename):
        screenshots.append(filename)
        return filename
    
    yield add_screenshot
    
    # 清理所有截图文件
    for screenshot in screenshots:
        if os.path.exists(screenshot):
            os.remove(screenshot)


@pytest.fixture
def browser_options():
    """浏览器选项fixture。"""
    return {
        "headless": True,
        "window_size": (1920, 1080),
        "timeout": 10
    }


# 跳过条件
skip_if_no_display = pytest.mark.skipif(
    os.environ.get("DISPLAY") is None and os.name != "nt",
    reason="需要显示器或Windows环境"
)

skip_if_no_network = pytest.mark.skipif(
    os.environ.get("NO_NETWORK") == "1",
    reason="网络连接不可用"
)


# 参数化fixture
@pytest.fixture(params=["chrome", "edge"])
def browser_type(request):
    """浏览器类型参数化fixture。"""
    return request.param


@pytest.fixture(params=[True, False])
def headless_mode(request):
    """无头模式参数化fixture。"""
    return request.param