from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gitool',
    version='0.1.0',
    author='DeepNeuralDog',
    author_email='md.hasibul.hasan.code@gmail.com',
    description='A command line tool to make using Git easier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DeepNeuralDog/gitool',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'gtool = gtool.cli:main',
            'acp = gtool.cli:handle_acp',
            'gnew = gtool.cli:handle_gnew'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)