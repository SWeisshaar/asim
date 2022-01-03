from setuptools import setup

setup(
    name='geneticalgo',
    version='0.0.1dev1',
    description="Semester Project - ASIM - Stock Trading",
    author="Student",
    author_email="student@uni-koeln.de",
    packages=["geneticalgo"],
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': ['yellowcab=yellowcab.cli:main']
    }
)