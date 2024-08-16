# Flask


This API allows you to upload CSV files, generate a summary of the data, and perform queries on the uploaded data.

### API KEY

All endpoints require an API key for access. The key should be provided in the request headers.
API Key: abcd

### ENDPOINTS

#### 1. Upload

Endpoint: /upload
Method: POST
Description: Upload a CSV file to the server. The file will be stored and a summary will be generated.

Headers:
api_key: abcd

Body:
file: The CSV file to upload (multipart/form-data).

`
curl -H "api_key: abcd" -X POST http://127.0.0.1:5000/upload -F "file=@/path/to/your/file.csv"
`

#### 2. Get Summary of Uploaded Data

Endpoint: /summary/<int:idx>
Method: GET
Description: Get the summary of the data stored at a specific index.

Headers:
api_key: abcd

Parameters:
idx: The index of the uploaded data.

`
curl -H "api_key: abcd" -X GET http://127.0.0.1:5000/summary/0 
`

#### 3. Query Data

Endpoint: /query/<int:idx>
Method: GET
Description: Query the uploaded data using a specific column and value.

Headers:
api_key: abcd

Parameters:
idx: The index of the uploaded data.
column: The column name to query.
value: The value to match in the column.

`
curl -H "api_key: abcd" -X GET "http://127.0.0.1:5000/query/0?column=ColumnName&value=Value"
`

