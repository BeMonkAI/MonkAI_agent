from setuptools import find_packages, setup
import os



def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

requirements_path = os.path.join(os.path.dirname(__file__), 'requeriments.txt')
install_requires=parse_requirements(requirements_path)       

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='monkai_agent',
    packages=find_packages(include=['monkai_agent', 'monkai_agent.*']),
    version='0.0.11',
    description='Monkai Agent Library for creating intelligent agents, flows quickly, easily, and customizable.',
    long_description=long_description,  # Add the content from README
    long_description_content_type="text/markdown",  # Specify Markdown or rst
    author='Monkai Team',
    install_requires=install_requires
)