BEGIN;
--
-- Create model AmazonListingPrice
--
CREATE TABLE "amazon_listing_prices" ("id" serial NOT NULL PRIMARY KEY, "asin" varchar(32) NOT NULL, "price" numeric(15, 2) NOT NULL, "original_price" numeric(15, 2) NOT NULL, "created_at" timestamp with time zone NOT NULL);
CREATE INDEX "amazon_listing_prices_asin_595a63e7" ON "amazon_listing_prices" ("asin");
CREATE INDEX "amazon_listing_prices_asin_595a63e7_like" ON "amazon_listing_prices" ("asin" varchar_pattern_ops);
COMMIT;
