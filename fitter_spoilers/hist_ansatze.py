from inspect import signature

import numpy as np


class Ansatz:
    def __init__(self, func, name, form):
        self.name = name
        self.form = form
        self.func = func
        self.num_params = len(signature(func).parameters) - 1


normal = Ansatz(
    lambda x, a, b, c: a * np.exp(-((x - b) ** 2) / c**2),
    "Normal",
    "f(x)= a * exp( -(x-b)^2 / c^2 )",
)
power = Ansatz(lambda x, a, b: a * np.exp(-b * x), "Power", "f(x)= a * exp( -b * x )")
norm_pow = Ansatz(
    lambda x, a, b, c, d, e: a * np.exp(-b * x) + c * np.exp(-((x - d) ** 2) / e**2),
    "Normal + Power",
    "f(x)= a * exp( -b * x ) + c * exp( -(x-d)^2 / e^2 ) + ",
)


hist_ansatze = (normal, power, norm_pow)
