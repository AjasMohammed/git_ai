from git import Repo
import os

working_dir = os.getcwd()
print(working_dir)

repo = Repo(working_dir)
print(repo.commit("main"))
print("==================")
print(repo.head.commit.message)
print("==================")
print(f"Active Branch: {repo.active_branch}")
print(f"Is Dirty: {repo.is_dirty()}")

print(f'Untracked Files: {repo.untracked_files}')
# diffs = repo.index.diff(repo.head.commit)
# print(diffs)
# for d in diffs:
#     print(d.a_path)
#     print(d.)

# staged_diff = repo.git.diff("--staged")
# print(type(staged_diff))
# with open("changes.txt", "w") as f:
#     f.write(staged_diff)

# print(repo.git.status())
diff = repo.git.diff("--staged")
print((diff))