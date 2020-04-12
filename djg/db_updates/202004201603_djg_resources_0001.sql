--
-- Create model AmazonListing
--
CREATE TABLE `amazon_listings` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `asin` varchar(32) NOT NULL UNIQUE, `parent_asin` varchar(32) NULL, `url` longtext NOT NULL, `category` varchar(255) NULL, `title` longtext NOT NULL, `price` numeric(15, 2) NOT NULL, `market_price` numeric(15, 2) NOT NULL, `quantity` smallint NULL, `features` longtext NULL, `description` longtext NULL, `specifications` longtext NULL, `variation_specifics` varchar(255) NULL, `review_count` smallint NULL, `avg_rating` double precision NULL, `is_fba` bool NOT NULL, `is_addon` bool NOT NULL, `is_pantry` bool NOT NULL, `has_sizechart` bool NOT NULL, `international_shipping` bool NOT NULL, `merchant_id` varchar(32) NULL, `merchant_name` varchar(100) NULL, `brand_name` varchar(100) NULL, `meta_title` longtext NULL, `meta_description` longtext NULL, `meta_keywords` longtext NULL, `status` smallint NULL, `created_at` datetime(6) NOT NULL, `updated_at` datetime(6) NOT NULL, `ts` datetime(6) NOT NULL);
--
-- Create model AmazonListingPicture
--
CREATE TABLE `amazon_listing_pictures` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `asin` varchar(32) NOT NULL, `picture_url` varchar(255) NOT NULL, `created_at` datetime(6) NOT NULL, `updated_at` datetime(6) NOT NULL, `ts` datetime(6) NOT NULL);
CREATE INDEX `amazon_listings_parent_asin_318fc513` ON `amazon_listings` (`parent_asin`);
CREATE INDEX `amazon_listing_pictures_asin_9a7f1e62` ON `amazon_listing_pictures` (`asin`);
CREATE INDEX `amazon_listing_pictures_picture_url_78f67a1c` ON `amazon_listing_pictures` (`picture_url`);
