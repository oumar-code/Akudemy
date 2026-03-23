# Akudemy

Akudemy is a microservice in the Akulearn platform ecosystem. It provides core educational features and APIs for the Akudemy product.

## Features
- REST API for educational content
- Scalable Node.js backend

## Getting Started

### Prerequisites
- Node.js 20+
- Docker (optional)

### Development
```bash
git clone <repo-url>
cd Akudemy
npm install
npm run dev
```

### Docker
```bash
docker build -t akudemy:latest .
docker run -p 8084:8080 akudemy:latest
```

### Testing
```bash
npm test
```

## Deployment & Automation
CI/CD, linting, testing, Docker build, and docs build are automated via [GitHub Actions](.github/workflows/ci.yml).

### Automation Steps
- Automated tests (Jest)
- Linting (ESLint)
- Docker image build
- Placeholder for docs build
- Progress tracked in automation_progress.md

## License
MIT
