from setuptools import find_namespace_packages, setup
import os

requires =  ['monkai-agent', 'azure-identity']

setup(
    name='monkai-agent-azure',
    packages=find_namespace_packages(include=['monkai_agent.azure*']),
    version='0.0.32',
    description='Azure integration for Monkai Agent Library',
    author='Monkai Team',
    install_requires=requires
)
