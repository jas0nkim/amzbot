BEGIN;
--
-- Alter field asin on amazonlisting
--
ALTER TABLE "amazon_listings" DROP CONSTRAINT "amazon_listings_asin_d58b8f46_pk";
CREATE INDEX "amazon_listings_asin_d58b8f46" ON "amazon_listings" ("asin");
--
-- Alter field domain on amazonlisting
--
ALTER TABLE "amazon_listings" ALTER COLUMN "domain" SET NOT NULL;
CREATE INDEX "amazon_listings_domain_d7615a65" ON "amazon_listings" ("domain");
CREATE INDEX "amazon_listings_domain_d7615a65_like" ON "amazon_listings" ("domain" varchar_pattern_ops);
--
-- Alter field domain on amazonlistingprice
--
ALTER TABLE "amazon_listing_prices" ALTER COLUMN "domain" SET NOT NULL;
CREATE INDEX "amazon_listing_prices_domain_278a9b3b" ON "amazon_listing_prices" ("domain");
CREATE INDEX "amazon_listing_prices_domain_278a9b3b_like" ON "amazon_listing_prices" ("domain" varchar_pattern_ops);
--
-- Alter field domain on amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" ALTER COLUMN "domain" SET NOT NULL;
CREATE INDEX "amazon_parent_listings_domain_5431471a" ON "amazon_parent_listings" ("domain");
CREATE INDEX "amazon_parent_listings_domain_5431471a_like" ON "amazon_parent_listings" ("domain" varchar_pattern_ops);
--
-- Alter field parent_asin on amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" DROP CONSTRAINT "amazon_parent_listings_parent_asin_541a6c16_pk";
CREATE INDEX "amazon_parent_listings_parent_asin_541a6c16" ON "amazon_parent_listings" ("parent_asin");
--
-- Add field id to amazonlisting
--
ALTER TABLE "amazon_listings" ADD COLUMN "id" serial NOT NULL PRIMARY KEY;
--
-- Add field id to amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" ADD COLUMN "id" serial NOT NULL PRIMARY KEY;
--
-- Create constraint unique_asin_domain on model amazonlisting
--
ALTER TABLE "amazon_listings" ADD CONSTRAINT "unique_asin_domain" UNIQUE ("asin", "domain");
--
-- Create constraint unique_asin_price_domain on model amazonlistingprice
--
ALTER TABLE "amazon_listing_prices" ADD CONSTRAINT "unique_asin_price_domain" UNIQUE ("asin", "domain");
--
-- Create constraint unique_parent_asin_domain on model amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" ADD CONSTRAINT "unique_parent_asin_domain" UNIQUE ("parent_asin", "domain");
COMMIT;
