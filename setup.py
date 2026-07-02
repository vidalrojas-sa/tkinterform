import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="tkinterform",
    version="0.1.0",
    python_requires=">=3.2",
    description="A package for building forms with Tkinter",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vidalrojas-sa/tkinterform.git",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords="tkinter, Tkinter, Tk, form, forms",
    packages=find_packages(),
)
