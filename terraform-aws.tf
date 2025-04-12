
provider "aws" {
  region = "us-west-2"
}

# S3 Bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = "customer-transactions-bucket"
  acl    = "private"
}

# API Gateway
resource "aws_api_gateway_rest_api" "api_gateway" {
  name        = "CustomerTransactionsAPI"
  description = "API Gateway for customer transactions"
}

resource "aws_api_gateway_resource" "api_resource" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "transactions"
}

resource "aws_api_gateway_method" "api_method" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.api_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "api_integration" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_resource.id
  http_method = aws_api_gateway_method.api_method.http_method
  type        = "AWS_PROXY"
  integration_http_method = "POST"
  uri         = aws_lambda_function.lambda_function.invoke_arn
}

# Lambda Function
resource "aws_lambda_function" "lambda_function" {
  function_name = "ProcessTransactions"
  handler       = "index.handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec_role.arn
  filename      = "lambda_function_payload.zip"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# SageMaker Endpoint
resource "aws_sagemaker_endpoint" "sagemaker_endpoint" {
  endpoint_name = "CustomerTransactionsEndpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.sagemaker_endpoint_config.name
}

resource "aws_sagemaker_endpoint_configuration" "sagemaker_endpoint_config" {
  name = "CustomerTransactionsEndpointConfig"

  production_variants {
    variant_name = "AllTraffic"
    model_name   = aws_sagemaker_model.sagemaker_model.name
    initial_instance_count = 1
    instance_type = "ml.m5.large"
  }
}

resource "aws_sagemaker_model" "sagemaker_model" {
  name = "CustomerTransactionsModel"
  execution_role_arn = aws_iam_role.sagemaker_exec_role.arn
  primary_container {
    image = "123456789012.dkr.ecr.us-west-2.amazonaws.com/sagemaker-model:latest"
    model_data_url = "s3://customer-transactions-bucket/model.tar.gz"
  }
}

resource "aws_iam_role" "sagemaker_exec_role" {
  name = "sagemaker_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_policy_attachment" {
  role       = aws_iam_role.sagemaker_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

# SageMaker Notebook Instance
resource "aws_sagemaker_notebook_instance" "sagemaker_notebook" {
  name = "CustomerTransactionsNotebook"
  instance_type = "ml.t2.medium"
  role_arn = aws_iam_role.sagemaker_exec_role.arn
}
