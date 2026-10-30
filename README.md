# Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible

## 📌 Project Overview

This project implements a self-healing infrastructure workflow that monitors an NGINX web service, detects failures, and automatically attempts recovery using Prometheus, Alertmanager, a Python Flask webhook, and Ansible.

The system continuously checks the availability of the NGINX website. When a failure is detected, Prometheus generates an alert, Alertmanager forwards it to the recovery webhook, and Ansible executes a playbook to restart the failed NGINX container.

## 🎯 Objectives

- Monitor web service availability using Prometheus.
- Detect NGINX failures using Blackbox Exporter.
- Generate and route alerts through Alertmanager.
- Automate service recovery using Ansible.
- Containerize the components using Docker Compose.
- Reduce manual intervention during service failures.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Prometheus | Monitoring and alert evaluation |
| Blackbox Exporter | HTTP health checks |
| Alertmanager | Alert routing |
| Python Flask | Recovery webhook |
| Ansible | Automated recovery playbook |
| NGINX | Web server |
| Git & GitHub | Version control and source hosting |

## 🏗️ Architecture

```text
              User / Browser
                    |
                    v
              NGINX Container
                    |
            HTTP Health Check
                    |
                    v
             Blackbox Exporter
                    |
                    v
                Prometheus
                    |
             NGINX Down Alert
                    |
                    v
               Alertmanager
                    |
              Webhook Request
                    |
                    v
           Python Flask Webhook
                    |
                    v
             Ansible Playbook
                    |
                    v
          Restart NGINX Container
                    |
                    v
           Health Check Succeeds
```

## ⚙️ Project Structure

```text
self-healing-infrastructure/
├── docker-compose.yml
├── nginx/
│   └── index.html
├── prometheus/
│   ├── prometheus.yml
│   ├── blackbox.yml
│   └── alert-rules.yml
├── alertmanager/
│   └── alertmanager.yml
├── recovery/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── ansible/
│   └── restart-nginx.yml
├── screenshots/
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Install the following on the machine where you want to run the project:

- Docker Desktop on Windows, or Docker Engine on Linux
- Docker Compose
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/ragulm456/self-healing-infrastructure.git
cd self-healing-infrastructure
```

### 2. Start the services

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

### 3. Access the services

| Service | Local URL |
|---|---|
| NGINX website | http://localhost:8085 |
| Prometheus | http://localhost:9090 |
| Prometheus targets | http://localhost:9090/targets |
| Alertmanager | http://localhost:9093 |
| Blackbox Exporter | http://localhost:9115 |

The Flask recovery webhook listens on port `5000`. It is intended for internal communication within the Docker Compose network.

## 🧪 Testing the Self-Healing Workflow

### Step 1: Verify NGINX

Open http://localhost:8085 and confirm that the website loads.

### Step 2: Simulate a failure

Run the following command in a terminal:

```bash
docker stop self-healing-nginx
```

### Step 3: Observe the alert

Open Prometheus at http://localhost:9090 and query:

```promql
probe_success{job="nginx-health"}
```

A value of `0` indicates a failed HTTP probe. After the configured alert duration, the `NginxDown` alert should fire.

Check Alertmanager at http://localhost:9093.

### Step 4: Verify automated recovery

View the recovery webhook logs:

```bash
docker logs self-healing-recovery --tail 50
```

The Flask webhook should receive the firing alert and execute the Ansible playbook.

### Step 5: Verify the service

Check the container:

```bash
docker ps --filter "name=self-healing-nginx"
```

Then open http://localhost:8085 again. After successful recovery, the website should load.

**Expected result:** NGINX is restarted automatically after the monitoring and alerting pipeline detects a failure.

## ✅ Implementation Results

- Configured HTTP health checks using Blackbox Exporter.
- Configured Prometheus alert rules for NGINX failure detection.
- Routed firing alerts to a Python Flask webhook through Alertmanager.
- Executed an Ansible playbook to restart the NGINX container.
- Verified recovery through container status, HTTP response status, and Prometheus probe results.

## 🔒 Security Considerations

- The recovery container mounts the Docker socket, which grants


