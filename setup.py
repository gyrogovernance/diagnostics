from setuptools import setup, find_packages

setup(
    name="gyrodiagnostics",
    version="0.1.0",
    description="Mathematical Physics-Informed AI Alignment Evaluation Suite",
    author="Korompilias, Basil",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "inspect-ai>=0.3.135",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)