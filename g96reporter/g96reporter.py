import glob
import os
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

        return (steps, True, True, False, False, self._enforcePeriodicBox)

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
        pass


class G96RPMDReporter:
    """G96RPMDReporter outputs a series of frames of each bead from a
    Simulation to several G96 files.

    To use it, make sure you are using the RPMDIntegrator, thencreate a
    G96RPMDReporter, then add it to the Simulation's list of reporters.
    """

    def __init__(
        self,
        file: str,
        reportInterval: int,
        enforcePeriodicBox: bool = None,
        atomSubset: List[int] = None,
    ) -> None:
        self._reportInterval = reportInterval
        self._file = file
        self._enforcePeriodicBox = enforcePeriodicBox
        self._atomSubset = atomSubset

        # not implemented
        if self._enforcePeriodicBox:
            raise NotImplementedError()

        if self._atomSubset:
            raise NotImplementedError()

        self._out_list = []

        for old_file in glob.glob(self._file.replace('.g96', '_*.g96')):
            os.remove(old_file)

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

        return (steps, False, False, False, False, self._enforcePeriodicBox)

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

        num_copies = simulation.integrator.getNumCopies()

        if len(self._out_list) == 0:
            for copy_idx in range(num_copies):
                out_file = self._file.replace(".g96", f"_{copy_idx}.g96")
                self._out_list.append(open(out_file, "w"))

        for copy_idx in range(num_copies):
            state = simulation.integrator.getState(
                copy_idx,
                getPositions=True,
                getVelocities=True,
            )

            g96mol = G96Mol(
                title=f"copy {copy_idx}",
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

            self._out_list[copy_idx].write(str(g96mol))

    def __del__(
        self,
    ) -> None:
        for out in self._out_list:
            out.close()
