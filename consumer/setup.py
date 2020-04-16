from setuptools import setup

packages = ["consumer"]

setup(
    name="consumer",
    version="0.0.1",
    description="simple consumer",
    url="http://github.com/iwpnd/kafka-spark-stream",
    author="Benjamin Ramser",
    author_email="ahoi@iwpnd.pw",
    license="MIT",
    include_package_data=True,
    install_requires=[],
    packages=packages,
    zip_safe=False,
    classifiers=["Programming Language :: Python :: 3"],
)
