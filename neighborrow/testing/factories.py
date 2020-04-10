from random import uniform

from ..models import Location

from faker import Faker

faker = Faker()


WWA_coords = (52.237049, 21.017532)


class CoordsGenerator:
    def __init__(self, coords, dev):
        self.coords = coords
        self.dev = dev

    def generate_lat(self):
        return self.coords[0] + uniform(-1, 1)

    def generate_lon(self):
        return self.coords[1] + uniform(-1, 1)


class ModelFactory:

    def generate(self, **kwargs):
        for arg, generator in self.generators.items():
            if arg not in kwargs:
                kwargs[arg] = generator()
        return self.model(**kwargs)


coords_gen = CoordsGenerator(WWA_coords, 1)


class LocationFactory(ModelFactory):
    model = Location

    generators = {
        'address': faker.address,
        'lat': coords_gen.generate_lat,
        'lon': coords_gen.generate_lon
    }
