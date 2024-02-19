import sys
import requests
import json
import markdown
import os

repository_description = None

if ("DESCRIPTION_FILE" not in os.environ):
    print("Description file environment variable is not specified")
    sys.exit(1)
if ("PYXIS_API_TOKEN" not in os.environ):
    print("API token environment variable is not specified")
    sys.exit(1)
if ("API_URL" not in os.environ):
    print("API URL environment variable is not specified")
    sys.exit(1)
if ("PROJECT_ID" not in os.environ):
    print("RedHat project ID environment variable is not specified")
    sys.exit(1)

if (os.path.isfile(os.environ["DESCRIPTION_FILE"] + '.md')):
    file = open(os.environ["DESCRIPTION_FILE"] + '.md', mode='r')
    markdown_data = file.read()
    file.close()
    repository_description=markdown.markdown(markdown_data)
elif (os.path.isfile(os.environ["DESCRIPTION_FILE"] + '.html')):
    file = open(os.environ["DESCRIPTION_FILE"] + '.html', mode='r')
    repository_description = file.read()
    file.close()

if (repository_description is None or len(repository_description) == 0):
    print("No description")
    sys.exit(1)

data = dict()
data['container'] = dict()
data['container']['repository_description'] = repository_description[:32768]

headers = {'accept' : 'application/json', 'X-API-KEY' : os.environ["PYXIS_API_TOKEN"], 'Content-Type' : 'application/json'}
result = requests.patch(os.environ["API_URL"] + os.environ["PROJECT_ID"], headers = headers, data = json.dumps(data))
print(result)
print(json.loads(result.content)['last_update_date'])
