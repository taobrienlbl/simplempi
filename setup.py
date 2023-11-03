from setuptools import setup, find_packages

setup(
    name="simplempi",
    version='0.1.4',
    description="A wrapper around mpi4py that offers simple scattering of iterable objects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Travis A. O'Brien",
    author_email="obrienta@iu.edu",
    url="https://github.com/taobrienlbl/simplempi",
    packages=find_packages(),
    install_requires=[
        "mpi4py",
    ],
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
