SET ROLE 'karma_police';

BEGIN;
--
-- Create model Karma
--
CREATE TABLE "karma" (
    "id" serial NOT NULL PRIMARY KEY,
    "karma" integer NOT NULL default 0,
    "users_id" integer NOT NULL
);

--
-- Create model User
--
CREATE TABLE "users" (
    "id" serial NOT NULL PRIMARY KEY,
    "email" varchar(256) NOT NULL,
    "password_hash" varchar(512) NOT NULL,
    "registration_date" timestamp with time zone NOT NULL
);

COMMIT;
