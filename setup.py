from setuptools import setup, find_packages

setup(
    name="DBFMapper",
    version="0.1.2",
    author="Brandon Jared Molina Vazquez",
    author_email="jaredbrandon970@gmail.com",
    description="Mapper of .dbf tables to python objects, (read only)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brandbold-Ch/DBFMapper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
