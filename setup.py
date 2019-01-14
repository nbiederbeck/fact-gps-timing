from setuptools import setup, find_packages

setup(
    name="GPSTiming",
    description="Interpolate FACT boardtime stamps with GPS triggers",
    version="0.2",
    author="Noah Biederbeck",
    author_email="noah.biederbeck@tu-dortmund.de",
    packages=find_packages(),
    install_requires=["astropy", "scipy", "numpy"],
)
