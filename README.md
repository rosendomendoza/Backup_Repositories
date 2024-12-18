# 🚀 Bjumper Backend Test: GitHub Backup API 🚀

## ⚙️ Features

- 📂 *Fetch Users*: Retrieve user information and their linked repositories from the GitHub API.
- 🔒 *Backup Users*: Store user data, including GitHub URL, as a backup in the database.
- 🗑️ *Delete User Backup*: Remove a user backup and all their linked repositories from the database.
- 📦 *Backup Repositories*: Validate ownership and store repositories linked to users in the database.
- 🗑️ *Delete Repositories*: Delete a backed-up repository from the database.

## 👨🏻‍🔬 User Stories

1. *As a* user,
   *I want to* fetch user information from GitHub,
   *So that* I can display their repositories.

2. *As a* user,
   *I want to* back up user data in the database,
   *So that* I can preserve key GitHub user information.

3. *As a* user,
   *I want to* delete a user backup and their repositories,
   *So that* I can manage and clean up backed-up data.

4. *As a* user,
   *I want to* back up repositories linked to GitHub users,
   *So that* I can store essential repository information.

5. *As a* user,
   *I want to* delete repository backups,
   *So that* I can remove unwanted repository records.

---

## 🌐 API Endpoints

| Endpoint                       | Method | Input                 | Description                                |
|--------------------------------|--------|-----------------------|--------------------------------------------|
| /api/users/fetch/            | GET    | username            | Fetch user information and repositories.   |
| /api/users/backup/           | POST   | username            | Back up a GitHub user in the database.     |
| /api/users/delete_backup/    | DELETE | username            | Delete a user backup and their repositories. |
| /api/repositories/backup/    | POST   | github_url, username | Back up a repository.                      |
| /api/repositories/delete/    | DELETE | github_url      | Delete a repository backup.                |

---

## 🚀 Deployment

This project uses *Docker* and *Docker Compose* for containerized development and deployment.

### 🔑 Prerequisites

- *Docker Desktop*: [Install Docker Desktop](https://www.docker.com/products/docker-desktop).
- *Docker Compose*: Included with Docker Desktop.

---

## 🌐 Getting Started

Follow these steps to get the project up and running:

### 💻 Installing

1. Clone the repository:

   bash

   `git clone https://github.com/rosendomendoza/Bjumper_Backend_Test`

   `cd Bjumper_Backend_Test`

2.	Add your environment variables in a .env file:

  ```
  POSTGRES_DB=postgres
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres
  POSTGRES_HOST=db
  POSTGRES_PORT=5432
  DEBUG=True
  ```

3.	Build the containers images:

  `docker-compose build`

4. Run the containers in background mode:

  `docker-compose up -d`

## 🔍 Testing

  `docker-compose exec web pytest`