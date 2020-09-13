# Reddit Topic Classifier

Deploy the [Reddit topic classification model](https://github.com/yusueliu/reddit) using a simple Flask app. Originally the model and serving code were together so we can test each time the model was updated, but we decided it was better for the model to have its own repository so development can take place separately. Each time this app is built it installs the latest version of the model.

Build the Docker container and run:
```
docker build -t reddit-classifier-api:latest .
docker run --name ml_api -d -p 8000:5000 --rm reddit-classifier-api:latest
``` 
Check that the container is up and running: go to `localhost:8000/health` in your browser and you should see `okay` on the page.


To make a prediction, navigate to `/scripts` and run
```
curl --header "Content-Type: application/json" --request POST --data @input_test.json localhost:8000/v1/predict/classification
```
You should get the response
```
{"errors":{},"predictions":["live convo"],"version":"0.1.0"}
```

We also have code in the CI pipeline to push the Docker image to AWS ECR, but this depends on you first creating a repository. 
