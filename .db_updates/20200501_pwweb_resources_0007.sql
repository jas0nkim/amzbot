BEGIN;
--
-- Add field domain to amazonlistingprice
--
ALTER TABLE "amazon_listing_prices" ADD COLUMN "domain" varchar(32) NULL;
COMMIT;
