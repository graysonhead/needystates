import setuptools

setuptools.setup(
    name='needystates',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Grayson Head',
    author_email='grayson@graysonhead.net',
    packages=setuptools.find_packages(),
    license='GPL V3',
    long_description=open('README.md').read()
)