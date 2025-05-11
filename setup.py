from setuptools import setup, find_packages

setup(
    name="piv_2025",
    version="0.0.1",
    author="Natalia Rojas",
    author_email="",
    description="",
    py_modules=["PIV_Oro"],
    install_requires=[
        "pandas==2.2.3",
        "openpyxl",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3"
    ]
)   