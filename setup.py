#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA自动化测试项目安装脚本
"""

from setuptools import setup, find_packages
import os
import sys

# 确保Python版本
if sys.version_info < (3, 8):
    raise RuntimeError("此项目需要Python 3.8或更高版本")

# 读取README文件
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# 读取requirements文件
def read_requirements(filename):
    """读取requirements文件并返回依赖列表。"""
    requirements = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if line and not line.startswith("#"):
                    # 处理内置模块（跳过）
                    if not any(builtin in line for builtin in [
                        "# 内置", "sqlite3", "smtplib", "email", "concurrent.futures",
                        "threading", "multiprocessing", "os", "sys", "subprocess",
                        "re", "json", "random", "math", "time", "datetime",
                        "pathlib", "os.path", "string", "collections", "itertools",
                        "functools", "typing", "warnings", "traceback", "copy",
                        "pickle", "zipfile", "tarfile", "socket", "urllib",
                        "queue", "unittest", "unittest.mock", "tempfile",
                        "globals", "locals", "builtins"
                    ]):
                        requirements.append(line)
    except FileNotFoundError:
        pass
    return requirements

# 基础依赖
install_requires = read_requirements("requirements_rpa.txt")

# 开发依赖
dev_requires = read_requirements("requirements-dev.txt")

# 测试依赖
test_requires = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-html>=4.0.0",
    "pytest-xdist>=3.3.0",
    "pytest-mock>=3.11.0",
    "pytest-timeout>=2.1.0",
]

# 文档依赖
docs_requires = [
    "sphinx>=7.1.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autodoc-typehints>=1.24.0",
]

setup(
    name="rpa-automation-test",
    version="1.0.0",
    description="基于Python和Selenium的RPA自动化测试框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RPA Team",
    author_email="rpa-team@example.com",
    url="https://github.com/Baijack-star/rpa-test",
    project_urls={
        "Bug Reports": "https://github.com/Baijack-star/rpa-test/issues",
        "Source": "https://github.com/Baijack-star/rpa-test",
        "Documentation": "https://github.com/Baijack-star/rpa-test/wiki",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="rpa automation testing selenium webdriver browser",
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "test": test_requires,
        "docs": docs_requires,
        "all": dev_requires + test_requires + docs_requires,
    },
    entry_points={
        "console_scripts": [
            "rpa-test=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": [
            "config/*.yaml",
            "config/*.yml",
            "config/*.json",
            "templates/*.html",
            "templates/*.xml",
        ],
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    test_suite="tests",
    tests_require=test_requires,
    cmdclass={},
    options={
        "build_scripts": {
            "executable": "/usr/bin/env python3",
        },
    },
)