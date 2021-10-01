import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='cppguts',
    version='1.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/tierra-colada/cppguts',
    license='MIT',
    author='kerim khemrev',
    author_email='tierracolada@gmail.com',
    description='Tool aimed at C/C++ source code correction that allows to '
                'automatically find and copy/paste new function definition',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url='https://github.com/tierra-colada/cppguts/archive/refs/tags/v1.0.2.tar.gz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
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
        'wheel',
        'libclang',
    ],
    include_package_data=True   # important to copy MANIFEST.in files
)
