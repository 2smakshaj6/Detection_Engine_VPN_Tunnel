from setuptools import setup, find_packages

setup(
    name="detection_engine",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "tqdm"
    ],
    author="Akshaj S M",
    description="VPN/Proxy detection engine with heuristics and optional API lookups",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'scan=detection_engine.run_engine:main',
        ]
    },
    package_data={
        "detection_engine": ["config/*.json"]
    }
)