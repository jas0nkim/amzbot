BEGIN;
--
-- Remove field id from amazonlisting
--
ALTER TABLE "amazon_listings" DROP COLUMN "id" CASCADE;
--
-- Remove field id from amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" DROP COLUMN "id" CASCADE;
--
-- Alter field asin on amazonlisting
--
ALTER TABLE "amazon_listings" DROP CONSTRAINT "amazon_listings_asin_key";
ALTER TABLE "amazon_listings" ADD CONSTRAINT "amazon_listings_asin_d58b8f46_pk" PRIMARY KEY ("asin");
--
-- Alter field parent_asin on amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" DROP CONSTRAINT "amazon_parent_listings_parent_asin_key";
ALTER TABLE "amazon_parent_listings" ADD CONSTRAINT "amazon_parent_listings_parent_asin_541a6c16_pk" PRIMARY KEY ("parent_asin");
COMMIT;
