docker build -t kcal-postgres:1.0 ./postgres
docker build -t kcal-app-image:1.0 ./site
docker-compose up -d