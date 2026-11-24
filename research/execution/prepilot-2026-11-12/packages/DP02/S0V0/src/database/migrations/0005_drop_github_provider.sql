-- PostgreSQL cannot drop an individual enum value. Keep this historical entry;
-- migration 0009 recreates the provider enum without 'github'.
SELECT 1;
