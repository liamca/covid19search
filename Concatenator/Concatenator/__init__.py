import json
import logging
import azure.functions as func


# This function accepts json-formatted authors with separate fields for first and last 
# names.  It reformats them into a list of full names, adhering to the custom skill
# input and output interface defined at https://docs.microsoft.com/azure/search/cognitive-search-custom-skill-interface.  

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python Concatenator processed a request.")

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(body=result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data):
    values = json.loads(json_data)["values"]
    
    # Prepare the output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)


## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value["recordId"]
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
        assert ('authors' in data), "'authors' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    # Parse out the first name, middle initial, and last name of an author, 
    # and reformat them together as a full name
    try:
        fullNames = []
        for c in value["data"]["authors"]:
            midInitial = ''
            for mi in c["middle"]:
                midInitial += mi + ' '
            if len(((c["first"] + ' ' + midInitial + c["last"]).strip())) > 2:
                fullNames.append((c["first"] + ' ' + midInitial + c["last"]).strip()) 
    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "text": fullNames
                    }
            })