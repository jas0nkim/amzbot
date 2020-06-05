BEGIN;
--
-- Add field parent_sku to item
--
ALTER TABLE "resrc_items" ADD COLUMN "parent_sku" varchar(32) NULL;
COMMIT;
