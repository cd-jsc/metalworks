-- Database initialization script for Inventory Management System
-- This script will be executed when the PostgreSQL container starts

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The Django migrations will handle creating the actual tables
-- This script is mainly for any initial setup or data seeding

-- You can add initial data here if needed
-- For example:

-- INSERT INTO auth_user (username, email, is_staff, is_active, is_superuser, date_joined, password)
-- VALUES ('admin', 'admin@example.com', true, true, true, NOW(), 'pbkdf2_sha256$...');

-- Note: The above is just an example. In practice, you should use Django's
-- createsuperuser command or fixtures for initial data.