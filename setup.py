import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

version = '0.2.0'

setuptools.setup(
    name="ups_turkey",
    version=version,
    author="Efraim GENC",
    author_email='info@kavimdigital.com',
    description="Easy integration for UPS Turkey",
    license="MIT",
    keywords=["ups_turkey", "ups-turkey", "ups", "turkey", "shipment"],
    packages=['ups_turkey'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/EfraimGENC/ups-turkey",
    download_url=f'https://github.com/EfraimGENC/ups-turkey/archive/refs/tags/v{version}.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "zeep>=4.1.0",
    ],
)