# Backend Setup

## Create Virtual Environment

```bash
python -m venv env
```

Activate

Windows

```bash
env\Scripts\activate
```

Mac/Linux

```bash
source env/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```