BEGIN;
--
-- Create model RawData
--
CREATE TABLE "resrc_raw_data" ("id" serial NOT NULL PRIMARY KEY, "url" text NOT NULL, "domain" varchar(32) NOT NULL, "data" jsonb NULL, "created_at" timestamp with time zone NOT NULL);
CREATE INDEX "resrc_raw_data_url_856f458a" ON "resrc_raw_data" ("url");
CREATE INDEX "resrc_raw_data_url_856f458a_like" ON "resrc_raw_data" ("url" text_pattern_ops);
CREATE INDEX "resrc_raw_data_domain_0d6ca9e4" ON "resrc_raw_data" ("domain");
CREATE INDEX "resrc_raw_data_domain_0d6ca9e4_like" ON "resrc_raw_data" ("domain" varchar_pattern_ops);
COMMIT;
