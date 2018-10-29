# PYAGU

Python scripts to build the conference network.

## Files

- `agu_api.py`: python interface for the AGU Open API.
- `build_coefficients.py`: use the abstracts database to find the connection between abstracts. 
Each connection has a weight representing how the two abstracts are correlated.
- `build_graph.py`: build graph files that can be imported into `Gephi`.
- `build_database.py`: generate JSON files containing the database for the web-app.

## Setup Python 3.6

1. From root directory, setup the Python environment using `python3 -m venv pyagu`.
2. `cd pyagu`.
3. `source bin/activate`.
4. `pip install -r requirements.txt`.

## How to build the network

1. Run `build_coefficients.py` to generate a file containing the weights of the network.
2. Run `build_graph.py` to generate a file to import in `Gephi`.
3. For each program, use `Gephi` to generate a `*.gexf` file (check the tutorial folder).

## How to build the database for the web-app

1. Setup output directory in `build_database.py`.
2. Run `build_database.py`.
