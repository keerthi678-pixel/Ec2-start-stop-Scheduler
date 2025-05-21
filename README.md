# Ec2-start-stop-Scheduler
To automate starting and stopping EC2 instances in a given region and schedule, using AWS Lambda + EventBridge (CloudWatch Events) — without manually specifying instance IDs.


 Step 1: Create IAM Role for Lambda
        
         Go to the IAM Console → Roles → Create Role
         
         Trusted Entity: Choose Lambda
         
         Attach Policies:
         
         Search and attach: AmazonEC2FullAccess
         
         Name it: LambdaEC2SchedulerRole
         
         Click Create Role
         
Step 2:  Step 2: Create the Lambda Function

         Go to the Lambda Console 
         
         Click Create Function
         
         Choose Author from Scratch
         
         Runtime: Python 3.12 (or 3.11/3.10)  
         
         Role: Use existing role
         
         Select: LambdaEC2SchedulerRole
         
         Click Create Function

Step 3:  Step 3: Add Code to Lambda

         Click Deploy to save
         

 Step 4: Create EventBridge Rule (Scheduler)
 
         🔸 For Starting EC2 Instances:
         
         Go to Amazon EventBridge → Rules → Create Rule
         
         Name: StartEC2Instances
         
         Type: Schedule
         
         Schedule Pattern:
         
         Choose cron and enter your desired time (e.g., every day at 8 AM UTC):
         cron(0 8 * * ? *)
         
         Target: Add target → Choose your Lambda function
         
         Constant (JSON text):
         
         {
         "region": "us-east-1",
          "action": "start"
         }
         
         Click Create

         🔸 For Stopping EC2 Instances:
         
         Repeat the same steps, with a different rule name and time:
         Name: StopEC2Instances
         
         Schedule: cron(0 20 * * ? *) (for 8 PM UTC)
         
         JSON Input:
         
         {
         "region": "us-east-1",
         "action": "stop"
         }  

 Step 5: Test Lambda 
 
         You can test manually from Lambda:
         
         Click Test in the Lambda Console
         
         Choose “Configure test event”
         
         Name: StartTest
         
         Input:
         
         {
         "region": "us-east-1",
         "action": "start"
         }
         
         Click Test
         
         Repeat with "action": "stop" to confirm stopping works.


