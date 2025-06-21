from fastapi import FastAPI,Path,HTTPException,Query
import json 
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