from typing import List, Tuple

import numpy as np
from openmm import unit

from ._libg96 import G96Mol


class G96Reporter:
    """G96Reporter outputs a series of frames from a Simulation to a G96 file.

    To use it, create a G96Reporter, then add it to the Simulation's list of
    reporters.
    """

    def __init__(
        self,
        file: str,
        reportInterval: int,
        enforcePeriodicBox: bool = None,
        atomSubset: List[int] = None,
    ) -> None:
        self._reportInterval = reportInterval
        self._out = open(file, "w")
        self._enforcePeriodicBox = enforcePeriodicBox
        self._atomSubset = atomSubset

        # not implemented
        if self._enforcePeriodicBox:
            raise NotImplementedError()

        if self._atomSubset:
            raise NotImplementedError()

    def describeNextReport(
        self,
        simulation,
    ) -> Tuple[int, bool, bool, bool, bool]:
        """Generate a report.

        Args:
            simulation (Simulation): The Simulation to generate a report for.
            state (State): The current state of the simulation.
        """

        steps = self._reportInterval \
            - simulation.currentStep % self._reportInterval

        return (steps, True, False, False, False, self._enforcePeriodicBox)

    def report(
        self,
        simulation,
        state,
    ) -> None:
        """Generate a report.

        Args:
            simulation (Simulation): The Simulation to generate a report for.
            state (State): The current state of the simulation.
        """

        state = simulation.context.getState(
            getPositions=True,
            getVelocities=True,
        )

        g96mol = G96Mol(
            title="",
            timestep=(
                simulation.context.getStepCount(),
                state.getTime().value_in_unit(unit.picosecond),
            ),
            position=state.getPositions(
                asNumpy=True).value_in_unit(unit.nanometer),
            velocity=state.getVelocities(asNumpy=True).value_in_unit(
                unit.nanometer / unit.picosecond),
            box_vectors=np.diag(state.getPeriodicBoxVectors(
                asNumpy=True).value_in_unit(unit.nanometer)),
        )

        self._out.write(str(g96mol))

    def __del__(
        self,
    ) -> None:
        self._out.close()
