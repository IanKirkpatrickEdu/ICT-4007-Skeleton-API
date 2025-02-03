# ICT-4007 Skeleton API
Skeleton API for testing weekly code projects

## Running The API

### Running In Replit

1. click 'run'
3. Check out the "webview" tab in Replit running at ???:80
   1. Replit will open a "Webview" tab with your API in it
   2. It is recommended to open the full link of this Webview tab in a new tab to get more space in the Replit editor. This link will change on separate runs so you can not rely on bookmarking this link. 
   3. It takes you to the base route of `???:80/`. To view the swagger version of the docs, go to `???:80/docs`.

### Running Locally

1. `poetry install`
   1. poetry is our chosen package manager, this will ensure you have what you need to run the API
2. `make run`
   1. This will run the application. Now you should be able to visit `http://localhost/` to see the root of your API
      1. For swagger docs visit `http://localhost/docs`

### Running Locally (without make)

1. `poetry install`
2. `poetry run uvicorn main:app --host=0.0.0.0 --port=80`

## Selecting Python Interpreter VS Code

1. Get your poetry env path (after running the install) `poetry env info --path`
2. Use this path as the response to the following VS Code Command
   1. Open Command Pallete
      1. Mac: `cmd + shift + p`
   2. Type: `Python: Select Interpreter`  
   3. Select: `Enter Python Path...` 
   4. paste the poetry env path