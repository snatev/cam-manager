from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    version = "0.2.2",
    name = "cam_manager",
    description = "A camera management library to easily handle cameras with OpenCV.",

    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",

    author = "snatev",
    author_email = "snatev@proton.me",
    url = "https://github.com/snatev/cam-manager",

    packages = find_packages(),
    install_requires = requirements,

    classifiers = [
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

    python_requires = ">=3.6",
)
