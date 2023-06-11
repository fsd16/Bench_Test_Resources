
from setuptools import setup

setup()

# """
# Project packaging and deployment
# More details: https://setuptools.pypa.io/en/latest/userguide/quickstart.html
# """
# import os
# from setuptools import setup, find_packages

# def __read__(file_name):
#     return open(os.path.join(os.path.dirname(__file__), file_name)).read()

# setup(
#     name='onegui',
#     version='3.0',
#     author='Finn Drabsch',
#     author_email='fdrabsch@enphaseenergy.com',
#     url="https://github.com/fsd16/One-Gui-To-Rule-Them-All",
#     options={'bdist_wheel': {'universal': False}},
#     packages=find_packages(where='src'),
#     package_dir={'': 'src'},
#     include_package_data=True,  # Include non-code resource files as mentioned in MANIFEST.in
#     description='A GUI program for controlling typical hardware bench equipment',
#     python_requires='>=3.7',
#     entry_points={},

#     install_requires=["enphase_ecdc>=5.30.58",
#                       "enphase_testlib>=1.0.51",
#                       "pyvisa>1.6",
#                       "PySide6==6.4.3;python_version<'3.8'",
#                       "PySide6;python_version>='3.8'"
#                       "pyqtgraph",
#                       "numpy'",
#     ],
#     extras_require={}
# )