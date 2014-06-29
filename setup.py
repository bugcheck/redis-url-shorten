from setuptools import setup, find_packages

setup(name='url_short',
      version='0.1',
      description='High-performance URL shortener backed by Redis',
      url='https://github.com/neeraj2608/redis-url-shorten',
      author='Raj Rao',
      test_suite='tests',
      install_requires=[
          'flask',
          'redis'
      ],
      zip_safe=False)
