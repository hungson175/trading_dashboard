#!/bin/bash
# Check if a commit message was provided
if [ $# -eq 0 ]
  then
    echo "No commit message provided"
    exit 1
fi

COMMIT_MESSAGE=$1

# Define your variables
SERVER_IP="18.142.57.169"
PROJECT_PATH="/home/ubuntu/trading_dashboard"
SSH_KEY_PATH="../LightsailDefaultKey-ap-southeast-1.pem"
LOCAL_FILES=(
  "./.keys"
#  "/path/to/your/local/file2"
# Add more file paths as needed
)
SERVER_FILES=(
  # "/home/ubuntu/trading_dashboard/.keys"
#  "/path/to/your/server/file2"
# Add more file paths as needed
)

# Step 1: Commit and push local changes to GitHub
git add .
git commit -m "$COMMIT_MESSAGE"
git push origin master

# Step 2: Pull the latest code from the server
ssh -i $SSH_KEY_PATH ubuntu@$SERVER_IP "cd $PROJECT_PATH && git pull"

# Step 3: Install new requirements on the server
ssh -i $SSH_KEY_PATH ubuntu@$SERVER_IP "cd $PROJECT_PATH && pip install -r requirements.txt"

# Step 4: Copy necessary files to the server
for i in ${!LOCAL_FILES[@]}; do
  scp -i $SSH_KEY_PATH ${LOCAL_FILES[$i]} ubuntu@$SERVER_IP:${SERVER_FILES[$i]}
done

# Step 5: Kill the existing FastAPI service
ssh -i $SSH_KEY_PATH ubuntu@$SERVER_IP "pkill -f 'uvicorn main:app'"

# Step 6: Start the new FastAPI service using venv Python
ssh -i $SSH_KEY_PATH ubuntu@$SERVER_IP "cd $PROJECT_PATH && source venv/bin/activate && nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &"

# Step 7: Verify the service is running
ssh -i $SSH_KEY_PATH ubuntu@$SERVER_IP "ps aux | grep uvicorn"

echo "Deployment completed! FastAPI service has been restarted."
