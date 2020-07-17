# valorant-pugfinder-api
An API for tracking Valorant PUGs

# Setup
Install and run MYSQL.

Then define the following environment variables:
```sh
export MYSQL_USERNAME=???
export MYSQL_PASSWORD=???
export MYSQL_DB=???
export MYSQL_SERVER=???
```

Next, set up a python virtual environment, and run
```
pip install -r requirements-dev.txt
```

Once the database and Python are set up, you can run the latest migrations with

```
python server.py db upgrade
```

And finally, run the server with
```
python server.py run
```