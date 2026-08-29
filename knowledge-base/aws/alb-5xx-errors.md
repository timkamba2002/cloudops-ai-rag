# Application Load Balancer 5XX Troubleshooting Runbook

## Purpose

This runbook provides troubleshooting procedures for elevated HTTP 5XX errors involving an AWS Application Load Balancer.

## Symptoms

Users experience:

- HTTP 500 errors
- HTTP 502 errors
- HTTP 503 errors
- HTTP 504 errors

## Troubleshooting Procedure

### 1. Review CloudWatch Metrics

Check ALB metrics including:

- HTTPCode_ELB_5XX_Count
- HTTPCode_Target_5XX_Count
- HealthyHostCount
- UnHealthyHostCount
- TargetResponseTime

Determine whether errors originate from the load balancer or application targets.

### 2. Check Target Group Health

Review the target group associated with the load balancer.

Verify that application targets are healthy.

Investigate failed health checks.

### 3. Check Application Logs

If HTTPCode_Target_5XX_Count is elevated, review application logs on the backend targets.

Look for:

- Application exceptions
- Database connection failures
- Dependency failures
- Resource exhaustion

### 4. Investigate 503 Errors

HTTP 503 errors may occur when the load balancer does not have healthy targets available.

Verify:

- Target registration
- Health check configuration
- Security groups
- Application availability

### 5. Investigate 504 Errors

HTTP 504 errors may indicate that a target did not respond before the load balancer timeout.

Review:

- TargetResponseTime
- Application latency
- Database latency
- External dependencies

## Escalation

Escalate when 5XX errors exceed the production alert threshold or significantly impact customer traffic.