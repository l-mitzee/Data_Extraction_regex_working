from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from doc_extract import DocumentDataExtraction
from google.cloud import storage

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.pdf_file_path = ''

# Configure Google Cloud Storage client
storage_client = storage.Client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
@cross_origin()
def submitRoute():
    pdf_file = request.files['pdf_file']
    if pdf_file.filename != '':
        clApp = ClientApp()
        clApp.pdf_file_path = os.path.join('uploads', pdf_file.filename)
        pdf_file.save(clApp.pdf_file_path)

        result = DocumentDataExtraction.extract_invoice_info(clApp.pdf_file_path)
        csv_file_path = 'invoice_info.csv'
        DocumentDataExtraction.write_to_csv(csv_file_path, [result])

        # Save the CSV file to GCS bucket
        bucket_name = 'doc_bucket_extract'  # Replace with your GCS bucket name
        destination_blob_name = 'invoice_info.csv'  # Specify the destination filename in the bucket

        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(csv_file_path)

        return jsonify(result)

    return jsonify({'error': 'No file uploaded.'})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=7000, debug=True)
