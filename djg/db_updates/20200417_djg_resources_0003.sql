BEGIN;
--
-- Add field site to amazonlisting
--
ALTER TABLE "amazon_listings" ADD COLUMN "site" varchar(32) NULL;
--
-- Add field site to amazonparentlisting
--
ALTER TABLE "amazon_parent_listings" ADD COLUMN "site" varchar(32) NULL;
COMMIT;
