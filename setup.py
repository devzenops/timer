from setuptools import setup, find_packages

setup(
    name='pomodoro',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pomodoro = src.menu:start_menu',
        ],
    },
)
