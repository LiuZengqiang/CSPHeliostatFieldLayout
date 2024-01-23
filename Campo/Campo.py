#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import matplotlib.pyplot as plt
from SunPosition import *
import numpy as np


def radial_stagger_campo(latitude, num_hst, width, height, hst_z, towerheight, R1, fb, dsep):
    """
    Generate a radial-stagger heliostat field, ref. Collado and Guallar, 2012, Campo: Generation of regular heliostat field.
    latitude: latitude of the field location, deg
    num_hst: number of heliostats
    width: heliostat width, m
    height: heliostat height, m
    hst_z: the vertical location of each heliostat, m
    towerheight: tower height, m
    R1: distance from the first row to the bottom of the tower, m
    fb: the field layout growing factor, f_{b,ref} in reference paper, higer fb lower heliostat density, in [0, 1]
    dsep: separation distance, m
    """

    # heliostat diagonal distantce
    DH = np.sqrt(height**2+width**2)

    # distance between contiguous helistat center on the X and Y plane
    DM = DH+dsep

    # minimum radial increment
    delta_Rmin = 0.866*DM

    # number of heliostats in the first row
    Nhel1 = int(2.*np.pi*R1/DM)

    # the total number of zones (estimated)
    # Nzones=int(np.log(5.44*3*(num_hst/az_rim*np.pi)/Nhel1**2+1)/np.log(4))+1

    X = {}
    Y = {}
    Nrows_zone = np.array([])
    Nhel_zone = np.array([])
    delta_az_zone = np.array([])

    num = 0
    i = 0
    sys.stderr.write('DM '+repr(DM)+'\n')
    sys.stderr.write('dRm '+repr(delta_Rmin)+'\n')

    while num < num_hst*3:
        Nrows = int((2.**(i))*Nhel1/5.44)
        Nhel = (2**(i))*Nhel1
        R = Nhel/2./np.pi*DM
        delta_az = 2.*np.pi/Nhel

        Nrows_zone = np.append(Nrows_zone, Nrows)
        Nhel_zone = np.append(Nhel_zone, Nhel)
        delta_az_zone = np.append(delta_az_zone, delta_az)

        nh = np.arange(Nhel)
        azimuth = np.zeros((int(Nrows), int(Nhel)))
        azimuth[0::2, :] = delta_az/2.+nh*delta_az  # the odd rows
        azimuth[1::2, :] = nh*delta_az

        row = np.arange(Nrows)
        r = R+row*delta_Rmin

        xx = r[:, None]*np.sin(azimuth)
        yy = r[:, None]*np.cos(azimuth)

        X[i] = xx
        Y[i] = yy
        num += len(xx.flatten())
        print('Zone', i, 'Nrow', Nrows, 'Nhel', Nhel)
        i += 1
    Nzones = i

    # expanding the field
    wr = width/height
    # last part of eq.(2) Francisco J. Collado, Jesus Guallar, Campo: Generation of regular heliostat fields, 2012
    const = (1.-(1.-fb)*wr/(2.*wr-(np.sqrt(1.+wr**2)+dsep/height))) * height

    XX = np.array([])  # heliostat position, x
    YY = np.array([])  # heliostat position, y
    ZONE = np.array([])  # zone index
    ROW = np.array([])   # row index among the rows in a zone
    TTROW = np.array([])  # row index among the total rows
    NHEL = np.array([])  # No. index among the heliostats in a row
    AZIMUTH = np.array([])

    for i in range(Nzones):
        Nrows = int(Nrows_zone[i])
        Nhel = int(Nhel_zone[i])
        delta_az = delta_az_zone[i]

        R = np.zeros((Nrows, Nhel))

        if i == 0:
            # first zone
            R[0] = R1  # first row
        else:
            # second zones
            R[0, ::2] = Rn+1.5*DRn
            R[0,  1::2] = Rn+1.5*DRn
            # R[0,-1]=0.5*(R[0,0]+Rn[-1])

        xx = X[i]
        yy = Y[i]
        zz = np.ones(np.shape(xx))*hst_z
        cosw, coseT = cal_cosw_coset(latitude, towerheight, xx, yy, zz)
        row = np.arange(Nrows)
        cosw = cosw.reshape(Nrows, Nhel)
        coseT = coseT.reshape(Nrows, Nhel)

        Delta_R = cosw/coseT*const
        Delta_R[Delta_R < delta_Rmin] = delta_Rmin

        for j in range(1, Nrows):
            R[j] = R[j-1]+Delta_R[j-1]

        Rn = R[-1]
        DRn = Delta_R[-1]

        nh = np.arange(Nhel)
        azimuth = np.zeros((Nrows, Nhel))
        azimuth[0::2, :] = delta_az/2.+nh*delta_az  # the odd rows
        azimuth[1::2, :] = nh*delta_az

        azimuth = azimuth.flatten()
        R = R.flatten()
        nhels, rows = np.meshgrid(nh, row)
        nhels = nhels.flatten()
        rows = rows.flatten()

        xx = R*np.sin(azimuth)
        yy = R*np.cos(azimuth)
        AZIMUTH = np.append(AZIMUTH, azimuth)
        ROW = np.append(ROW, rows)
        NHEL = np.append(NHEL, nhels)
        zone = np.ones(np.shape(rows))*i

        XX = np.append(XX, xx)
        YY = np.append(YY, yy)
        ZONE = np.append(ZONE, zone)

        if len(TTROW) == 0:
            TTROW = np.append(TTROW, rows)
        else:
            TTROW = np.append(TTROW, rows+np.max(TTROW)+1)

    num_hst = int(num_hst)

    XX = XX[:num_hst]
    YY = YY[:num_hst]
    ZONE = ZONE[:num_hst]
    ROW = ROW[:num_hst]
    NHEL = NHEL[:num_hst]
    TTROW = TTROW[:num_hst]
    AZIMUTH = AZIMUTH[:num_hst]*180./np.pi

    hstpos = np.zeros(num_hst*3).reshape(num_hst, 3)
    hstpos[:, 0] = XX
    hstpos[:, 1] = YY
    hstpos[:, 2] = hst_z
    output_file = open("layout.csv", "w")
    output_file.write("id,x,y,z\n")
    for i in range(len(hstpos)):
        output_file.write(
            str(i)+","+str(hstpos[i][0])+","+str(hstpos[i][1])+","+str(hstpos[i][2])+"\n")
    output_file.close()

    plt.scatter(XX, YY, s=5.0)
    ax = plt.gca()
    ax.set_aspect(1)
    plt.savefig("layout.png")
    plt.close()

    return hstpos


