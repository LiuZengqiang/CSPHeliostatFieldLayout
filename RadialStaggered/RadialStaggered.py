#!/usr/bin/env python3
import numpy as np
def radial_staggered_fun(start_ang, end_ang, az_space, rmin, rmax, r_space) -> list:
    """
    start_ang: the start angle clockwise from the X axis that define the field's boundaries, rad
    end_ang: the end angle clockwise from the X axis that define the field's boundaries, rad
    az_space: the azimuthal space between two heliostats, rad
    rmin: the minimum boundaries of the field in the radial direction, m
    rmax: the maximum boundaries of the field in the radial direction, m
    r_space: the space between radial lines of heliostats, m
    """

    rs = np.r_[rmin:rmax:r_space]
    angs = np.r_[start_ang:end_ang:az_space/2.0]

    # 1st stagger:
    xs1 = np.outer(rs[::2], np.cos(angs[::2])).flatten()
    ys1 = np.outer(rs[::2], np.sin(angs[::2])).flatten()

    # 2nd staggeer:
    xs2 = np.outer(rs[1::2], np.cos(angs[1::2])).flatten()
    ys2 = np.outer(rs[1::2], np.sin(angs[1::2])).flatten()

    xs = np.r_[xs1, xs2]
    ys = np.r_[ys1, ys2]
    zs = np.ones(np.shape(xs))*0.0

    pos = np.vstack((xs, ys, zs)).T

    output_file = open("layout.csv", "w")
    output_file.write("id,x,y,z\n")
    print("heliostat number:", len(xs))
    for i in range(len(xs)):
        output_file.write(str(i)+","+str(xs[i])+","+str(ys[i])+","+"0\n")

    output_file.close()


if __name__ == "__main__":
    """
    start_ang: the start angle clockwise from the X axis that define the field's boundaries, rad
    end_ang: the end angle clockwise from the X axis that define the field's boundaries, rad
    az_space: the azimuthal space between two heliostats, rad
    rmin: the minimum boundaries of the field in the radial direction, m
    rmax: the maximum boundaries of the field in the radial direction, m
    r_space: the space between radial lines of heliostats, m
    """
    start_ang = 0.0
    end_ang = 2.0*np.pi
    az_space = 2.0*np.pi/50.0
    rmin = 80.0
    rmax = 200.0
    r_space = 5.0
    radial_staggered_fun(start_ang, end_ang, az_space, rmin, rmax, r_space)
