StudioKart — Full-Stack Python & Django E-Commerce Store (v6)
=============================================================

Setup & Run Instructions (VS Code / Terminal):
1. Extract this ZIP folder and open `studiokart_django` in terminal.
   (Delete any old `db.sqlite3` file first if replacing a previous version.)
2. Install dependencies:
   pip install -r requirements.txt
3. Run migrations & collectstatic:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
4. Start the server:
   python manage.py runserver
5. Open http://127.0.0.1:8000/ and hard-refresh (Ctrl + Shift + R).
