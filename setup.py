from setuptools import find_packages, setup

setup(
    name="tasklite",
    version="0.1.0",
    description="A tiny, dependency-free task manager for the command line.",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "tasklite=src.cli:main",
        ],
    },
)
