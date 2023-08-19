from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import List
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

class HealthDiagnosisAssistant:
    def __init__(self):
        """Initialize the HealthDiagnosisAssistant."""
        self.symptom_encoder = LabelEncoder()
        self.condition_encoder = LabelEncoder()
        self.random_forest_classifier = RandomForestClassifier()
        self.svm_classifier = SVC()

    def preprocess_data(self, data):
        """Preprocess the provided data to encode symptoms and conditions."""
        symptoms = []
        conditions = []
        for symptoms_list, condition in data:
            symptoms.extend(symptoms_list)
            conditions.append(condition)
        
        self.symptoms_encoded = self.symptom_encoder.fit_transform(symptoms)
        self.conditions_encoded = self.condition_encoder.fit_transform(conditions)

    def train_models(self):
        """Train the machine learning models."""
        self.random_forest_classifier.fit(self.symptoms_encoded.reshape(-1, 1), self.conditions_encoded)
        self.svm_classifier.fit(self.symptoms_encoded.reshape(-1, 1), self.conditions_encoded)
    
    def diagnose_with_ml(self, symptoms):
        """Diagnose health conditions using machine learning models."""
        symptoms_encoded = [self.symptom_encoder.transform([symptom])[0] for symptom in symptoms]
        predicted_condition_rf = self.random_forest_classifier.predict([[s] for s in symptoms_encoded])
        predicted_condition_svm = self.svm_classifier.predict([[s] for s in symptoms_encoded])
        
        predicted_condition_rf = self.condition_encoder.inverse_transform(predicted_condition_rf)
        predicted_condition_svm = self.condition_encoder.inverse_transform(predicted_condition_svm)
        
        return predicted_condition_rf[0], predicted_condition_svm[0]

class SymptomInput(BaseModel):
    """Input model for symptoms."""
    symptoms: List[str]

assistant = HealthDiagnosisAssistant()

# Sample dataset with symptoms and conditions
data = [
    (["fever", "cough"], "flu"),
    (["fever", "shortness of breath"], "pneumonia"),
    (["headache", "nausea"], "migraine"),
    # Add more data entries
]

assistant.preprocess_data(data)
assistant.train_models()

@app.post("/diagnose")
def diagnose(symptoms_input: SymptomInput):
    """Diagnose health conditions based on input symptoms."""
    symptoms = symptoms_input.symptoms
    predicted_condition_rf, predicted_condition_svm = assistant.diagnose_with_ml(symptoms)
    return {
        "predicted_condition_rf": predicted_condition_rf,
        "predicted_condition_svm": predicted_condition_svm
    }
