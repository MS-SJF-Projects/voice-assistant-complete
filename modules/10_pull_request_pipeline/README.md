# Pull request pipeline

In this stage we'll add automation to the project. We're going to automatically run tests and lint the code every time one makes a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)(PR) to your repository. This will help us to catch bugs early and keep the code clean.

People usually call such an automation a "pipeline" or a "workflow", and running quality checks on a PR is an important part of so called "Continuous Integration", or simply "CI". 

If your code is hosted on GitHub, a simple way to create a workflow is to use [Github Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions). This is what we will do in this tutorial.

> For more information on the concept of pipelines, see ["What is a CI/CD pipeline?"](https://www.redhat.com/en/topics/devops/what-cicd-pipeline)

1. Confirm you're on the main branch in your terminal with the following command

    ```sh
    git rev-parse --abbrev-ref HEAD
    ```

    The above command should output `main`

2. Make sure all your changes are committed and pushed to the `main` branch

    ```sh
    git add --all
    git commit -m "Initial commit"
    git push
    ```

3. Create a branch off your `main` branch in git

    ```sh
    # Your branch name. This can be anything you want, but feature/<feature_name> is a common practice
    BRANCH_NAME="feature/add-pr-pipeline"
    git branch $BRANCH_NAME
    git checkout $BRANCH_NAME
    ```

4. Create a `.github/workflows` folder in the root of the project

    > For Github to recognize a workflow, it must be defined in the `.github/workflows` directory in a repository. You can have multiple workflows, each of which can perform a different set of tasks.

5. In the above folder create a `pull_request.yaml` file with the below content:

    > Workflow files use YAML syntax, and must have either a .yml or .yaml file extension. If you're new to YAML and want to learn more, see ["Learn YAML in Y minutes."](https://learnxinyminutes.com/docs/yaml/)

    This workflow file will run every time there is a pull request created or changes that targets the `main` branch. This workflow run on `ubuntu` linux inside of the `mcr.microsoft.com/vscode/devcontainers/python:0-3.10-bullseye` container image and executes two steps: install python dependencies and run tests.

    ```yaml
    name: Pull request

    on:
      pull_request:
        branches: [main]

    jobs:
      build:
        runs-on: ubuntu-latest
        container:
          image: mcr.microsoft.com/vscode/devcontainers/python:0-3.10-bullseye
        steps:
          - uses: actions/checkout@v2

          - name: Install dependencies
            run: |
            cd src/04_add_images
            pip install -r requirements.txt

          - name: Run tests
            run: pytest ./src/

    ```

    > For more information about the workflow file syntax, see ["Understanding the workflow file"](https://docs.github.com/en/actions/using-workflows/about-workflows#understanding-the-workflow-file)

6. Make sure all the tests are passing by running the `Run tests` step command locally first. If not, fix the tests

7. Commit and push these changes to your new branch

    > **TIP:** Keep your commit messages short and consistent and use imperative statements, for example "Add PR pipeline". For more tips and examples on writing commit messages, see ["How to Write a Git Commit Message"](https://cbea.ms/git-commit/example)

8. [Create a pull request on Github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) from your new branch to the `main` of your fork.

This should trigger the workflow that we just created.

9.  Look for the run in the [the workflow history](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/viewing-workflow-run-history) on Github and make sure it ran without any errors

    If the run doesn't appear in the list, make sure the PR targets the main branch and that you've formatted the `pull_request.yaml` correctly.

10. Add an additional step with linting to the pipeline by adding the below code to the end of `pull_request.yaml`:

    > **TIP:** make sure you're using the correct indentation when adding this to the file

    ```yaml
          - name: Lint python
            run: pylint --disable=C,R0801 src/ 
    ```

11. Make sure all the linting is passing by running the `Lint python` step command locally first. If it's failing, fix the issues found
12. Commit and push your changes
13. Check that your pipeline has successfully passed
14. Merge your PR
