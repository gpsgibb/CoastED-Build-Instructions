Point(1) =  {0,     0,     0,      dxmax};
Point(2) =  {xsize, 0,     0,      dxmax};
Point(3) =  {xsize, ysize, 0,      dxmax};
Point(4) =  {0,     ysize, 0,      dxmax};
Point(5) =  {xsize, ysize, height, dxmax};
Point(6) =  {xsize, 0,     height, dxmax};
Point(10) = {0,     0,     height, dxmax};
Point(14) = {0,     ysize, height, dxmax};

Line(1) = {4, 3};
Line(2) = {3, 2};
Line(3) = {2, 1};
Line(4) = {1, 4};
Line(8) = {5, 6};
Line(9) = {6, 10};
Line(10) = {10, 14};
Line(11) = {14, 5};
Line(13) = {3, 5};
Line(14) = {2, 6};
Line(18) = {1, 10};
Line(22) = {4, 14};

// Bottom surface
Line Loop(6) = {2, 3, 4, 1};
Plane Surface(6) = {6};
Physical Surface( bottomBoundary ) = {6};


// Eastern boundary
Line Loop(15) = {2, 14, -8, -13};
Plane Surface(15) = {15};
Physical Surface( eastBoundary ) = {15};


// Southern boundary
Line Loop(19) = {3, 18, -9, -14};
Plane Surface(19) = {19};
Physical Surface( southBoundary ) = {19};


// Western boundary
Line Loop(23) = {4, 22, -10, -18};
Plane Surface(23) = {23};
Physical Surface( westBoundary ) = {23};


// Northern boundary
Line Loop(27) = {1, 13, -11, -22};
Plane Surface(27) = {27};
Physical Surface( northBoundary ) = {27};


// Top surface
Line Loop(28) = {8, 9, 10, 11};
Plane Surface(28) = {28};
Physical Surface( topBoundary ) = {28};


Surface Loop(1) = {6, 28, 15, 19, 23, 27};
surfaceLoopID=1;

