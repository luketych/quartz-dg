Project Configuration with Hybrid .env and Config Pattern

Purpose

This document outlines a robust configuration management approach for a Node.js project using a hybrid pattern that combines the simplicity of .env files with the clarity and scalability of a central config module.

This strategy improves:
	•	Environment-specific flexibility
	•	Code readability and consistency
	•	Validation of required variables
	•	Testability and mocking

⸻

Technologies Used
	•	dotenv: Loads environment variables from a .env file.
	•	process.env: Built-in Node.js API for accessing environment variables.
	•	JavaScript/TypeScript: Configuration module can be written in either.
	•	Optional schema validation: Libraries like zod or joi can validate config structure.

⸻

Implementation

Step 1: Install dotenv

npm install dotenv

Step 2: Create .env

API_KEY=abc123
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASS=secret
ENABLE_COOL_FEATURE=true

Step 3: Create config/index.js or config/index.ts

// config/index.js
import dotenv from 'dotenv';
dotenv.config();

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

export const config = {
  env: process.env.NODE_ENV || 'development',
  apiKey: requireEnv('API_KEY'),
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    user: requireEnv('DB_USER'),
    pass: requireEnv('DB_PASS'),
  },
  featureFlags: {
    enableCoolFeature: process.env.ENABLE_COOL_FEATURE === 'true',
  },
};

Step 4: Use in Project Code

import { config } from './config';

console.log(config.db.host);


⸻

Optional Enhancements
	•	Add schema validation with zod or joi to validate config structure.
	•	Load .env.production, .env.test, etc., based on NODE_ENV.
	•	Freeze the config object using Object.freeze(config) to prevent mutation.
	•	Use TypeScript for full static typing support.

⸻

Testing Strategy

Unit Tests
	1.	Test Default Values:
	•	Assert that fallback defaults are applied if optional env vars are missing.
	2.	Test Required Variables:
	•	Confirm requireEnv() throws an error if a required variable is not set.
	3.	Test Config Output Shape:
	•	Ensure config has the expected keys and types.
	4.	Test Feature Flags:
	•	Simulate various combinations of flags like ENABLE_COOL_FEATURE.

Integration Tests
	1.	Startup Tests:
	•	Run the app with different .env files and assert that it boots with correct config.
	2.	Environment Switching:
	•	Use NODE_ENV=test or NODE_ENV=production and confirm appropriate config is loaded.
	3.	Mocking process.env:
	•	In test runners like Mocha or Vitest, stub process.env to simulate missing or malformed values.

Static Checks
	•	Add a linter rule or CI check that ensures no direct usage of process.env outside the config module.

⸻

Summary

Feature	.env Only	Config Only	Hybrid (Recommended)
Centralized Access	❌	✅	✅
Required Var Checks	❌	✅	✅
Support for Secrets & CI/CD	✅	✅	✅
Supports Refactoring	❌	✅	✅
Test-Friendly	❌	✅	✅

This hybrid approach is scalable, developer-friendly, and production-ready. It balances environment flexibility with programmatic control and offers a maintainable foundation for configuration management in modern Node.js applications.
