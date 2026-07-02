import numpy as np
import matplotlib.pyplot as plt

class NACA4Digit():
    """
    Generate and visualize NACA 4-digit airfoils.

    Parameters
    ----------
    chord : float
        Chord length.
    mcamber : float
        Maximum camber as a fraction of chord.
    p : float
        Position of maximum camber.
    mthick : float
        Maximum thickness as a fraction of chord.
    n_points : int
        Number of coordinate points.
    """

    def __init__(self, chord, mcamber, p, mthick, n_points):
       
        self.chord = chord
        self.mcamber = mcamber
        self.p = p
        self.mthick = mthick
        self.n_points = n_points

        #initialize data containers 
        self.X = np.linspace(0, chord,  n_points)
        self.Yc = None
        self.dYcdx = None
        self.Yt = None
        self.Teta = None
        self.Xu = None
        self.Xl = None
        self.Yu = None
        self.Yl = None

        # creatation of airfoil
        self.compute_airfoil()


    def compute_camber_thick(self):

        self.Yc = []
        self.dYcdX = []
        self.Yt = []

        for x in self.X:

            yt = 5 * self.mthick * (
                0.2969 * np.sqrt(x)
                - 0.1260 * x
                - 0.3516 * x**2
                + 0.2843 * x**3
                - 0.1015 * x**4
            )
            self.Yt.append(yt)
            if self.mcamber == 0:
                yc = 0
                dycdx = 0

            elif x <= self.p:
                yc = (self.mcamber / self.p**2) * (2 * self.p * x - x**2)

                dycdx = (2 * self.mcamber / self.p**2) * (self.p - x)

            else:
                yc = (self.mcamber / (1 - self.p)**2) * (
                    1 - 2 * self.p + 2 * self.p * x - x**2
                )

                dycdx = (2 * self.mcamber / (1 - self.p)**2) * (self.p - x)

            self.Yc.append(yc)
            self.dYcdX.append(dycdx)


    def compute_airfoil(self):

        self.compute_camber_thick()

        self.Teta = []
        for dycdx in self.dYcdX:
            teta = np.arctan(dycdx)
            self.Teta.append(teta)

        self.Xu = []
        self.Xl = []
        self.Yu = []
        self.Yl = []

        for x, yt, teta, yc in zip(self.X, self.Yt, self.Teta, self.Yc):

            xu = x - yt * np.sin(teta)
            xl = x + yt * np.sin(teta)

            yu = yc + yt * np.cos(teta)
            yl = yc - yt * np.cos(teta)

            self.Xu.append(xu)
            self.Xl.append(xl)
            self.Yu.append(yu)
            self.Yl.append(yl)

    def plot(self):
        
        plt.figure(figsize=(12, 4))

        plt.plot(self.Xu, self.Yu, label="Upper Surface")
        plt.plot(self.Xl, self.Yl, label="Lower Surface")
        plt.plot(self.X, self.Yc, "--", label="Camber Line")

        plt.axis("equal")
        plt.grid(True)
        plt.xlabel("x/c")
        plt.ylabel("y/c")

        code = (
            f"{int(self.mcamber * 100):1d}"
            f"{int(self.p * 10):1d}"
            f"{int(self.mthick * 100):02d}"
        )

        plt.title(f"NACA {code}")
        plt.legend()

        plt.show()



