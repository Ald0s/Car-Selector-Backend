# Vehicle Selector
![Selector](/meta/selector.png)

A (hopefully) modern example of a car selector system; one that you'd expect to find on car sale site. Originally built on Flask, I have reworked the application to now use FastAPI. We're still using SQLAlchemy, but in the 2.0 dialect! For the frontend, the application now uses a NextJS (ReactJS) frontend to fetch data from our server and display it appropriately.

The data source for vehicles has also drastically changed; with features now down to a vehicle's optionable specifics. The full dataset is both absolutely huge, and was a real pain for me to assemble; so I'll only be releasing a snippet of the total set. Find this snippet [here](api/import/vehicles.json).

## This set contains the following information:
* ## Toyota
  * ### 86
  * ### Chaser
  * ### MR2
  * ### Supra
* ## Mazda
  * ### 6
  * ### MX-5
  * ### RX-7

All year models and possible options are included for these models.


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

### Python packages
* fastapi
* sqlalchemy
* uvicorn[standard]
* pytest
* httpx
* fastapi-pagination

### Authors
* **Alden Viljoen**