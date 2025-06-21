from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')



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
