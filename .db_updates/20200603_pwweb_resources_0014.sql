BEGIN;
--
-- Create model Item
--
CREATE TABLE "resrc_items" ("id" serial NOT NULL PRIMARY KEY, "domain" varchar(32) NOT NULL, "sku" varchar(32) NOT NULL, "title" text NOT NULL, "brand_name" varchar(100) NULL, "picture_url" varchar(255) NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL);
--
-- Create model ItemPrice
--
CREATE TABLE "resrc_item_prices" ("id" serial NOT NULL PRIMARY KEY, "domain" varchar(32) NOT NULL, "sku" varchar(32) NOT NULL, "price" numeric(15, 2) NOT NULL, "original_price" numeric(15, 2) NOT NULL, "quantity" smallint NULL, "store_location" varchar(255) NULL, "job_id" varchar(64) NULL, "created_at" timestamp with time zone NOT NULL);
CREATE INDEX "resrc_items_domain_ab610d08" ON "resrc_items" ("domain");
CREATE INDEX "resrc_items_domain_ab610d08_like" ON "resrc_items" ("domain" varchar_pattern_ops);
CREATE INDEX "resrc_items_sku_1c88b679" ON "resrc_items" ("sku");
CREATE INDEX "resrc_items_sku_1c88b679_like" ON "resrc_items" ("sku" varchar_pattern_ops);
CREATE INDEX "resrc_item_prices_domain_94f000cf" ON "resrc_item_prices" ("domain");
CREATE INDEX "resrc_item_prices_domain_94f000cf_like" ON "resrc_item_prices" ("domain" varchar_pattern_ops);
CREATE INDEX "resrc_item_prices_sku_f6f8f750" ON "resrc_item_prices" ("sku");
CREATE INDEX "resrc_item_prices_sku_f6f8f750_like" ON "resrc_item_prices" ("sku" varchar_pattern_ops);
CREATE INDEX "resrc_item_prices_job_id_8616f4e8" ON "resrc_item_prices" ("job_id");
CREATE INDEX "resrc_item_prices_job_id_8616f4e8_like" ON "resrc_item_prices" ("job_id" varchar_pattern_ops);
COMMIT;
