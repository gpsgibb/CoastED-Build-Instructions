#!/bin/bash -login

module swap PrgEnv-cray coasted-gcc

unset ZOLTAN_POST_LINK_OPTS ZOLTAN_DIR ZOLTAN_INCLUDE_OPTS ZOLTAN_DEPS ZOLTAN_PRE_LINK_OPTS


if [ "$PETSC_DIR" == "" ]
then
   echo "PETSC_DIR must be defined first as your install directory."
   exit 1
fi

if test -d "$PETSC_DIR"
then
   echo "PETSC_DIR directory '$PETSC_DIR' already exists."
   echo "Please either delete or change PETSC_DIR directory."
   exit 1
fi

export TARGET_PETSC_DIR="$PETSC_DIR"

export TARG_PETSC_DIR="$PETSC_DIR"
export PETSC_DIR=`pwd`
export PETSC_ARCH=sandybridge


EXTRA_LIBS="-L$PETSC_DIR/$PETSC_ARCH/lib"

./configure --prefix="$TARGET_PETSC_DIR" --with-shared-libraries=0 \
--with-batch=0 \
--with-pic=1 --with-debugging=0 \
--with-fortran-interfaces=1 \
--with-hypre=1 --download-hypre=1 \
--with-prometheus=1 --download-prometheus=1 \
--with-pic=1 --with-mpi-shared=1  --with-debugging=0 \
--with-single-library=1 \
--with-cc=cc --with-cxx=CC --with-fc=ftn \
--CFLAGS="-O2 $CFLAGS -I$MPICH_DIR/include -I$HOME/include" \
--CXXFLAGS="-O2 $CXXFLAGS -I$MPICH_DIR/include -I$HOME/include" \
--FCFLAGS="-O2 $FCFLAGS -I$MPICH_DIR/include -I$HOME/include " \
--LIBS="-O2 $EXTRA_LIBS -L$MPICH_DIR/lib -L$HOME/local/lib" \
F90FLAGS=$F90FLAGS F77=$F77 F90=$F90 FFLAGS=$FFLAGS CPPFLAGS=$CPPFLAGS \
--with-ptscotch=1 --download-ptscotch=1 \
--with-metis --with-metis-dir=$METIS_DIR \
--with-parmetis=1 --download-parmetis=1 \


make PETSC_DIR=`pwd`  MAKE_NP=8 all
make PETSC_DIR="$TARGET_PETSC_DIR" PETSC_ARCH=sandybridge install
