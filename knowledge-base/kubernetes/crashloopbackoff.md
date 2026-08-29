# Kubernetes CrashLoopBackOff Troubleshooting Runbook

## Purpose

This runbook provides troubleshooting procedures for Kubernetes
pods experiencing CrashLoopBackOff.

## Symptoms

A pod repeatedly starts, crashes, and is restarted by Kubernetes.

Example:

kubectl get pods

NAME              READY   STATUS             RESTARTS
api-server-123    0/1     CrashLoopBackOff   5

## Troubleshooting Procedure

### 1. Check Pod Logs

Run:

kubectl logs <pod-name>

Review the logs for application errors, configuration problems,
missing dependencies, or failed connections.

### 2. Check Previous Container Logs

If the container has already restarted, run:

kubectl logs <pod-name> --previous

This displays logs from the previous failed container instance.

### 3. Describe the Pod

Run:

kubectl describe pod <pod-name>

Review the Events section for:

- Failed health checks
- Image errors
- Volume mount failures
- Resource problems
- Configuration errors

### 4. Check Environment Variables

Verify that required environment variables, ConfigMaps, and Secrets
are correctly configured.

### 5. Check Resource Limits

Review CPU and memory requests and limits.

A container exceeding its memory limit may be terminated with
OOMKilled.

Check with:

kubectl describe pod <pod-name>

### 6. Check Health Probes

Review:

- livenessProbe
- readinessProbe
- startupProbe

Incorrect probe configuration can repeatedly restart an otherwise
healthy application.

## Escalation

Escalate the incident if:

- Multiple applications are affected
- Multiple Kubernetes nodes are unhealthy
- The issue appears related to cluster networking or storage
- Production availability is significantly impacted