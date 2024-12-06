# digital-business-system

## Digital Business Applications Final Project

### Set up virtual environment

```shell
python -m venv myenv

# Windows
.\myenv\Scripts\activate

# macOS and Linux
source myenv/bin/activate
```

### Start the server

```shell
# Install dependencies
pip install -r requirements.txt

uvicorn src.main:app --reload
```
