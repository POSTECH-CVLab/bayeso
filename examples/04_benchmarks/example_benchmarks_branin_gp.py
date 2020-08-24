# example_gp_benchmarks_branin
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: April 28, 2020

import numpy as np

from bayeso import bo
from bayeso import acquisition
from bayeso.gp import gp
from bayeso.utils import utils_bo
from bayeso.utils import utils_plotting
from benchmarks.two_dim_branin import Branin


STR_FUN_TARGET = 'branin'
PATH_SAVE = '../figures/benchmarks/'

obj_fun = Branin()


def fun_target(X):
    return obj_fun.output(X)

def main():
    num_points = 100
    is_fixed_noise = False
    bounds = obj_fun.get_bounds()

    model_bo = bo.BO(bounds, debug=True)
    X_init = model_bo.get_initial('uniform', fun_objective=fun_target, int_samples=num_points)
    X_test = bo.get_grids(bounds, 50)
    mu, sigma, Sigma = gp.predict_optimized(X_init, fun_target(X_init), X_test, is_fixed_noise=is_fixed_noise, debug=True)


if __name__ == '__main__':
    main()

