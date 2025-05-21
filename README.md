---

# Ec2-start-stop-Scheduler

Automate starting and stopping EC2 instances in a given region and on a schedule, using AWS Lambda + EventBridge (CloudWatch Events) — without manually specifying instance IDs.

---

## Step 1: Create IAM Role for Lambda

1. Go to the IAM Console → Roles → Create Role
2. Trusted Entity: Choose Lambda
3. Attach Policies:
    - Search and attach: **AmazonEC2FullAccess**
4. Name it: `LambdaEC2SchedulerRole`
5. Click **Create Role**

---

## Step 2: Create the Lambda Function

1. Go to the Lambda Console
2. Click **Create Function**
3. Choose **Author from Scratch**
4. Runtime: Python 3.12 (or 3.11/3.10)
5. Role: Use existing role  
    - Select: `LambdaEC2SchedulerRole`
6. Click **Create Function**

---

## Step 3: Add Code to Lambda

1. Add your Lambda code (see [lambda_function.py](lambda_function.py) or insert your logic).
2. Click **Deploy** to save.

---

## Step 4: Create EventBridge Rule (Scheduler)

### For Starting EC2 Instances

1. Go to Amazon EventBridge → Rules → Create Rule
2. Name: `StartEC2Instances`
3. Type: **Schedule**
4. Schedule Pattern:  
    - Choose **cron** and enter your desired time (e.g., every day at 8 AM UTC):
      ```
      cron(0 8 * * ? *)
      ```
5. Target: Add target → Choose your Lambda function
6. Constant (JSON text):
    ```json
    {
      "region": "us-east-1",
      "action": "start"
    }
    ```
7. Click **Create**

### For Stopping EC2 Instances

1. Repeat the steps above with a different rule name and time:
    - Name: `StopEC2Instances`
    - Schedule: `cron(0 20 * * ? *)` (for 8 PM UTC)
    - JSON Input:
      ```json
      {
        "region": "us-east-1",
        "action": "stop"
      }
      ```

---

## Step 5: Test Lambda

You can test manually from Lambda:

1. Click **Test** in the Lambda Console
2. Choose **Configure test event**
3. Name: `StartTest`
4. Input:
    ```json
    {
      "region": "us-east-1",
      "action": "start"
    }
    ```
5. Click **Test**
6. Repeat with `"action": "stop"` to confirm stopping works.

---

### Notes

- Make sure the AWS region matches your EC2 instances.
- For production, use least privilege for IAM roles.
- Add logging and error handling to your Lambda code for easier debugging and monitoring.

---
