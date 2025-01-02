import azure.functions as func
import logging
import json, os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
 
 
search_end = os.getenv('SEARCH_END')
search_key = os.getenv('SEARCH_KEY')
embed_end = os.getenv('EMBED_END')
embed_key = os.getenv('EMBED_KEY')
chat_end = os.getenv('CHAT_END')
chat_key = os.getenv('CHAT_KEY')
 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
@app.route(route="search_doc")
def search_doc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    if req.method == "OPTIONS":
        logging.info("Handling preflight request")
        return func.HttpResponse(
            "",
            status_code=200,  
            headers={
                'Access-Control-Allow-Origin': '*',  # Allow all origins (you can restrict this to your specific domain)
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )
 
    try:
        # Parse request body
        req_body = req.get_json()
        query = req_body.get('query')
        department = req_body.get('department', None)
 
        if not query:
            return func.HttpResponse(
                "Query cannot be empty.", status_code=400,
                headers={
                    'Access-Control-Allow-Origin': '*',  # Allow all origins for CORS
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            )
 
        # Perform the search
        search_results = search_documents(query, department)
 
        # Prepare response
        return func.HttpResponse(
            json.dumps(search_results),  # Convert list to JSON string
            status_code=200,
            mimetype="application/json",
            headers={
                    'Access-Control-Allow-Origin': '*',  # Allow all origins for CORS
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }  # Set the correct MIME type
        )
 
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"Error performing search: {str(e)}", status_code=500,
            headers={
                    'Access-Control-Allow-Origin': '*',  # Allow all origins for CORS
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
        )
 
def search_documents(query, Department):
    """
    Search documents in Azure Cognitive Search, optionally filtered by category.
    """
    try:
        credential = AzureKeyCredential(search_key)
        search_client = SearchClient(endpoint=search_end, index_name="batch1-index", credential=credential)
 
        # Build search parameters
        search_filter = f"Department eq '{Department}'" if Department else None
        logging.info(f"Search filter: {search_filter}")
 
        # Perform search
        results = search_client.search(search_text=query, filter=search_filter, top=10)
        logging.info(f"Search results: {results}")
 
       
        search_results = []
        for result in results:
            search_results.append(result)
 
        return search_results
 
    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        return "[]"
 
    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        return []