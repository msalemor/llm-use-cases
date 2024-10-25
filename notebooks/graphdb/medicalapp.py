from contextlib import asynccontextmanager
import os
from neo4j import GraphDatabase, Record
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from dotenv import load_dotenv

load_dotenv()

# Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
    print("Please set NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD environment variables")
    exit(1)

# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def add_sample_data():
    sample_patients = [
        Patient(patient_id="1", name="John Doe", age=30, gender="Male"),
        Patient(patient_id="2", name="Jane Smith", age=25, gender="Female")
    ]
    sample_records = [
        PatientRecord(patient_id="1", record_type="EHR",
                      details="General check-up"),
        PatientRecord(patient_id="1", record_type="Lab",
                      details="Blood test results"),
        PatientRecord(patient_id="2", record_type="Imaging",
                      details="X-ray results")
    ]
    for patient in sample_patients:
        add_patient(patient)
    for record in sample_records:
        add_record(record)

    # print(get_patient_records("1"))
    # print(find_patients_by_gender_and_record_type("Male", "Lab"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("Starting app")
    add_sample_data()
    yield
    # Clean up the ML models and release the resources
    print("Shutting down app")
    driver.close()


app = FastAPI(lifespan=lifespan)


# Pydantic models
class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str


class PatientRecord(BaseModel):
    patient_id: str
    record_type: str
    details: str

# Helper function to execute Neo4j queries


def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return result

# Endpoint to add a patient


@app.post("/patients/")
def add_patient(patient: Patient):
    query = """
    MERGE (p:Patient {patient_id: $patient_id})
    SET p.name = $name, p.age = $age, p.gender = $gender
    """
    parameters = patient
    execute_query(query, parameters)
    return {"message": "Patient added successfully"}

# Endpoint to add a record


@app.post("/records/")
def add_record(record: PatientRecord):
    query = """
    MATCH (p:Patient {patient_id: $patient_id})
    CREATE (p)-[:HAS_RECORD]->(r:Record {record_type: $record_type, details: $details})
    """
    parameters = record
    execute_query(query, parameters)
    return {"message": "Record added successfully"}

# Endpoint to get a patient's records


@app.get("/patients/{patient_id}/records/")
def get_patient_records(patient_id: str):
    with driver.session() as session:
        query = """
        MATCH (p:Patient {patient_id: $patient_id})-[:HAS_RECORD]->(r:Record)
        RETURN p, collect(r) as records
        """
        parameters = {"patient_id": patient_id}
        # result = execute_query(query, parameters)
        result = session.run(query, parameters)
        records = []
        for record in result:
            patient = record["p"]
            records = record["records"]
        if not records:
            raise HTTPException(
                status_code=404, detail="Patient not found or no records available")
        return {"patient": dict(patient), "records": [dict(r) for r in records]}

# Sample data for querying


@app.get("/patients/{gender}/records/{record_type}")
def find_patients_by_gender_and_record_type(gender: str, record_type: str):
    with driver.session() as session:
        query = """
        MATCH (p:Patient {gender: $gender})-[:HAS_RECORD]->(r:Record {record_type: $record_type})
        RETURN p, collect(r) as records
        """
        parameters = {"gender": gender, "record_type": record_type}
        result = session.run(query, parameters)
        patients = []
        for record in result:
            patient = record["p"]
            records = record["records"]
            patients.append({"patient": dict(patient), "records": [
                            dict(r) for r in records]})
        if not patients:
            raise HTTPException(
                status_code=404, detail="No patients found with the given gender and record type")
        return patients


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
