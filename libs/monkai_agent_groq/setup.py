from setuptools import find_namespace_packages, setup
import os



#requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requires = [ 'monkai-agent','groq']

setup(
    name='monkai-agent-groq',
    packages=find_namespace_packages(include=['monkai_agent.groq*']),
    version='0.0.32',
    description='Groq integration for Monkai Agent Library',
    author='Monkai Team',
    install_requires=requires
)
