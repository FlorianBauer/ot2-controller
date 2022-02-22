from setuptools import find_packages, setup

setup(
    name="ot2-controller",
    version="0.2.0",
    author="Florian Bauer",
    author_email="<florian.bauer.dev@gmail.com>",
    packages=find_packages(),
    install_requires=[
        "paramiko==2.7.2",
        "scp==0.13.2",
        "sila2==0.5.5",
    ],
    include_package_data=True,
)
