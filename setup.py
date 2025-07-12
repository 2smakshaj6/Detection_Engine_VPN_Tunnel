from setuptools import setup, find_packages

# Load README.md as the long description (recommended)
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="detection_engine",
    version="0.1.6",
    author="Akshaj S M",
    description="Detect VPN, Proxy, Tor, Botnets & abusive IPs using hybrid threat intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2smakshaj6/Detection_Engine_VPN_Tunnel/tree/pypi-module",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "scan=detection_engine.run_engine:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "requests",
        "tqdm",
        "python-dotenv"
    ],
)