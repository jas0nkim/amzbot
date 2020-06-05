BEGIN;
--
-- Remove field quantity from itemprice
--
ALTER TABLE "resrc_item_prices" DROP COLUMN "quantity" CASCADE;
--
-- Remove field store_location from itemprice
--
ALTER TABLE "resrc_item_prices" DROP COLUMN "store_location" CASCADE;
--
-- Add field online_availability to itemprice
--
ALTER TABLE "resrc_item_prices" ADD COLUMN "online_availability" smallint DEFAULT 1 NOT NULL;
ALTER TABLE "resrc_item_prices" ALTER COLUMN "online_availability" DROP DEFAULT;
--
-- Add field online_urgent_quantity to itemprice
--
ALTER TABLE "resrc_item_prices" ADD COLUMN "online_urgent_quantity" smallint NULL;
--
-- Add field store_availabilities to itemprice
--
ALTER TABLE "resrc_item_prices" ADD COLUMN "store_availabilities" jsonb NULL;
COMMIT;
