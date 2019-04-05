#!/usr/bin/env python
#
#    Copyright (C) 2009 Dr Angus Creech (acwc2@hw.ac.uk)
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



# Locks nodes according to what's in the GMSH msh file


def init( boundaryID, meshname ):
    global boundnodes, vertSmall, horizSmall

    # Really, the error metric for judging elements
    vertSmall = 20.0
    horizSmall = 300.0


    # How many nodes in mesh?

    meshfile = open( meshname, "r" )

    linestr = meshfile.readline()

    while linestr.find("$Nodes") < 0:
        linestr = meshfile.readline()

    numnodes = int(meshfile.readline())


    # read in nodes from mesh

    allnodes = {}

    for i in range(0, numnodes, 1):

        words = meshfile.readline().split()

        id = int(words[0])
        x = float(words[1])
        y = float(words[2])
        z  = float(words[3])

        allnodes[ id ] = (x, y, z)

    linestr = meshfile.readline()


    # Now find the elements section ...

    while linestr.find("$Elements") < 0:
        linestr = meshfile.readline()

    numelems = int(meshfile.readline())


    # read in the elements, match nodes to boundary

    boundnodes = {}

    for i in range(0, numelems, 1):

        words = meshfile.readline().split()

        eID   = int(words[0])
        etype = int(words[1])
        entityID = int(words[2])
        geomID =  int(words[3])

        if( not (etype == 4 or etype == 2) ):
            print "Error: only recognise triangular adn tetrahedral elements (type=2 or 4)!"
            exit(1)

        if ( geomID == boundaryID ):
            elenodes = words[5:9]

            for cnodeID in elenodes:
                nodeID = int( cnodeID )

                if ( nodeID > 0 ):
                    boundnodes[ nodeID ] = allnodes[ nodeID ]


    meshfile.close()



# ---------------------------------------------------------------------------
# now lock a node if it's found on the list.


def val( (x, y, z), t):

    # default is no lock
    lockvalue = 0

    for nodeID in boundnodes:
        (nx, ny, nz) = boundnodes[ nodeID ] 

        # if we find the same point
        if( abs(nx-x) < horizSmall and \
                abs(ny-y) < horizSmall and \
                abs(nz-z) < vertSmall ):

            lockvalue = 1
            break

    return lockvalue

