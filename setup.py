import setuptools

setuptools.setup(
    name="openmm-g96-reporter",
    version="0.0.1",
    description="G96 format reporter for OpenMM",
    author="mizu-bai",
    author_email="shiragawa4519@outlook.com",
    url="https://github.com/mizu-bai/openmm-g96-reporter",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.8",
    install_requirements=[
        "numpy>1.20.0",
    ],
)
