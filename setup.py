from setuptools import find_packages, setup

setup(
    name="ot2_controller",
    version="0.3.0",
    author="Florian Bauer",
    author_email="<florian.bauer.dev@gmail.com>",
    packages=find_packages(),
    install_requires=[
        "paramiko >=2.7.2, <2.9.0",
        "scp <=0.13.2, <0.15.0",
        "sila2 ==0.10.4",
    ],
    include_package_data=True,
)
