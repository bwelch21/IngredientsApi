aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin ***REMOVED***.dkr.ecr.us-east-1.amazonaws.com

sudo docker run -it --rm -w /ingredients-api -p 8000:8000 \
-e OPENAI_API_KEY=***REMOVED*** \
***REMOVED***.dkr.ecr.us-east-1.amazonaws.com/ingredients-api