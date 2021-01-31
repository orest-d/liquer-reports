import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liquer-reports",
    version="0.0.1",
    author="Orest Dubay",
    author_email="orest3.dubay@gmail.com",
    description="LiQuer-enabler library for creating reports and interactive dashboards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orest-d/liquer-reports",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['liquer-framework'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
