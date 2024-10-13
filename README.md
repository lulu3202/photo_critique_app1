# Photo Critique App Using Streamlit and Gemini-1.5-Flash-8B!

	Step 1: Set Up Your Environment Using venv in VS Code 
	By setting up a virtual environment (venv), you ensure that your project’s dependencies are isolated and manageable. This approach helps prevent conflicts between different projects and maintains a clean global Python environment. Here’s a quick outline:
		• Create a Virtual Environment using python -m venv venv.
		• Activate the Virtual Environment (venv\Scripts\activate on Windows or source venv/bin/activate on macOS/Linux).
		• Install Required Packages (streamlit, google-generativeai, python-dotenv, Pillow).
		• Configure VS Code to Use the Virtual Environment’s Interpreter.
		
	Step 2 : Retrieve Googles API key 
		• Store API Keys Securely in a .env file.
		• dotenv: Loads environment variables from a .env file.
		• Test_env.py to ensure everything works 
	
	Step 3: Imports and Configuration
		• google.generativeai: Google’s Generative AI SDK to interact with Gemini models.
		• streamlit: For building the web interface.
		• PIL (Pillow): For handling image uploads and display.
	
	Step 4: Function Definitions
	• Quick note on how I got my inspiration 
	• get_gemini_response: Sends the input prompt and image data to Gemini and retrieves the response.
	• get_image_content: Processes the uploaded image file and prepares it for the API call.
	
	
	Step 5: Streamlit interface description
	•  Run and Test Your Streamlit App within the virtual environment
	• Stream run app3.py for 3 different versions

![image](https://github.com/user-attachments/assets/5f4d7487-2bd4-45f4-aa02-7de4c9a7d96f)

![image](https://github.com/user-attachments/assets/222598b2-58c7-4de3-8cd1-c51a3bd8a291)



