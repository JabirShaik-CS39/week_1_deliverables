# The Class & Objects 
class SmartDevice:
    def __init__(self, name, brand):
        self.name = name    
        self.brand = brand  
    def status(self):
        return f"{self.name} by {self.brand} is online."
device_one = SmartDevice("Echo Dot", "Amazon")
device_two = SmartDevice("Nest Thermostat", "Google")
print(device_one.status())
print(device_two.status())



# Inheritance
class SmartDevice:
    def __init__(self, name):
        self.name = name
class Speaker(SmartDevice):  # Child Class inherits from SmartDevice
    def play_music(self):
        return f"🔊 {self.name} is now playing your favorite playlist."
my_speaker = Speaker("Living Room Speaker")  # Instantiating the child class
print(my_speaker.name)  # It has access to 'name' (inherited) and 'play_music' (its own)
print(my_speaker.play_music())



# Encapsulation
class Speaker:
    def __init__(self, name, volume=20):
        self.name = name
        self.__volume = volume  # Private attribute (hidden)
    def get_volume(self):       # Getter Method (Safe reading)
        return self.__volume
    def set_volume(self, value):     # Setter Method (Safe modifying with guardrails)
        if 0 <= value <= 100:
            self.__volume = value
            return f"Volume set to {self.__volume}%"
        else:
            return "❌ Access Denied: Volume must be between 0 and 100."
my_speaker = Speaker("Smart Speaker") # Object Creation
print(f"Initial Volume: {my_speaker.get_volume()}%") # Direct access fails: print(my_speaker.__volume) will throw an error
print(my_speaker.set_volume(50))   # Changes successfully
print(my_speaker.set_volume(120))  # Blocked by validation


# Polymorphism
class Speaker:
    def turn_on(self):
        return "🔊 Speaker chimes: 'Connected to network.'"
class Thermostat:
    def turn_on(self):
        return "🌡️ Thermostat clicks: Display screen activated."
living_room_speaker = Speaker() # Two completely different classes
hallway_thermostat = Thermostat()
device_list = [living_room_speaker, hallway_thermostat] # A unified list containing different objects
for device in device_list:  # The exact same method call yields completely different actions
    print(device.turn_on())



# Abstraction
from abc import ABC, abstractmethod
class SmartDevice(ABC):
    @abstractmethod
    def reboot(self):
        """Every child class MUST write its own reboot logic."""
        pass
class SmartLight(SmartDevice):
    # If we don't define 'reboot', this class will crash too.
    def reboot(self):
        return "💡 Light bulb flashes yellow while restarting firmware..."
my_light = SmartLight()
print(my_light.reboot())
