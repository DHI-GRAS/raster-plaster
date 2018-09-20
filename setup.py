from setuptools import setup, find_packages
import os


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as fp:
    install_requires = fp.read()


setup(
    name='raster-plaster',
    description='merge rasters in clever ways',
    author='Philip Graae',
    author_email='phgr@dhigroup.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        raster-plaster=raster_plaster.scripts.cli:cli
    '''
)