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

`G96Reporter`

```python
from g96reporter import G96Reporter

simulation.reporters.append(G96Reporter("traj.g96", 1000))
```

Then the `traj.g96` trajectory can be converted to `trr` and `xtc` format:

```
$ gmx -f traj.g96 -o traj.trr
$ gmx -f traj.g96 -o traj.xtc
```

`G96RPMDReporter`

```python
from g96reporter import G96Reporter, G96RPMDReporter

simulation.reporters.append(G96Reporter("traj_centroid.g96", 100))
simulation.reporters.append(G96RPMDReporter("traj_bead.g96", 100))
```

## Example

See folder `examples/`.

## License

BSD-2-Clause license
