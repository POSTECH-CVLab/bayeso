# test_bo
# author: Jungtaek Kim (jtkim@postech.ac.kr)
# last updated: August 07, 2020

import numpy as np
import pytest

from bayeso import bo


TEST_EPSILON = 1e-5

def test_get_grids():
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    arr_range_2 = np.array([
        [0.0, 10.0],
        [2.0, 2.0],
        [5.0, 5.0],
    ])

    truth_arr_grid_1 = np.array([
        [0., -2., -5.],
        [0., -2., 0.],
        [0., -2., 5.],
        [5., -2., -5.],
        [5., -2., 0.],
        [5., -2., 5.],
        [10., -2., -5.],
        [10., -2., 0.],
        [10., -2., 5.],
        [0., 0., -5.],
        [0., 0., 0.],
        [0., 0., 5.],
        [5., 0., -5.],
        [5., 0., 0.],
        [5., 0., 5.],
        [10., 0., -5.],
        [10., 0., 0.],
        [10., 0., 5.],
        [0., 2., -5.],
        [0., 2., 0.],
        [0., 2., 5.],
        [5., 2., -5.],
        [5., 2., 0.],
        [5., 2., 5.],
        [10., 2., -5.],
        [10., 2., 0.],
        [10., 2., 5.],
    ])
    truth_arr_grid_2 = np.array([
        [0., 2., 5.],
        [0., 2., 5.],
        [0., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
        [0., 2., 5.],
        [0., 2., 5.],
        [0., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
        [0., 2., 5.],
        [0., 2., 5.],
        [0., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [5., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
        [10., 2., 5.],
    ])

    with pytest.raises(AssertionError) as error:
        bo.get_grids('abc', 3)
    with pytest.raises(AssertionError) as error:
        bo.get_grids(arr_range_1, 'abc')
    with pytest.raises(AssertionError) as error:
        bo.get_grids(np.arange(0, 10), 3)
    with pytest.raises(AssertionError) as error:
        bo.get_grids(np.ones((3, 3)), 3)
    with pytest.raises(AssertionError) as error:
        bo.get_grids(np.array([[0.0, -2.0], [10.0, 20.0]]), 3)

    arr_grid_1 = bo.get_grids(arr_range_1, 3)
    arr_grid_2 = bo.get_grids(arr_range_2, 3)

    assert (arr_grid_1 == truth_arr_grid_1).all()
    assert (arr_grid_2 == truth_arr_grid_2).all()

def test_get_best_acquisition():
    fun_objective = lambda x: x**2 - 2.0 * x + 1.0
    arr_initials = np.expand_dims(np.arange(-5, 5), axis=1)

    with pytest.raises(AssertionError) as error:
        bo.get_best_acquisition(1, fun_objective)
    with pytest.raises(AssertionError) as error:
        bo.get_best_acquisition(arr_initials, None)
    with pytest.raises(AssertionError) as error:
        bo.get_best_acquisition(np.arange(-5, 5), fun_objective)

    best_initial = bo.get_best_acquisition(arr_initials, fun_objective)
    assert len(best_initial.shape)
    assert best_initial.shape[0] == 1
    assert best_initial.shape[1] == arr_initials.shape[1]
    assert best_initial == np.array([[1]])

def test_check_optimizer_method_bo():
    directminimize = None
    cma = None

    with pytest.raises(AssertionError) as error:
        bo._check_optimizer_method_bo(2, 2, True)
    with pytest.raises(AssertionError) as error:
        bo._check_optimizer_method_bo('DIRECT', 'abc', True)
    with pytest.raises(AssertionError) as error:
        bo._check_optimizer_method_bo('DIRECT', 2, 'abc')
    with pytest.raises(AssertionError) as error:
        bo._check_optimizer_method_bo('ABC', 2, True)

def test_choose_fun_acquisition():
    dict_hyps = {'lengthscales': np.array([1.0, 1.0]), 'signal': 1.0, 'noise': 0.01}
    with pytest.raises(AssertionError) as error:
        bo._choose_fun_acquisition(1, dict_hyps)
    with pytest.raises(AssertionError) as error:
        bo._choose_fun_acquisition('abc', dict_hyps)
    with pytest.raises(AssertionError) as error:
        bo._choose_fun_acquisition('pi', 1)

def test_check_hyps_convergence():
    dict_hyps_1 = {'lengthscales': np.array([1.0, 1.0]), 'signal': 1.0, 'noise': 0.01}
    dict_hyps_2 = {'lengthscales': np.array([2.0, 1.0]), 'signal': 1.0, 'noise': 0.01}

    with pytest.raises(AssertionError) as error:
        bo._check_hyps_convergence(1, dict_hyps_1, 'se', True)
    with pytest.raises(AssertionError) as error:
        bo._check_hyps_convergence([dict_hyps_1], 1, 'se', True)
    with pytest.raises(AssertionError) as error:
        bo._check_hyps_convergence([dict_hyps_1], dict_hyps_1, 1, True)
    with pytest.raises(AssertionError) as error:
        bo._check_hyps_convergence([dict_hyps_1], dict_hyps_1, 1, 'abc')
    
    assert bo._check_hyps_convergence([dict_hyps_1], dict_hyps_1, 'se', False)
    assert not bo._check_hyps_convergence([dict_hyps_2], dict_hyps_1, 'se', False)

def test_load_bo():
    # legitimate cases
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    arr_range_2 = np.array([
        [0.0, 10.0],
        [2.0, 2.0],
        [5.0, 5.0],
    ])
    # wrong cases
    arr_range_3 = np.array([
        [20.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    arr_range_4 = np.array([
        [20.0, 10.0],
        [4.0, 2.0],
        [10.0, 5.0],
    ])

    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(np.arange(0, 10))
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_3)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_4)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_cov=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_cov='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_acq=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_acq='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, is_ard='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, is_ard=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, prior_mu=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_optimizer_method_gp=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_optimizer_method_gp='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_optimizer_method_bo=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_optimizer_method_bo='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_modelselection_method=1)
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, str_modelselection_method='abc')
    with pytest.raises(AssertionError) as error:
        model_bo = bo.BO(arr_range_1, debug=1)

    model_bo = bo.BO(arr_range_1)
    model_bo = bo.BO(arr_range_2)

def test_get_initial():
    np.random.seed(42)
    arr_range = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)
    fun_objective = lambda X: np.sum(X)
    model_bo = bo.BO(arr_range)

    with pytest.raises(AssertionError) as error:
        model_bo.get_initial(1)
    with pytest.raises(AssertionError) as error:
        model_bo.get_initial('grid', fun_objective=None)
    with pytest.raises(AssertionError) as error:
        model_bo.get_initial('uniform', fun_objective=1)
    with pytest.raises(AssertionError) as error:
        model_bo.get_initial('uniform', int_samples='abc')
    with pytest.raises(AssertionError) as error:
        model_bo.get_initial('uniform', int_seed='abc')
    with pytest.raises(NotImplementedError) as error:
        model_bo.get_initial('abc')

    arr_initials = model_bo.get_initial('grid', fun_objective=fun_objective)
    truth_arr_initials = np.array([
        [0.0, -2.0, -5.0],
    ])
    assert (np.abs(arr_initials - truth_arr_initials) < TEST_EPSILON).all()

    arr_initials = model_bo.get_initial('sobol', int_samples=3)
    arr_initials = model_bo.get_initial('sobol', int_samples=3, int_seed=42)
    truth_arr_initials = np.array([
        [4.84375, 1.3125, 0.46875],
        [3.59375, -0.1875, -0.78125],
        [8.59375, 1.8125, 4.21875],
    ])
    assert (np.abs(arr_initials - truth_arr_initials) < TEST_EPSILON).all()

    arr_initials = model_bo.get_initial('uniform', int_samples=3, int_seed=42)
    truth_arr_initials = np.array([
        [3.74540119, 1.80285723, 2.31993942],
        [5.98658484, -1.37592544, -3.4400548],
        [0.58083612, 1.46470458, 1.01115012],
    ])
    assert (np.abs(arr_initials - truth_arr_initials) < TEST_EPSILON).all()

def test_optimize():
    np.random.seed(42)
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range_1.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)
    model_bo = bo.BO(arr_range_1)

    with pytest.raises(AssertionError) as error:
        model_bo.optimize(1, Y)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, 1)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(np.random.randn(num_X), Y)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(np.random.randn(num_X, 1), Y)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, np.random.randn(num_X))
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, np.random.randn(num_X, 2))
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, np.random.randn(3, 1))
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, Y, str_initial_method_ao=1)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, Y, str_initial_method_ao='abc')
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, Y, str_mlm_method=1)
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, Y, str_mlm_method='abc')
    with pytest.raises(AssertionError) as error:
        model_bo.optimize(X, Y, int_samples='abc')

    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

