import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="blinker-py",
  version="0.0.1",
  author="Diandeng Tech",
  author_email="lvzhou@diandeng.tech",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)