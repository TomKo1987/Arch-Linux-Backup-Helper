from setuptools import setup, find_packages

setup(
    name="backup-helper",
    version="1.0.0",
    description="GUI Backup Tool for Arch Linux",
    author="TomKo1987",
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "keyring",
        "psutil"
    ],
    entry_points={
        'console_scripts': [
            'backup-helper = backup_helper:main'
        ]
    },
)
