# GitHub Workflows

## `update-bluesdev.yml` - Automated Documentation Updates

This workflow automatically updates the blues.dev documentation site with the latest Notecard API schemas.

### Triggers

1. **Release Trigger**: Automatically runs when a new release is published
2. **Manual Trigger**: Can be manually dispatched via GitHub Actions UI

### Setup Requirements

#### 1. GitHub Token Secret

The workflow requires a GitHub token with write access to the `blues/blues.dev` repository:

1. Create a Personal Access Token (Classic) or Fine-grained token with:
   - `contents: write` - To create branches and commits
   - `pull-requests: write` - To create pull requests
   - `metadata: read` - To read repository metadata

2. Add the token as a repository secret named `BLUES_DEV_TOKEN`:
   - Go to repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `BLUES_DEV_TOKEN`
   - Value: Your GitHub token

#### 2. Repository Permissions

Ensure the workflow has the necessary permissions by adding this to repository settings or the workflow file (already included):

```yaml
permissions:
  contents: read
```

### Manual Trigger Options

When manually triggering the workflow, you can customize:

- **branch**: Target branch in blues.dev repository (default: `main`)
- **pr_title**: Custom title for the pull request (optional)

### Workflow Behavior

#### Automatic (Release Trigger)
- Triggered when a new release is published
- Uses the release tag as the version identifier
- Creates a PR with release-specific information
- Links to the GitHub release notes

#### Manual Trigger
- Can be run on any branch/commit
- Uses timestamp as version identifier
- Creates a PR marked as manually triggered
- Useful for testing changes before release

### Output

The workflow creates:

1. **New Branch**: `update-notecard-api-docs-{version}` in blues.dev
2. **Pull Request**: With detailed change information and validation status
3. **Commit**: With comprehensive message including source commit reference

### Error Handling

- If no changes are detected, the workflow completes successfully without creating a PR
- Failed runs will show detailed error messages in the workflow log
- The workflow preserves all existing metadata and introduction files

### Monitoring

Check workflow runs in:
- Actions tab of the notecard-schema repository
- Workflow summary shows PR creation status
- Failed runs will have detailed logs for troubleshooting

### Testing

Before enabling in production:

1. Test with a fork and manual trigger
2. Verify the `BLUES_DEV_TOKEN` has proper permissions
3. Ensure the blues.dev repository structure hasn't changed
4. Run the `update_docs.py` script locally first

### Troubleshooting

Common issues:

- **Token permissions**: Ensure the token has write access to blues/blues.dev
- **Branch conflicts**: The workflow creates unique branch names to avoid conflicts
- **No changes**: If schemas haven't changed, no PR will be created (normal behavior)
- **Path issues**: Verify the blues.dev repository structure matches expectations
