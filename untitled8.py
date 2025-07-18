

import spacy
import scispacy
import en_ner_bc5cdr_md
import pandas as pd
import re
nlp=spacy.load('en_ner_bc5cdr_md')
nlp_spacy=spacy.load('en_core_web_sm')

dataset=pd.read_csv('/content/medications.csv')
dataset.head()

medical_labels_to_preserve = ['DISEASE', 'DRUG', 'FORMULA', 'MEDICAL_CONDITION', 'CHEMICAL'] =
for index, row in dataset.iterrows():
    description_text = str(row['DESCRIPTION'])
    reason_desciption_text = str(row['REASONDESCRIPTION'])

    doc_description = nlp(description_text)
    entities_description = [(ent.text, ent.label_) for ent in doc_description.ents]

    doc_reason_description = nlp(reason_description_text)
    entities_reason_description = [(ent.text, ent.label_) for ent in doc_reason_description.ents]

    all_entities = entities_description + entities_reason_description
    cleaned_formatted_entities = []
    for text, label in all_entities:
        if label in medical_labels_to_preserve:
            cleaned_text = text
        else:
            lower_text = text.lower()
            text_with_8s = re.sub(r'\d', '8', lower_text)
            cleaned_text = re.sub(r'[^a-z8\s]', '', text_with_8s)

        cleaned_formatted_entities.append(f"{cleaned_text} ({label})")

    if cleaned_formatted_entities:
        print(cleaned_formatted_entities)

medical_labels_to_preserve = ['DISEASE', 'DRUG', 'FORMULA', 'MEDICAL_CONDITION', 'CHEMICAL']
non_medical_columns_to_process = ['START', 'STOP', 'PATIENT', 'ENCOUNTER', 'CODE', 'REASONCODE']

for index, row in dataset.iterrows():
    all_entities_spacy = []
    for col_name in non_medical_columns_to_process:
        text_to_process = str(row[col_name])
        doc = nlp_spacy(text_to_process)

        entities_in_column = [(ent.text, ent.label_) for ent in doc.ents]
        all_entities_spacy.extend(entities_in_column)

    cleaned_entities = []
    for text,label in all_entities_spacy:
        if label in medical_labels_to_preserve:
            cleaned_text = text
        else:
            lower_text_spacy = text.lower()
            text_with_8 = re.sub(r'\d', '8', lower_text_spacy)
            cleaned_text_spacy = re.sub(r'[^a-z8\s]', '', text_with_8)
            cleaned_entities.append(f"{cleaned_text_spacy} ({label})")

    if cleaned_entities:

        formatted_entities = " ".join(cleaned_entities)
        print(formatted_entities)

