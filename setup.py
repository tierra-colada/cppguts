import setuptools

setuptools.setup(
    name='cppguts',
    version='0.1.0',
    packages=setuptools.find_packages(),
    url='https://github.com/tierra-colada/cppguts',
    license='MIT',
    author='kerim khemrev',
    author_email='tierracolada@gmail.com',
    description='python package aimed at C++ source code correction',
    download_url='https://github.com/tierra-colada/cppguts/archive/refs/tags/v0.1.0.tar.gz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='c cpp c-parser cpp-parser c-editor cpp-editor c-generator cpp-generator',
    entry_points={
        'console_scripts': ['editcpp=cppguts.editcpp:main',
                            'dumpcpp=cppguts.dumpcpp:main']
    },
    python_requires='>=3',
    install_requires=[
        'libclang',
    ],
    include_package_data=True   # important to copy MANIFEST.in files
)
