BEGIN;
--
-- Add field meta_description to item
--
ALTER TABLE "resrc_items" ADD COLUMN "meta_description" text NULL;
--
-- Add field meta_image to item
--
ALTER TABLE "resrc_items" ADD COLUMN "meta_image" text NULL;
--
-- Add field meta_title to item
--
ALTER TABLE "resrc_items" ADD COLUMN "meta_title" text NULL;
--
-- Add field meta_data to rawdata
--
ALTER TABLE "resrc_raw_data" ADD COLUMN "meta_data" jsonb NULL;
COMMIT;
