# -----------------------------------------------------------------------------
# Module for Fluidity to extract depths from
# (Inbuilt code is crap)
# -----------------------------------------------------------------------------

import nc_depth_io
        


# -----------------------------------------------------------------------------
# Fluidity entry point



def val(pt, t):

    depth = nc_depth_io.calculateDepth(pt)

    return depth
