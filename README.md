# TFsum

_A Terraform plan summarizer_

This action reads your Terraform plan (json), create a super slim summary and writes that as comment in your pull_request.

## Usage

The action:

```yaml
- uses: harmw/tfsum-action@master
  with:
    github_token: ${{ github.token }}
```

Depending on how you're using TF in your _actions_, make sure it outputs clean json (`terraform_wrapper:true`):

```yaml
- uses: hashicorp/setup-terraform@v1
  with:
    terraform_wrapper: false

- name: Terraform
  run: |
    terraform -chdir=tests/terraform/ init
    terraform -chdir=tests/terraform/ plan -no-color -out tf.plan
    terraform -chdir=tests/terraform/ show -json tf.plan > tf.plan.json
```

## Development

Black :tada:

Install dependencies: `pip install -r requirements-dev.txt`

Testing:
```bash
make test
```
