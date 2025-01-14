from setuptools import setup, find_packages

setup(
    name="mqtt_mongo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'paho-mqtt',
    ],
)