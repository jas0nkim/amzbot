BEGIN;
--
-- Alter field upc on item
--
ALTER TABLE "resrc_items" ALTER COLUMN "upc" TYPE varchar(20) USING "upc"::varchar(20);
COMMIT;
