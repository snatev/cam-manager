from setuptools import setup, find_packages

setup(
    version = "0.1.0",
    name = "cam_manager",
    description = "A camera management library to easily handle cameras with OpenCV.",

    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",

    author = "snatev",
    author_email = "snatev@proton.me",
    url = "https://github.com/snatev/cam-manager",

    packages = find_packages(),
    install_requires = [
        "opencv-python"
    ],

    classifiers = [
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

    python_requires = ">=3.6",
)
