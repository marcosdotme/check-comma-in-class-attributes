class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name,
        self.age = age

    def greet(self) -> None:
        print(f"Hi, my name is {self.name} and I'm {self.age} years old!")
