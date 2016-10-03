from github import Github

# First create a Github instance:
g = Github("jfaisal.knysys@gmail.com", "knysys@123")

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print repo.name
    repo.edit(has_wiki=False)