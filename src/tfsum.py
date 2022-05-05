import json
import logging
import os
import sys

import github

logging.basicConfig(level=logging.INFO)
logging.info("Running TFsum")

try:
    # format: myname/something
    repo_name = os.environ["GITHUB_REPOSITORY"]
    github_token = os.environ["INPUT_TOKEN"]
    # this should be mounted once the action is running, it contains the root of the checkout
    workspace = os.environ["GITHUB_WORKSPACE"]
    # format: refs/pull/1/merge
    ref = os.environ["GITHUB_REF"]
    skip_noop = bool(os.environ.get("INPUT_SKIP_NOOP", True))
except Exception as e:
    logging.error(f"Failed to load key from environment: {e}")
    sys.exit()

plan_file = workspace + "/" + os.environ.get("INPUT_PLAN_FILE", "tf.plan.json")

try:
    with open(plan_file) as jf:
        plan = json.load(jf)
except Exception as e:
    logging.error(f"Failed to open {plan_file}: {e}")
    sys.exit()

actions = {}

logging.info(f"Parsing plan in {plan_file}")
for r in plan["resource_changes"]:
    c = r["change"]
    for action in c["actions"]:
        if skip_noop and (action == "no-op"):
            continue
        if action in actions:
            actions[action] += 1
        else:
            actions[action] = 1

actions_performed = list(map(lambda l: f"{l}: {actions[l]}", actions))
summary = ", ".join(actions_performed)

logging.info(f"Actions found: {summary}")

try:
    # ref format: refs/pull/<pr_number>/merge
    logging.info(f"Extracting PR number from {ref}")
    pr_number = int(ref.split("/")[2])
except Exception as e:
    logging.error(f"Failed: {e}")
    sys.exit()

logging.info(f"Connecting to GitHub for PR{pr_number} in {repo_name}")
try:
    gh = github.Github(github_token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    logging.info("Creating comment")
    pr.create_issue_comment(f":wrench: Terraform plan summary: `{summary}`")

except Exception as e:
    logging.error(f"Failed to connect: {e}")
    sys.exit()

logging.info("Done")
