## Installation

### Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.12.4 version
- pip

### Steps
1. Open your cmd and navigate to your desktop directory
2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd harmonix-deploy-railway 
3.   **Create a virtual environment**:
     ```bash
       python -m venv venv
       source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
4.   **Install dependencies**:
      ```bash
      pip install -r requirements.txt
5.    **Set up the database**:
        ```bash
        python manage.py migrate
6.    **Create a superuser (optional)**:
        ```bash
        python manage.py createsuperuser
7.    **Run the development server**:
        ```bash
        python manage.py runserver
8.   **Access the app**: Open your browser and go to __http://127.0.0.1:8000/__.
