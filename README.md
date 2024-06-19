# AMS ROADCAST

## Deployment Step

### Initial Setup

```
git clone https://github.com/Pranav-Khurana/ams_roadcast.git

cd ams_roadcast/

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt 
```

### Setup Environment Variables

Please add your DB url and secret key

```
DATABASE_URL=<DATABASE_URL>
SECRET_KEY=<SECRET_KEY>
```

### Create Schema and Initialize Project

```
source venv/bin/activate
python add_initial_user.py 
```

### Run the Project

```
flask run 
```

please access application on port 5000