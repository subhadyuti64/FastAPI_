from fastapi import FastAPI,Path,HTTPException,Query
import json 
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
app = FastAPI()

@app.get("/")

def hello():
    return {"message": "Patient Management System API"}

@app.get('/about')

def about():
    return {"message": "Fully Functioning API for managing Patient Records"}

# Load Patients from JSON
def get_patient():
    with open('patients.json', 'r') as file:
        data = json.load(file)
        
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# Get All Patients
@app.get('/view')
def view_patient():
    data = get_patient()
    
    return data

# Path Parameters
@app.get('/patient/{patient_id}')  

def get_patient_id(patient_id: str = Path(...,description="ID of the Patient",example="P001")):
    data = get_patient()
    
    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404,detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description="Sort by height,weight or bmi"), order: str = Query('asc',description="Sort in Ascending or Descending order")):
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid field to sort by. Select from {valid_fields}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order. Select 'asc' or 'desc'")
    data = get_patient()
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by],reverse=(order=='desc'))
    return sorted_data

class Patient(BaseModel):
    
    id: Annotated[str,Field(...,description="ID of the Patient",example="P001")]
    name: Annotated[str, Field(...,description="Name of the Patient",example="Subha")]
    city: Annotated[str, Field(...,description="Address of the Patient",example="Puri")]
    age: Annotated[int, Field(...,gt=0,lt=120,description="Age of the Patient",example=25)] 
    gender: Annotated[Literal['male','female','other'],Field(...,description="Gender of the Patient",example="female")]
    height: Annotated[float,Field(...,gt=0,description="Height of the Patient in mtrs",example=165.5)]
    weight: Annotated[float,Field(...,gt=0,description="Weight of the Patient in kg",example=70.5)]

    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
        
@app.post('/create')

def create_patient(patient: Patient):
    data = get_patient()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})



class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]




@app.put('/edit')

def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = get_patient()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient = data[patient_id]
    
    updated_patient = patient_update.model_dump(exclude_unset=True)
    
    for key, value in updated_patient.items():
        existing_patient[key] = value
        
    existing_patient['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient)
    