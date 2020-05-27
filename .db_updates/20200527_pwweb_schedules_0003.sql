BEGIN;
--
-- Alter field added_at on version
--
ALTER TABLE "sched_versions" ALTER COLUMN "added_at" DROP NOT NULL;
COMMIT;
