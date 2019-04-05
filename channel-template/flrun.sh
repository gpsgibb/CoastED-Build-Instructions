#!/bin/bash
#    Copyright (C) 2009 Dr Angus Creech (angus_creech@hotmail.com)
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation,
#    version 2.1 of the License.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this software; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
#    USA
#
# ----------------------------------------------------------------------------
# cfdrun.sh:
#
# Requries the follwing software installed:
# - GMSH
# - GMT tools package
#
# For meshing, you need to supply the following files:
# - contour file in ascii XYZ format
# - a GMSH .geo file defining the problem volume
#
# Examples of both are provided and used in this script.
#
# --------- user defined variables -------------------------------------------


module use /work/z01/z01/gpsgibb/coasted/modules
module swap PrgEnv-cray coasted-gcc

contourfile=contour.xyz
prefix=channel

grdinterv=100

if [ "$1" == "clean" ]
then
    ncpus=1
    dxmax=10
else
    if [ "$2" == "" ]
    then
	echo "usage: flrun.sh <ncores> <dxmax> | clean"
	exit 1
    else
	ncpus="$1"
	dxmax="$2"
    fi
fi


# How far does the simulation domain extend into the atmosphere?
height=500

# Dimensions can be set here.
# Extent will be calculated from contour file if maxx and maxy left blank
maxx=1000
maxy=500
maxz=$height

echo "dxmax=""$dxmax"";" > dxmaxgrid.geo


# --------- end of user defined variables ------------------------------------

roughnessfile=$prefix-roughness.xyz
heightgrd=height.grd
roughgrd=roughness.grd
geofile=$prefix.geo
topogeofile=topography.geo
turbgeofile=turbines.geo
meshfile=$prefix.msh
xyzgrdfile=height-grid.xyz
roughnesspgm=roughness.pgm


echo "------------------------------------------------------------------------------"
echo "  FLRUN"
echo ""
echo "  Simulation: $prefix"
echo "  Started on `date`"
echo "  $ncpus processors"
echo "------------------------------------------------------------------------------"

# kill old fluidity processes

echo "*** Deleting old simulation results"

rm -f nohup.out *.{pvtu,vtu} *.{log,err}* *.{node,edge,face,ele,halo} *.pyc *~
rm -rf "$prefix"_[0-9]
rm -rf "$prefix"_[0-9][0-9]
rm -rf "$prefix"_[0-9][0-9][0-9]
rm -rf "$prefix"_[0-9][0-9][0-9][0-9]
rm -rf convergence_test_*
rm -f turbines-output.csv matrixdump matrixdump.info turbines.state
rm -f $prefix.msh "$prefix"_[0-9].msh "$prefix"_[0-9][0-9].msh 
rm -f "$prefix"_[0-9][0-9][0-9].msh 
rm -f "$prefix"-topo.msh
rm -f "$prefix".stat
rm -f $prefix_[0-9][0-9].msh $prefix_[0-9][0-9][0-9].msh
rm -f core 
rm -f topography.geo turbines.geo wind.geo
rm -f height.grd height-grid.xyz
rm -rf *PressureMesh* *VelocityMesh* *CoordinateMesh*
rm -f lillgrund_*.flml
rm -f stderr stdout


if [ "$1" == "clean" ]
then
    exit 0
fi



echo "*** Running GMSH"

aprun -n 1 gmsh -3 -bin -3 $prefix.geo | grep Info | grep elements | awk '{print $5, $6}'
# ./reorder_gmsh $prefix.msh $prefix-ordered.msh
# mv -f $prefix-ordered.msh $prefix.msh

echo "*** Partitioning mesh ..."

if [ "$ncpus" != "1" ] 
then
    aprun -n 1 /work/z01/z01/gpsgibb/coasted/coasted/bin/fldecomp -m gmsh -n $ncpus -f $prefix >/dev/null
fi


echo "  *** Finished on `date`"
