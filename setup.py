from setuptools import setup

setup(
    name='sparqRL',
    version='0.1.0',
    author='Jordan Palmer',
    author_email='jordan.palmer@datasparq.ai',
    packages=['sparqRL', 'sparqRL.test'],
    # scripts=['bin/script1','bin/script2'],
    # url='http://pypi.python.org/pypi/PackageName/',
    license='LICENSE.txt',
    description='Reinforcement Learning Component',
    long_description=open('README.txt').read(),
    install_requires=[
       "pytest",
        "sparse",
    ],
)