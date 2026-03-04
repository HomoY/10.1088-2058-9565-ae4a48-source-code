# Quantifying the advantages of applying quantum approximate algorithms to portfolio optimisation source code
This repository contains the source code required to plot the data presented in:

Yuan, H., Long, C. K., Lepage, H. V. & Barnes, C. H. Quantifying the advantages of applying quantum approximate algorithms to portfolio optimisation. Quantum Science and Technology (2026) doi:http://iopscience.iop.org/article/10.1088/2058-9565/ae4a48.

A Python library is developed for this project and have been packaged. The decision to distribute the library separately was taken to increase the reusability of the code and improve the code quality and robustness by decoupling the modules. The supporting libray to reproduce the data is in

### [Quantum solver to the Global Minimal Variance Portfolio (QGMVP)](https://github.com/HomoY/QGMVP)

**Source code repository:** [https://github.com/HomoY/QGMVP](hhttps://github.com/HomoY/QGMVP)

# How to install
- Clone the repo
- `cd` to the repo folder and run `pip install -r requirements.txt` from the cloned repo under your virtual environment
- `chmod +x fetchdata.sh` and `./fetchdata.sh` to download data from figshare
- You will also need to install [$\LaTeX$](https://www.latex-project.org) to get figures correct.

# Reproducing the figures
Open [figure.ipynb](figure.ipynb) in Jupyter Notebook or VS Code and run the code cells sequentially to reproduce the figures and results.


