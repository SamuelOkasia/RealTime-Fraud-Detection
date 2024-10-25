provider "aws" {
  region = "eu-west-2"
}

# ECS Cluster
resource "aws_ecs_cluster" "fraud_detection_cluster" {
  name = "RealTime-Fraud-Detection"

  # capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  service_connect_defaults {
    namespace = "arn:aws:servicediscovery:eu-west-2:786955137666:namespace/ns-di5lktrutt3wx3n7"
  }
}


# VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = "172.31.0.0/16"
}

# Subnets
resource "aws_subnet" "subnet_a" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "172.31.16.0/20"
  availability_zone = "eu-west-2a"
}

resource "aws_subnet" "subnet_b" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "172.31.32.0/20"
  availability_zone = "eu-west-2b"
}

resource "aws_subnet" "subnet_c" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "172.31.0.0/20"
  availability_zone = "eu-west-2c"
}

# Security Groups
resource "aws_security_group" "default_sg" {
  vpc_id = aws_vpc.main_vpc.id
  description = "default VPC security group"
  revoke_rules_on_delete = false
}

resource "aws_security_group" "launch_wizard_sg" {
  vpc_id = aws_vpc.main_vpc.id
  description = "launch-wizard-1 security group"
  revoke_rules_on_delete = false
}


# Backend ECS Service
resource "aws_ecs_service" "backend_service" {
  name            = "backend-service"
  cluster         = aws_ecs_cluster.fraud_detection_cluster.id
  desired_count   = 1
  launch_type     = "FARGATE"
  task_definition = "fraud-detection-backend-task"
  network_configuration {
    subnets         = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id, aws_subnet.subnet_c.id]
    security_groups = [aws_security_group.default_sg.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = "arn:aws:elasticloadbalancing:eu-west-2:786955137666:targetgroup/backend-target/d436c44bce054d2c"
    container_name   = "backend-container"
    container_port   = 8000
  }
}

# Frontend ECS Service
resource "aws_ecs_service" "frontend_service" {
  name            = "frontend-service"
  cluster         = aws_ecs_cluster.fraud_detection_cluster.id
  desired_count   = 1
  launch_type     = "FARGATE"
  task_definition = "fraud-detection-frontend-task"
  network_configuration {
    subnets         = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id, aws_subnet.subnet_c.id]
    security_groups = [aws_security_group.default_sg.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = "arn:aws:elasticloadbalancing:eu-west-2:786955137666:targetgroup/frontend-target/1410702cfeb66b8e"
    container_name   = "frontend-container"
    container_port   = 3000
  }
}
