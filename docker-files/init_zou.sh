#!/bin/bash
set -e

zou upgrade-db
zou init-data
zou create-admin admin@example.com --password mysecretpassword
