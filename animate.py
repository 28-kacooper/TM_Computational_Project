import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

R = 1.0

data=np.load("")
t, Q =  data["t"], data["q"]


""" Animation structure copied from 064 code which is adopted from Prof. Saeta's baseline code. """

class Animator:
    # necessary for class structure
    def __init__(self, t, Q, R=1.0):
        self.t, self.Q, self.R = t, Q, R          
        self.fig = plt.figure(figsize=(7, 7))
        self.ax = self.fig.add_subplot(projection="3d")
        self.lim = 1.1 * np.sqrt(R**2 + Q[:, 0].max()**2)

    # sets up limits and labels axes, also makes it so we have a cubic frame
    def set_ax_lim(self, ax):
        L = self.lim
        ax.set(xlim=(-L, L), ylim=(-L, L), zlim=(-L, L),
               xlabel="x", ylabel="y", zlabel="z")
        ax.set_box_aspect((1, 1, 1))

    
    # this was a prof. saeta reccomendation for this, but i think this essentially moves through time and 
    # draws line between known points in order to form finite steps to draw
    """Gives us q at continuous time to form full frame"""
    # TO-DO: figure out if easier/better method for visual integration
    def state(self, t):
        return [np.interp(t, self.t, self.Q[:, i]) for i in range(4)]

    """This returns a 3x3 matric that converts the body frame into the intertial frame. 
    We generally need the body-frame coords in spherical , but they need to be Cartesisan in order to set up"""
    def rotation(self, t):
        r, psi, theta, phi = self.state(t)
        Rh = [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
        Th = [np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), -np.sin(theta)]
        Ph = [-np.sin(phi), np.cos(phi), 0.0]
        return np.column_stack([Rh, Th, Ph])
    
   
    # this moves things from the body to the inertial / lab frame and then applies rotation to each point in matrix
    def body_to_lab(self, t, arrays):
        Rot = self.rotation(t)
        return [a @ Rot.T for a in arrays]        

    # To-do: Figure out if we / how we record multiple masses with this
    def mass_position(self, t):
        r, ps, th, ph = self.state(t)
        body = np.array([[self.R, -r*np.cos(ps), r*np.sin(ps)]])   
        return self.body_to_lab(t, [body])[0][0]

    # draws a frame for each position
    def show(self, t):
        ax = self.ax
        ax.clear()
        self.set_ax_lim(ax)
        r, ps, th, ph = self.state(t)
        R = self.R

        """To-O:Fic the rest of this """

if __name__ == "__main__":
    data = np.load("traj.npz")
    anim = Animator(data["t"], data["q"])
    times = data["t"][::10]
    ani = FuncAnimation(anim.fig, lambda t: anim.show(t), frames=times,
                        interval=33, blit=False)   # blit must be False with ax.clear()
    plt.show()