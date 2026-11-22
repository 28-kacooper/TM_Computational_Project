import numpy as np
from scipy.integrate import solve_ivp

"""Parameters can be put here ; assuming non-dimensionalized constants"""
kappa = 
r0 = 
time_scale
n # number of points

def M_mat(q):
    """ Assume we want Lagrangian of q^TMq + ... """
    r, psi, theta, phi = q
    comb = np.sqrt(1+r**2) # non-dimensionalized version of sqrt(R**2 + r**2)
    M = np.zeros((4, 4), dtype=complex)
    M[0,0] = 1
    M[0,2] = comb*np.cos(psi)
    M[0,3] = -comb*np.sin(psi)*np.sin(theta)
    M[1,1] = r**2
    M[1,2] = -r*comb*np.sin(psi)
    M[1,3] = -r*comb*np.cos(psi)*np.sin(theta)
    M[2,2] = comb**2
    M[3,3] = comb**2*np.sin(theta)**2
    #i'm too lazy to fill the lower triangle but will come bac

"""Potential matrix"""
def U_mat(q):
    r, psi, theta, phi = q
    return np.cos(theta) + r*np.cos(psi)*np.sin(theta) + 0.5*kappa*(r - r0)**2

"""To-Do: plug in euler-lagrange"""


if __name__ == "__main__"":
    s0 = np.array([r, psi, theta, phi, rdot, psifot, thetaot, phidot])
    t_range = np.linspace(0, T_END, N_PTS)
    # sol = solve_ivp(double_dot_here, (0, T_END), s0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
