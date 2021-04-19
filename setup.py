import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="intervul",
    version="0.0.2",
    author="Matias Pacheco",
    author_email="Matias.Pacheco.A@gmail.com",
    description="Interfaces for inhouse FEM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpacheco62/intervul",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3',
    install_requires=["scipy"],
    scripts=['scripts/geoToVtk', 
             'scripts/getForcesVul',
             'scripts/intervtk',
             'scripts/makeInitial',
             'scripts/repairContact'
             ]
)
