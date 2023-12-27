#!/usr/bin/env python3
import numpy as np

def mueen_fun(lm, wm, z0, fa, dS, lr, Ht, BL, PSImax, Rmax, Rmin) -> list:
    '''
    lm: heliostat length, m
    wm: heliostat width, m
    z0: height of the heliostat center from the base, m
    fa: ratio of the reflecting surface to the total surface of a heliostat
    dS: ratio of heliostat separation distance to heliostat length
    lr: receiver height, m
    Ht: aim point height, m
    Dt: tower diameter, m
    BL: terrain slope rising away from the tower, radian
    PSImax: maximum angular direction, radians (in 1 and 2 quadrant, total angle is 2.0*PSImax), radian
    Rmax: maximum ring radius in the field, m
    Rmin: minimum ring radius in the field, m
    '''

    # STEP 1
    f = wm/lm
    Am = f * fa * lm*lm  # net area of the heliostat reﬂecting surface, m2
    z1 = Ht-0.5*lr  # receiver bottom height, m
    rm = lm*0.5  # radius of a heliostat-representing circle in front view, m

    # STEP 2
    DM_A = []
    DM_A.append(lm*(np.sqrt(1+f*f)+dS))
    DM_A.append(2*wm)
    DM = np.max(DM_A)  # characteristic diameter, m
    Drmin = DM*np.cos(np.pi/6.)*np.cos(BL)  # minimum radial distance between two adjacent rings, m

    # STEP 3
    max_group_num = int((Rmax - Rmin)/DM + 1)  # estimate maximum number of group
    max_ring_per_group = max_group_num  # estimate maximum number of ring in one group

    # R[i][j]: radius of ring i in group j, m
    R = np.zeros((max_ring_per_group, max_group_num))
    i = 0  # ring index in group j
    j = 0  # group index
    R[0][0] = Rmin  # radius of the heliostats in the first ring in the first group is Rmin

    G = np.zeros(max_group_num)  # G->Gamma. G[j], angular direction unit for group j, radians
    NRG = np.zeros(max_group_num)  # NRG[j], number of ring in group j
    G[0] = 0.5*DM/R[i][j]  # angular direction unit for group j, radians

    # STEP 4
    while (R[i][j] <= Rmax):  # DO STEPS 5 to 12
        # calculate the radius of each ring in all possible group
        # STEP 5
        # R[0][0] = Rmin, so the first iteration just need calculate R[1][0]
        i = i+1

        R[i][j] = R[i-1][j]*np.cos(G[j])+np.sqrt(np.power((DM*np.cos(BL)), 2.0) -
                                                 np.power((R[i-1][j]*np.sin(G[j])), 2.0))
        # STEP 6
        while (i > 0 and R[i][j] <= Rmax):  # DO STEPS 7 to 12
            # calculate the radius of each ring the group j
            # STEP 7
            zm = z0+R[i-1][j]*np.tan(BL)
            a = z1*z1*(rm*rm-R[i-1][j]*R[i-1][j])
            b = 2*R[i-1][j]*z1*(z1-zm)
            c = rm*rm-(zm-z1)*(zm-z1)
            yr = (-b + np.sqrt(b*b-4.*a*c))/(2.*a)
            A = -((2*z1*yr+np.tan(BL))*np.tan(BL) + z1*z1*yr*yr)
            B = 2*(z1-z0)*(z1*yr+np.tan(BL))
            C = rm*rm*(1+z1*z1*yr*yr)-(z1-z0)*(z1-z0)

            ym2_A = []
            ym2_A.append((-B-np.sqrt(B*B-4*A*C))/(2*A))
            ym2_A.append(R[i][j]+Drmin)
            ym2 = np.max(ym2_A)

            # STEP 8

            Nm = 0  # number of heliostat in the ring
            if (i % 2 == 0):  # essential ring
                Nm = 2*(int(PSImax*0.5/G[j]))+1
            else:  # staggered ring
                Nm = 2*(int((PSImax-G[j])*0.5/G[j]))+2
            # STEP 9
            # land area of the part of the field under consideration, m2
            Af = PSImax*int(np.power((ym2+DM*0.5), 2.0) - np.power((R[i][j] + 0.5*DM), 2.0))

            # measure of mirror density, ratio of net reflecting surface area to covered land area
            delta = ((1.0*Nm)*Am)/Af

            # STEP 10
            zm = z0+R[i][j]*np.tan(BL)
            a = z1*z1*(rm*rm-R[i][j]*R[i][j])
            b = 2*R[i][j]*z1*(z1-zm)
            c = rm*rm-(zm-z1)*(zm-z1)
            yr = (-b + np.sqrt(b*b-4.*a*c))/(2.*a)

            A = -((2*z1*yr+np.tan(BL))*np.tan(BL) + z1*z1*yr*yr)
            B = 2*(z1-z0)*(z1*yr+np.tan(BL))
            C = rm*rm*(1+z1*z1*yr*yr)-(z1-z0)*(z1-z0)
            ym2_A = []
            ym2_A.append((-B-np.sqrt(B*B-4*A*C))/(2*A))
            ym2_A.append(R[i][j]+Drmin)
            ym2_t = np.max(ym2_A)

            # STEP 11
            G[j+1] = DM*0.5/ym2_t  # next group j+1
            Nm_t = 2*(int(PSImax*0.5/G[j+1]))+1
            Af_t = PSImax*(np.power((ym2_t+0.5*DM), 2.) - np.power((R[i][j]+0.5*DM), 2.))
            delta_t = ((1.0*Nm_t)*Am)/Af_t

            # STEP 12
            if (delta >= delta_t):
                # if this group can add a new ring
                i = i+1
                R[i][j] = ym2
            else:
                # if this group can not add a new ring, then add a new group
                NRG[j] = i+1
                j = j+1
                i = 0
                R[i][j] = ym2_t

        if (R[i][j] >= Rmax):
            break
        # elimination of calculation error
        if (R[int(NRG[j-1]-1)][j-1]-R[i][j] < DM):
            R[i][j] = R[int(NRG[j-1]-1)][j-1] + DM

    # STEP 13
    if (i > 0):
        # if i>0, the group j has been created
        NG = j+1  # Number of heliostat groups
        NRG[j] = i+1  # Number of ring in a group j
    else:
        # if i=0, the group j has not been created
        NG = j
    m = 1
    PSI = []  # angular direction of heliostat[m]
    x = []  # position.x of heliostat[m]
    y = []  # position.y of heliostat[m]
    z = []  # position.z of heliostat[m]
    eff = []  # group index of heliostat[m]

    output_file = open("output.csv", "w")
    output_file.write("id,x,y,z\n")
    # STEP 14
    # output the information of all heliostat
    for j in range(0, NG):
        # for group j
        nmax = int(PSImax/G[j])  # rough calculation of the number of heliostat in this group

        # correction the number of heliostat in this group
        while ((1.0*nmax)*G[j]+np.arctan(DM*0.5/R[int(NRG[j]-1)][j])) > np.pi:
            nmax = nmax-1

        for i in range(0, int(NRG[j])):
            # for ring i in group j
            if (i % 2 == 0):  # essential ring
                for n in range(0, nmax+1, 2):
                    PSI.append(1.0*(n)*G[j])
                    x.append(R[i][j]*np.sin(PSI[-1]))
                    y.append(R[i][j]*np.cos(PSI[-1]))
                    z.append(z0+R[i][j]*np.tan(BL))
                    eff.append(j)
                    output_file.write(str(m)+","+str(x[-1])+","+str(y[-1])+","+str(z[-1])+"\n")
                    m = m + 1
                    if (n > 0):
                        x.append(-x[-1])
                        y.append(y[-1])
                        z.append(z[-1])
                        eff.append(j)
                        output_file.write(str(m)+","+str(x[-1])+","+str(y[-1])+","+str(z[-1])+"\n")
                        m = m + 1
            else:  # staggered ring
                for n in range(1, nmax+1, 2):
                    PSI.append(1.0*(n)*G[j])
                    x.append(R[i][j]*np.sin(PSI[-1]))
                    y.append(R[i][j]*np.cos(PSI[-1]))
                    z.append(z0+R[i][j]*np.tan(BL))
                    eff.append(j)
                    output_file.write(str(m)+","+str(x[-1])+","+str(y[-1])+","+str(z[-1])+"\n")
                    m = m+1
                    x.append(-x[-1])
                    y.append(y[-1])
                    z.append(z[-1])
                    eff.append(j)
                    output_file.write(str(m)+","+str(x[-1])+","+str(y[-1])+","+str(z[-1])+"\n")
                    m = m+1
    print("heliostat number:", m-1)
    print("group number:", NG)
    output_file.close()


if __name__ == "__main__":
    lm = np.sqrt(8.)  # heliostat length, m
    wm = np.sqrt(8.)  # heliostat width, m
    z0 = 7.3     # height of the heliostat center from the base, m
    fa = 1.      # ratio of the reflecting surface to the total surface of a heliostat
    dS = 1.      # ratio of heliostat separation distance to heliostat length
    lr = 12.     # receiver height, m
    Ht = 75.0      # aim point height, m
    Dt = 8       # tower diameter, m
    BL = 0.0      # terrain slope rising away from the tower, radian
    PSImax = np.pi   # maximum angular direction, radians (in 1 and 2 quadrant, total angle is 2.0*PSImax), radian
    Rmax = 3.2*Ht  # maximum ring radius in the field, m
    Rmin = 0.8*Ht      # minimum ring radius in the field, m

    mueen_fun(lm, wm, z0, fa, dS, lr, Ht, BL, PSImax, Rmax, Rmin)

