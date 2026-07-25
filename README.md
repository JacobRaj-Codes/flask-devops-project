# Flask DevOps Pipeline Project

A containerized Python Flask REST API with a full CI/CD pipeline: automated
testing, static code analysis via **SonarCloud**, Docker image builds, and
container vulnerability scanning via **Trivy**.

## Stack
Python · Flask · Docker · GitHub Actions · SonarCloud · Trivy

## Architecture

```
Push to GitHub
      │
      ▼
 ┌─────────┐     ┌───────────────┐     ┌───────────────┐     ┌─────────────┐
 │  Tests   │ ──▶ │  SonarCloud    │ ──▶ │ Docker Build   │ ──▶ │ Trivy Scan   │
 │ (pytest) │     │ (code quality) │     │ (push to GHCR) │     │ (image scan) │
 └─────────┘     └───────────────┘     └───────────────┘     └─────────────┘
```

## API Endpoints

| Method | Path            | Description        |
|--------|-----------------|---------------------|
| GET    | `/health`       | Health check        |
| GET    | `/tasks`        | List all tasks      |
| GET    | `/tasks/<id>`   | Get a single task   |
| POST   | `/tasks`        | Create a task       |
| DELETE | `/tasks/<id>`   | Delete a task        |

## Local Development

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Run the app
python app/app.py                 # http://localhost:5000

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing
```

## Run with Docker

```bash
docker build -t flask-devops-app .
docker run -p 5000:5000 flask-devops-app
curl http://localhost:5000/health
```

## Setting Up the CI/CD Pipeline

### 1. Push this repo to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Flask API with CI/CD pipeline"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Set up SonarCloud (free for public repos)
1. Go to [sonarcloud.io](https://sonarcloud.io) and sign in with GitHub.
2. Click **+ > Analyze new project**, select your repo, and import it.
3. Choose **"With GitHub Actions"** as the analysis method — SonarCloud will
   show you your **Organization Key** and **Project Key**.
4. Update `sonar-project.properties` in this repo with those values.
5. Go to **My Account > Security** on SonarCloud and generate a token.
6. In your GitHub repo: **Settings > Secrets and variables > Actions > New
   repository secret**, add it as `SONAR_TOKEN`.

### 3. Container registry (GitHub Container Registry)
No setup needed — the workflow uses the built-in `GITHUB_TOKEN` to push
images to `ghcr.io` automatically. Images will appear under your GitHub
profile's **Packages** tab.

> Prefer Docker Hub instead? Swap the `docker/login-action` step to use
> `docker.io` with `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` secrets.

### 4. Trigger the pipeline
Push to `main` or open a pull request — the workflow at
`.github/workflows/ci-cd.yml` runs automatically. Check the **Actions** tab
to watch it, and the **Security > Code scanning** tab for Trivy's results.

## Roadmap / Ideas to Extend This Project
- [ ] Add a quality gate that fails the build if SonarCloud coverage drops below a threshold
- [ ] Set `exit-code: 1` in the Trivy step to fail builds on CRITICAL/HIGH vulnerabilities
- [ ] Deploy the built image to a live environment (Render, Fly.io, AWS ECS)
- [ ] Add a `docker-compose.yml` for local multi-service development
- [ ] Add rate limiting / request validation with `flask-limiter` and `marshmallow`
