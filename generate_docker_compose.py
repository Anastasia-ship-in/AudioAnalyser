import yaml

# Задайте дані для генерації
compose_data = {
    'version': '3.8',
    'services': {
        'web': {
            'image': 'tiangolo/uvicorn-gunicorn-fastapi:python3.12',
            'container_name': 'audio_analyser_app',
            'volumes': ['./:/app'],
            'ports': ['8000:80'],
            'environment': [
                'PYTHONUNBUFFERED=1',
                'SQLALCHEMY_DATABASE_URI=postgresql://<username>:<password>@db:5432/<dbname>'
            ],
            'depends_on': ['db'],
        },
        'db': {
            'image': 'postgres:latest',
            'container_name': 'audio_analyser_db',
            'environment': {
                'POSTGRES_DB': '<dbname>',
                'POSTGRES_USER': '<username>',
                'POSTGRES_PASSWORD': '<password>',
            },
            'volumes': ['postgres_data:/var/lib/postgresql/data'],
        },
    },
    'volumes': {
        'postgres_data': {}
    },
}

with open('docker-compose.yml', 'w') as file:
    yaml.dump(compose_data, file, default_flow_style=False)

print("docker-compose.yml був успішно згенерований.")
