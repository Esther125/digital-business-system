# digital-business-system

## Digital Business Applications Final Project

### Setup virtual environment

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
cd backend
uvicorn main:app --reload
```

### Setup pre-commit

```bash
pre-commit install

# Manually check all files
pre-commit run --all-files
```

### ENV setting
In Amazon db IAM Security credentials you can get Access keys, create a new one or use existed one
```bash
AWS_ACCESS_KEY_ID='AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'
```
