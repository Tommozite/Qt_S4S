from inspect import signature

import numpy as np


class Ansatz:
    def __init__(self, func, name, form):
        self.name = name
        self.form = form
        self.func = func
        self.num_params = len(signature(func).parameters) - 1


const = Ansatz(lambda x, a: a, "Constant", "f(x)= a")
linear = Ansatz(lambda x, a, b: a * x + b, "Linear", "f(x)= a * x + b")
quadratic = Ansatz(
    lambda x, a, b, c: a * x**2 + b * x + c, "Quadratic", "f(x)= a * x^2+ b * x + c"
)
cubic = Ansatz(
    lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
    "Cubic",
    "f(x)= a * x^3 + b * x^2 + c * x + d",
)
exp = Ansatz(lambda x, a, b: a * np.exp(b * x), "Exponential", "f(x)= a * exp(b * x)")
log = Ansatz(lambda x, a, b: a * np.log(b * x), "Logarithm", "f(x)= a * ln(b * x)")
sin = Ansatz(
    lambda x, a, b, c: a * np.sin(b * x + c), "Sine", "f(x)= a * sin(b * x + c)"
)
cos = Ansatz(
    lambda x, a, b, c: a * np.sin(b * x + c), "Cosine", "f(x)= a * cos(b * x + c)"
)
tan = Ansatz(
    lambda x, a, b, c: a * np.sin(b * x + c), "Tangent", "f(x)= a * tan(b * x + c)"
)


simple_ansatze = (const, linear, quadratic, cubic, exp, log, sin, cos, tan)
