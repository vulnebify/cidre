from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cidre-cli",
    version="1.0.4",
    packages=find_packages(),
    install_requires=["netaddr==1.3.0", "requests==2.32.3"],
    entry_points={
        "console_scripts": [
            "cidre=cidre.cli:main",
        ],
    },
    author="Alex @ Vulnebify",
    author_email="contact.pypi@vulnebify.com",
    description="A CLI tool for fetching and managing CIDR IP ranges from RIRs with firewall integration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vulnebify/cidre",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
