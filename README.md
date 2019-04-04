# Installation Instructions for CoastED on ARCHER

## Software Requirements
- CoastED (github link [here](https://github.com/CoastED/coasted))
- ParMetis 3.2.0 (download [here](http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/OLD/ParMetis-3.2.0.tar.gz))
- PETSc 3.6.4 (download [here](http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.6.4.tar.gz))
- The scripts `coasted-gcc`, `build-petsc.sh` and `coasted-build-gcc.sh` included in this repository.

### Useful Third Party Software
- gmsh (download [here](http://gmsh.info//src/older/gmsh-2.10.1-source.tgz))

## 1. Setting up the Environment
Choose a directory to act as the root directory for your install. In this directory create a `modules/` directory to contain your module file, `coasted-gcc`. Also create `contrib/` and `contrib/gcc/` directories to contain the compiled third party libraries.

Download the dependencies into the rCOASTEDoot directory

Copy the `coasted-gcc` file into the `modules` directory and edit it so that the lines defining `COASTED_HOME`, `workDir` and `contribDir` point to the directories `coasted/`, `contrib/` and `contrib/gcc/` respectively.

The directory tree should be:
```
[CoastED Root Directory]
   ├──  coasted/
   │  └──  [...Contents of Coasted Github repo...]
   ├──  contrib/
   │  └──  gcc/
   ├──  modules/
   │  └──  coasted-gcc
   ├──  ParMetis-3.2.0.tar.gz
   └──  petsc-3.6.4.tar.gz
```

Every time you use CoastED remember to use the `coasted-gcc` module:
```
$ module use /path/to/coasted/module/directory
$ module swap PrgEnv-cray coasted-gcc
```
You may wish to add the `module use` command into your `.bashrc` so that it is loaded at login.


## 2. Build Parmetis
Load the `coasted-gcc` module and (if you haven't already done so) extract Parmetis and `cd` into its directory.

Modify the `Makefile.in` so that `CC` and `LD` point to `cc` rather than `mpicc`. Then run `make`

Finally, copy `libparmetis.a` and `libmetis.a` to `contrib/gcc/lib` and copy `parmetis.h` to `contrib/gcc/include`.

## 3. Build PETSc
Load `coasted-gcc`, extract PETSc into the root directory and `cd` into this. Copy `build-petsc.sh` into this directory and run it to compile PETSc (can take a while so get a cuppa :tea: :coffee:). This should install PETSc to `contrib/gcc/petsc/`.


## 4. Build Coasted
In the `coasted` directory, edit `fldecomp/metis/Makefile` to change `CC=mpicc` to `CC=cc`.

Copy `coasted-build-gcc.sh` into the `coasted` directory.

CoastED uses compile time optimisations. To that end we need to point a fluidity input file at the build script to successfully build CoastED. As an example we can use the one in `channel-template` in this repository.

```
./coasted-build-gcc.sh cto=/path/to/channel.flml
```
This should successfully build CoastED after an hour or so.

*If the configuration step fails with `Error. Currently, only optimisation for 2D is supported` running `dos2unix` on the input file may help as Windows end of line characters confuse the build process.*

## 5. Building Third Party Software
### Building gmsh

*It is advised to not use the `coasted-gcc` module for this, but instead use `PrgEnv-gnu` to prevent cmake from trying to link against PETSc libraries*

Extract the tarball, `cd` into the newly extracted directory, and create a `build/` directory. Move to this directory and run
```
$ cmake -DBLAS_LAPACK_LIBRARIES=/opt/cray/libsci/16.11.1/GNU/5.1/x86_64/lib/libsci_gnu.a -DCMAKE_INSTALL_PREFIX=/work/z01/z01/gpsgibb/coasted/contrib/gcc
$ make -j6
$ make install
```
(remembering to change the install prefix to your `contrib/gcc/` directory) to build gmsh.
