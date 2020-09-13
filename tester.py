import sys

def str_to_class(str):
    return getattr(sys.modules[__name__], str)


class First:
    def __init__(self):
        self.__class__ == 'First'

    @staticmethod
    def print_method():
        print("First PRINTER METHOD!")

class Second:
    def __init__(self):
        self.__class__ == 'Second'

    @staticmethod
    def print_method():
        print("Second PRINTER METHOD!")



def func(class_name):
    str_to_class(class_name).print_method()



func('First')
func('Second')

