from setuptools import setup, find_packages

setup(
    name='feed_reader',
    version='0.0.1-dev',
    description='A High level rss feed reader',
    install_requires=[
        'requests',
    ],
    author='Yash Pokar',
    author_email='hello@yashpokar.com',
    packages=find_packages(),
)
