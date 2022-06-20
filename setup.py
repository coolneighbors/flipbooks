from setuptools import setup

setup(
    name='flipbooks',
    url='https://github.com/austinh2001/flipbooks.git',
    author='Aaron Meisner',
    author_email='aaron.meisner@noirlab.edu',
    # Needed to actually package something
    packages=['flipbooks'],
    # Needed for dependencies
    install_requires=['requests','PILLOW','imageio'],
    # *strongly* suggested for sharing
    version='0.5',
    # The license can be anything you like
    license='MIT',
    description='A pipeline for downloading and modifying Cool Neighbors flipbook images.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)