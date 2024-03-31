import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

print('Initiating Model Training')

training_dataset = pd.read_csv('api/ai_model/dataset/disease_diagnosis.csv')

# desired_diseases = [
#     'GERD',
#     'Diabetes ',
#     'Migraine',
#     'Bronchial Asthma',
#     'hepatitis A',
#     'Heart attack',
#     'Hypothyroidism',
#     'Hyperthyroidism',
#     'Urinary tract infection',
#     'Gastroenteritis',
#     'Allergy',
# ]

# training_dataset = training_dataset[training_dataset['prognosis'].isin(
#     desired_diseases)]

training_symptoms = training_dataset.drop('prognosis', axis=1)
# training_symptoms = training_symptoms.drop('Unnamed: 133', axis=1)
training_disease = training_dataset['prognosis']

training_symptoms, testing_symptoms, training_disease, testing_disease = train_test_split(
    training_symptoms, training_disease, test_size=0.2, random_state=42)

random_forest_model = RandomForestClassifier()
random_forest_model.fit(training_symptoms, training_disease)


joblib.dump(random_forest_model, 'api/ai_model/classification_model.pkl')
print('Model Trained and Exported')
