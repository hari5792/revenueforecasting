provider "aws" {
  region = "us-west-2"  # Change to your preferred region
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-00572d57e771a4823"  # Amazon Linux 2 AMI for us-east-1
  instance_type = "t2.micro"
  
  tags = {
    Name = "MyTerraformEC2"
  }
}
