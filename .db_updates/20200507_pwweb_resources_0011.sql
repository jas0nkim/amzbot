BEGIN;
--
-- Add field http_status to rawdata
--
ALTER TABLE "resrc_raw_data" ADD COLUMN "http_status" smallint NULL;
COMMIT;
