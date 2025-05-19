from setuptools import setup, find_packages

setup(
    name="model_app",
    version="0.1",
    packages=find_packages(include=['model*']),
    install_requires=[
        "flask==2.3.2",
        "fastapi==0.109.1",
        "numpy==1.26.4",
        "pytest==8.0.2",
        "httpx==0.27.0"
    ],
    python_requires=">=3.9",
)