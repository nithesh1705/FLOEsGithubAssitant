import git
import os
import shutil

os.system("title FLOE's GitHub Assistant")

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"

def ensure_directory_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"{RED}Error: This folder path does not exist: {folder_path}{RESET}")
        return False
    return True

def create_branch():
    repo_url = input("Enter the repository URL: ")
    repo_name = input(f"Enter the repository name: ")
    folder_path = input(f"Enter the folder path to connect with the repo: ")
    if not ensure_directory_exists(folder_path):
        return
    repo_dir = folder_path
    if os.path.exists(repo_dir) and os.listdir(repo_dir):
        print(f"{RED}Error: The directory {repo_dir} already exists and it is not empty.{RESET}")
        return
    try:
        repo = git.Repo.clone_from(repo_url, repo_dir)
        # repo.git.checkout('-b', 'main')
        readme_path = os.path.join(repo_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(f"# {repo_name}\n\nThis is the initial commit of the {repo_name} repository.")
        repo.index.add([readme_path])
        repo.index.commit('Initial commit with README.md')
        repo.git.push('origin', 'main')
        repo.git.checkout('-b', 'develop')
        repo.git.push('origin', 'develop')
        print(f"{GREEN}Created 'main' and 'develop' branches in {CYAN}{repo_name}{GREEN} repository.{RESET}")
    except git.exc.GitCommandError as e:
        print(f"{RED}Git error: {e}{RESET}")

def clone_repo():
    repo_url = input("Enter the repository URL: ")
    repo_name = input(f"Enter the repository name: ")
    folder_path = input(f"Enter the folder path to clone the repo: ")
    if not ensure_directory_exists(folder_path):
        return
    repo_dir = folder_path
    git.Repo.clone_from(repo_url, repo_dir)
    print(f"{GREEN}Cloned {CYAN}{repo_name}{GREEN} repository to {repo_dir}.{RESET}")

def push_develop():
    repo_url = input("Enter the repository URL: ")
    repo_name = input(f"Enter the repository name: ")
    folder_path = input(f"Enter the folder path: ")
    commit_message = input("Enter the commit message: ")
    if not ensure_directory_exists(folder_path):
        return
    repo_dir = folder_path
    repo = git.Repo(repo_dir)
    repo.git.checkout('develop')
    repo.git.add(all=True)
    repo.git.commit('-m', commit_message)
    repo.git.push('origin', 'develop')
    print(f"{GREEN}Pushed code to 'develop' branch in {CYAN}{repo_name}{GREEN} repository.{RESET}")

def push_main():
    repo_url = input("Enter the repository URL: ")
    repo_name = input(f"Enter the repository name: ")
    folder_path = input(f"Enter the folder path: ")
    commit_message = input("Enter the commit message: ")
    if not ensure_directory_exists(folder_path):
        return
    repo_dir = folder_path
    repo = git.Repo(repo_dir)
    repo.git.checkout('main')
    repo.git.merge('develop')
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        repo.git.commit('-m', commit_message)
        print(f"{GREEN}Committed changes with message: '{commit_message}'{RESET}")
    else:
        print(f"{YELLOW}No changes to commit.{RESET}")
    repo.git.push('origin', 'main')
    print(f"{GREEN}Pushed code to 'main' branch in {CYAN}{repo_name}{GREEN} repository.{RESET}")

def exit_program():
    print("Exiting the program...")
    exit(0)

def main_menu():
    checkr = True
    while checkr:
        print(f"\n{CYAN}FLOE's GitHub Assistant{RESET}")
        print(f"{YELLOW}{'-' * 24}{RESET}")
        print(f"\n{WHITE}Please choose an option:{RESET}")
        print(f"{YELLOW}1. {WHITE}Create Develop branch{RESET}")
        print(f"{YELLOW}2. {WHITE}Clone Repo{RESET}")
        print(f"{YELLOW}3. {WHITE}Push to Develop branch{RESET}")
        print(f"{YELLOW}4. {WHITE}Push to Main branch{RESET}")
        print(f"{YELLOW}5. {WHITE}Exit{RESET}")
        choice = int(input(f"{YELLOW}\nEnter your choice: {RESET}"))
        if choice == 1:
            create_branch()
        elif choice == 2:
            clone_repo()
        elif choice == 3:
            push_develop()
        elif choice == 4:
            push_main()
        elif choice == 5:
            exit_program()
            checkr = False
        else:
            print(f"{RED}Invalid choice, please try again.{RESET}")
        checkr = True

if __name__ == "__main__":
    main_menu()
