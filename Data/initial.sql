CREATE DATABASE bizpulse_dwh;

-- Skema untuk menampung data mentah hasil extract dari MySQL
CREATE SCHEMA IF NOT EXISTS staging;

-- Skema untuk menampung Star Schema (Fact & Dimension) hasil transformasi
CREATE SCHEMA IF NOT EXISTS analytics;