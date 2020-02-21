# cdmx
Datos Abiertos - Ciudad de México

# Description

This repo has as objective to have a version control system on publicly available data.
This project runs a python script(download_files.py) on AWS Codebuild, where it runs the script and updates the github repo.
The repo needs to exist on CodeCommit and on github.

# Install

 
```
aws cloudformation deploy --template-file cloudformation-pipeline.yaml \
    --stack-name=<stack_name>                          \
    --parameter-overrides                                   \
      RepositoryName=<repo_name>                       \
      RepositoryCloneUrl=https://git-codecommit.<aws_region>.amazonaws.com/v1/repos/<repo_name> \
      RepositoryBranch=master          \
      RepositoryMirrorUrl=https://<github_user>:<github_token>@github.com/<github_repo_path>.git         \
      --capabilities CAPABILITY_IAM
```
