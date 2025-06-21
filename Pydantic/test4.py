from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi



data = {
    'name': "Subha",
    'email': 'subha@gmail.com',
    'age': 21,
    'height': 1.7,
    'weight': 75.5,
    'married' : False,
    'allergies': ['egg','milk'],
    'contact_details':{
        'phone':'9876543210'
    }
}


def insert_data(patient : Patient):
    print("Name: ",patient.name)
    print("Age: ",patient.age)
    print("Email: ",patient.email)
    print("Married: ",patient.married)
    print("Weight: ",patient.weight)
    print('BMI', patient.bmi)
    print("Allergies: ",patient.allergies)
    print("Contact Details: ",patient.contact_details)
    print("insert_data() called")
    

patient = Patient(**data)
insert_data(patient)

