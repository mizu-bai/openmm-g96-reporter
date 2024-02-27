from sys import stdout

from openmm import *
from openmm.app import *
from openmm.unit import *

from g96reporter import G96Reporter

pdb = PDBFile('input.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
system = forcefield.createSystem(
    pdb.topology,
    nonbondedMethod=PME,
    nonbondedCutoff=1 * nanometer,
    constraints=HBonds
)
integrator = LangevinMiddleIntegrator(
    300 * kelvin,
    1 / picosecond,
    0.004 * picoseconds
)
simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)
simulation.minimizeEnergy()
# simulation.reporters.append(PDBReporter('output.pdb', 1000))
simulation.reporters.append(G96Reporter("output.g96", 1000))
simulation.reporters.append(StateDataReporter(
    stdout,
    1000,
    step=True,
    potentialEnergy=True,
    temperature=True,
))
simulation.step(10000)
