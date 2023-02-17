# Launch for dev
docker compose up -d db redis adminer
docker compose up zou_init

docker compose up zou zou_event zou_job

# Launch for tests
docker compose up -d db redis adminer
time docker compose up zou_test

# Or:
docker compose run --rm --entrypoint="py.test --alluredir=/allure_results tests/models/test_comments.py" zou_test

allure serve ./allure_results

# With history:
rm -rf allure_results ; mkdir allure_results ; mv allure-report/history allure_results/ ; docker compose run --entrypoint="py.test --alluredir=/allure_results tests/models/test_comments.py" zou_test ; allure generate --clean allure_results

(cd allure-report ; python3 -m http.server 8000)
