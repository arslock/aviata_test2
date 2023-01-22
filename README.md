# aviata_test

1. Go inside airflow service's 'app' directory and add .env file with LOCAL_IP='Your own local ip'
2. Run each service with command docker-compose up --build
3. Make a POST request to http://0.0.0.0:9000/search
4. Then GET request to http://0.0.0.0:9000/results/{search_id}/{currency} 