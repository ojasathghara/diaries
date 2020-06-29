# Diaries | A simple blog application to share your thoughts anonymously.
---

### Current features include:
- A simple webapp to create, read, update and delete posts.
- View posts by other users
- Powerful user authentication system
- Upload your avatar
- Login, Logout, Password reset feature
  
### Let people know what you think about almost anything. Share your views anonymously.

## Notes for developers:

### Tech Stack
- Django 3.0 on Python 3.6.9. (See installed app versions in requirements.txt)
- HTML, CSS and Bootstrap 4.
- Crispy forms for forms customizations

### How to setup
1. Clone the repo to local system:
   - `git clone https://github.com/ojaswi825/diaries_pro.git`

2. cd to cloned repo:
    - `cd diaries_pro`

3. Create a virtual environment:
    - `python3 -m venv venv`

4. Activate the venv created:
    - `source venv/bin/activate` or `venv\scripts\activate.bat` for windows

5. Put your smtp settings for mail related operations:
   1. Activate less secure apps for your google account
   2. Open diaries/settings.py and enter your google account details in the SMTP configuration section.
   
6. Migrate the databases:
    - `python manage.py makemigrations`
    - `python manage.py migrate`

7. Launch the app:
   - `python manage.py runserver`
   - To quit press `^C`

8. Populate posts (optional):
    1. Create some fake users
    2. run `python manage.py shell < populate_posts.py`

### Thoughts, new features and pull requests are welcomed!

