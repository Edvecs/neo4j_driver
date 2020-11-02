# neo4j_driver
Connect to neo4j driver with serverless.

The task is to create a Lambda function which can connect to a Neo4j database.

## Set up the development environment

There are several ways to implement end to end automation of setting up a Lambda function.

You can use Cloudformation, Terraform. There is an end to end solution example for Terraform on this link: https://learn.hashicorp.com/tutorials/terraform/lambda-api-gateway

What I found the easiest to start from scratch is the Serverless framework:

https://www.npmjs.com/package/serverless

To set up the serverless you have to install it:

```$ npm install -g serverless```

The working directory is: 

```$ cd neo4j```

Because this implementation uses Python and we use custom modules you will need to install a serverless plugin to installed:

```$ sls plugin install -n serverless-python-requirements```

Before you deploy the service you should set up the user credentials from command line:

```$ serverless config credentials --provider aws --key <KEY> --secret <SECRET>```

*Note:* The best would have been if we set up a service user with the right policies (SSM parameter access, AWS logs, etc... ) in advance.

## Work with the Lambda function

To test the service before deploying it:

```$ serverless invoke local --data '{"body": "{\"database\": \"movies\"}"}' --function main ```

If you want to set up the service from this git project you should run:

```$ serverless deploy ```

After a successful deploy check if the "lambda_ssm_full_access" role assigned to the lambda function.

## Test

To test your deployed service you can use curl with POST-ing a json request:

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"database": "movies"}' \
 https://<YOUR_API_GATEWAY_URI>/
```

The Gateway URI can be collected from the AWS Lambda function page or displayed after a successful serverless deploy.

## Testing, monitoring and logging

* With Python I could have add unit tests combined with Magic Mock
* Monitoring can be done with the build in Cloudwatch:  https://aws.amazon.com/cloudwatch/
* Amazon collects audit logs which can be collected and reached. Cloudwatch uses the same logs.

## Useful pages:
* AWS with Python: https://www.scalyr.com/blog/aws-lambda-with-python/
* Add database to the Neo4j module: https://towardsdatascience.com/neo4j-cypher-python-7a919a372be7
* Maybe this is the right approach to the JWT encryption: https://www.serverless.com/examples/aws-python-auth0-custom-authorizers-api
* AWS SAM seems to me as a good approach for development and deployed: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html

