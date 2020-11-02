from distutils.core import setup

setup(name='sbgn2an',
      version='0.1',
      description='Library for computing initial states and stories of a Process Description map',
      author="Adrien Rougny, Loïc Paulevé",
      author_email="adrienrougny@gmail.com, loic.pauleve@lri.fr",
      packages=['sbgn2an'],
      package_data = {"sbgn2an": ["*.asp"]},
     )
