#!/bin/bash --login



export LD_LIBRARY_PATH=$ANACONDA_LIB:$LD_LIBRARY_PATH:/work/y07/y07/cse/vtk/5.10.1/GNU/lib/vtk-5.10


if test -f Makefile
then
    echo "CLEANING"
    make clean
    make distclean

    mv -f Makefile Makefile.bak

fi

debuggingConfig=""
precisionFlag=""
debugCompile=""
fcheckCompile=""

for arg in $@
do
    case $arg in
        "debug" )
            echo "CONFIGURING FOR DEBUG"
            # --enable-debugging doesn't work with extruded meshes. Sheesh.
            debuggingConfig="" 
            debugCompile="-ggdb -fbacktrace -fstack-usage -fstack-check"
            ;;
        "check" )
            echo "Adding memory checks"
            fcheckCompile="-fcheck=bounds -fcheck=all -fstack-usage -fstack-check"
            ;;
        cto=* )
            echo "Will try to use compile-time optimisations"
            flml_file="`echo $arg | sed 's/^cto=//g'`"
            if [ "$flml_file" != "" ] 
            then
                ctoConfig="--enable-cto=$flml_file"
            fi
            ;;

        "single" )
            echo "Compiling in single-precision (32-bit) mode"
            precisionFlag="--enable-dp=no"
            petscDoubleOnlyLibs=""
            ;;

    esac
done


xflags="-O2 -march=native -funroll-loops -ffast-math -DHAVE_LIBNUMA"


# xflags="-g -ggdb"
# confflags="--enable-debugging"

./configure "$confflags" \
--enable-2d-adaptivity --enable-openmp \
--enable-shared \
$ctoConfig $precisionFlag \
CFLAGS="$CFLAGS $CPPFLAGS $xflags" \
CXXFLAGS="$CXXFLAGS $CPPFLAGS $xflags" \
FFLAGS="$FFLAGS $CPPFLAGS $xflags" \
FCFLAGS="$FCFLAGS $CPPFLAGS $xflags" \
CPPFLAGS="$CPPFLAGS" \
LIBS="-L$CONTRIB_DIR/lib -lparmetis -lmetis"

make -j 4
make -j 4 fltools

