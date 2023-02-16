docker compose up -d db redis adminer

# Launch for dev
docker compose up zou_init

docker compose up zou zou_event zou_job

# Launch for tests
time docker compose up zou_test

allure serve ./allure_results
