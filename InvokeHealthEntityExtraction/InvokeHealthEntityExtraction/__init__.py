import json
import logging
import azure.functions as func
import os
import pickle
import requests

# Global configuration
max_sentences = 15
ta_url = TODO


"""
This function accepts json-formatted data with separate fields for a research paper's title, abstract, and body.  
It reformats the data into the format that the Text Analytics for Health container needs, by taking chunks of text
first from the title, then abstract, and then the body until we have reached a maximum of <max_sentences> chunks.
Then the Text Analytics for Health is called with this text, and its output is reformatted into lists of entities.
The inputs and outputs of this function adhere to the Cognitive Search custom skill interface defined at 
https://docs.microsoft.com/azure/search/cognitive-search-custom-skill-interface.  
"""
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info("Python InvokeHealthEntityExtraction function processed a request.")

    try:
        body = json.dumps(req.get_json())
        logging.info("Body: " + body)
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body, context)
        return func.HttpResponse(body=result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data, context):
    values = json.loads(json_data)["values"]
    
    # Load UMLS dictionary
    logging.info("Function directory is " + context.function_directory)
    if os.path.isfile(os.path.join(context.function_directory, "umls_concept_dict.pickle")):
        logging.info("The umls_concept_dict.pickle file was found.")
    else:
        logging.warn("The umls_concept_dict.pickle file was not found.")
    with open(os.path.join(context.function_directory, "umls_concept_dict.pickle"), "rb") as handle:
        umls_concept_dict = pickle.load(handle)
    logging.info("UMLS dictionary loaded")

    # Prepare the output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value, umls_concept_dict)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)