def test_optimize_str_acq():
    np.random.seed(42)
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range_1.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)

    model_bo = bo.BO(arr_range_1, str_acq='pi')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    model_bo = bo.BO(arr_range_1, str_acq='ucb')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    model_bo = bo.BO(arr_range_1, str_acq='aei')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    model_bo = bo.BO(arr_range_1, str_acq='pure_exploit')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    model_bo = bo.BO(arr_range_1, str_acq='pure_explore')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

def test_optimize_str_optimize_method_bo():
    np.random.seed(42)
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range_1.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)

    model_bo = bo.BO(arr_range_1, str_optimizer_method_bo='L-BFGS-B')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    # TODO: add DIRECT test, now it causes an error.

    model_bo = bo.BO(arr_range_1, str_optimizer_method_bo='CMA-ES')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

def test_optimize_str_mlm_method():
    np.random.seed(42)
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range_1.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)

    model_bo = bo.BO(arr_range_1)
    next_point, dict_info = model_bo.optimize(X, Y, str_mlm_method='converged')
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

def test_optimize_str_modelselection_method():
    np.random.seed(42)
    arr_range_1 = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range_1.shape[0]
    num_X = 5
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)

    model_bo = bo.BO(arr_range_1, str_modelselection_method='loocv')
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

def test_optimize_is_normalized():
    np.random.seed(42)
    arr_range = np.array([
        [0.0, 10.0],
        [-2.0, 2.0],
        [-5.0, 5.0],
    ])
    dim_X = arr_range.shape[0]
    num_X = 1
    X = np.random.randn(num_X, dim_X)
    Y = np.random.randn(num_X, 1)

    model_bo = bo.BO(arr_range, str_acq='ei', is_normalized=True)
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

    X = np.array([
        [3.0, 0.0, 1.0],
        [2.0, -1.0, 4.0],
        [9.0, 1.5, 3.0],
    ])
    Y = np.array([
        [100.0],
        [100.0],
        [100.0],
    ])

    model_bo = bo.BO(arr_range, str_acq='ei', is_normalized=True)
    next_point, dict_info = model_bo.optimize(X, Y)
    next_points = dict_info['next_points']
    acquisitions = dict_info['acquisitions']
    cov_X_X = dict_info['cov_X_X']
    inv_cov_X_X = dict_info['inv_cov_X_X']
    hyps = dict_info['hyps']
    time_overall = dict_info['time_overall']
    time_gp = dict_info['time_gp']
    time_acq = dict_info['time_acq']

    assert isinstance(next_point, np.ndarray)
    assert isinstance(next_points, np.ndarray)
    assert isinstance(acquisitions, np.ndarray)
    assert isinstance(cov_X_X, np.ndarray)
    assert isinstance(inv_cov_X_X, np.ndarray)
    assert isinstance(hyps, dict)
    assert isinstance(time_overall, float)
    assert isinstance(time_gp, float)
    assert isinstance(time_acq, float)
    assert len(next_point.shape) == 1
    assert len(next_points.shape) == 2
    assert len(acquisitions.shape) == 1
    assert next_point.shape[0] == dim_X
    assert next_points.shape[1] == dim_X
    assert next_points.shape[0] == acquisitions.shape[0]

