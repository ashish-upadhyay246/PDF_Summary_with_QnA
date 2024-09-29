from flask import Flask, request, jsonify
import modules

app = Flask(__name__)
text = ""

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file_path = f"./{file.filename}"
        file.save(file_path)
        global text
        try:
            text = modules.scrape_text(file_path)
            return jsonify({"message": f"File {file.filename} uploaded and processed", "file_path": file_path}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to process the file: {str(e)}"}), 500

    return jsonify({"error": "Unexpected error"}), 500

@app.route('/query', methods=['POST'])
def query_pdf():
    data = request.json
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        gemini_response = modules.main(text, question)
        response = {"result": gemini_response}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process the query: {str(e)}"}), 500  # Handle processing errors

if __name__ == '__main__':
    app.run(debug=True)