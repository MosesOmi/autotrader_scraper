# autotrader_scraper

Before beginning this project, a website needs to be chosen where data will be scraped from and analysed. I had decided to choose auto trader as I am a car fanatic and it is a website that provides concise detail on any vehicle of your choice.

I began by creating a Scraper class. This class will contain all the methods used to scrape data from auto trader. The first method created was one to bypass cookies. Other methods implemented included finding a car based on my location and retrieving the link to each car on a webpage after a search is carried out. The class is always initialised in the ‘ if __name__ == "__main__" ‘ block.

After a search is carried out, I not only retrieved the link for the details page of each car but I also created a function which retrieves text and image data from each page. Once the data was extracted, it was immediately stored in a dictionary before being saved locally in a JSON format. A method was also created that can find image links and download them from each page using the urllib library.

Once all functions were created, I added docstrings for each one to ensure that other users can understand. Unit tests were created in another file and ran to ensure that each method was returning the correct data type.

Once unit testing was complete, I created an S3 bucket on the AWS console. After creating this , I updated my code so that as it runs, it uploads my raw JSON and image data for each record to the S3 bucket using the AWS Python SDK and boto3. 

I also created a free tier micro RDS database as I converted my data into tables so I was now able to store any tabular data I had into this database. Pandas was used to create a data frame for each record then psycopg2 and sqlalchemy were used to upload to RDS.

A Dockerfile was then created to build the scraper locally before being pushed to Dockerhub. After this, an EC2 instance was created on the AWS console for the purpose of deploying my scraper. Docker was then installed on the EC2 instance so that my image could be pulled from Dockerhub.

Once all of this was done, a Prometheus container was set up to monitor the scraper. A docker container running Prometheus was created then the prometheus.yml config file was configured. A node exporter was then created to monitor hardware metrics while the scraper is running locally. The daemon file for the docker and the prometheus.yml was then configured so that the metrics for the container could be monitored. After observing these metrics I created a Grafana dashboard for them.

I lastly set up a CI/CD pipeline for the docker image. I started by setting up the relevant GitHub secrets that contained the required credentials to push to my Dockerhub account. A GitHub action was then created along with a cronjob that was set to restart the scraper every day.
