from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Modding tools for Baldur\'s Gate 3'

# Setting up
setup(
    name="bg3modutils",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="<mail@neuralnine.com>",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    keywords=['python', 'bg3', 'baldurs gate', 'modding bg3', 'mod bg3', 'mod baldurs gate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
