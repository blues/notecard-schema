#!/usr/bin/env python3
"""
Script to update the blues.dev repository with generated MDX documentation.

This script:
1. Clones the blues.dev repository to a temporary directory
2. Navigates to the Notecard API documentation directory
3. Preserves existing _meta.json files
4. Replaces the directory contents with newly generated MDX files
5. Optionally commits and pushes changes
"""

import os
import shutil
import tempfile
import subprocess
import argparse


class DocsUpdater:
    def __init__(self, repo_url="https://github.com/blues/blues.dev.git", dry_run=False, clone_dir=None):
        self.repo_url = repo_url
        self.dry_run = dry_run
        self.clone_dir = clone_dir
        self.use_temp_dir = clone_dir is None
        self.temp_dir = None
        self.target_path = None

    def clone_repository(self):
        """Clone the blues.dev repository to specified or temporary directory."""
        print("Cloning blues.dev repository...")

        if self.use_temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix="blues-dev-")
            clone_target = self.temp_dir
        else:
            # Use specified directory, create if it doesn't exist
            clone_target = os.path.abspath(self.clone_dir)
            if os.path.exists(clone_target):
                if os.listdir(clone_target):
                    raise ValueError(f"Directory {clone_target} already exists and is not empty")
            else:
                os.makedirs(clone_target, exist_ok=True)
            self.temp_dir = clone_target

        try:
            subprocess.run([
                "git", "clone", self.repo_url, clone_target
            ], check=True, capture_output=True, text=True)
            print(f"Repository cloned to: {clone_target}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
            print(f"Git output: {e.stderr}")
            raise

        # Set the target path
        self.target_path = os.path.join(
            clone_target,
            "wireless-dev-site",
            "content",
            "en",
            "api-reference",
            "04 Notecard API"
        )

        if not os.path.exists(self.target_path):
            raise FileNotFoundError(f"Target directory not found: {self.target_path}")

        print(f"Target directory: {self.target_path}")
        return True

    def preserve_meta_files(self):
        """Collect all existing _meta.json files and Introduction _main.mdx from the target directory."""
        print("Collecting existing _meta.json files and Introduction content...")
        preserved_files = {}

        if not os.path.exists(self.target_path):
            print("Target directory doesn't exist, no files to preserve")
            return preserved_files

        # Walk through all subdirectories to find _meta.json files and Introduction _main.mdx
        for root, _, files in os.walk(self.target_path):
            # Preserve all _meta.json files
            if "_meta.json" in files:
                meta_path = os.path.join(root, "_meta.json")
                rel_path = os.path.relpath(meta_path, self.target_path)

                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    preserved_files[rel_path] = content
                    print(f"  Preserved: {rel_path}")
                except Exception as e:
                    print(f"  Warning: Could not read {rel_path}: {e}")
            
            # Preserve Introduction _main.mdx specifically
            if "_main.mdx" in files:
                # Check if this is the Introduction directory
                dir_name = os.path.basename(root)
                if dir_name == "00 Introduction":
                    main_path = os.path.join(root, "_main.mdx")
                    rel_path = os.path.relpath(main_path, self.target_path)
                    
                    try:
                        with open(main_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        preserved_files[rel_path] = content
                        print(f"  Preserved: {rel_path}")
                    except Exception as e:
                        print(f"  Warning: Could not read {rel_path}: {e}")

        print(f"Preserved {len(preserved_files)} files (_meta.json + Introduction)")
        return preserved_files

    def generate_new_docs(self, schema_dir, output_dir):
        """Generate new MDX documentation using the existing script."""
        print("Generating new MDX documentation...")

        # Import and use the existing generation script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        generate_script = os.path.join(script_dir, "generate_mdx_from_schema.py")

        if not os.path.exists(generate_script):
            raise FileNotFoundError(f"Generation script not found: {generate_script}")

        try:
            cmd = [
                "python3", generate_script,
                "--all", "--tidy",
                "--schema_dir", schema_dir,
                "--output_dir", output_dir
            ]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("MDX generation completed successfully")
            if result.stdout:
                print("Generation output:")
                print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error generating MDX files: {e}")
            print(f"Generation output: {e.stderr}")
            raise

    def replace_directory_contents(self, new_docs_dir, preserved_meta_files):
        """Replace the target directory contents with new documentation."""
        print("Replacing directory contents...")

        if self.dry_run:
            print("DRY RUN: Would replace directory contents")
            self.show_changes_preview(new_docs_dir, preserved_meta_files)
            return

        # Remove existing contents except for .git if it exists
        if os.path.exists(self.target_path):
            for item in os.listdir(self.target_path):
                item_path = os.path.join(self.target_path, item)
                if item == '.git':
                    continue  # Preserve .git directory if it exists

                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                print(f"  Removed: {item}")

        # Copy new documentation
        if os.path.exists(new_docs_dir):
            for item in os.listdir(new_docs_dir):
                src = os.path.join(new_docs_dir, item)
                dst = os.path.join(self.target_path, item)

                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
                print(f"  Added: {item}")

        # Restore preserved files (_meta.json and Introduction _main.mdx)
        for rel_path, content in preserved_meta_files.items():
            file_path = os.path.join(self.target_path, rel_path)
            file_dir = os.path.dirname(file_path)

            # Create directory if it doesn't exist
            os.makedirs(file_dir, exist_ok=True)

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Restored: {rel_path}")
            except Exception as e:
                print(f"  Warning: Could not restore {rel_path}: {e}")

    def show_changes_preview(self, new_docs_dir, preserved_meta_files):
        """Show a preview of changes that would be made."""
        print("\nPREVIEW OF CHANGES:")
        print("=" * 50)

        print(f"Target directory: {self.target_path}")
        print(f"Source directory: {new_docs_dir}")

        print(f"\nWould preserve {len(preserved_meta_files)} files (_meta.json + Introduction):")
        for file_path in preserved_meta_files.keys():
            print(f"  - {file_path}")

        if os.path.exists(new_docs_dir):
            print(f"\nWould copy new documentation structure:")
            for root, dirs, files in os.walk(new_docs_dir):
                level = root.replace(new_docs_dir, '').count(os.sep)
                indent = '  ' * level
                rel_path = os.path.relpath(root, new_docs_dir)
                if rel_path != '.':
                    print(f"{indent}{os.path.basename(root)}/")

                subindent = '  ' * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")

    def commit_changes(self, commit_message="Update Notecard API documentation"):
        """Commit the changes to the repository."""
        if self.dry_run:
            print("DRY RUN: Would commit changes")
            return

        print("Committing changes...")
        try:
            # Change to the repository directory
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)

            # Check if there are any changes
            result = subprocess.run([
                "git", "status", "--porcelain"
            ], capture_output=True, text=True)

            if not result.stdout.strip():
                print("No changes to commit")
                return False

            # Add all changes
            subprocess.run([
                "git", "add", "."
            ], check=True)

            # Commit changes
            subprocess.run([
                "git", "commit", "-m", commit_message
            ], check=True)

            print("Changes committed successfully")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Error committing changes: {e}")
            raise
        finally:
            os.chdir(original_cwd)

    def push_changes(self):
        """Push changes to the remote repository."""
        if self.dry_run:
            print("DRY RUN: Would push changes")
            return

        print("Pushing changes...")
        try:
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)

            subprocess.run([
                "git", "push"
            ], check=True)

            print("Changes pushed successfully")

        except subprocess.CalledProcessError as e:
            print(f"Error pushing changes: {e}")
            raise
        finally:
            os.chdir(original_cwd)

    def cleanup(self):
        """Clean up temporary directory if using temp directory."""
        if self.use_temp_dir and self.temp_dir and os.path.exists(self.temp_dir):
            print(f"Cleaning up temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
        elif not self.use_temp_dir:
            print(f"Repository remains at: {self.temp_dir}")

    def update_docs(self, schema_dir, commit=False, push=False, commit_message=None):
        """Main method to update documentation."""
        try:
            # Step 1: Clone repository
            self.clone_repository()

            # Step 2: Preserve existing _meta.json files and Introduction content
            preserved_files = self.preserve_meta_files()

            # Step 3: Generate new documentation to a temporary directory
            with tempfile.TemporaryDirectory(prefix="notecard-docs-") as temp_output:
                print(f"Generating docs to temporary directory: {temp_output}")
                self.generate_new_docs(schema_dir, temp_output)

                # Step 4: Replace directory contents
                self.replace_directory_contents(temp_output, preserved_files)

            # Step 5: Optionally commit changes
            if commit and not self.dry_run:
                has_changes = self.commit_changes(
                    commit_message or "Update Notecard API documentation from schema"
                )

                # Step 6: Optionally push changes
                if push and has_changes:
                    self.push_changes()

            print("Documentation update completed successfully!")

        except Exception as e:
            print(f"Error updating documentation: {e}")
            raise
        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description="Update blues.dev repository with generated Notecard API documentation"
    )

    parser.add_argument(
        "--schema_dir",
        default=".",
        help="Directory containing the schema files (default: current directory)"
    )

    parser.add_argument(
        "--repo_url",
        default="https://github.com/blues/blues.dev.git",
        help="URL of the blues.dev repository to clone"
    )

    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit the changes to the repository"
    )

    parser.add_argument(
        "--push",
        action="store_true",
        help="Push the changes to the remote repository (requires --commit)"
    )

    parser.add_argument(
        "--commit-message",
        help="Custom commit message (default: 'Update Notecard API documentation from schema')"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making any changes"
    )

    parser.add_argument(
        "--dir",
        help="Directory to clone the repository to (default: use temporary directory)"
    )

    args = parser.parse_args()

    if args.push and not args.commit:
        print("Error: --push requires --commit")
        return 1

    # Validate schema directory
    if not os.path.exists(args.schema_dir):
        print(f"Error: Schema directory not found: {args.schema_dir}")
        return 1

    # Check for required files
    req_files = [f for f in os.listdir(args.schema_dir) if f.endswith('.req.notecard.api.json')]
    if not req_files:
        print(f"Error: No .req.notecard.api.json files found in {args.schema_dir}")
        return 1

    print(f"Found {len(req_files)} schema files to process")

    try:
        updater = DocsUpdater(
            repo_url=args.repo_url,
            dry_run=args.dry_run,
            clone_dir=args.dir
        )
        updater.update_docs(
            schema_dir=args.schema_dir,
            commit=args.commit,
            push=args.push,
            commit_message=args.commit_message
        )

        return 0

    except Exception as e:
        print(f"Failed to update documentation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
