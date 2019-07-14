import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

random.seed(time.time())

"""
    Visualization utilities
"""

def tet_to_cart_coords(tet_coords):
    """
        Purpose:  This function supports visualization of quaternary phase diagram

        Techical:
                  It transforms OA-OB-OD Tetrahedron coordinates into Cartesian coordinates. 
                  For this, it places O at O, and OA along y (leaving C on top of the tetrahedron
                  and B, together with O and A, on the xy-plane)
  
                                          C
                                        o
                                   z   o  o
                                   ^  o  o  o
                                   | o        o
                                   |o  y  o     o
                                O  o - -> - - - - o  A
                                  /   o    o    o
                                 /       o    o
                                x           o
                                              B
        Parameters:
                  tet_coords = numpy.array([
                                composition_of_element_A_along_OA_binary,
                                composition_of_element_B_along_OB_binary,
                                composition_of_element_C_along_OC_binary])
                  (Note: sum of above 3 compositions must be smaller of equal 1,
                   leaving the forth composition balancing to 1)
    """
    OA_proj_onto_xyz = np.array([np.zeros((np.size(tet_coords[:,0]),1))[:,0],
                                 tet_coords[:,0],
                                 np.zeros((np.size(tet_coords[:,0]),1))[:,0]])
    OB_proj_onto_xyz = np.array([tet_coords[:,1]*math.sin(math.pi/3),
                                 tet_coords[:,1]*math.cos(math.pi/3),
                                 np.zeros((np.size(tet_coords[:,1]),1))[:,0]])
    OC_proj_onto_xyz = np.array([tet_coords[:,2]*(math.sqrt(3)/3.0)*math.sin(math.pi/6.0),
                                 tet_coords[:,2]*(math.sqrt(3)/3.0)*math.cos(math.pi/6.0),
                                 tet_coords[:,2]*math.sqrt(6)/3.0])

    cart_coords = np.array([
                             OA_proj_onto_xyz[0,:] + OB_proj_onto_xyz[0,:] + OC_proj_onto_xyz[0,:],
                             OA_proj_onto_xyz[1,:] + OB_proj_onto_xyz[1,:] + OC_proj_onto_xyz[1,:],
                             OA_proj_onto_xyz[2,:] + OB_proj_onto_xyz[2,:] + OC_proj_onto_xyz[2,:]
                            ])
    return cart_coords.transpose()


