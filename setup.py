from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    'rpy',
    'numpy',
    'matplotlib'
]

setup(name='PyPAM',
    version=version,
    description="Reads light curves and photosynthetic yield values, obtained from PyhtoPAM equipment. Plot values of light and photosynthesis parameters. alpha, Ik, ETR(max) and Beta",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 1 - Planning'# {'2': 'Pre-Alpha', '3': 'Alpha'}
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
    ],
    keywords='music oceanography data',
    author='Arnaldo Russo',
    author_email='arnaldorusso@gmail.com',
    url='https://github.com/arnaldorusso/PyPAM',
    download_url='https://github.com/arnaldorusso/PyPAM/archive/master.tar.gz',
    license='PSF',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    platforms='any',
)
