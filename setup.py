from setuptools import find_packages, setup

setup(
    name="ot2-controller",
    packages=find_packages(),
    install_requires=[
        "opentrons==3.20.1",
        "opentrons-shared-data==3.20.1",
        "paramiko==2.7.2",
        "scp==0.13.2",
        "sila2==0.5.5",
    ],
    include_package_data=True,
)
