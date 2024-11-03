# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:
Here I assume that the cost is for production level (P1)

| Azure Resource           | Service Tier                              | Monthly Cost |
|--------------------------|-------------------------------------------|-------------|
| *Azure Postgres Database* | General Purpose, 4 vCores, 128 GB Storage | $549.20    |
| *Azure Service Bus*      | Premium, 1 Daily Message Unit | $668.00       |
| *Azure App Service*      | Premium v3 (P0V3): 1 Core, 4 GB RAM, 250 GB Storage   | $61.32        |
| *Azure Function*         | Premium EP1: 1 Core, 3.5 GB Ram, 250 GB Storage                               | $310.54     |
| *Azure App Service Plan* | Premium P0v3: 1 Cỏe, 4 GB Ram, 250 GB Storage                           | $61.32       |

## Architecture Explanation
Azure Web App provides a fully managed environment for developers to build and deploy web applications without worrying about the underlying infrastructure. It's well-suited for small-scale applications that require minimal maintenance. With Azure Web App, developers can host the entire source code, including HTML, CSS, JavaScript, and other frontend components, ensuring the application performs well and responds quickly to user actions.

On the other hand, Azure Function is a serverless computing service designed to execute small pieces of code in response to specific events, like data changes, user actions, or scheduled triggers. It’s particularly useful for handling asynchronous operations that run in the background without disrupting the user experience. By leveraging Azure Function, developers can offload time-consuming tasks, like sending large volumes of emails, to ensure the main application remains responsive.

To summarize, Azure Web App is an excellent choice for straightforward applications with low maintenance needs, while Azure Function is perfect for background tasks that improve performance without affecting frontend responsiveness. By combining these tools thoughtfully, developers can create an optimized and scalable application system.