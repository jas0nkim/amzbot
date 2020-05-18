BEGIN;
--
-- Add field job_id to rawdata
--
ALTER TABLE "resrc_raw_data" ADD COLUMN "job_id" varchar(64) NULL;
CREATE INDEX "resrc_raw_data_job_id_061b1aa5" ON "resrc_raw_data" ("job_id");
CREATE INDEX "resrc_raw_data_job_id_061b1aa5_like" ON "resrc_raw_data" ("job_id" varchar_pattern_ops);
COMMIT;
