from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in booking/__init__.py
from booking import __version__ as version

setup(
	name="booking",
	version=version,
	description="Booking Management",
	author="kinisi",
	author_email="vasanth@kinisi.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
