# Vehicle Selector

A (hopefully) modern example of a car selector system; one that you'd expect to find on car sale site. Originally built on Flask, I have reworked the application to now use FastAPI. We're still using SQLAlchemy, but in the 2.0 dialect! For the frontend, the application now uses a NextJS (ReactJS) frontend to fetch data from our server and display it appropriately.

![Selector](/meta/selector.png)


## Vehicles Dataset
The dataset being used for vehicles has also drastically changed; with features now down to a vehicle's optionable specifics for their specific year models. The full dataset is both absolutely huge, and took a lot of work to assemble; so I'll only be releasing a snippet of the total set. Find this [here](api/import/vehicles.json). Here's a quick summary of the dataset's general structure, as well as a brief idea on what kind of data is available.

![JSON](/meta/json.png)


### This set contains all options for all year models in the following models:
* ### Toyota
  * #### 86
  * #### Chaser
  * #### MR2
  * #### Supra
* ### Mazda
  * #### 6
  * #### MX-5
  * #### RX-7


## Installation
```
# Clone the repo.
$ git clone https://github.com/Ald0s/Car-Selector-Backend.git
$ cd Car-Selector-Backend/

# Create frontend & install packages.
$ npm install

# Create API environment, install packages and run tests.
$ cd api/
$ pipenv install
$ export APP_ENV=Test; pipenv run pytest

# Run the API.
$ cd ..
$ npm run start-api

# Create a new tab and run the frontend application.
$ npm run dev

# View the project. The default is displayed below; this may vary if you change settings.
http://localhost:3000/

```

## Python packages
* fastapi
* sqlalchemy
* uvicorn[standard]
* pytest
* httpx
* fastapi-pagination

## Authors
* **Alden Viljoen**