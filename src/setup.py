import setuptools

setuptools.setup(
    name="aws",
    version="1.0.0",
    author="steven hurwitt",
    author_email="stevenhurwitt@gmail.com",
    description="main function",
    long_description="aws data analytics toolkit python repo.",
    long_description_content_type = "text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)

