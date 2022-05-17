import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setuptools.setup(
    name='tooltime',
    version='0.1.4',
    description='tooltime makes it easier to perform operations on time data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sslivkoff/tooltime',
    packages=setuptools.find_packages(),
    install_requires=[
        'typing_extensions',
    ],
    extras_require={
        'full': [
            'numpy',
            'pandas',
        ],
    },
    python_requires='>=3.6',
    package_data={
        'tooltime': ['py.typed'],
    },
)
