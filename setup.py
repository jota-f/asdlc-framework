#!/usr/bin/env python3
"""
Setup script for A-SDLC Framework
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="asdlc-framework",
    version="1.0.0",
    author="A-SDLC Framework Team",
    author_email="contact@asdlc-framework.com",
    description="Framework revolucionário para desenvolvimento de software com agentes de IA especializados",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/asdlc-framework",
    project_urls={
        "Bug Tracker": "https://github.com/seu-usuario/asdlc-framework/issues",
        "Documentation": "https://github.com/seu-usuario/asdlc-framework#readme",
        "Source Code": "https://github.com/seu-usuario/asdlc-framework",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "asdlc=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "asdlc": [
            "prompts/*.md",
            "templates/*.md",
            "examples/*/*",
        ],
    },
    keywords=[
        "ai",
        "software-development",
        "framework",
        "agents",
        "llm",
        "openai",
        "code-generation",
        "project-management",
        "development-lifecycle",
        "automation",
    ],
    license="MIT",
    platforms=["any"],
    zip_safe=False,
) 