## Time-to-Live (TTL) in Amazon Neptune

This repo is a code sample accompanying the blog post (TODO - URL). The following are instructions to setup the TTL sample. 

## Prerequisites
To run this example, you need an AWS account with permission to create resources such as a Neptune cluster. 

## Provision resources 
We provide two configurations.

### Provision New Neptune Cluster and Supporting TTL Resources
Download a copy of the CloudFormation template (cfn/neptune_ttl_main.yaml) from this repository. Then complete the following steps:

1.	On the AWS CloudFormation console, choose **Create stack**.
2.	Choose **With new resources (standard)**.
3.	Select U**pload a template file**.  
4.	Choose **Choose file** to upload the local copy of the template that you downloaded. The name of the file is neptune_ttl_main.yaml. 
5.	Choose **Next**.
6.	Enter a stack name of your choosing. 
7.	In the **Parameters** section, use defaults for the remaining parameters.
8.	Choose **Next**.
9.	Continue through the remaining sections.
10.	Read and select the check boxes in the **Capabilities** section.
11.	Choose **Create stack**.
12.	When the stack is complete, navigate to the **Outputs** section and follow the link for the output NeptuneSagemakerNotebook. 

This opens in your browser the Jupyter files view. 

### Provision TTL Resources for Existing Neptune Cluster
Download a copy of the CloudFormation template (cfn/neptune_ttl_main-existing.yaml) from this repository. Then complete the following steps:

1.	On the AWS CloudFormation console, choose **Create stack**.
2.	Choose **With new resources (standard)**.
3.	Select U**pload a template file**.  
4.	Choose **Choose file** to upload the local copy of the template that you downloaded. The name of the file is neptune_ttl_main-existing.yaml. 
5.	Choose **Next**.
6.	Enter a stack name of your choosing. 
7.	In the **Parameters** section, use defaults for the remaining parameters.
8.	Choose **Next**.
9.	Continue through the remaining sections.
10.	Read and select the check boxes in the **Capabilities** section.
11.	Choose **Create stack**.
12.	When the stack is complete, navigate to the **Outputs** section and follow the link for the output NeptuneSagemakerNotebook. 

This opens in your browser the Jupyter files view. 
We encourage you to review the stack with your security team prior to using it in a production environment.

## Running the Examples
Open the TTL_Notebook.ipynb notebook in the Sagemaker notebook instance provisioned. Follow the steps to add nodes and edges with a specified TTL property to the Neptune database instance. Confirm these objects were added, then watch them expire and be deleted from the database. 

We recommend you follow along with the blog post to understand the end-to-end process.

## Cost
The template creates resources in services including Amazon Neptune, Amazon DynamoDB, AWS Step Functions, AWS Lambda, and Amazon EventBridge. Please refer to pricing guides for these services. 

## Clean up
If you’re done with the solution and wish to avoid future charges, delete the CloudFormation stack. 



## License

This library is licensed under the MIT-0 License. See the LICENSE file.

