# EC2 High CPU Troubleshooting Runbook

## Purpose

This runbook provides procedures for investigating sustained high CPU utilization on Amazon EC2 instances.

## Symptoms

CloudWatch reports CPUUtilization consistently above 80 percent.

Possible symptoms include:

- Slow application response
- Increased request latency
- Application timeouts
- Instance health degradation

## Troubleshooting Procedure

### 1. Review CloudWatch Metrics

Check:

- CPUUtilization
- NetworkIn
- NetworkOut
- DiskReadOps
- DiskWriteOps

Determine when CPU utilization increased and whether other metrics changed at the same time.

### 2. Connect to the Instance

Connect through AWS Systems Manager Session Manager or SSH when permitted.

Run:

top

or:

htop

Identify processes consuming excessive CPU.

### 3. Review Application Logs

Check application and system logs for:

- Increased traffic
- Application errors
- Background jobs
- Runaway processes

### 4. Review Traffic

Determine whether high CPU corresponds with legitimate increases in application traffic.

Review load balancer request metrics when applicable.

### 5. Evaluate Scaling

If high utilization results from legitimate traffic growth, evaluate:

- EC2 Auto Scaling
- Scaling policies
- Instance size
- Application optimization

## Escalation

Escalate when CPU utilization causes production degradation or the underlying process cannot be identified.