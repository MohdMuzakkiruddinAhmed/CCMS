from setuptools import setup, find_packages

setup(
    name="ccms",
    version="1.0.0",
    description="Case Count Metric System for ER cluster comparison",
    author="Talburt et al.",
    author_email="mccakmak@ualr.edu",
    url="https://github.com/YOUR-ORG/ccms",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "web": ["flask>=2.3.0", "pandas>=1.5.0"],
        "test": ["pytest>=7.0"],
    },
    entry_points={
        "console_scripts": [
            "ccms=ccms.core:main",
        ],
    },
)
