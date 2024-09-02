# Contributing Guide to **vc2sng**

We welcome contributions to this project! If you'd like to contribute, please follow the guidelines below.

## Forking the Repository

1. Click the "Fork" button in the top right corner of the repository page on GitHub.
2. This will create a copy of the repository in your own GitHub account.

## Cloning the Repository

1. Open a terminal on your local machine.
2. Change to the directory where you want to clone the repository.
3. Run the following command to clone the repository:

git clone https://github.com/your-username/vc2sng.git

Replace `your-username` with your GitHub username.

## Creating a Branch

1. Change to the cloned repository directory on your local machine.
2. Run the following command to create a new branch for your changes:

git checkout -b your-branch-name

Replace `your-branch-name` with a descriptive name for your branch.

## Making Changes

1. Make the changes you want to contribute to the project.
2. Save the changes to your local repository.

## Committing Changes

1. Run the following command to stage your changes for commit:

git add .

2. Run the following command to commit your changes:

git commit -m "Your commit message"

Replace `"Your commit message"` with a brief description of the changes you made.

## Pushing Changes

1. Run the following command to push your changes to your fork on GitHub:

git push origin your-branch-name

Replace `your-branch-name` with the name of the branch you created earlier.

## Creating a Pull Request

1. Go to the original repository on GitHub (https://github.com/jaateixeira/vc2sng/).
2. Click the "New pull request" button.
3. Select your fork and branch from the dropdown menus.
4. Write a description of the changes you made and why they should be merged into the project.
5. Click the "Create pull request" button.

## Review and Merge

1. The project maintainers will review your pull request.
2. If there are any suggested changes, make the changes and push them to your branch.
3. Once the changes have been approved, the project maintainers will merge your pull request into the main branch of the repository.

## Updating Your Fork

1. If you want to keep your fork up-to-date with the main repository, you can add it as a remote and fetch the latest changes.
2. Run the following command to add the main repository as a remote:

git remote add upstream https://github.com/jaateixeira/vc2sng.git

3. Run the following command to fetch the latest changes from the main repository:

git fetch upstream

4. Run the following command to merge the latest changes into your local branch:

git merge upstream/main

5. Run the following command to push the merged changes to your fork on GitHub:

git push origin your-branch-name

Replace `your-branch-name` with the name of the branch you created earlier.

## Thank You

Thank you for contributing to this project! We appreciate your help in making it better.
