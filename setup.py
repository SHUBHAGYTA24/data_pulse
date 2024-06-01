from setuptools import setup, find_packages

setup(
    name='data_drift',
    version='0.1.0',  
    description='A Python package for detecting drift in data sets.',
    long_description='This package provides a DriftDetector class that calculates statistical drift metrics between two pandas DataFrames. It supports various numerical metrics and categorical mode, and can handle data grouped by a specified granularity level.',
    url='https://github.com/your-username/drift-detector',  # Replace with your project URL (optional)
    author='Shubhagyta Swaraj Jayswal',
    author_email='shubhagytaswaraj@gmail.com',
    packages=find_packages(exclude=[]),  # Automatically find all packages
    install_requires=[ 
        'pandas>=1.0.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Data Analysis :: Data Mining',
    ],
)
