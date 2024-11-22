<h1 align='center'> Shark Attack CRUD App </h1>

## Running the API

1. Clone the repository

2. Create a virtual environment

```
python3 -m venv <name_of_venv>
```
3. Go to the virtual environment's directory and activate it
```
bin/activate
```
4. Install the requirements

```
pip install -r requirements.txt
```

5. CD into shark_app directory 

6. Run the API with uvicorn

```
uvicorn main:app --reload
```

The message "Project connected to the MongoDB database!" muts appear if everything is right. From this point, one can use the Swagger documentation to test the API and MongoDB Compass to visualize the collections and documents. 

The code used to upload to MongoDB is in `requests_to_app.ipynb`

<h1 align='center'> Modeling Task </h1>

You can find the modeling task in `data_prep_and_modeling.ipynb`

In order to run it you can use the same virtual environment as for the other task. 

The data used for training is in `shark_data_cleaned.csv`.

The data uploaded to MongoDB is in `shark_data_cleaned_with_year.csv`.

<h1 align='center'> Frontend Task </h1>

An attempt is in `my-app`, not much was achieved there though. 