# openmm-g96-reporter

G96 format based reporter for OpenMM

## Installation

Pip

```
$ pip install git+https://github.com/mizu-bai/openmm-g96-reporter
```

From source

```
$ git clone https://github.com/mizu-bai/openmm-g96-reporter.git
$ cd openmm-g96-reporter
$ pip install .
```

## Usage

```python
from g96reporter import G96Reporter

simulation.reporters.append(G96Reporter("traj.g96", 1000))
```

Then the `traj.g96` trajectory can be converted to `trr` and `xtc` format:

```
$ gmx -f traj.g96 -o traj.trr
$ gmx -f traj.g96 -o traj.xtc
```

## Example

Here is an example in folder `examples`, in which `G96Reporter` was used instead of `PDBReporter`.

## License

BSD-2-Clause license
