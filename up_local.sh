# Ensure docker is installed and running
echo Running the following command: docker build -t task-nest .
sudo docker build -t task-nest .
echo "Running the following command: docker run -d -p 3000:3000 task-nest"
sudo docker run -d -p 3000:3000 task-nest
