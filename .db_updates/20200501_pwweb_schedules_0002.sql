BEGIN;
--
-- Alter unique_together for version (0 constraint(s))
--
ALTER TABLE "sched_versions" DROP CONSTRAINT "sched_versions_project_version_9329c495_uniq";
--
-- Create constraint unique_project_version on model version
--
ALTER TABLE "sched_versions" ADD CONSTRAINT "unique_project_version" UNIQUE ("project", "version");
COMMIT;
