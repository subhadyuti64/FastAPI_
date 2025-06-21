from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model


data = {
    'name': "Subha",
    'email': 'subha@gmail.com',
    'linkedin_url':'http://linkedin.com/1322',
    'age': '67',
    'weight': 75.5,
    "married" : False,
    'allergies': ['eggs', 'milk'],
    'contact_details':{
        'phone':'9876543210',
        'emergency':'9876543211'
    }
}


def insert_data(patient : Patient):
    print("Name: ",patient.name)
    print("Age: ",patient.age)
    print("Email: ",patient.email)
    print("Married: ",patient.married)
    print("Weight: ",patient.weight)
    print("Allergies: ",patient.allergies)
    print("Contact Details: ",patient.contact_details)
    print("insert_data() called")
    

patient = Patient(**data)
insert_data(patient)
