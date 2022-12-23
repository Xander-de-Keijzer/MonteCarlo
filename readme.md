Mersenne Twister, Part 1, and Part 2
====================================

This project contains three classes: `MersenneTwister`, `Part1`, and `Part2`. The `MersenneTwister` class is a implementation of the [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) random number generator, which is a fast and high-quality pseudo-random number generator (PRNG). The `Part1` and `Part2` classes use the `MersenneTwister` class to simulate the results of a football (soccer) league.

MersenneTwister
---------------

The `MersenneTwister` class has the following `__init__` function:

### `__init__(self, seed: int=0, **kwargs) -> None`

Initialize a `MersenneTwister` instance with the given seed value and optional parameters.

Parameters:

*   `seed`: The seed value for the PRNG. Default is 0.
*   `kwargs`: Additional parameters for the PRNG. The allowed parameters are `w`, `r`, `n`, `m`, `a`, `b`, `c`, `d`, `f`, `u`, `l`, `s`, and `t`. These parameters must be integers.

Part1
-----

The `Part1` class has the following `__init__` function:

### `__init__(self, sims: int=10_000) -> None`

Initialize a `Part1` instance for simulating a football league.

Parameters:

*   `sims`: The number of simulations to run. Default is 10,000.

Part2
-----

The `Part2` class has the following `__init__` function:

### `__init__(self, sims: int=10_000, goal_sims: int=10) -> None`

Initialize a `Part2` instance for simulating a football league.

Parameters:

*   `sims`: The number of simulations to run. Default is 10,000.
*   `goal_sims`: The number of goal simulations to run for each match. Default is 10.