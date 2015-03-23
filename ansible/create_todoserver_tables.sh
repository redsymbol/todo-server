#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Creates the initial database tables for todoserver.
# Assumes DB and roles are already created.
# Touches /srv/FLAGS/todoapi/create_initial_db_tables

sudo -u postgres psql todoserver < /srv/todoapi/dbcreate.sql
touch /srv/FLAGS/todoapi/create_initial_db_tables