def cal_cosw_coset(latitude, towerheight, xx, yy, zz):
    '''
    The factors to growing the heliostat field, see eq.(2) Francisco J. Collado, Jesus Guallar, Campo: Generation of regular heliostat fields, 2012

    ``Arguments``
      * latitude (float)   : latitude of the field location (deg)
      *	towerheight (float): tower height (m)
  * xx, yy, zz (float) : coordinates of heliostats

    ``Returns``
      * cosw (array) : cos(omega)
      * coseT (array): cos(epsilon_T) 

    '''

    hst_pos = np.append(xx, (yy, zz))
    hst_pos = hst_pos.reshape(3, len(xx.flatten()))  # 3 x n
    tower_vec = -hst_pos
    tower_vec[-1] += towerheight
    tower_vec /= np.sqrt(np.sum(tower_vec**2, axis=0))  # 3 x n
    unit = np.array([[0.], [0.], [1.]])
    unit = np.repeat(unit, len(tower_vec[0]), axis=1)
    coseT = np.sum(tower_vec*unit, axis=0)

    sun = SunPosition()
    dd = sun.days(21, 'Mar')  # Equinox Day
    delta = sun.declination(dd)
    h = np.arange(8, 17)  # hour

    omega = -180.+15.*h
    theta = sun.zenith(latitude, delta, omega)  # solar zenith angle

    phi = np.array([])  # solar azimuth angle
    for i in range(len(h)):
        p = sun.azimuth(latitude, theta[i], delta, omega[i])
        phi = np.append(phi, p)

    theta *= np.pi/180.
    phi *= np.pi/180.

    cosw = np.zeros(len(tower_vec[0]))
    sun_z = np.cos(theta)
    sun_y = -np.sin(theta)*np.cos(phi)
    sun_x = -np.sin(theta)*np.sin(phi)
    sun_vec = np.append(sun_x, (sun_y, sun_z))
    sun_vec = sun_vec.reshape(3, len(sun_x))  # 3xs

    for i in range(len(sun_vec[0])):
        sv = np.repeat(sun_vec[:, i], len(tower_vec[0])
                       ).reshape(3, len(tower_vec[0]))
        hst_norms = sv+tower_vec
        hst_norms /= np.linalg.norm(hst_norms, axis=0)
        cosw += np.sum(sv*hst_norms, axis=0)
    cosw /= float(len(sun_vec[0]))
    return cosw, coseT


if __name__ == '__main__':
    """
    Generate a radial-stagger heliostat field, ref. Collado and Guallar, 2012, Campo: Generation of regular heliostat field.
    latitude: latitude of the field location, deg
    num_hst: number of heliostats
    width: heliostat width, m
    height: heliostat height, m
    hst_z: the vertical location of each heliostat, m
    towerheight: tower height, m
    R1: distance from the first row to the bottom of the tower, m
    fb: the field layout growing factor, f_{b,ref} in reference paper, higer fb lower heliostat density, in [0, 1]
    dsep: separation distance, m
    """

    heliostat_pos = radial_stagger_campo(latitude=34., num_hst=6230, width=10., height=10., hst_z=0.,
                                         towerheight=250, R1=80, fb=1.0, dsep=0.)
