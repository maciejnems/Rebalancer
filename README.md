# Rebalancer
This repository contains a proof of concept implementation of the Rebalancer protocol. It utilizes the CadCAD framework to simulate the execution of this protocol based on historical data downloaded from Coingecko (can be found in `data` folder).

This is a part of my Master of Science thesis for the Theoretical Computer Science Department of Jagiellonian University

## Requirements
This project supports Python 3.8. Unfortunately, it does not work with any higher version of Python, as CadCAD library is not compatible with them.
Because of that, we recommend the usage of Conda, to prepare a python environment.
To run the project first install Python requirements in the `requirements.txt` file.

So example usage with conda would be:
```
conda create --name rebalancer python=3.8
conda activate rebalancer
conda install --file requirements.txt 
```

## Running simulation
To execute simulations run:
```
python run_simulations.py
```
This by default runs a comparison of `Rebalancer` to `Balancer` on 10 tokens [ltc, eos, bch, xrp, link, dot, trx, doge, ada, usdc].
To run other scenarios, open the file `Rebalancer/simulations/__init__.py`. Next, modify its content to run the simulation you want to. This can be done by uncommented specific lines of code.


## Tests
Simply run
```
pytest
```

## Results
Plots for results of simulation can be found in the `results` folder.