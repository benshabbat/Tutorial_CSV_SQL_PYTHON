from fastapi import FastAPI, File, UploadFile
from io import StringIO
import pandas as pd

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Read the file contents as bytes
    contents = await file.read()

    # Decode the bytes to a string
    csv_string = contents.decode("utf-8")

    # Use StringIO to treat the string as a file-like object
    csv_buffer = StringIO(csv_string)       
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(csv_buffer)

    # You can now process the DataFrame (e.g., print it, save to DB, etc.)
    print(df.head())

    # Close the buffer and the uploaded file
    csv_buffer.close()
    await file.close()
    return {"filename": file.filename, "message": "CSV processed successfully!"}