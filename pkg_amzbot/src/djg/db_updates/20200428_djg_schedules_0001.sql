BEGIN;
--
-- Create model Job
--
CREATE TABLE "sched_jobs" ("job_id" varchar(64) NOT NULL PRIMARY KEY, "project" varchar(32) NOT NULL, "spider" varchar(32) NOT NULL, "version" varchar(32) NULL, "settings" jsonb NULL, "other_params" jsonb NULL, "start_time" timestamp with time zone NULL, "end_time" timestamp with time zone NULL, "status" smallint NOT NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL);
--
-- Create model Version
--
CREATE TABLE "sched_versions" ("id" serial NOT NULL PRIMARY KEY, "project" varchar(32) NOT NULL, "version" varchar(32) NOT NULL, "status" smallint NOT NULL, "added_at" timestamp with time zone NOT NULL, "deleted_at" timestamp with time zone NULL);
CREATE INDEX "sched_jobs_job_id_5fe6c472_like" ON "sched_jobs" ("job_id" varchar_pattern_ops);
CREATE INDEX "sched_jobs_project_7e23038b" ON "sched_jobs" ("project");
CREATE INDEX "sched_jobs_project_7e23038b_like" ON "sched_jobs" ("project" varchar_pattern_ops);
CREATE INDEX "sched_jobs_spider_4be7c654" ON "sched_jobs" ("spider");
CREATE INDEX "sched_jobs_spider_4be7c654_like" ON "sched_jobs" ("spider" varchar_pattern_ops);
ALTER TABLE "sched_versions" ADD CONSTRAINT "sched_versions_project_version_9329c495_uniq" UNIQUE ("project", "version");
CREATE INDEX "sched_versions_project_85b224db" ON "sched_versions" ("project");
CREATE INDEX "sched_versions_project_85b224db_like" ON "sched_versions" ("project" varchar_pattern_ops);
CREATE INDEX "sched_versions_version_de6b638c" ON "sched_versions" ("version");
CREATE INDEX "sched_versions_version_de6b638c_like" ON "sched_versions" ("version" varchar_pattern_ops);
COMMIT;
