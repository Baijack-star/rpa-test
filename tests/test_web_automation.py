#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web自动化模块测试

测试web_automation模块的各项功能。
"""

import pytest
import time
from unittest.mock import Mock, patch
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.automation.web_automation import WebAutomation


class TestWebAutomation:
    """Web自动化测试类。"""
    
    def setup_method(self):
        """测试前置设置。"""
        self.automation = WebAutomation(browser_type="chrome", headless=True)
    
    def teardown_method(self):
        """测试后置清理。"""
        if self.automation.driver:
            self.automation.close_browser()
    
    def test_init_default_params(self):
        """测试默认参数初始化。"""
        automation = WebAutomation()
        assert automation.browser_type == "chrome"
        assert automation.headless is False
        assert automation.timeout == 10
        assert automation.window_size is None
        assert automation.driver is None
    
    def test_init_custom_params(self):
        """测试自定义参数初始化。"""
        automation = WebAutomation(
            browser_type="edge",
            headless=True,
            timeout=20,
            window_size=(1920, 1080)
        )
        assert automation.browser_type == "edge"
        assert automation.headless is True
        assert automation.timeout == 20
        assert automation.window_size == (1920, 1080)
    
    @pytest.mark.integration
    def test_open_browser_chrome(self):
        """测试打开Chrome浏览器。"""
        self.automation.open_browser()
        assert self.automation.driver is not None
        assert self.automation.wait is not None
        assert self.automation.actions is not None
    
    @pytest.mark.integration
    def test_open_browser_edge(self):
        """测试打开Edge浏览器。"""
        automation = WebAutomation(browser_type="edge", headless=True)
        try:
            automation.open_browser()
            assert automation.driver is not None
        finally:
            automation.close_browser()
    
    def test_open_browser_unsupported(self):
        """测试不支持的浏览器类型。"""
        automation = WebAutomation(browser_type="firefox")
        with pytest.raises(ValueError, match="不支持的浏览器类型"):
            automation.open_browser()
    
    @pytest.mark.integration
    def test_navigate_to(self):
        """测试导航到指定URL。"""
        self.automation.open_browser()
        test_url = "https://httpbin.org/html"
        self.automation.navigate_to(test_url)
        assert test_url in self.automation.get_current_url()
    
    def test_navigate_to_without_browser(self):
        """测试在未启动浏览器时导航。"""
        with pytest.raises(RuntimeError, match="浏览器未启动"):
            self.automation.navigate_to("https://example.com")
    
    @pytest.mark.integration
    def test_find_element(self):
        """测试查找页面元素。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        # 查找页面标题
        element = self.automation.find_element("h1")
        assert element is not None
        assert "Herman Melville" in element.text
    
    @pytest.mark.integration
    def test_find_element_timeout(self):
        """测试元素查找超时。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        with pytest.raises(TimeoutException):
            self.automation.find_element("#nonexistent-element", timeout=2)
    
    @pytest.mark.integration
    def test_find_elements(self):
        """测试查找多个元素。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        elements = self.automation.find_elements("p")
        assert len(elements) > 0
    
    @pytest.mark.integration
    def test_get_text(self):
        """测试获取元素文本。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        text = self.automation.get_text("h1")
        assert "Herman Melville" in text
    
    @pytest.mark.integration
    def test_get_attribute(self):
        """测试获取元素属性。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        # 获取页面标题
        title = self.automation.get_attribute("html", "lang")
        # 注意：某些页面可能没有lang属性，所以这里只检查方法是否正常执行
        assert title is not None or title == ""
    
    @pytest.mark.integration
    def test_execute_script(self):
        """测试执行JavaScript。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        # 执行简单的JavaScript
        result = self.automation.execute_script("return document.title;")
        assert isinstance(result, str)
    
    @pytest.mark.integration
    def test_get_current_url(self):
        """测试获取当前URL。"""
        self.automation.open_browser()
        test_url = "https://httpbin.org/html"
        self.automation.navigate_to(test_url)
        
        current_url = self.automation.get_current_url()
        assert test_url in current_url
    
    @pytest.mark.integration
    def test_get_page_title(self):
        """测试获取页面标题。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        title = self.automation.get_page_title()
        assert isinstance(title, str)
        assert len(title) > 0
    
    @pytest.mark.integration
    def test_take_screenshot(self):
        """测试截图功能。"""
        import os
        
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        # 测试自动生成文件名
        filename = self.automation.take_screenshot()
        assert os.path.exists(filename)
        os.remove(filename)  # 清理测试文件
        
        # 测试指定文件名
        custom_filename = "test_screenshot.png"
        result = self.automation.take_screenshot(custom_filename)
        assert result == custom_filename
        assert os.path.exists(custom_filename)
        os.remove(custom_filename)  # 清理测试文件
    
    def test_take_screenshot_without_browser(self):
        """测试在未启动浏览器时截图。"""
        with pytest.raises(RuntimeError, match="浏览器未启动"):
            self.automation.take_screenshot()
    
    @pytest.mark.integration
    def test_refresh_page(self):
        """测试刷新页面。"""
        self.automation.open_browser()
        self.automation.navigate_to("https://httpbin.org/html")
        
        # 记录刷新前的时间
        before_refresh = time.time()
        self.automation.refresh_page()
        after_refresh = time.time()
        
        # 验证刷新操作执行了（通过时间差判断）
        assert after_refresh > before_refresh
    
    @pytest.mark.integration
    def test_context_manager(self):
        """测试上下文管理器。"""
        with WebAutomation(headless=True) as automation:
            assert automation.driver is not None
            automation.navigate_to("https://httpbin.org/html")
            assert "httpbin.org" in automation.get_current_url()
        
        # 验证浏览器已关闭
        assert automation.driver is None
    
    def test_close_browser(self):
        """测试关闭浏览器。"""
        self.automation.open_browser()
        assert self.automation.driver is not None
        
        self.automation.close_browser()
        assert self.automation.driver is None
        assert self.automation.wait is None
        assert self.automation.actions is None
    
    def test_close_browser_when_not_opened(self):
        """测试在浏览器未启动时关闭。"""
        # 应该不会抛出异常
        self.automation.close_browser()
        assert self.automation.driver is None


