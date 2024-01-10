import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CTDbscan",
    version="1.0.0",
    author="Junlang Li",
    author_email="lijunlang1123@163.com",
    description="Spatial clustering of continuous trajectories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    'pandas>=1.5.2',
],
)