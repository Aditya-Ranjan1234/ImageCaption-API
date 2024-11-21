# ImageCaption-API

## Image Caption and Music Genre Generation API

This API analyzes images to generate captions, identify potential privacy risks, and recommend music genres based on the visual content of the image. It leverages FastAPI, LlamaIndex, and multimodal AI models to perform these tasks.

## Features:
**Image Caption Generation**: Generates a high-level description of the image.    
**Music Genre Recommendation**: Suggests a fitting music genre based on the image content.   
**Privacy Analysis**: Identifies potential privacy or security risks in the image.  

## Technologies:
**FastAPI** for the API backend  
**LlamaIndex** for multimodal AI image processing  
**Ollama** models for privacy and music genre generation  

## Steps to Run Locally

### 1. Clone the Repository:
```bash
git clone https://github.com/Aditya-Ranjan1234/ImageCaption-API.git
cd image-caption-api
```

### 2. Install Dependencies:
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

### 3. Run the Ollama Server:
To use the `Ollama` model, start the Ollama server on port 11434 by running the following command:
```bash
ollama run llava-llama3
ollama serve
```
This will start the Ollama server with the `llava-llama3` model and make it available on port `11434`.

### 4. Run the FastAPI Server:
Start the FastAPI server with Uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
uvicorn app:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 0  # in case CPU instead of GPU so long processing times
```
This will start the API locally on `http://localhost:8000`.

### 5. Expose the API Publicly Using ngrok:
To make the API accessible from the internet, use ngrok:
```bash
ngrok http 8000
```
This will generate a public URL that you can use to interact with the API, such as `https://<ngrok-subdomain>.ngrok-free.app`.

### 6. Test the API:
You can test the API using tools like **curl**, **Postman**, or any frontend by sending a POST request to the `/analyze-image` endpoint with an image.

### Example curl Command:
```bash
curl -X POST -F "file=@path/to/images/test.jpg" https://<ngrok-subdomain>.ngrok-free.app/analyze-image
```

### 7. View the Output:
The response will include:
**Image Description**: A high-level summary of the image.  
**Music Genre**: The most fitting music genre based on the image.  
**Privacy Information**: Any potential privacy risks or concerns detected in the image.  

## Contributing:
Feel free to fork the repo, make changes, and submit pull requests for improvements!

## License:
This project is licensed under the GPL License.
