BEGIN;
--
-- Rename table for amazonlisting to resrc_amazon_listings
--
ALTER TABLE "amazon_listings" RENAME TO "resrc_amazon_listings";
--
-- Rename table for amazonlistingprice to resrc_amazon_listing_prices
--
ALTER TABLE "amazon_listing_prices" RENAME TO "resrc_amazon_listing_prices";
--
-- Rename table for amazonparentlisting to resrc_amazon_parent_listings
--
ALTER TABLE "amazon_parent_listings" RENAME TO "resrc_amazon_parent_listings";
COMMIT;
