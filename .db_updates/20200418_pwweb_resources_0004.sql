BEGIN;
--
-- Rename field site on amazonlisting to domain
--
ALTER TABLE "amazon_listings" RENAME COLUMN "site" TO "domain";
--
-- Rename field site on amazonparentlisting to domain
--
ALTER TABLE "amazon_parent_listings" RENAME COLUMN "site" TO "domain";
COMMIT;
