from __future__ import division

import os

from nose.tools import raises, with_setup
from numpy.testing import assert_equal, assert_allclose

import numpy as np

from ..util import read_param_file, scale_samples, unscale_samples, \
                   compute_groups_from_parameter_file


def setup_function():
    filename = "SALib/tests/test_params.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test1 0.0 100.0\n")
         ofile.write("Test2 5.0 51.0\n")


def setup_csv_param_file_with_whitespace_in_names():
    filename = "SALib/tests/test_params_csv_whitespace.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test 1,0.0,100.0\n")
         ofile.write("Test 2,5.0,51.0\n")


def setup_tab_param_file_with_whitespace_in_names():
    filename = "SALib/tests/test_params_tab_whitespace.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test 1\t0.0\t100.0\n")
         ofile.write("Test 2\t5.0\t51.0\n")


def setup_csv_param_file_with_whitespace_in_names_comments():
    filename = "SALib/tests/test_params_csv_whitespace_comments.txt"
    with open(filename, "w") as ofile:
         ofile.write("# Here is a comment\n")
         ofile.write("'Test 1',0.0,100.0\n")
         ofile.write("'Test 2',5.0,51.0\n")


def teardown():
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".txt")]
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".csv")]
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".tab")]


@with_setup(setup_function, teardown)
def test_readfile():
    '''
    Tests a standard parameter file is read correctly
    '''

    filename = "SALib/tests/test_params.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test1', 'Test2'])


@with_setup(setup_csv_param_file_with_whitespace_in_names, teardown)
def test_csv_readfile_with_whitespace():
    '''
    A comma delimited parameter file with whitespace in the names
    '''

    filename = "SALib/tests/test_params_csv_whitespace.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_tab_param_file_with_whitespace_in_names, teardown)
def test_tab_readfile_with_whitespace():
    '''
    A tab delimited parameter file with whitespace in the names
    '''

    filename = "SALib/tests/test_params_tab_whitespace.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_csv_param_file_with_whitespace_in_names_comments, teardown)
def test_csv_readfile_with_comments():
    '''
    '''

    filename = "SALib/tests/test_params_csv_whitespace_comments.txt"

    pf = read_param_file(filename)

    print(pf['bounds'], pf['num_vars'], pf['names'])

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


# Test scale samples
def test_scale_samples():
    '''
    Simple test to ensure that samples are correctly scaled
    '''

    params = np.arange(0, 1.1, 0.1).repeat(2).reshape((11, 2))

    bounds = [[10, 20], [-10, 10]]

    desired = np.array([np.arange(10, 21, 1), np.arange(-10, 12, 2)], dtype=np.float).T
    scale_samples(params, bounds)
    assert_allclose(params, desired, atol=1e-03, rtol=1e-03)

def test_unscale_samples():
    '''
    Simple test to unscale samples back to [0,1] range
    '''
    params = np.array([np.arange(10, 21, 1), np.arange(-10, 12, 2)], dtype=np.float).T
    bounds = [[10, 20], [-10, 10]]

    desired = np.arange(0, 1.1, 0.1).repeat(2).reshape((11, 2))
    unscale_samples(params, bounds)
    assert_allclose(params, desired, atol=1e-03, rtol=1e-03)


@raises(ValueError)
def test_scale_samples_upper_lt_lower():
    '''
    Raise ValueError if upper bound lower than lower bound
    '''
    params = np.array([[0, 0], [0.1, 0.1], [0.2, 0.2]])
    bounds = [[10, 9], [-10, 10]]
    scale_samples(params, bounds)


@raises(ValueError)
def test_scale_samples_upper_eq_lower():
    '''
    Raise ValueError if upper bound lower equal to lower bound
    '''
    params = np.array([[0, 0], [0.1, 0.1], [0.2, 0.2]])
    bounds = [[10, 10], [-10, 10]]
    scale_samples(params, bounds)


def test_compute_groups_from_parameter_file():
    '''
    Tests that a group file is read correctly
    '''
    actual_matrix, actual_unique_names = \
        compute_groups_from_parameter_file(['Group 1', 'Group 2', 'Group 2'], 3)

    assert_equal(actual_matrix, np.matrix('1,0;0,1;0,1', dtype=np.int))
    assert_equal(actual_unique_names, ['Group 1', 'Group 2'])
