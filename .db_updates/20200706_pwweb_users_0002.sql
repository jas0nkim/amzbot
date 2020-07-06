BEGIN;
--
-- Create model UserProduct
--
CREATE TABLE "users_products" ("id" serial NOT NULL PRIMARY KEY, "domain" varchar(32) NOT NULL, "sku" varchar(32) NOT NULL, "user_id" integer NOT NULL);
ALTER TABLE "users_products" ADD CONSTRAINT "users_products_user_id_e3bada69_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "users_products_domain_b6a1f69a" ON "users_products" ("domain");
CREATE INDEX "users_products_domain_b6a1f69a_like" ON "users_products" ("domain" varchar_pattern_ops);
CREATE INDEX "users_products_sku_5e5ea45f" ON "users_products" ("sku");
CREATE INDEX "users_products_sku_5e5ea45f_like" ON "users_products" ("sku" varchar_pattern_ops);
CREATE INDEX "users_products_user_id_e3bada69" ON "users_products" ("user_id");
COMMIT;
