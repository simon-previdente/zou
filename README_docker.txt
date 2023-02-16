docker compose up -d db redis adminer

docker compose up zou_init

docker compose up zou zou_event zou_job

time docker compose up zou_test

allure serve ./allure_results
