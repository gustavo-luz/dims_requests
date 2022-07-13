clone this repository and enter it
git clone https://github.com/gustavo-luz/dims_requests
cd dims_requests

Docker build - sudo docker build -t dims_requests:latest .
Docker run - sudo docker run -d -it --name dims_requests --rm dims_requests:latest

# dashboard.py
Dashboard will handle authentication of google spreadsheets and heroku's app and manage it's data based on pandas dataframes.
Necessary to run main project's program

# request.py
Request will use dashboard's function to format data and upload it to google spreadsheets.
It is the main project's program

# heroku.py
Since real containers are not implemented yet, 'heroku.py' will hold functions regard simulating those container's posts.
Not necessary to run main project's program, just a useful tool while physical containers are not implemented yet.


# presentation.py
Presentation will run 'heroku.py' functions and 'request.py' to upload simulated data.
Not necessary to run main project's program, just a useful tool while physical containers are not implemented yet.
