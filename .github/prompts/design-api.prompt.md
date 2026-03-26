---
description: Design a REST or GraphQL API with OpenAPI spec generation
agent: API Design
---

# Design an API

Design a complete API based on the following requirements:

**API Requirements:** ${input:apiRequirements}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — coding style and project settings
   - `docs/PLAYBOOK.md` — architecture decisions and patterns
   - `docs/CODE_INVENTORY.md` — existing endpoints and models
   - `docs/API_DOCUMENTATION.md` — current API documentation and conventions

2. **Gather and clarify requirements:**
   - Identify the core resources and their relationships
   - Define the target consumers (frontend, mobile, third-party, internal)
   - Determine authentication and authorization requirements
   - Establish rate limiting and pagination needs

3. **Design the resource model:**
   - Define each resource with its properties and types
   - Map relationships: one-to-one, one-to-many, many-to-many
   - Design request and response schemas with validation rules
   - Plan for versioning strategy (URL path, header, or query param)

4. **Define endpoints:**
   - Follow RESTful conventions: proper HTTP methods and status codes
   - Design consistent URL patterns (`/resources`, `/resources/{id}`)
   - Plan query parameters for filtering, sorting, and searching
   - Define error response format with actionable error codes

5. **Security review:**
   - Specify authentication mechanism (JWT, OAuth2, API key)
   - Define authorization rules per endpoint and role
   - Plan input validation and sanitization for all parameters
   - Address OWASP API Security Top 10 risks

6. **Generate the OpenAPI specification:**
   - Produce a valid OpenAPI 3.0+ spec in YAML format
   - Include schemas, examples, and descriptions for every endpoint
   - Document error responses for each endpoint
   - Add security scheme definitions

7. **Update documentation:**
   - Append the API design to `docs/API_DOCUMENTATION.md`
   - Include example request/response pairs for each endpoint
   - Document rate limits, pagination patterns, and error handling

8. **Report results:**
   - Summary of designed resources and endpoints
   - OpenAPI spec file location
   - Security considerations and recommendations
   - Suggested implementation order (dependencies between endpoints)
