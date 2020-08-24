About bayeso
############

Simple, but essential Bayesian optimization package.
It is designed to run advanced Bayesian optimization with implementation-specific and application-specific modifications as well as to run Bayesian optimization in various applications simply.
This package contains the codes for Gaussian process regression and Gaussian process-based Bayesian optimization.
Some famous benchmark and custom benchmark functions for Bayesian optimization are included in `bayeso-benchmarks <https://github.com/jungtaekkim/bayeso-benchmarks>`_, which can be used to test the Bayesian optimization strategy. If you are interested in this package, please refer to that repository.

Supported Python Version
========================

We test our package in the following versions.

- Python 2.7 (It will be excluded due to the maintenance schedule for Python 2.7, but it is currently tested.)
- Python 3.6
- Python 3.7
- Python 3.8

Related Package for Benchmark Functions
=======================================

The related package **bayeso-benchmarks**, which contains some famous benchmark functions and custom benchmark functions is hosted in `this repository <https://github.com/jungtaekkim/bayeso-benchmarks>`_. It can be used to test a Bayesian optimization strategy.

The details of benchmark functions implemented in **bayeso-benchmarks** are described in `these notes <https://jungtaek.github.io/notes/benchmarks_bo.pdf>`_.

Contributor
===========

- `Jungtaek Kim <http://mlg.postech.ac.kr/~jtkim/>`_ (POSTECH)

Citation
========

.. code-block:: latex

    @misc{KimJ2017bayeso,
        author={Kim, Jungtaek and Choi, Seungjin},
        title={{bayeso}: A {Bayesian} optimization framework in {Python}},
        howpublished={\url{http://bayeso.org}},
        year={2017}
    }

Contact
=======

- Jungtaek Kim: `jtkim@postech.ac.kr <mailto:jtkim@postech.ac.kr>`_

License
=======

`MIT License <https://github.com/jungtaekkim/bayeso/blob/master/LICENSE>`_

