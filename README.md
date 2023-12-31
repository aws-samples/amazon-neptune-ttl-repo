THIS REPO IS UNDER CONSTRUCTION. CHECK BACK FOR UDPATES.

## Time-to-Live (TTL) in Amazon Neptune

This repo is a code sample accompanying the blog post (TODO - URL). The following are instructions to setup the TTL sample. 

## Prerequisites
To run this example, you need an AWS account with permission to create resources such as a Neptune cluster. 

## Provision resources 
We provide two configurations. 

We encourage you to review the stack with your security team prior to using it in a production environment.

### Provision New Neptune Cluster and Supporting TTL Resources
If you do not already have a Neptune cluster, we recommend using this option. 

Download a copy of the CloudFormation template (cfn/neptune_ttl_main.yaml) from this repository. Then complete the following steps:

1.	On the AWS CloudFormation console, choose **Create stack**.
2.	Choose **With new resources (standard)**.
3.	Select **Upload a template file**.  
4.	Choose **Choose file** to upload the local copy of the template that you downloaded. The name of the file is neptune_ttl_main.yaml. 
5.	Choose **Next**.
6.	Enter a stack name of your choosing. 
7.	In the **Parameters** section, enter a value for ApplicationID. For the remaining parameters, use defaults.
8.	Choose **Next**.
9.	Continue through the remaining sections.
10.	Read and select the check boxes in the **Capabilities** section.
11.	Choose **Create stack**.
12.	When the stack is complete, navigate to the **Outputs** section and follow the link for the output NeptuneSagemakerNotebook. 

This opens in your browser the Jupyter files view. 

### Provision TTL Resources for Existing Neptune Cluster
If you already have a Neptune cluster, you may use this option. 

Download a copy of the CloudFormation template (cfn/neptune_ttl_main-existing.yaml) from this repository. Then complete the following steps:

1.	On the AWS CloudFormation console, choose **Create stack**.
2.	Choose **With new resources (standard)**.
3.	Select U**pload a template file**.  
4.	Choose **Choose file** to upload the local copy of the template that you downloaded. The name of the file is neptune_ttl_main-existing.yaml. 
5.	Choose **Next**.
6.	Enter a stack name of your choosing. 
7.	In the **Parameters** section, enter an ApplicationID. Also provide details of your existing Neptune cluster by setting values for NeptuneClusterId, NeptuneClusterResourceId, NeptuneEndpoint, NeptunePort, VPC, SubnetIds, SecurityGroupIds, RouteTableIds. You may use defaults for remaining parameters.
8.	Choose **Next**.
9.	Continue through the remaining sections.
10.	Read and select the check boxes in the **Capabilities** section.
11.	Choose **Create stack**.
12.	When the stack is complete, navigate to the **Outputs** section and follow the link for the output NeptuneSagemakerNotebook. 

This opens in your browser the Jupyter files view. 

## Running the Examples
Open the TTL_Notebook.ipynb notebook in the Sagemaker notebook instance provisioned. Follow the steps to add nodes and edges with a specified TTL property to the Neptune database instance. Confirm these objects were added, then watch them expire and be deleted from the database. 

We recommend you follow along with the blog post to understand the end-to-end process.

## Cost
The template creates resources in services including Amazon Neptune, Amazon DynamoDB, AWS Step Functions, AWS Lambda, and Amazon EventBridge. Please refer to pricing guides for these services. 

## Clean up
If you’re done with the solution and wish to avoid future charges, delete the CloudFormation stack.

## Limitations
This repo is a proof of concept of the approach described in the blog post. Here are a few gaps:
- We support TTL for property graph. We do not currently support TTL for RDF.
- We support TTL on nodes and edges. We do not support TTL on properties.
- We do not support modification or removal of TTL on nodes and edges.
- The Lambda function that removes nodes and edges when they expire is not designed to handle supernodes. If you have a TTL on a node with a large number of edges, refer to discussion in our blog post for design options.

## Error Handling
Here is the current behavior of error handling in DynamoStreamsToNeptuneLambda, the Lambda function that removes nodes and edges when they expire.
- The function logs in CloudWatch all attempted drops. Errors are caught and logged in CloudWatch.
- The function addresses errors calling Neptune by following retry logic discussed in [https://docs.aws.amazon.com/neptune/latest/userguide/lambda-functions-examples.html#lambda-functions-examples-python](https://docs.aws.amazon.com/neptune/latest/userguide/lambda-functions-examples.html#lambda-functions-examples-python). It distinguishes retriable from non-retriable errors. It attempts to reconnect to the Neptune cluster if the existing connection fails.
- The function's trigger is DynamoDB streams. When the function returns an error, the Lambda service follows retry logic.  See [https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html) and [https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-dynamodb-eventsourcemapping](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-dynamodb-eventsourcemapping) for documentation on Lambda triggers for DynamoDB streams. Note:
  * Lambda retries a finite number of times the Lambda function on error.
  * Lambda splits/bisects the batch into two on error. This is useful when there is too much work to do in the batch or if part of the batch is causing an error.  

There are two levels of retries: 
- The Lambda function itself retries a drop several times with backoff. It also reconnected a failed connection to Neptune.
- The Lambda service retries a failed batch from DynamoDB streams, as mentioned above.

If there is a serious failure such that Neptune cannot drop objects, you can find a record of what was ATTEMPTED in the CloudWatch log group for this function. We recommend searching the log group for two strings:
    * _NODELOG_
    * _EDGELOG_

Here are enhancements you might consider:
- Customize trigger parameters discussed here [https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-ddb-params](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html#services-ddb-params). 
In particular, set an SQS queue or SNS topic for discarded streams records. 

## License
This library is licensed under the MIT-0 License. See the LICENSE file.

