from sys import stdout

from openmm import *
from openmm.app import *
from openmm.unit import *

from g96reporter import G96Reporter, G96RPMDReporter

print('------------------------------------------')
print(' PIMD simulation of q-TIP4P/F water model ')
print('------------------------------------------')

pdb = PDBFile('qtip4pf.pdb')

forcefield = ForceField('qtip4pf.xml')

system = forcefield.createSystem(
    pdb.topology,
    nonbondedMethod=PME,
    nonbondedCutoff=1.0 * nanometer,
    constraints=None,
    rigidWater=False,
)

integrator = RPMDIntegrator(8, 300 * kelvin, 1.0 / picosecond, 0.0005 * picoseconds)

simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

simulation.reporters.append(G96Reporter("traj_centroid.g96", 100))
simulation.reporters.append(G96RPMDReporter("traj_bead.g96", 100))

simulation.reporters.append(StateDataReporter(
    stdout,
    1000,
    time=True,
    potentialEnergy=True,
    kineticEnergy=True,
    totalEnergy=True,
    temperature=True,
    density=True,
))

print('Starting simulation')

simulation.step(20000)

print('Finished Simulation')
