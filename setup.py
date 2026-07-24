from setuptools import setup, find_packages

setup(
    name="enlang",
    version="1.0.0",
    description="Universal Natural English Programming Language Transpiler & Engine",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Spandan",
    url="https://github.com/spandan/enlang",
    packages=find_packages(),
    py_modules=["enlang"],
    entry_points={
        "console_scripts": [
            "enlang=enlang:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],
)
