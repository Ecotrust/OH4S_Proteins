# OH4S Infrastructure Documentation

This file documents the Oregon Harvest for Schools (OH4S) production infrastructure, which is defined as code with [OpenTofu](https://opentofu.org/) and deployed as Docker containers on a single AWS EC2 instance.

These docs are written for engineers who need to operate the existing infrastructure and deploy updates. At the end you will be able to run `tofu plan` / `tofu apply` using the infrastructure code in [`../infra/`](../infra/).

---  

## Prerequisites

Before you can run the OH4S infrastructure code, set up the following on your machine. 

### Accounts

- **AWS account access** to the Ecotrust account that hosts OH4S, with permission to create IAM users or to be added to the existing `terraform` IAM group. 
- **GitHub access** to [`Ecotrust/OH4S_Proteins`](https://github.com/Ecotrust/OH4S_Proteins).
- **VPN access**, if SSH is restricted to the Ecotrust VPN IP range (see the `allowed_ssh_cidr` setting in [`infra/networking.tf`](../infra/networking.tf))

### Tools to install

| Tool                         | Why                                                 | Install                                                                       |
| ---------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------- |
| **OpenTofu** (`tofu`)        | Runs the infrastructure code                        | https://opentofu.org/docs/intro/install/                                      |
| **AWS CLI v2**               | Configures credentials and lets you verify identity | https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html |
| **Git**                      | Clone the repo                                      | https://git-scm.com/downloads                                                 |
| An editor (e.g. **VS Code**) | Edit `.tf` and `.tfvars` files                      | optional                                                                      |

> **Why OpenTofu instead of Terraform?** OpenTofu is a drop-in, open-source fork of Terraform. The commands are the same except you type `tofu` instead of `terraform`. The repo's files use the `.tf` / `.tfvars` extensions and the `terraform { }` configuration block.

**Verify your installs**

```bash
tofu version
aws --version
git --version
```

### Get the code

```bash
git clone https://github.com/Ecotrust/OH4S_Proteins
cd OH4S_Proteins
git checkout main
git pull
```

All infrastructure code lives in the [`infra/`](../infra/) directory. The application and its Docker setup live in [`app/`](../app/) and [`docker/`](../docker/).

---  

## AWS IAM and Credentials

OpenTofu authenticates to AWS using a dedicated IAM user named `terraform`, accessed through an AWS CLI profile. This document covers the following cases:

- **The common case:** the `terraform` user and group already exist — you just need credentials and a local profile.
- **First-time bootstrap:** the IAM resources don't exist yet and you're creating them. (Most engineers can skip this.)

### Common case: configure a local AWS profile

Look in 1Password for the existing `terraform` IAM user. You should find an **access key ID** and **secret access key**. Then:

1. Configure a named profile (this document uses `oh4s`):

   ```bash
   aws configure --profile oh4s
   ```

   Enter when prompted:
   - **AWS Access Key ID** — the saved access key from 1Password
   - **AWS Secret Access Key** — the saved secret key from 1Password
   - **Default region name** — `us-west-2`
   - **Default output format** — `json`

2. Confirm the credentials landed in `~/.aws/credentials` and the profile in `~/.aws/config`:

   ```bash
   cat ~/.aws/config
   cat ~/.aws/credentials
   ```

3. Verify the profile works and shows the expected identity:

   ```bash
   aws sts get-caller-identity --profile oh4s
   ```

   This should return the `terraform` user's ARN. 
   *If it errors, your keys are wrong or the profile name is misspelled.*

---  


### First-time bootstrap :caution: most engineers can skip this

> Skip this section unless you're standing up the `terraform` IAM identity for
> the first time, or replicating this pattern in a new project.

These steps were performed once in the AWS Management Console, using the WCOA Blue Pages project's IAM setup as a reference.

1. **Create an IAM user group** named `terraform`. (Add users to it later.)

2. **Create an IAM policy** for the group:
   - Copy the policy document from the reference project (WCOA Blue Pages).
   - Review every statement for accuracy.
   - Rename anything that references the other project so it points at OH4S resources.

1. **Attach the policy** to the `terraform` group.

2. **Create an IAM user** named `terraform` and add it to the `terraform` group.
   This is the identity OpenTofu uses (and, where applicable, the role it assumes when running via the CLI).

3. **Create an access key** for the user:
   - Use case: **Command Line Interface (CLI)**.
   - Check the confirmation box and continue.
   - **Copy both the access key ID and the secret access key** from the final screen and store both in 1Password.

4. Confirm group membership:

   ```bash
   aws iam list-groups-for-user --user-name terraform --profile oh4s
   ```

Once the user has a key, follow the **Common case** steps above to set up your
local profile.

If `aws sts get-caller-identity` succeeds but `tofu` still fails to authenticate, OpenTofu may not be reading your profile. Here are two reliable options to fix:

- Export the profile for the shell session (this is the better option):
  ```bash
  export AWS_PROFILE=oh4s
  ```
- Or export the keys directly to the default profile:
  ```bash
  export AWS_ACCESS_KEY_ID=...
  export AWS_SECRET_ACCESS_KEY=...
  ```

---  

## OpenTofu Walkthrough

This section explains every file in [`infra/`](../infra/), how they fit together, and the exact commands to provision or update the infrastructure.

### OpenTofu concepts

Definition of two keywords that appear constantly in `.tf` files:

- **`data`** — references something that *already exists* in AWS. OpenTofu reads it but does not create or manage it (e.g. the default VPC and subnets).
- **`resource`** — something OpenTofu *creates and manages*. If you change it, `tofu apply` changes the real thing in AWS.

OpenTofu records what it has created in a **state file**. The state is the difference between what exists and what your code says should exist. `tofu plan` uses the state file to show diffs. This project stores state remotely in S3 so the whole team shares one copy (see [`terraform.tf`](#terraformtf)).

### The files in `infra/`

| File                                               | Purpose                                             |
| -------------------------------------------------- | --------------------------------------------------- |
| [`main.tf`](#maintf)                               | AWS provider + all input variable declarations      |
| [`terraform.tf`](#terraformtf)                     | Provider versions and the S3 remote state backend   |
| [`terraform.tfvars`](#configuring-terraformtfvars) | Your values for the variables (git-ignored)         |
| [`networking.tf`](#networkingtf)                   | Default VPC/subnet lookups and the security group   |
| [`iam.tf`](#iamtf)                                 | EC2 instance role, S3 read policy, instance profile |
| [`ec2.tf`](#ec2tf)                                 | Key pair, the EC2 instance, and its Elastic IP      |
| [`user_data.tftpl`](#user_datatftpl)               | Script that runs on boot                            |
| [`outputs.tf`](#outputstf)                         | Values printed after apply                          |

#### `main.tf`

Declares the `aws` provider (region driven by `var.aws_region`, default `us-west-2`) and the stack input variables. Variables marked `sensitive = true` (secret key, DB password, Mapbox token, SSH key) are hidden in OpenTofu's output.

#### `terraform.tf`

Pins the AWS provider (`hashicorp/aws ~> 5.92`), requires OpenTofu/Terraform `>= 1.2`, and configures the S3 remote state backend:

```hcl
backend "s3" {
  bucket = "oh4s-tf-state"
  key    = "production/terraform.tfstate"
  region = "us-west-2"
}
```

The `production/` key isolates this environment's state. If you ever add a staging environment, it would use a different key (e.g. `staging/...`) against the same bucket.

#### `networking.tf`

- Looks up the account's default VPC and its subnets via `data` blocks — these already exist, so OpenTofu just reads them.
- Defines the security group `oh4s-sg`:
  - **Ingress 80 (HTTP)** open to `0.0.0.0/0`.
  - **Ingress 22 (SSH)** restricted to `var.allowed_ssh_cidr`.
  - **Egress** all traffic (needed for package installs and pulls).
  - **HTTPS (443)** TLS port

#### `iam.tf`

Creates the instance's identity and permissions (all managed by OpenTofu):

- `aws_iam_role.oh4s_ec2` (`oh4s-ec2-role`) — a role EC2 can assume.
- `aws_iam_role_policy.oh4s_s3_read` — grants `s3:GetObject` on `oh4s-db-dump/*` and `s3:ListBucket` on the bucket.
- `aws_iam_instance_profile.oh4s` (`oh4s-ec2-profile`) — the wrapper that attaches the role to the EC2 instance.

> The `oh4s-db-dump` S3 bucket holding the SQL dump is referenced by this
> policy but is not created by this code and is expected to already exist. 
> Confirm the bucket and the dump object referenced by `db_dump_file_path` exist before applying.

#### `ec2.tf`

- `aws_key_pair.oh4s` — registers your `ssh_public_key` so you can SSH in.
- `aws_instance.oh4s` — the server itself. Wires together the AMI, instance type, security group, subnet, and instance profile, and passes all the Django/DB variables into [`user_data.tftpl`](#user_datatftpl) via `templatefile(...)`.
- `aws_eip.oh4s` — an Elastic IP attached to the instance so the public address is stable across stop/start.

#### `outputs.tf`

Prints `ec2_public_ip` (the Elastic IP) after apply.

### Configuring `terraform.tfvars`

`terraform.tfvars` supplies your values for the variables in `main.tf`.

Here is a template to use for `terraform.tfvars`:

```hcl
aws_region        = "us-west-2"
project_name      = "oh4s"
ec2_instance_type = "t3.micro"
ec2_ami           = "ami-042d89c65bc8c9896" # Ubuntu 26.04 LTS, us-west-2

# SSH public key (contents of ~/.ssh/oh4s.pub)
ssh_public_key    = "ssh-ed25519 AAAA... you@ecotrust.org"
# IP in CIDR form. When on the VPN, use the VPN egress IP.
allowed_ssh_cidr  = "x.x.x.x/32"

django_secret_key    = "<generate a strong random value>"
django_allowed_hosts = "<the Elastic IP and/or domain>"
sql_db_name          = "postgres"
sql_db_user          = "postgres"
sql_db_password      = "<strong password>"
sql_host             = "db"          # the Postgres service name in docker-compose
sql_port             = 5432
mapbox_token         = "<your Mapbox token>"
db_dump_file_path    = "s3://oh4s-db-dump/<YYYYMMDD>_oh4s_db_dump.sql"
```

Note: it is fine to leave a value blank temporarily if it's genuinely unknown and not required for what you're applying, but blanks for required secrets will break the app at boot.

### Running OpenTofu

From the `infra/` directory, with your AWS profile active (`export AWS_PROFILE=oh4s`):

```bash
cd infra

tofu init 
tofu plan    
tofu apply
```

### Iterating

You will likely need to run plan and apply a few times.

```
tofu plan → tofu apply → read errors → fix .tf or .tfvars → repeat
```

---  

## Deploy

Deploy with `tofu apply`. This creates the EC2 instance, the instance bootstraps the application by itself. 

When the instance launches, AWS runs the script generated from [`infra/user_data.tftpl`](../infra/user_data.tftpl). OpenTofu fills the template placeholders (`${django_secret_key}`, `${sql_host}`, etc.) with your `terraform.tfvars` values before handing it to the instance.

> **Keep `.env` keys and `user_data.tftpl` in sync.** 
> [`docker/.env.template`](../docker/.env.template) is the canonical list of expected keys.

### Verify deployment

`tofu apply` printed `ec2_public_ip`. Retrieve it again any time with:

```bash
cd infra && tofu output ec2_public_ip
```

Check the app responds:

```bash
curl -I http://<ec2_public_ip>/
```


---  

## Troubleshooting and Security

**`tofu init` can't access the S3 backend**:

The `terraform` user needs permission to read/write to the S3 bucket. If init fails reaching the backend, verify your IAM permissions include access to it, and that the region matches.


**Resource already exists / role already exists**:

Just re-run:

```bash
tofu apply
```

**App doesn't respond after apply**:

The instance launches in seconds, but the first-boot script takes several minutes (installing Docker, building the image, restoring the DB). If it's still down after ~10 minutes:

SSH in and read the boot log:
```bash
sudo tail -n 100 /var/log/cloud-init-output.log
```

Check containers:
```bash
docker compose -f docker-compose.prod.yaml ps
docker compose -f docker-compose.prod.yaml logs web
docker compose -f docker-compose.prod.yaml logs db
```
