from setuptools import setup, find_namespace_packages

setup(
    name="monkai-agent-groq",
    version="0.1.0",
    packages=find_namespace_packages(include=['monkai_agent.*']),
    install_requires=[
        "monkai-agent>=0.1.0",
        "groq"
    ],
)