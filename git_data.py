from git import Repo
import os

working_dir = os.getcwd()
print(working_dir)

repo = Repo(working_dir)
print(repo.head.commit.message)
# diffs = repo.index.diff(repo.head.commit)
# print(diffs)
# for d in diffs:
#     print(d.a_path)
#     print(d.)

staged_diff = repo.git.diff("--staged")
print(type(staged_diff))
# with open("changes.txt", "w") as f:
#     f.write(staged_diff)