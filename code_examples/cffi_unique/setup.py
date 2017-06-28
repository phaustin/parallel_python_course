import os
import re
import sys
import platform
import subprocess


from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args=[]
        if platform.system() == "Windows":
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        cmake_args += ["-DCMAKE_INSTALL_PREFIX={}".format(env['PREFIX'])]
        print(f"calling cmake with {' '.join(cmake_args)}")
        env['CXX']='clang++'
        env['CC']='clang'
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
        # status,result=subprocess.getstatusoutput('echo "pha here PWD: $PWD"')
        # print(result)
        # status,result=subprocess.getstatusoutput('echo "pha here PREFIX: $PREFIX"')
        # print(result)
        # status,result=subprocess.getstatusoutput('echo "pha here CMAKE_INSTALL_PREFIX: $CMAKE_INSTALL_PREFIX"')
        # print(result)
        # status,result=subprocess.getstatusoutput('ls -R $PREFIX/*')
        # print(result)
        subprocess.check_call(['make', 'install'], cwd=self.build_temp)


setup(
    name='make_unique',
    packages=['make_unique'],
    version='0.1',
    author='Phil Austin',
    author_email='paustin@eos.ubc.ca',
    description='A test project using pybind11 and CMake',
    long_description='',
    ext_modules=[CMakeExtension('make_unique')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)
