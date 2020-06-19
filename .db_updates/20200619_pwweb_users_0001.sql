BEGIN;
--
-- Create model UserProfile
--
CREATE TABLE "users_user_profile" ("id" serial NOT NULL PRIMARY KEY, "latitude" double precision NULL, "longitude" double precision NULL, "address" varchar(255) NULL, "city" varchar(50) NULL, "province" varchar(50) NULL, "postal_code" varchar(50) NULL, "county" varchar(50) NULL, "user_id" integer NOT NULL UNIQUE);
ALTER TABLE "users_user_profile" ADD CONSTRAINT "users_user_profile_user_id_c0f3ff8b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
