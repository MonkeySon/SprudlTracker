class FuelPoint:
    def __init__(self, location, fuelType, price):
        self.location = location
        self.fuelType = fuelType
        self.price = price

    def __str__(self):
        return self.location + ' (' + self.fuelType + '): ' + str(self.price)
    
    def __repr__(self):
        return self.__str__()