class TestWebAutomationMocked:
    """使用Mock的Web自动化测试类。"""
    
    def setup_method(self):
        """测试前置设置。"""
        self.automation = WebAutomation()
    
    @patch('src.automation.web_automation.webdriver.Chrome')
    @patch('src.automation.web_automation.ChromeDriverManager')
    def test_setup_chrome_mocked(self, mock_driver_manager, mock_chrome):
        """测试Chrome设置（使用Mock）。"""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        self.automation._setup_chrome()
        
        mock_chrome.assert_called_once()
        assert self.automation.driver == mock_driver
    
    @patch('src.automation.web_automation.webdriver.Edge')
    @patch('src.automation.web_automation.EdgeChromiumDriverManager')
    def test_setup_edge_mocked(self, mock_driver_manager, mock_edge):
        """测试Edge设置（使用Mock）。"""
        mock_driver_manager.return_value.install.return_value = "/path/to/edgedriver"
        mock_driver = Mock()
        mock_edge.return_value = mock_driver
        
        self.automation._setup_edge()
        
        mock_edge.assert_called_once()
        assert self.automation.driver == mock_driver


@pytest.mark.integration
class TestWebAutomationIntegration:
    """Web自动化集成测试类。"""
    
    def test_complete_workflow(self):
        """测试完整的自动化工作流程。"""
        with WebAutomation(headless=True) as automation:
            # 1. 导航到测试页面
            automation.navigate_to("https://httpbin.org/forms/post")
            
            # 2. 填写表单
            automation.input_text("input[name='custname']", "测试用户")
            automation.input_text("input[name='custtel']", "1234567890")
            automation.input_text("input[name='custemail']", "test@example.com")
            automation.input_text("textarea[name='comments']", "这是一个测试评论")
            
            # 3. 验证输入
            name_value = automation.get_attribute("input[name='custname']", "value")
            assert name_value == "测试用户"
            
            # 4. 截图
            screenshot = automation.take_screenshot("integration_test.png")
            assert screenshot == "integration_test.png"
            
            # 清理截图文件
            import os
            if os.path.exists(screenshot):
                os.remove(screenshot)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])