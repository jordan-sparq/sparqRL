from setuptools import setup, find_packages
import os
from typing import List

def get_requirements(requirements_file: str) -> List[str]:
    """Read requirements from requirements.txt"""

    file_path = os.path.join(os.path.dirname(__file__), requirements_file)
    with open(file_path, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if not line.startswith("#") and line]
    lines = [line for line in lines if not line.startswith("-") and line]
    return lines


setup(
    name='sparqRL',
    version='0.1.0',
    author='Jordan Palmer',
    author_email='jordan.palmer@datasparq.ai',
    packages=find_packages(exclude=["test"]),
    # scripts=['bin/script1','bin/script2'],
    # url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='Reinforcement Learning Component',
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements("requirements.txt"),
)