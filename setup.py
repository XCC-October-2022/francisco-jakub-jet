from setuptools import setup, find_packages


dependencies = ["typer>=0.6", "structlog>=22.1.0", "python-dotenv>=0.21", "PyGithub>=1.55", "pygit2>=1.10"]
dev_dependencies = [
    "pytest>=7.1",
    "flake8>=5",
]

setup(
    name="jet",
    description="Github queuing system with other github functionalities",
    version="0.1",
    install_requires=dependencies,
    extras_require={
        "dev": dev_dependencies,
    },
    entry_points={
        "console_scripts": [
            "jet = jet.cli:main"
        ]
    },
    packages=find_packages("src"),
    package_dir={"": "src"},
)
