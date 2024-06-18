# System Design: Live-Assistant Platform Utilizing Generative AI

## Overview

The Live-Assistant Platform aims to allow companies to create and deploy their own AI agents using generative AI systems like ChatGPT, Gemini, or LLaMA3. These AI agents can be embedded as chat boxes on the companies' landing pages, providing live assistance to end-users by answering questions based on the knowledge fed by the companies.

## Components

### 1. Admin Portal
- **User Management:** Admins can manage companies.
- **Agent Management:** Admins can monitor and control AI agents created by companies and manage end-users who interact with the agents.
- **Analytics:** Admins can view usage statistics, performance metrics, and other relevant data.

### 2. Company Portal
- **Agent Configuration:** Companies can create and configure their AI agents, feeding them specific data and knowledge.
- **Agent Management:** Companies can manage their AI agents, including updating the knowledge base and setting interaction protocols.
- **User Management:** Companies can view and manage end-users who interact with their agents.
- **Analytics:** Companies can access detailed analytics about their agents' performance and user interactions.

### 3. Embedded AI Agent
- **JavaScript Widget:** An embeddable JavaScript widget that companies can integrate into their landing pages.
- **Chat Interface:** A user-friendly chat interface for end-users to interact with the AI agent.
- **Real-time Interaction:** The AI agent responds to user queries in real-time using the knowledge fed by the company.

## Architecture

### 1. Frontend

#### Admin Portal
- **Framework:** React.js
- **Components:** User management, agent management, analytics dashboards
- **APIs:** Interact with backend services for managing companies, agents, and end-users

#### Company Portal
- **Framework:** React.js
- **Components:** Agent configuration, user management, analytics dashboards
- **APIs:** Interact with backend services for managing agents and viewing analytics

#### Embedded AI Agent
- **Framework:** Vanilla JavaScript/React.js
- **Components:** Chat box UI, interaction handler
- **APIs:** Interact with backend AI services to fetch responses

### 2. Backend

#### Services
- **User Management Service:** Handles CRUD operations for admin and company accounts.
- **Agent Management Service:** Manages the creation, configuration, and deployment of AI agents.
- **Knowledge Base Service:** Stores and retrieves knowledge fed by companies.
- **AI Integration Service:** Interfaces with generative AI models like ChatGPT, Gemini, or LLaMA3 to process user queries and generate responses.
- **Retrieval-Augmented Generation (RAG) Service:** Utilizes LLaMA Index or LangChain to enhance the AI agent's responses with relevant information from the knowledge base.
- **Analytics Service:** Collects and processes data for usage statistics and performance metrics.

#### Databases
- **User Database:** Stores information about admins and companies.
- **Agent Database:** Stores configuration details and metadata of AI agents.
- **Knowledge Base:** Stores the data and knowledge fed by companies.
- **Analytics Database:** Stores interaction logs, usage statistics, and performance metrics.
- **Short-term Memory Store:** Redis, used for storing short-term memory of each end-user of each agent with a TTL of 1 day.

### 3. Infrastructure

#### Hosting
- **Cloud Provider:** AWS/GCP/Azure
- **Services:** EC2/VMs, S3/Blob Storage, RDS/Cloud SQL, Redis for short-term memory storage

#### Security
- **Authentication:** OAuth2.0, JWT
- **Authorization:** Role-based access control (RBAC)
- **Data Encryption:** TLS/SSL for data in transit, AES for data at rest

### 4. APIs

#### Admin API
- **Endpoints:**
  - `POST /admin/login`: Authenticate an admin.
  - `GET /admin/companies`: Retrieve a list of all companies.
  - `POST /admin/companies`: Create a new company.
  - `DELETE /admin/companies/{companyId}`: Delete a company.
  - `GET /admin/agents`: Retrieve a list of all AI agents.
  - `GET /admin/agents/{agentId}/users`: Retrieve a list of all end-users for a specific AI agent.
  - `GET /admin/analytics`: Retrieve platform-wide analytics.

- **Authentication:** Admin-level access tokens

#### Company API
- **Endpoints:**
  - `POST /company/login`: Authenticate a company user.
  - `GET /company/agents`: Retrieve a list of all AI agents for the company.
  - `POST /company/agents`: Create a new AI agent.
  - `PUT /company/agents/{agentId}`: Update an AI agent.
  - `DELETE /company/agents/{agentId}`: Delete an AI agent.
  - `POST /company/agents/{agentId}/knowledge`: Update​⬤