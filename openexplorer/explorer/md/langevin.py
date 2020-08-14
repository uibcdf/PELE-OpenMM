import simtk.unit as u
from simtk.unit import Quantity
from simtk.openmm import LangevinIntegrator

class Langevin():

    _explorer = None
    _initialized = False
    _context = None
    _integrator = None

    _timestep = Quantity(value=2.0, unit=u.femtosecond)
    _temperature = Quantity(value=298.0, unit=u.kelvin)
    _collision_rate = Quantity(value=1.0, unit=/u.picosecond)

    def __init__(self, explorer):

        self._explorer=explorer

    def _initialize():

        system = self._explorer.context.getSystem()
        platform = self._explorer.context.getPlatform()
        if platform.getName()=='CUDA':
            properties['CudaPrecision'] = 'mixed'

        self._integrator = LangevinIntegrator(self._temperature, self._collision_rate, self._timestep)
        self._context = Context(system, self._integrator, platform, properties)
        self._initialized = True

    def set_parameters(self, temperature=Quantity(value=298.0, unit=u.kelvin), collision_rate=Quantity(value=1.0, unit=/u.picosecond)
            timestep=Quantity(value=2.0, unit=u.femtosecond)):

        self._timestep = timestep
        self._temperature = temperature
        self._collision_rate = collision_rate

        self._integrator.setFriction(self._collision_rate.value_in_unit(/u.picosecond))
        self._integrator.setTemperature(self._temperature.value_in_unit(u.kelvin))
        self._integrator.setStepSize(self._timestep.value_in_unit(u.picoseconds))

    def _set_coordinates(self, coordinates):

        self._context.setPositions(coordinates)

    def _get_coordinates(self):

        return self._context.getState(getPositions=True).getPositions(asNumpy=True)

    def _coordinates_to_explorer(self):

        self._explorer.set_coordinates(self._get_coordinates())

    def _coordinates_from_explorer(self):

        self._set_coordinates(self._explorer.get_coordinates())

    def run(self, steps=0):

        if not self._initialized:

            self._initialize()

        self._coordinates_from_explorer()
        self._integrator.step(steps)
        self._coordinates_to_explorer()

    def __call__(self, *args, **kwargs):

        return self.run(*args, **kwargs)
