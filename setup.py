from distutils.core import setup

setup(
    name='Blinker',
    version='0.2.0',
    author='i3water',
    packages=['Blinker', 'BlinkerAdapters', 'BlinkerUtility'],
    # package_dir={'Blinker':'', 'BlinkerAdapters':'', 'BlinkerUtility':''},
    url='https://github.com/blinker-iot/blinker-py',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    description='Blinker library in python',
    long_description=open('README.md').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ]
)