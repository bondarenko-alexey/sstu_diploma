from distutils.core import setup
import py2exe
 
setup(
    windows=[{"script":"view.py"}],
    options={"py2exe": {"includes":["sip"]}}
)