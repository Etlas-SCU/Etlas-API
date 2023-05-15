# ETLAS

This is the backend application for ***ETLAS***, an electronic tour guide. It contains an archive of the most popular tours, landmarks, monuments, statues, etc. of several places. It also contains a timeline of the history of several places. 
It also contains a knowledge check section where the users can test their knowledge about the history of several places. And most importantly, it contains a feature that allows the users to capture the landmarks, monuments, statues, etc. around them and get information about them from the ***ETLAS*** database directly.  
The application is built using **Django** and **Django REST Framework**, along with **Celery** for the background tasks and **Redis** as a broker for Celery. It also uses **PostgreSQL** as a database and **Backblaze B2 Storage** for the cloud storage.

## Features

* **Articles:** Each article is about some topic/monument/statue/landmark, and it tells a bit of history and related stories about it.
* **Timeline:** The history timeline of several places/countries. Each timeline consists of many eras, and each era starts and ends at some times and has its own story/properties as well.
* **Tours:** A set of the most liked or most visited together places/landmarks/statues as a recommendation from the ETLAS team for the users to help them choose their own tours without the need for a tour guide.
* **Knowledge check:** A set of interesting multiple-choice questions (MCQs) to let the users test their knowledge about historic topics/landmarks/monuments/statues.
* **Users:** Models, serializers, urls, views, permissions that are responsible for all the functionalities related to users, their accounts, and authorization.
* **API:** The main app for the project that contains the settings, main urls, celery settings, configs for the cloud storage, and much more.
* **Authentication:** The default app for authentication in Django and contains all the main authentication functionalities of logging in, signing up, email verification, and much more.
* **Social auth:** This app is responsible for all the authentication functionalities using social media accounts like Google, Facebook, and Twitter.

## Contributing

We welcome contributions to ETLAS! If you would like to contribute, please follow these steps:

1. Fork the project on GitHub.
2. Clone your fork to your local machine.
3. Create a new branch for your changes.
4. Make your changes and commit them to your branch.
5. Push your changes to your fork.
6. Open a pull request against the original project.

## Getting Started

To get started with ETLAS, you will need to:

1. Install Python 3.6 or higher.
2. Install Django 3.1 or higher.
3. Install the requirements.txt file.
4. Create a database and migrate the models.
5. Run the development server.

## Running the Project

To run the project, simply run the following command in the project directory:


```python 
 python3 manage.py runserver
 ```
Use code with caution. Learn more
The project will be available at http://127.0.0.1:8000/ in your web browser.

### Happy Coding!