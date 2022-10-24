import setuptools


# Load description
with open('README.md', 'r') as fr:
    long_description = fr.read()

# Load version string
loaded_vars = dict()
with open('cvvis2d/version.py') as fv:
    exec(fv.read(), loaded_vars)
    version = loaded_vars['__version__']


setuptools.setup(
    name="cvvis2d",
    version=version,
    author="snototter",
    author_email="snototter@users.noreply.github.com",
    description="Visualization pipeline based on viren2d.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snototter/viren2d-visualizers",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'viren2d @ git+https://github.com/snototter/viren2d.git'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
