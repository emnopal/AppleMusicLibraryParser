from setuptools import setup

setup(
    name="AppleMusicLibraryParser",
    version="0.1.1",
    packages=["AppleMusicLibraryParser"],
    install_requires=[
        "PyYAML==6.0",
        "pandas==1.4.4"
    ],
    author="Muhammad Naufal",
    author_email="mnaufal0999@gmail.com",
    description="Convert XML to CSV",
    url="https://github.com/emnopal/AppleMusicLibraryParser",
)
