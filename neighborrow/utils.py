import os


def disable_on_production(func):

    def inner():

        if os.environ['FLASK_ENV'] == 'production':
            print('Command not allowed.')
            return False

        func()

    return inner
