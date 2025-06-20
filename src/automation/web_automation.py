#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web自动化核心模块

提供基于Selenium的Web自动化功能，包括浏览器控制、元素操作、数据提取等。
"""

import time
import logging
from typing import Optional, List, Dict, Any, Union
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class WebAutomation:
    """Web自动化核心类。
    
    提供完整的Web自动化功能，包括浏览器管理、页面操作、元素交互等。
    
    Attributes:
        driver: WebDriver实例
        wait: WebDriverWait实例
        actions: ActionChains实例
        logger: 日志记录器
    """
    
    def __init__(self, browser_type: str = "chrome", headless: bool = False, 
                 timeout: int = 10, window_size: tuple = None):
        """初始化Web自动化实例。
        
        Args:
            browser_type: 浏览器类型，支持 'chrome' 和 'edge'
            headless: 是否以无头模式运行
            timeout: 默认等待超时时间（秒）
            window_size: 浏览器窗口大小，格式为 (width, height)
        """
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.timeout = timeout
        self.window_size = window_size
        
        self.driver: Optional[webdriver.Chrome | webdriver.Edge] = None
        self.wait: Optional[WebDriverWait] = None
        self.actions: Optional[ActionChains] = None
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def open_browser(self) -> None:
        """打开浏览器。
        
        Raises:
            ValueError: 不支持的浏览器类型
            WebDriverException: 浏览器启动失败
        """
        try:
            if self.browser_type == "chrome":
                self._setup_chrome()
            elif self.browser_type == "edge":
                self._setup_edge()
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser_type}")
            
            # 设置窗口大小
            if self.window_size:
                self.driver.set_window_size(*self.window_size)
            else:
                self.driver.maximize_window()
            
            # 初始化等待和动作链
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.actions = ActionChains(self.driver)
            
            self.logger.info(f"成功启动{self.browser_type}浏览器")
            
        except Exception as e:
            self.logger.error(f"启动浏览器失败: {e}")
            raise
    
    def _setup_chrome(self) -> None:
        """配置Chrome浏览器。"""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # 添加常用选项
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        
        # 自动下载并配置ChromeDriver
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def _setup_edge(self) -> None:
        """配置Edge浏览器。"""
        options = webdriver.EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # 添加常用选项
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        # 自动下载并配置EdgeDriver
        service = EdgeService(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=options)
    
    def navigate_to(self, url: str) -> None:
        """导航到指定URL。
        
        Args:
            url: 目标URL
            
        Raises:
            WebDriverException: 导航失败
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        try:
            self.driver.get(url)
            self.logger.info(f"成功导航到: {url}")
        except Exception as e:
            self.logger.error(f"导航失败: {e}")
            raise
    
    def find_element(self, selector: str, by: By = By.CSS_SELECTOR, 
                    timeout: Optional[int] = None) -> webdriver.remote.webelement.WebElement:
        """查找页面元素。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Returns:
            找到的WebElement对象
            
        Raises:
            TimeoutException: 元素在指定时间内未找到
        """
        if not self.wait:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(EC.presence_of_element_located((by, selector)))
            self.logger.debug(f"找到元素: {selector}")
            return element
        except TimeoutException:
            self.logger.error(f"元素未找到: {selector}")
            raise
    
    def find_elements(self, selector: str, by: By = By.CSS_SELECTOR) -> List[webdriver.remote.webelement.WebElement]:
        """查找多个页面元素。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            
        Returns:
            WebElement对象列表
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        elements = self.driver.find_elements(by, selector)
        self.logger.debug(f"找到{len(elements)}个元素: {selector}")
        return elements
    
    def click_element(self, selector: str, by: By = By.CSS_SELECTOR, 
                     timeout: Optional[int] = None) -> None:
        """点击页面元素。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Raises:
            TimeoutException: 元素在指定时间内未找到
            ElementNotInteractableException: 元素不可交互
        """
        element = self.find_element(selector, by, timeout)
        
        # 等待元素可点击
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.element_to_be_clickable((by, selector)))
        
        try:
            element.click()
            self.logger.info(f"成功点击元素: {selector}")
        except ElementNotInteractableException:
            # 如果普通点击失败，尝试使用JavaScript点击
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"使用JavaScript点击元素: {selector}")
    
    def input_text(self, selector: str, text: str, by: By = By.CSS_SELECTOR, 
                  clear_first: bool = True, timeout: Optional[int] = None) -> None:
        """在输入框中输入文本。
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
            by: 定位方式，默认为CSS_SELECTOR
            clear_first: 是否先清空输入框
            timeout: 等待超时时间，默认使用实例设置
        """
        element = self.find_element(selector, by, timeout)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        self.logger.info(f"在元素 {selector} 中输入文本: {text}")
    
    def get_text(self, selector: str, by: By = By.CSS_SELECTOR, 
                timeout: Optional[int] = None) -> str:
        """获取元素文本内容。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Returns:
            元素的文本内容
        """
        element = self.find_element(selector, by, timeout)
        text = element.text
        self.logger.debug(f"获取元素 {selector} 的文本: {text}")
        return text
    
    def get_attribute(self, selector: str, attribute: str, 
                     by: By = By.CSS_SELECTOR, timeout: Optional[int] = None) -> str:
        """获取元素属性值。
        
        Args:
            selector: 元素选择器
            attribute: 属性名
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Returns:
            属性值
        """
        element = self.find_element(selector, by, timeout)
        value = element.get_attribute(attribute)
        self.logger.debug(f"获取元素 {selector} 的属性 {attribute}: {value}")
        return value
    
    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR, 
                        timeout: Optional[int] = None) -> webdriver.remote.webelement.WebElement:
        """等待元素出现。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Returns:
            找到的WebElement对象
        """
        return self.find_element(selector, by, timeout)
    
    def wait_for_element_clickable(self, selector: str, by: By = By.CSS_SELECTOR, 
                                  timeout: Optional[int] = None) -> webdriver.remote.webelement.WebElement:
        """等待元素可点击。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
            
        Returns:
            可点击的WebElement对象
        """
        if not self.wait:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        
        element = wait.until(EC.element_to_be_clickable((by, selector)))
        self.logger.debug(f"元素可点击: {selector}")
        return element
    
    def scroll_to_element(self, selector: str, by: By = By.CSS_SELECTOR, 
                         timeout: Optional[int] = None) -> None:
        """滚动到指定元素。
        
        Args:
            selector: 元素选择器
            by: 定位方式，默认为CSS_SELECTOR
            timeout: 等待超时时间，默认使用实例设置
        """
        element = self.find_element(selector, by, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"滚动到元素: {selector}")
    
    def take_screenshot(self, filename: str = None) -> str:
        """截取当前页面截图。
        
        Args:
            filename: 截图文件名，如果不提供则自动生成
            
        Returns:
            截图文件路径
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        filepath = self.driver.save_screenshot(filename)
        self.logger.info(f"截图已保存: {filename}")
        return filename
    
    def execute_script(self, script: str, *args) -> Any:
        """执行JavaScript代码。
        
        Args:
            script: JavaScript代码
            *args: 传递给脚本的参数
            
        Returns:
            脚本执行结果
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        result = self.driver.execute_script(script, *args)
        self.logger.debug(f"执行JavaScript: {script[:50]}...")
        return result
    
    def switch_to_frame(self, frame_reference: Union[str, int, webdriver.remote.webelement.WebElement]) -> None:
        """切换到指定框架。
        
        Args:
            frame_reference: 框架引用（名称、索引或WebElement）
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.switch_to.frame(frame_reference)
        self.logger.info(f"切换到框架: {frame_reference}")
    
    def switch_to_default_content(self) -> None:
        """切换回主文档。"""
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.switch_to.default_content()
        self.logger.info("切换回主文档")
    
    def switch_to_window(self, window_handle: str) -> None:
        """切换到指定窗口。
        
        Args:
            window_handle: 窗口句柄
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.switch_to.window(window_handle)
        self.logger.info(f"切换到窗口: {window_handle}")
    
    def get_current_url(self) -> str:
        """获取当前页面URL。
        
        Returns:
            当前页面URL
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """获取当前页面标题。
        
        Returns:
            页面标题
        """
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        return self.driver.title
    
    def refresh_page(self) -> None:
        """刷新当前页面。"""
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.refresh()
        self.logger.info("页面已刷新")
    
    def go_back(self) -> None:
        """返回上一页。"""
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.back()
        self.logger.info("返回上一页")
    
    def go_forward(self) -> None:
        """前进到下一页。"""
        if not self.driver:
            raise RuntimeError("浏览器未启动，请先调用 open_browser()")
        
        self.driver.forward()
        self.logger.info("前进到下一页")
    
    def close_browser(self) -> None:
        """关闭浏览器。"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None
            self.actions = None
            self.logger.info("浏览器已关闭")
    
    def __enter__(self):
        """上下文管理器入口。"""
        self.open_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口。"""
        self.close_browser()
    
    def __del__(self):
        """析构函数，确保浏览器被关闭。"""
        self.close_browser()