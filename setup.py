import setuptools
from __version__ import __version__

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Image Recognition',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: C++',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
]

try:
    long_description = open('README.md', encoding='utf-8').read()
except:
    long_description = open('README.md').read()

packages = setuptools.find_packages()

install_requires = open('requirements.txt').read().strip().split('\n')
tests_require = open('tests-requirements.txt').read().strip().split('\n')

setuptools.setup(name='Yaml Merge',
                 version=__version__,
                 description='Merge Yaml Files',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 author='Till Pohland',
                 author_email='till.pohland',
                 license='MIT',
                 platforms=['Any'],
                 classifiers=classifiers,
                 url='url',
                 packages=packages,
                 install_requires=install_requires,
                 tests_require=tests_require,
                )
