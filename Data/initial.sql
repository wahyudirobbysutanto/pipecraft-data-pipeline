-- Schema for staging tables (raw data from source systems)
CREATE SCHEMA IF NOT EXISTS staging;

-- Schema for analytics tables (Star Schema - Fact & Dimension) hasil transformasi
CREATE SCHEMA IF NOT EXISTS analytics;