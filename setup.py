# 🌸 FLORA - Setup Script
# Script de instalación y configuración del proyecto FLORA

from setuptools import setup, find_packages
import os

# Leer README para descripción larga
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README_FLORA.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Sistema de cifrado híbrido post-cuántico con autodestrucción caótica"

# Leer requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="flora-crypto",
    version="0.1.0-alpha",
    author="Crypto Flower Team",
    author_email="team@cryptoflower.dev",
    description="Sistema de cifrado híbrido post-cuántico con autodestrucción caótica",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/cryptoflower/flora",
    project_urls={
        "Bug Tracker": "https://github.com/cryptoflower/flora/issues",
        "Documentation": "https://flora.readthedocs.io/",
        "Source Code": "https://github.com/cryptoflower/flora",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
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
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="cryptography, encryption, post-quantum, chaos, security, hybrid",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "pytest-cov>=2.12.0",
            "black>=21.7b0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.15.0",
        ],
        "benchmarks": [
            "pytest-benchmark>=3.4.1",
            "memory-profiler>=0.60.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "flora=flora.cli:main",
            "flora-test=flora.test_flora:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)
