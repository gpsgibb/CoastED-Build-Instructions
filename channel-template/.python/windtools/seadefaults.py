# Tabular data for sea wind stuff 

# Drag coefficients for two sets of data:
# 1)
# 'Sea surface drag coefficients in the Risoe air sea experiement'
# L. Mahrt et al
# Journal of Geophysical research vol. 101, no. June 15, 1996.
#
# 2)
# #Drag of Sea Surface'
# V.J Makin et al
# B-L Meteorology, 1995

def getWindspeedDragData():
    # Mahrt et al.
    # u0_arr=[4, 11, 13, 16]
    # cD_arr=[0.001, 0.00125, 0.0015, 0.002]

    # Makin et al
    u0_arr=[0.5, 2.5, 5, 20]
    cD_arr=[0.00125, 0.0011, 0.00125, 0.00225]
    
    return [u0_arr, cD_arr]

def getWindspeedRoughnessData():
    from math import exp, log, sqrt
    
    (u0_arr, cD_arr) = getWindspeedDragData()

    kappa = 0.41

    z0_arr=[]
    
    for this_cD in cD_arr:
        # This equation based on effective roughness calculations 
        # in Makin, pp178
        this_z0 = exp( log(10) - kappa/sqrt(this_cD))
        z0_arr.append(this_z0)

        
    return( (u0_arr, z0_arr) )