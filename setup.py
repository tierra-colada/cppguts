from setuptools import setup

setup(
    name='cppguts',
    version='0.1.0',
    packages=['cppguts'],
    url='https://github.com/tierra-colada/cppguts',
    license='MIT',
    author='kerim khemrev',
    author_email='tierracolada@gmail.com',
    description='python package aimed at c++ source code correction',
    entry_points={
        'console_scripts': ['correctcpp=cppguts.correctcpp:main',
                            'dumpcpp=cppguts.dumpcpp:main']
    },
    install_requires=[
        'libclang',
    ],
)
