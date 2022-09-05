import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="ups_turkey",
    version="1.0.0",
    author="Efraim GENC",
    description="Easy integration for UPS Turkey",
    license="MIT",
    keywords=["ups_turkey", "ups-turkey", "ups", "turkey", "shipment"],
    packages=['ups_turkey'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/EfraimGENC/ups-turkey",
    download_url = 'https://github.com/EfraimGENC/ups-turkey/archive/refs/tags/v1.0.0.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "zeep>=4.1.0",
    ],
)