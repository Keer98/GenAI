from abc import ABC, abstractmethod

# Base class (Data Abstraction and Inheritance)
class Vehicle(ABC):
    def __init__(self, make, model, fuel_capacity):
        self.make = make
        self.model = model
        self.fuel_capacity = fuel_capacity
        self.__fuel_level = 0  # Private variable
        self.speed = 0

    @abstractmethod
    def accelerate(self):
        pass

    # Getter for fuel_level
    def get_fuel_level(self):
        return self.__fuel_level

    # Setter for fuel_level
    def set_fuel_level(self, fuel_amount):
        if fuel_amount <= self.fuel_capacity:
            self.__fuel_level = fuel_amount
        else:
            print(f"Cannot set fuel level beyond capacity of {self.fuel_capacity} liters.")

    def refuel(self, fuel_amount):
        """Common method for refueling vehicles"""
        if fuel_amount <= (self.fuel_capacity - self.__fuel_level):
            self.__fuel_level += fuel_amount
            print(f"{self.make} {self.model} refueled with {fuel_amount} liters.")
        else:
            print(f"Cannot overfill the fuel tank. Max capacity is {self.fuel_capacity} liters.")

    @abstractmethod
    def get_fuel_efficiency(self):
        """Abstract method for calculating fuel efficiency"""
        pass

# Derived class for Car (Inheritance, Polymorphism)
class Car(Vehicle):
    def __init__(self, make, model, fuel_capacity, seating_capacity):
        super().__init__(make, model, fuel_capacity)
        self.seating_capacity = seating_capacity

    def accelerate(self):
        """Specific behavior for accelerating a car"""
        self.speed += 10
        print(f"{self.make} {self.model} car accelerates to {self.speed} km/h.")

    def get_fuel_efficiency(self):
        """Fuel efficiency specific to cars"""
        return f"Fuel efficiency: {12} km/l for {self.make} {self.model} car."

# Derived class for Truck (Inheritance, Polymorphism)
class Truck(Vehicle):
    def __init__(self, make, model, fuel_capacity, cargo_capacity):
        super().__init__(make, model, fuel_capacity)
        self.cargo_capacity = cargo_capacity

    def accelerate(self):
        """Specific behavior for accelerating a truck"""
        self.speed += 5
        print(f"{self.make} {self.model} truck accelerates to {self.speed} km/h.")

    def get_fuel_efficiency(self):
        """Fuel efficiency specific to trucks"""
        return f"Fuel efficiency: {8} km/l for {self.make} {self.model} truck."

# Derived class for Motorcycle (Inheritance, Polymorphism)
class Motorcycle(Vehicle):
    def __init__(self, make, model, fuel_capacity):
        super().__init__(make, model, fuel_capacity)

    def accelerate(self):
        """Specific behavior for accelerating a motorcycle"""
        self.speed += 20
        print(f"{self.make} {self.model} motorcycle accelerates to {self.speed} km/h.")

    def get_fuel_efficiency(self):
        """Fuel efficiency specific to motorcycles"""
        return f"Fuel efficiency: {30} km/l for {self.make} {self.model} motorcycle."

# Encapsulation
def vehicle_info(vehicle):
    """Function that takes any vehicle and prints basic info (Polymorphism)"""
    print(f"Make: {vehicle.make}, Model: {vehicle.model}, Speed: {vehicle.speed} km/h")
    print(f"Fuel Level: {vehicle.get_fuel_level()} liters")  # Access private variable via getter
    print(vehicle.get_fuel_efficiency())

# Usage of the system
car = Car("Toyota", "Camry", 50, 5)
truck = Truck("Volvo", "FH16", 300, 10000)
motorcycle = Motorcycle("Yamaha", "MT-07", 15)

# Refuel all vehicles
car.refuel(30)
truck.refuel(150)
motorcycle.refuel(10)

# Accelerate vehicles
car.accelerate()
truck.accelerate()
motorcycle.accelerate()

# Print information of vehicles
vehicle_info(car)
vehicle_info(truck)
vehicle_info(motorcycle)
