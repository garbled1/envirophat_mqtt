from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="envirophat_mqtt",
    version="1.0",
    description="Feed data from a pimoroni envirophat into mqtt",
    license='Apache 2.0',
    packages=['envirophat_mqtt'],
    author='Tim Rightnour',
    author_email='the@garbled.one',
    url='https://github.com/garbled1/envirophat_mqtt',
    project_urls={
        'Gitub Repo': 'https://github.com/garbled1/envirophat_mqtt',
    },
    install_requires=[
        'envirophat',
        'paho-mqtt'
    ],
    python_requires='>3.5',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'envirophat_mqtt=envirophat_mqtt.__main__:main'
        ]
    }
)
