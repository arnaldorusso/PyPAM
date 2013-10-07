from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='PyPAM',
    version=version,
    description="Read light curves and photosynthetic yield values, obtained from PyhtoPAM equipment. Plot values of light and photosynthesis parameters. alpha, Ik, ETR(max) and Beta.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='Pulse Amplitude Modulate, Photosynthesis, Fluorescence, Electron Transport Rate (ETR), Primary Production, Phytoplankton',
    author='Arnaldo Russo',
    author_email='arnaldorusso@gmail.com',
    url='http://ciclotux.blogspot.com',
    license='PSF',
    packages=find_packages('pypam'),
    package_dir = {'': 'pypam'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['PyPAM=pypam:main']
    }
)
