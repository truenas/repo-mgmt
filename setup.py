from setuptools import find_packages, setup


install_requires = [
    'pyyaml',
]


setup(
    name='mirror_mgmt',
    description='A framework for managing TrueNAS SCALE mirrors',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    platforms='any',
    install_requires=[
        'coloredlogs',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'mirror_mgmt = mirror_mgmt.main:main',
        ],
    },
)
