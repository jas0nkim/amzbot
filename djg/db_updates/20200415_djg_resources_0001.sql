BEGIN;
--
-- Create model AmazonListing
--
CREATE TABLE "amazon_listings" ("id" serial NOT NULL PRIMARY KEY, "asin" varchar(32) NOT NULL UNIQUE, "parent_asin" varchar(32) NOT NULL, "picture_urls" varchar(255)[] NULL, "url" text NOT NULL, "category" varchar(255) NULL, "title" text NOT NULL, "price" numeric(15, 2) NOT NULL, "market_price" numeric(15, 2) NOT NULL, "quantity" smallint NULL, "features" text NULL, "description" text NULL, "specifications" text NULL, "variation_specifics" varchar(255) NULL, "is_fba" boolean NOT NULL, "is_addon" boolean NOT NULL, "is_pantry" boolean NOT NULL, "has_sizechart" boolean NOT NULL, "international_shipping" boolean NOT NULL, "merchant_id" varchar(32) NULL, "merchant_name" varchar(100) NULL, "brand_name" varchar(100) NULL, "meta_title" text NULL, "meta_description" text NULL, "meta_keywords" text NULL, "status" smallint NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL);
--
-- Create model AmazonParentListing
--
CREATE TABLE "amazon_parent_listings" ("id" serial NOT NULL PRIMARY KEY, "parent_asin" varchar(32) NOT NULL UNIQUE, "asins" varchar(32)[] NULL, "review_count" smallint NULL, "avg_rating" double precision NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL);
CREATE INDEX "amazon_listings_asin_d58b8f46_like" ON "amazon_listings" ("asin" varchar_pattern_ops);
CREATE INDEX "amazon_listings_parent_asin_318fc513" ON "amazon_listings" ("parent_asin");
CREATE INDEX "amazon_listings_parent_asin_318fc513_like" ON "amazon_listings" ("parent_asin" varchar_pattern_ops);
CREATE INDEX "amazon_parent_listings_parent_asin_541a6c16_like" ON "amazon_parent_listings" ("parent_asin" varchar_pattern_ops);
COMMIT;
