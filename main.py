class my_staticmethod:
    ...


class Dog:
    @staticmethod
    def bark():
        print("Bark")

    @my_staticmethod
    def my_bark():
        print("Bark")
