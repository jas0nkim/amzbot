BEGIN;
--
-- Create model Crawl
--
CREATE TABLE "rprt_crawls" ("id" serial NOT NULL PRIMARY KEY, "link" text NOT NULL, "domain" varchar(32) NOT NULL, "key_one" varchar(32) NULL, "key_two" varchar(32) NULL, "job_id" varchar(64) NOT NULL, "errors" jsonb NULL, "status" smallint NOT NULL, "created_at" timestamp with time zone NOT NULL);
CREATE INDEX "rprt_crawls_job_id_8a01af1f" ON "rprt_crawls" ("job_id");
CREATE INDEX "rprt_crawls_job_id_8a01af1f_like" ON "rprt_crawls" ("job_id" varchar_pattern_ops);
COMMIT;
