# Plantes de Jardin (Backyard Plants)

## 💡 Inspiration

Plants are an essential part of our backyards but they wither frequently because they are afflicted and the disease is not recognised at an early stage. Moreover, the disease can spread from one plant to the other adversely affecting our environment and biodiversity. The mission of our projects is to identify plant diseases early and suggest appropriate methods for their treatment.

## 💻 What it does

Plantes de Jardin can be used by anyone to detect if their plant is healthy or sick, as well as provide treatment options all with just a click of a picture.<br>
Currently following Plants are supported -
- Corn
- Pepper Bell
- Potato
- Tomato

It can also be used to check out current weather conditions and forecasts and can also be used to find up a range of information about different types of plants.

## ⚙️How we built it
- ML: Python, TensorFlow
- Frontend: HTML, CSS, JS
- Backend: Django
- Database: CockroachDB
- Authentication: Auth0

## Use of CockroachDB

- We have used CockroachDB as a primary database because it is an easy-to-use, open-source and indestructible SQL database.

## 🔑 Auth0

- We have used Auth0 for secure user authentication

## Use of Google Cloud

- We have used Google Cloud's Secure Storage to store the training data and Google Cloud's GPU enabled Notebooks for a training our Model at a Blazing Fast Speed

## 🧠 Challenges we ran into

As we had 24826 images in our Dataset (taken from the infamous PlantVillage Dataset), training our model was a very hectic and time consuming task as our machines were not capable enough to handle such heavy computations. It took us three hours to train and evaluate the performance of our first model which turned out to be not so good. <br>
So we decided to shifted all our data to Google Cloud's Secure Storage and use Google Cloud's GPU enabled notebooks and were effectively able to reduce our training time to just about 10 minutes for the later models.

## 🏅 Accomplishments that we're proud of

We are happy to achieve an Accuracy of 91% on our testing data (2496 images) and that we completed the project in this short frame of time and we learned a lot from this hackathon.

## 📖 What we learned

We learned about renting GPUs to reduce our training time and collaboration.

## 🚀 What's next for Plantes de Jardin

Improving the accuracy of the model.

## Installing and Running
Go to the backend folder and run
```
pip install -r requirements.txt
python manage.py runserver
```
