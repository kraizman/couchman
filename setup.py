from setuptools import setup, find_packages
import os
    #packages = find_packages(),
    #include_package_data = True,
    #find_packages(exclude=("*.pyc", "*.log", "*.json.*",)),
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    install_requires = ['couchdb>=0.6'],
    name = "couchman",
    version = "0.3",
    author = "Pavel Krayzman",
    author_email = "pasha@smscoin.com",
    description = ("Utility for manipulating and monitoring couch db"),
    license = "GPL",
    keywords = "couch db replication views manager",
    url = "https://github.com/kraizman/CouchDB-Replications-Manager",
    include_package_data = True,
    package_data = {'media' : ['*.png'] },
    packages=['couchman', 'media', 'couchman.UI'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GPL License",
    ],
)
