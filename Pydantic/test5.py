from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'Rourkela', 'state': 'Odisha', 'pin': '769008'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Subha', 'gender': 'male', 'age': 21, 'address': address1}

patient1 = Patient(**patient_dict)
# print("Name: ",patient1.name)
# print("Age: ",patient1.age)
# print("Gender: ", patient1.gender)
# print("City: ", patient1.address.city)
# print("State: ", patient1.address.state)
# print("Pincode: ",patient1.address.pin)

# Serialisation
temp = patient1.model_dump() # Export as Dictionary
print(temp)
print(type(temp))


temp2 = patient1.model_dump_json() # Export as JSON
print(temp2)
print(type(temp))


# print(temp['name'])
# print(temp['gender'])
# print(temp['age'])
# print(temp['address'])




