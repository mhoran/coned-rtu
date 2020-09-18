coned-rtu
=========

A script for scraping ConEd real-time usage and writing to MySQL.

Environment Variables
---------------------

`CONED_USER`: ConEd username\
`CONED_PASS`: ConEd password\
`CONED_TOTP`: ConEd TOTP secret\
`OPOWER_ACCOUNT_ID`: Account ID for Opower API\
`OPOWER_METER`: Meter number for Opower API\
`MYSQL_USER`: User for connecting to MySQL\
`MYSQL_PASS`: Password for connecting to MySQL\
`MYSQL_HOST`: MySQL host\
`MYSQL_DB`: MySQL database name

Example Kubernetes Deployment
-----------------------------

```
apiVersion: v1
data:
  coned_pass: <base64-encoded-coned-password>
  coned_totp_secret: <base64-encoded-totp-secret>
  mysql_pass: <base64-encoded-mysql-password>
kind: Secret
metadata:
  name: coned-scrape-secrets
  namespace: default
type: Opaque
---
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  annotations:
  name: coned-scrape
  namespace: default
spec:
  concurrencyPolicy: Forbid
  failedJobsHistoryLimit: 1
  jobTemplate:
    metadata:
      creationTimestamp: null
    spec:
      backoffLimit: 0
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - env:
            - name: CONED_USER
              value: <email-address>
            - name: CONED_PASS
              valueFrom:
                secretKeyRef:
                  name: coned-scrape-secrets
                  key: coned_pass
            - name: CONED_TOTP
              valueFrom:
                secretKeyRef:
                  name: coned-scrape-secrets
                  key: coned_totp_secret
            - name: OPOWER_ACCOUNT_ID
              value: <opower-account-id>
            - name: OPOWER_METER
              value: "<opower-meter>"
            - name: MYSQL_USER
              value: <mysql-user>
            - name: MYSQL_PASS
              valueFrom:
                secretKeyRef:
                  name: coned-scrape-secrets
                  key: mysql_pass
            - name: MYSQL_HOST
              value: mysql-service
            - name: MYSQL_DB
              value: coned
            image: matthoran/coned-rtu
            imagePullPolicy: Always
            name: coned-scrape
            resources:
              requests:
                cpu: "0"
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
          dnsPolicy: ClusterFirst
          restartPolicy: Never
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
          volumes:
          - name: coned-scrape-secrets
            secret:
              defaultMode: 420
              secretName: coned-scrape-secrets
      ttlSecondsAfterFinished: 0
  schedule: "30 * * * *"
  successfulJobsHistoryLimit: 3
  suspend: false
```
