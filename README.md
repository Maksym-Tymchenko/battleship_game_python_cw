# Battleship Game Python Coursework

## Context

This is a coursework assignment that I completed as part of my Python module in my MSc Artificial Intelligence. The details of the coursework are described in <em>description.pdf</em>. My contribution consisted in completing some of the classes in the existing project structure described below in order to create a battleship game that has manual, automatic and AI mode.

You can play the game against an AI player by cloning the repository and running `python3 main.py 2`.

## Project Structure

```
Project folder/
├─ battleship/
│  ├─ board.py
│  ├─ convert.py
│  ├─ game.py
│  ├─ player.py
│  ├─ ship.py
│  ├─ simulation.py
├─ tests/
│  ├─ test_board.py
│  ├─ test_player.py
│  ├─ test_ship.py
│  ├─ test_shipfactory.py
├─ main.py
```


### `battleship/`

- `board.py` contains the `Board` class (Task 2).

- `convert.py` contains some utility methods to convert between a string representation of a cell (e.g. `"B1"`) and its $(x,y)$ coordinate equivalent (e.g. `(2,1)`). **Do not edit this file**. There is no need to understand the content of this file. 

- `game.py` contains the logic that allows you to play and visualise the game (and implicitly for you to analyse the output). **Do not edit this file**. There is no need to understand the content of this file (although you might find it helpful for understanding how the classes work).

- `player.py` contains the `Player`, `ManualPlayer`, and `RandomPlayer` classes, and also the skeleton for the `AutomaticPlayer` class (Task 4). **Do not edit `Player`, `ManualPlayer`, and `RandomPlayer`**.

- `ship.py` contains the `Ship` class (Task 1) and the `ShipFactory` class (Task 3).

- `simulation.py` contains classes for running different kinds of games. You are welcome to edit the files here, although it will not be assessed.
 


### `tests/`

Contains an example test case for each of the four tasks.

- `test_board.py`
- `test_player.py`
- `test_ship.py`
- `test_shipfactory.py`

You can run the test via `python3 -m tests.test_board` (and similarly for the other tests).


### `main.py`

Allows you to run a simulation of a battleship game.

Running `python3 main.py` or `python3 main.py 0` will give you a manual game between two humans.

Running `python3 main.py 1` will give you a manual game between a human and a `RandomPlayer`.

etc.

See the file for more information about the type of games you can run. You may freely edit this file - it will not be assessed.
