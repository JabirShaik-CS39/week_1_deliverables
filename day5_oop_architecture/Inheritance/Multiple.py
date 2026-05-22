# Multiple Inheritance example in Python
class Camera:    # Parent Class 1
    def take_photo(self):
        return " Photo captured successfully."
class Phone:     # Parent Class 2
    def make_call(self):
        return " Dialing phone number..."
class Smartphone(Camera, Phone):  # Child Class inheriting from BOTH Camera and Phone
    def browse_web(self):
        return " Loading web browser."
my_phone = Smartphone()
print(my_phone.take_photo()) # From Camera
print(my_phone.make_call())  # From Phone
print(my_phone.browse_web()) # From Smartphone