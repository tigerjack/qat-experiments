# qat-experiments
A collection of experiments using the open source [Atos
myQLM](https://myqlm.github.io/ "myqlm") or [Atos
QLM](https://atos.net/en/solutions/quantum-learning-machine "qlm")

The code here can be run on the open-source [myQLM
simulator](https://github.com/myQLM). Support for the [QLM
simulator](https://atos.net/en/solutions/quantum-learning-machine) is planned.

# Installation #
If you would like to test the code and you do not have access to a QLM, you can
install the open source
[myQLM](https://myqlm.github.io/myqlm_specific/install.html).

The best way to install the code would be through
[pyenv](https://github.com/pyenv/pyenv) and the
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv). Refer to their
guides on how to install them. After both of them are installed, you can run.

```
pyenv install 3.9.10 # install python version 3.9.10
pyenv virtualenv 3.9.10 myqlm_env # create a virtual environment with that python version
```

where `3.9.10` is the python version used for this code and `myqlm_env` is the
name of the virtual environment (you can change whatever name you like). You can
also try other python version, but be sure they are available on myQLM website
[documentation](https://myqlm.github.io/myqlm_specific/install.html).

Then, you can install myQLM inside the environment by launching

```
pyenv activate myqlm_env
pip install myqlm
```

If you want to use `jupyter notebook`s, you should also execute

```
pip install jupyter
```

Then, you can clone this repository and activate the environment.

```
cd <SOME_DIR>
git clone https://github.com/tigerjack/qat-experiments.git
cd qat-experiments
pyenv activate myqlm_env
```

where `<SOME_DIR>` can be whatever directory you want this repository to be
contained in.


# Use the code #


# Contribution Guidelines #
If you would like to contribute to the code, please open a [GitHub
issue](https://github.com/tigerjack/qat-utils/issues). You can learn all the
details of myQLM by following the documentation freely available at
[https://myqlm.github.io/](https://myqlm.github.io/). You can also ask for help
on the official [slack channel](https://myqlmworkspace.slack.com/).


# To implement list #
  * Algorithms
    * [ ] Simon
    * [x] Deutsch-Jozsa
    * [x] Bernstein-Vazirani
    * [x] Grover
    * [x] Quantum teleportation

