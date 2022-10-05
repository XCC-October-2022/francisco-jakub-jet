from setuptools import setup, find_packages


dependencies = ["typer>=0.6", "structlog>=22.1.0", "python-dotenv>=0.21", "PyGithub>=1.55"]
dev_dependencies = [
    "pytest>=7.1",
    "flake8>=5",
]

setup(
    name="jet",
    description="Github queuing system",
    version="0.1",
    install_requires=dependencies,
    extras_require={
        "dev": dev_dependencies,
    },
    entry_points={
        "console_scripts": [
            "converter = roman.cli:main"
        ]
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
)
