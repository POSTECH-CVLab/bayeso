# test_gp
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: August 07, 2020

import pytest
import numpy as np
import typing

from bayeso import constants
from bayeso.gp import gp
try:
    from bayeso.gp import gp_tensorflow
except: # pragma: no cover
    gp_tensorflow = None
try:
    from bayeso.gp import gp_gpytorch
except: # pragma: no cover
    gp_gpytorch = None
from bayeso.utils import utils_covariance


TEST_EPSILON = 1e-7

def test_sample_functions_typing():
    annos = gp.sample_functions.__annotations__

    assert annos['mu'] == np.ndarray
    assert annos['Sigma'] == np.ndarray
    assert annos['num_samples'] == int
    assert annos['return'] == np.ndarray

def test_sample_functions():
    num_points = 10
    mu = np.zeros(num_points)
    Sigma = np.eye(num_points)
    num_samples = 5

    with pytest.raises(AssertionError) as error:
        gp.sample_functions(mu, 'abc')
    with pytest.raises(AssertionError) as error:
        gp.sample_functions('abc', Sigma)
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(mu, np.eye(20))
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(mu, np.ones(num_points))
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(np.zeros(20), Sigma)
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(np.eye(10), Sigma)
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(mu, Sigma, num_samples='abc')
    with pytest.raises(AssertionError) as error:
        gp.sample_functions(mu, Sigma, num_samples=1.2)


    functions = gp.sample_functions(mu, Sigma, num_samples=num_samples)
    assert functions.shape[1] == num_points
    assert functions.shape[0] == num_samples

def test_get_optimized_kernel_typing():
    annos = gp.get_optimized_kernel.__annotations__

    assert annos['X_train'] == np.ndarray
    assert annos['Y_train'] == np.ndarray
    assert annos['prior_mu'] == typing.Union[callable, type(None)]
    assert annos['str_cov'] == str
    assert annos['str_framework'] == str
    assert annos['str_optimizer_method'] == str
    assert annos['str_modelselection_method'] == str
    assert annos['fix_noise'] == bool
    assert annos['debug'] == bool
    assert annos['return'] == typing.Tuple[np.ndarray, np.ndarray, dict]

def test_get_optimized_kernel():
    np.random.seed(42)
    dim_X = 3
    num_X = 10
    num_instances = 5
    X = np.random.randn(num_X, dim_X)
    X_set = np.random.randn(num_X, num_instances, dim_X)
    Y = np.random.randn(num_X, 1)
    prior_mu = None

    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 1)
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, 1, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, 1, prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(1, Y, prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(np.ones(num_X), Y, prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, np.ones(num_X), prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(np.ones((50, 3)), Y, prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, np.ones((50, 1)), prior_mu, 'se')
    with pytest.raises(ValueError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'abc')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_framework=1)
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_optimizer_method=1)
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_modelselection_method=1)
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'se', fix_noise=1)
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'se', debug=1)

    # INFO: tests for set inputs
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X_set, Y, prior_mu, 'se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X, Y, prior_mu, 'set_se')
    with pytest.raises(AssertionError) as error:
        gp.get_optimized_kernel(X_set, Y, prior_mu, 'set_se', debug=1)

    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'eq')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'matern32')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'matern52')
    print(hyps)

    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_optimizer_method='BFGS')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_optimizer_method='L-BFGS-B')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_optimizer_method='Nelder-Mead')
    print(hyps)

    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_modelselection_method='loocv')
    print(hyps)

    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_framework='scipy')
    print(hyps)

    if gp_tensorflow is not None:
        cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_framework='tensorflow')
        print(hyps)

    if gp_gpytorch is not None:
        cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se', str_framework='gpytorch')
        print(hyps)

    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X_set, Y, prior_mu, 'set_se')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X_set, Y, prior_mu, 'set_se', str_optimizer_method='L-BFGS-B')
    print(hyps)
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X_set, Y, prior_mu, 'set_se', str_modelselection_method='loocv')
    print(hyps)

def test_predict_with_cov_typing():
    annos = gp.predict_with_cov.__annotations__

    assert annos['X_train'] == np.ndarray
    assert annos['Y_train'] == np.ndarray
    assert annos['X_test'] == np.ndarray
    assert annos['cov_X_X'] == np.ndarray
    assert annos['inv_cov_X_X'] == np.ndarray
    assert annos['hyps'] == dict
    assert annos['str_cov'] == str
    assert annos['prior_mu'] == typing.Union[callable, type(None)]
    assert annos['debug'] == bool
    assert annos['return'] == typing.Tuple[np.ndarray, np.ndarray, np.ndarray]

