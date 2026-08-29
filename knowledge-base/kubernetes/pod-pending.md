# Kubernetes Pod Pending Troubleshooting Runbook

## Purpose

This runbook provides troubleshooting procedures for Kubernetes pods that remain in the Pending state.

## Symptoms

A pod has been created but is not being scheduled onto a Kubernetes worker node.

Example:

kubectl get pods

NAME             READY   STATUS    RESTARTS
payment-api      0/1     Pending   0

## Troubleshooting Procedure

### 1. Describe the Pod

Run:

kubectl describe pod <pod-name>

Review the Events section for scheduling errors.

Common messages include:

- Insufficient CPU
- Insufficient memory
- Node selector mismatch
- Untolerated taints
- PersistentVolumeClaim not bound

### 2. Check Node Resources

Run:

kubectl get nodes

Then:

kubectl top nodes

Determine whether worker nodes have enough CPU and memory available.

### 3. Check Taints and Tolerations

Run:

kubectl describe node <node-name>

Check whether node taints are preventing the pod from being scheduled.

### 4. Check Persistent Storage

Run:

kubectl get pvc

Verify that required PersistentVolumeClaims are successfully bound.

### 5. Check Scheduling Requirements

Review the pod configuration for:

- nodeSelector
- nodeAffinity
- podAffinity
- podAntiAffinity
- topology constraints

Incorrect scheduling requirements can prevent Kubernetes from finding an eligible node.

## Escalation

Escalate if multiple workloads cannot be scheduled or if the cluster does not have sufficient compute capacity.