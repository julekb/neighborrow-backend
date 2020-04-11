import os
from random import uniform, randrange

from ..models import User, Item, Location

from faker import Faker

f = Faker('pl_PL')


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
    def __init__(self, *args, **kwargs):
        """
        Factories are not allowed on production server.
        """
        if os.environ['FLASK_ENV'] == 'production':
            raise
        super(ModelFactory, self).__init__(*args, **kwargs)

    def generate(self, **kwargs):
        for arg, generator in self.generators.items():
            if arg not in kwargs:
                kwargs[arg] = generator()
        return self.model(**kwargs)


coords_gen = CoordsGenerator(WWA_coords, 1)


class UserFactory(ModelFactory):
    model = User

    generators = {
        'first_name': f.first_name,
        'last_name': f.last_name,
        'password': f.password,
        'email': f.email,
        'phone': lambda: randrange(100000000, 999999999)
    }


class ItemFactory(ModelFactory):
    model = Item

    generators = {
        'name': f.word,
        'description': f.text,
        'price': lambda: randrange(200)
    }


class LocationFactory(ModelFactory):
    model = Location

    generators = {
        'address': f.address,
        'lat': coords_gen.generate_lat,
        'lon': coords_gen.generate_lon
    }
