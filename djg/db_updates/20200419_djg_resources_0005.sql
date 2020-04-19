BEGIN;
--
-- Rename field market_price on amazonlisting to original_price
--
ALTER TABLE "amazon_listings" RENAME COLUMN "market_price" TO "original_price";
COMMIT;