def plot_tetrahedron(fig, elements, **kwargs):
    """
        Purpose:   Visualize the tetrahedron representing quaternary phase diagram

        Technical:
                   The function places O at O, and OA along y (leaving C on top of
                   the tetrahedron and B, together with O and A, on the xy-plane)
  
                                          C
                                        o
                                   z   o  o
                                   ^  o  o  o
                                   | o        o
                                   |o  y  o     o
                                O  o - -> - - - - o  A
                                  /   o    o    o
                                 /       o    o
                                x           o
                                              B
        Parameter:
                   elements: list of elements in quaternary, e.g. ['Cr','Fe','Mn','Ni']

    """
    edge_color = 'blue'
    text_size = 16
    text_color = 'black'
    for key in kwargs.keys():
        if key == 'edge_color':
            edge_color = kwargs[key]
        if key == 'text_size':
            text_size = int(kwargs[key])
        if key == 'text_color':
            text_color = kwargs[key]

    ax = fig.gca(projection='3d')
    edge_OA = np.array([
                        [0., 0., 0.],
                        [0., 1., 0.]
                        ])
    edge_OB = np.array([
                        [0., 0., 0.],
                        [math.sin(math.pi/3.0), math.cos(math.pi/3), 0.]
                        ])
    edge_BA = np.array([
                        [math.sin(math.pi/3.0), math.cos(math.pi/3), 0.],
                        [0., 1., 0.]
                        ])
    edge_OC = np.array([
                        [0., 0., 0.],
                        [(math.sqrt(3)/3.)*math.sin(math.pi/6),
                         (math.sqrt(3)/3.)*math.cos(math.pi/6),
                         math.sqrt(6)/3.]
                        ])
    edge_BC = np.array([
                        [math.sin(math.pi/3.0), math.cos(math.pi/3), 0.0],
                        [(math.sqrt(3)/3.0)*math.sin(math.pi/6.0),
                        (math.sqrt(3)/3.0)*math.cos(math.pi/6.0),
                        math.sqrt(6)/3.0]
                        ])
    edge_AC = np.array([
                        [0.0, 1.0, 0.0],
                        [(math.sqrt(3)/3.0)*math.sin(math.pi/6.0),
                        (math.sqrt(3)/3.0)*math.cos(math.pi/6.0),
                         math.sqrt(6)/3.0]
                        ])
    ax.plot(edge_OA[:,0], edge_OA[:,1], edge_OA[:,2], color=edge_color)
    ax.plot(edge_OB[:,0], edge_OB[:,1], edge_OB[:,2], color=edge_color)
    ax.plot(edge_BA[:,0], edge_BA[:,1], edge_BA[:,2], color=edge_color)
    ax.plot(edge_OC[:,0], edge_OC[:,1], edge_OC[:,2], color=edge_color)
    ax.plot(edge_BC[:,0], edge_BC[:,1], edge_BC[:,2], color=edge_color)
    ax.plot(edge_AC[:,0], edge_AC[:,1], edge_AC[:,2], color=edge_color)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.text(0, 0, 0, elements[0], color=text_color, fontsize=text_size)
    ax.text(0, 1, 0, elements[1], color=text_color, fontsize=text_size)
    ax.text(math.sin(math.pi/3.0), math.cos(math.pi/3), 0., elements[2], color=text_color, fontsize=text_size)
    ax.text((math.sqrt(3)/3.0)*math.sin(math.pi/6.0),
            (math.sqrt(3)/3.0)*math.cos(math.pi/6.0),
            math.sqrt(6)/3.0,
            elements[3], color=text_color, fontsize=text_size)

    return


def scatter_compositions_at_one_temperature(
        fig, list_of_comps_in_tet_coords, assoc_temp_in_K, **kwargs):
    
    point_color = 'red'
    point_marker = 'o'
    for key in kwargs.keys():
        if key == 'point_color':
            point_color = kwargs[key]
        if key == 'point_marker':
            point_marker = kwargs[key]

    ax = fig.gca(projection='3d')

    if len(list_of_comps_in_tet_coords[0,:]) == 3: # Quaternary
        cart_coords = tet_to_cart_coords(list_of_comps_in_tet_coords)
        ax.scatter(cart_coords[:,0], cart_coords[:,1], cart_coords[:,2],
                   c=point_color, marker=point_marker)
        ax.text(0.0, 0.5, 1.025, str(assoc_temp_in_K) + ' K')
    
    return


def plot_quaternary_at_one_temperature(composition_as_dict, temperature):
    element_list = []
    for key in composition_as_dict.keys():
        element_list.append(key.split()[0]) # [O, A, B, C] in tetrahedron coords
    if numel(element_list) != 4:
        print('This plot is for quaternary!!!')
        exit()
    tet_coords = []
    for key in composition_as_dict.keys()[1:]:
        tet_coords.append(composition_as_dict[key][:])
    tet_coords = np.array(tet_coords)
    fig = plt.figure()
    plot_tetrahedron(fig, element_list[1:])
    scatter_compositions_at_one_temperature(fig, tet_coords.transpose())
    plt.show()


"""
    Computational Thermodynamics Utililies
"""

def compute_TX_equilibrium_infinite(tdb_filename, element_list, temperature_T, composition_X_as_dict):
    error = 1.0 
    fix_factor = 0.0
    while error > 0.0:
        tqini()
        tqrpfil(tdb_filename, element_list)
        tqsetc('N', 0, 1.0)
        tqsetc('P', 0, 1.e5)
        tqsetc('T', 0, temperature_T + fix_factor * float(random.randint(0,100))/10000.)
        for key in list(composition_X_as_list.keys()[1:]):
            tqsetc('X', key.split()[0], composition_X_as_dict[key] + fix_factor * float(random.randint(0,100))/1000000.)
        error = tqce()
        if error > 0.0:
            fix_factor = fix_factor + 0.1
        tqrseterr()