def test_predict_with_cov():
    np.random.seed(42)
    dim_X = 2
    num_X = 5
    num_X_test = 20
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)
    X_test = np.random.randn(num_X_test, dim_X)
    prior_mu = None
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se')
    
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu='abc')
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov=1, prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, cov_X_X, inv_cov_X_X, 1, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, cov_X_X, 1, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, 1, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)

    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, 1, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, 1, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(1, Y, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(np.random.randn(num_X, 1), Y, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(np.random.randn(10, dim_X), Y, X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)

    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, np.random.randn(10, 1), X_test, cov_X_X, inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, np.random.randn(3, 3), inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, np.random.randn(10), inv_cov_X_X, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, cov_X_X, np.random.randn(10), hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_cov(X, Y, X_test, np.random.randn(10), np.random.randn(10), hyps, str_cov='se', prior_mu=prior_mu)

def test_predict_with_hyps_typing():
    annos = gp.predict_with_hyps.__annotations__

    assert annos['X_train'] == np.ndarray
    assert annos['Y_train'] == np.ndarray
    assert annos['X_test'] == np.ndarray
    assert annos['hyps'] == dict
    assert annos['str_cov'] == str
    assert annos['prior_mu'] == typing.Union[callable, type(None)]
    assert annos['debug'] == bool
    assert annos['return'] == typing.Tuple[np.ndarray, np.ndarray, np.ndarray]

def test_predict_with_hyps():
    np.random.seed(42)
    dim_X = 2
    num_X = 5
    num_X_test = 20
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)
    X_test = np.random.randn(num_X_test, dim_X)
    prior_mu = None
    cov_X_X, inv_cov_X_X, hyps = gp.get_optimized_kernel(X, Y, prior_mu, 'se')
    
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, Y, X_test, hyps, str_cov='se', prior_mu='abc')
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, Y, X_test, hyps, str_cov=1, prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, Y, X_test, 1, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, Y, 1, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, 1, X_test, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(1, Y, X_test, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(np.random.randn(num_X, 1), Y, X_test, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(np.random.randn(10, dim_X), Y, X_test, hyps, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_hyps(X, np.random.randn(10, 1), X_test, hyps, str_cov='se', prior_mu=prior_mu)
    
    mu_test, sigma_test, Sigma_test = gp.predict_with_hyps(X, Y, X_test, hyps, str_cov='se', prior_mu=prior_mu)
    print(mu_test)
    print(sigma_test)
    print(Sigma_test)

def test_predict_with_optimized_hyps_typing():
    annos = gp.predict_with_optimized_hyps.__annotations__

    assert annos['X_train'] == np.ndarray
    assert annos['Y_train'] == np.ndarray
    assert annos['X_test'] == np.ndarray
    assert annos['str_cov'] == str
    assert annos['str_optimizer_method'] == str
    assert annos['prior_mu'] == typing.Union[callable, type(None)]
    assert annos['fix_noise'] == float
    assert annos['debug'] == bool
    assert annos['return'] == typing.Tuple[np.ndarray, np.ndarray, np.ndarray]

def test_predict_with_optimized_hyps():
    np.random.seed(42)
    dim_X = 2
    num_X = 5
    num_X_test = 20
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)
    X_test = np.random.randn(num_X_test, dim_X)
    prior_mu = None
    
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, X_test, str_cov='se', prior_mu='abc')
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, X_test, str_cov=1, prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, 1, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, 1, X_test, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(1, Y, X_test, str_cov='se', prior_mu=prior_mu)

    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(np.random.randn(num_X, 1), Y, X_test, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(np.random.randn(10, dim_X), Y, X_test, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, np.random.randn(10, 1), X_test, str_cov='se', prior_mu=prior_mu)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, X_test, str_optimizer_method=1)
    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, X_test, fix_noise=1)

    with pytest.raises(AssertionError) as error:
        gp.predict_with_optimized_hyps(X, Y, X_test, debug=1)
    
    mu_test, sigma_test, Sigma_test = gp.predict_with_optimized_hyps(X, Y, X_test)
    print(mu_test)
    print(sigma_test)
    print(Sigma_test)
