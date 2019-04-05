dxmin  = 1;
dxmax  = 10;
xsize  = 1000;
ysize  = 250;
height = 50;

// These define the physical IDs of the boundaries

Mesh.CharacteristicLengthMin=dxmin;
Mesh.CharacteristicLengthMax=dxmax;


westBoundary=23;
eastBoundary=15;
northBoundary=27;
southBoundary=19;
topBoundary=28;
bottomBoundary=6;

Merge "dxmaxgrid.geo";
Merge "flatsea.geo";

Surface Loop(654321) = { 23, 15, 27, 19, 28, 6 };
the_loops[0]=654321;

// Turbine stuff
// Merge "turbines.geo";


// Created final surface loop

Volume(999) = {the_loops[]};

Physical Volume(1) = {999};

