BEGIN;
--
-- Delete model AmazonListing
--
DROP TABLE "resrc_amazon_listings" CASCADE;
--
-- Delete model AmazonListingPrice
--
DROP TABLE "resrc_amazon_listing_prices" CASCADE;
--
-- Delete model AmazonParentListing
--
DROP TABLE "resrc_amazon_parent_listings" CASCADE;
COMMIT;
