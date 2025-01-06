FROM python:3.9-slim
RUN git clone https://github.com/MelecaZane/GymApp.git
WORKDIR /GymApp
RUN pip install -r requirements.txt
RUN sudo apt update
RUN sudo apt install -y sqlite3
EXPOSE 5007
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:flask_app"]