## Perform an operation on a record
def transform_value(value, umls_concept_dict):
    try:
        recordId = value["recordId"]
    except AssertionError  as error:
        return (
            {
            "recordId": 0,
            "errors": [ { "message": "You must provide a recordId in your input. " + error.args[0] }   ]       
            })

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('title' in data), "'title' field is required in 'data' object."
        assert ('body' in data), "'body' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:
        documents = {
            "documents": []
        }
        id_counter = 1

        if len(data["title"]) > 1:
            documents["documents"].append({
                      "language": "en",
                      "id": str(id_counter),
                      "text": data["title"]
                    })
            id_counter += 1

        if "abstract" in data:
            for c in data["abstract"]:
                documents["documents"].append({
                        "language": "en",
                        "id": str(id_counter),
                        "text": c
                    })
                id_counter += 1

        if id_counter < max_sentences:
            if "body" in data:
                for c in data["body"]:       
                    documents["documents"].append({
                            "language": "en",
                            "id": str(id_counter),
                            "text": c
                        })
                    id_counter += 1
                    if id_counter == max_sentences:
                        break
        
        logging.info("Documents: " + json.dumps(documents, indent = 4))
        json_response = requests.post(url = ta_url, json = documents).json()
        json_object = json.dumps(json_response, indent = 4) 
        logging.info("Response from TA: " + json_object)

        # Initialize health entities
        CONDITION_QUALIFIER = []
        DIAGNOSIS = []
        DIRECTION = []
        EXAMINATION_NAME = []
        EXAMINATION_RELATION = []
        FAMILY_RELATION = []
        GENDER = []
        GENE = []
        MEDICATION_CLASS = []
        MEDICATION_NAME = []
        ROUTE_OR_MODE = []
        SYMPTOM_OR_SIGN = []
        TREATMENT_NAME = []
        BODY_STRUCTURE = []
        VARIANT = []
        logging.info("Initialized health entities")

        # Put the output of the Text Analytics Entity Extraction in the interface for a custom skill output
        for doc in json_response["documents"]:
            logging.info("Document: " + json.dumps(doc))
            for ent in doc["entities"]:
                #logging.info("Entity: " + json.dumps(ent))
                if "links" in ent:
                    for link in ent["links"]:
                        if link["dataSource"] == "UMLS":
                            if ent['type'] == 'TREATMENT_NAME':
                                TREATMENT_NAME.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'BODY_STRUCTURE':
                                BODY_STRUCTURE.append(umls_concept_dict[link['id']])
                            if ent['type'] == 'CONDITION_QUALIFIER':
                                CONDITION_QUALIFIER.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'DIAGNOSIS':
                                DIAGNOSIS.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'DIRECTION':
                                DIRECTION.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'EXAMINATION_NAME':
                                EXAMINATION_NAME.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'EXAMINATION_RELATION':
                                EXAMINATION_RELATION.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'FAMILY_RELATION':
                                FAMILY_RELATION.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'GENDER':
                                GENDER.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'GENE':
                                GENE.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'MEDICATION_CLASS':
                                MEDICATION_CLASS.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'MEDICATION_NAME':
                                MEDICATION_NAME.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'ROUTE_OR_MODE':
                                ROUTE_OR_MODE.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'SYMPTOM_OR_SIGN':
                                SYMPTOM_OR_SIGN.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'TREATMENT_NAME':
                                TREATMENT_NAME.append(umls_concept_dict[link['id']])
                            elif ent['type'] == 'VARIANT':
                                VARIANT.append(umls_concept_dict[link['id']])
                            break  # Once we've found the UMLS link, we don't need to go through the rest.  
                            # TODO: remove this break, as per Liam
                else:
                    logging.info("No links for " + ent["text"])
        
        # Unique terms and back to list
        BODY_STRUCTURE = list(set(BODY_STRUCTURE))
        CONDITION_QUALIFIER = list(set(CONDITION_QUALIFIER))
        DIAGNOSIS = list(set(DIAGNOSIS))
        DIRECTION = list(set(DIRECTION))
        EXAMINATION_NAME = list(set(EXAMINATION_NAME))
        EXAMINATION_RELATION = list(set(EXAMINATION_RELATION))
        FAMILY_RELATION = list(set(FAMILY_RELATION))
        GENDER = list(set(GENDER))
        GENE = list(set(GENE))
        MEDICATION_CLASS = list(set(MEDICATION_CLASS))
        MEDICATION_NAME = list(set(MEDICATION_NAME))
        ROUTE_OR_MODE = list(set(ROUTE_OR_MODE))
        SYMPTOM_OR_SIGN = list(set(SYMPTOM_OR_SIGN))
        TREATMENT_NAME = list(set(TREATMENT_NAME))
        VARIANT = list(set(VARIANT))

        entities = {"health_entities": []}
        entities["health_entities"].append({"treatmentName":TREATMENT_NAME, "examinationName": EXAMINATION_NAME, 
                                   "bodyStructure": BODY_STRUCTURE, "diagnosis": DIAGNOSIS, "conditionQualifier": CONDITION_QUALIFIER, "direction": DIRECTION,
                                   "examinationRelation": EXAMINATION_RELATION, "familyRelation": FAMILY_RELATION, "gender": GENDER, "gene": GENE,
                                   "medicationClass": MEDICATION_CLASS, "medicationName": MEDICATION_NAME, "routeOrMode": ROUTE_OR_MODE, "symptomOrSign": SYMPTOM_OR_SIGN,
                                   "variant": VARIANT})

        json_str = json.dumps(entities, indent = 4) 
        logging.info("Entities output: " + json_str)

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record " + recordId }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "treatmentName": TREATMENT_NAME, 
                "examinationName": EXAMINATION_NAME,
                "bodyStructure": BODY_STRUCTURE, 
                "diagnosis": DIAGNOSIS, 
                "conditionQualifier": CONDITION_QUALIFIER, 
                "direction": DIRECTION,
                "examinationRelation": EXAMINATION_RELATION, 
                "familyRelation": FAMILY_RELATION, 
                "gender": GENDER, 
                "gene": GENE,
                "medicationClass": MEDICATION_CLASS, 
                "medicationName": MEDICATION_NAME, 
                "routeOrMode": ROUTE_OR_MODE, 
                "symptomOrSign": SYMPTOM_OR_SIGN,
                "variant": VARIANT
                    }
            })