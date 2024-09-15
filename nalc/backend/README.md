 **NALC**

**Overview**

This application demonstrates a basic AI-powered search functionality, leveraging React JS for the frontend, Python Django for the backend, and OpenAI for the AI model.

**Technology Stack**

- **Frontend:** React JS
- **Backend:** Python Django
- **AI Model:** OpenAI

**Setup**

1. **Clone the repository:**

   ```bash
   git clone GIT REPO
   ```

2. **Install dependencies:**

   - **Frontend:**

     ```bash
     cd frontend
     npm install
     ```

   - **Backend:**

     ```bash
     cd backend
     pip install -r requirements.txt
     ```

3. **Set up OpenAI API key:**

   - Create an account on OpenAI and obtain your API key.
   - Set the `OPENAI_API_KEY` environment variable to your API key in the backend configuration.

**Running the Application**

1. **Start the backend server:**

   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Start the frontend development server:**

   ```bash
   cd frontend
   npm start
   ```

**Usage**

1. Access the application in your web browser, typically at `http://127.0.0.1:3000/`.
2. Enter your search query in the input field.
3. The application will send the query to the backend, which will process it using the OpenAI model and return relevant results.
4. The frontend will display the results in a user-friendly format.

- **Project structure:**
   - `frontend/`: Contains the React JS frontend code.
   - `backend/`: Contains the Python Django backend code.
- **Configuration:** Refer to the backend configuration file for details on API keys and other settings.
- **Customization:** The application can be further customized by modifying the frontend components and backend logic.
