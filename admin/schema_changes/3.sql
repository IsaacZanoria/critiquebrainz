BEGIN;

ALTER TABLE review DROP COLUMN is_archived;

COMMIT;