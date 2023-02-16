#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER zoutest;
	CREATE DATABASE zoutest;
	GRANT ALL PRIVILEGES ON DATABASE zoutest TO zoutest;
EOSQL
