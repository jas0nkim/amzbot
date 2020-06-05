BEGIN;
--
-- Add field upc to item
--
ALTER TABLE "resrc_items" ADD COLUMN "upc" smallint NULL;
COMMIT;
