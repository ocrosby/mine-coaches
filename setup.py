from setuptools import setup, find_packages

setup(
    name="mine-coaches",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "bs4",
        "requests",
        "pydantic"
    ],
)