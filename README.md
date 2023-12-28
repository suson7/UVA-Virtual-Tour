# UVATOUR: Virtual Tours of University of Virginia

![UVATOUR Logo](users/static/users/images/tundy.jpeg)

---

**UVATOUR** is a Django-based web application that offers an interactive and immersive experience of virtual tours across the University of Virginia (UVA). Whether you're a prospective student, an alum looking to reminisce, or just curious, dive in to explore UVA's iconic landmarks and hidden treasures!

## Features

- **Interactive Campus Map**: Navigate through the UVA grounds with a click.
- **Guided Virtual Walkthroughs**: Experience the campus with student narrators.
- **Customized Tour Paths**: Handpick your spots or go with our recommended trails.
- **Historical Insights**: Unearth the stories behind every brick of UVA.
- **Mobile Optimized**: Take UVA with you, wherever you go!

## Getting Started

### Prerequisites

- Python (3.7 or higher)
- pip
- SQLite3 (if deploying locally)

### Local Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/your_username/UVATOUR.git
2. Enter the project directory:
   ```bash
   cd UVATOUR
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Migrate the database:
   ```bash
   python manage.py migrate
5. Run the server:
   ```bash
   python manage.py runserver
6. Open your browser and visit http://localhost:8000/.

## Deploying to Heroku
Our setup is Heroku-friendly. Follow the steps:

1. Set up a new Heroku app.
2. Attach a PostgreSQL add-on.
3. Configure environment variables (SECRET_KEY, DEBUG_VALUE, etc.).
4. Deploy your code.
5. Migrate the database on Heroku.

## Acknowledgments
Props to University of Virginia for inspiration and resources.
Kudos to the open-source community and all contributors.