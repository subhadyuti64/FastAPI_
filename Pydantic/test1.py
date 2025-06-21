# Type inference in Python is not that great
# def insert_data(name : str,age : int):
#     print("Name: ",name)
#     print("Age: ",age)
#     print("insert_data() called")
    
# insert_data('Subha',21)

# Way to validate type manually
def update_data(name : str,age : int):
    if type(name) != str:
        raise TypeError("Name should be a string")
    if type(age) != int:
        raise TypeError("Age should be an integer")
    print("Name: ",name)
    print("Age: ",age)
    print("Updated")
    
# update_data('Subha',21) # Valid
# update_data('Subha','21') # Invalid


# Pydantic
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Subha', 'Rohit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)] # We didnt write only list but instead used List[str] because we want to validate it that the list should contain a list of String. -> Two level validation
    contact_details: Dict[str, str] # We didnt write only dict but instead used Dict[str,str] because we want to validate it thatthe dict should contain a dict of String and String.->Two level validation


data = {
    'name': "Subha",
    'email': 'subha@gmail.com',
    'linkedin_url':'http://linkedin.com/1322',
    'age': '21',
    'weight': 75.5,
    'contact_details':{
        'phone':'9876543210'
    }
}


patient = Patient(**data)
# print(patient)

def insert_data(patient : Patient):
    print("Name: ",patient.name)
    print("Age: ",patient.age)
    print("Email: ",patient.email)
    print("Married: ",patient.married)
    print("Weight: ",patient.weight)
    print("Allergies: ",patient.allergies)
    print("Contact Details: ",patient.contact_details)
    print("insert_data() called")
    
insert_data(patient)