# determine os
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)    pg_cmd="psql -U postgres";;
    *)          pg_cmd="sudo -u postgres psql"
esac

${pg_cmd} -c "DROP DATABASE IF EXISTS karma_police"
${pg_cmd} -c "DROP ROLE IF EXISTS karma_police"
${pg_cmd} -c "CREATE USER karma_police WITH PASSWORD 'karma_police';"
${pg_cmd} -c "CREATE DATABASE karma_police ENCODING 'UTF8';"
${pg_cmd} -c "GRANT ALL PRIVILEGES ON DATABASE karma_police TO karma_police;"

cat sql/create_tables.sql | ${pg_cmd} -d karma_police -a
# cat sql/sample_data.sql | ${pg_cmd} -d karma_police -a
