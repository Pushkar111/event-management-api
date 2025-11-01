# Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style update (formatting, renaming)
- [ ] ♻️ Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test update
- [ ] 🔧 Configuration change
- [ ] 🔒 Security fix

## Related Issues

<!-- Link to related issues. Use "Fixes #123" to auto-close issues when PR is merged -->

Fixes #(issue number)
Related to #(issue number)

## Changes Made

<!-- List the main changes made in this PR -->

- Change 1
- Change 2
- Change 3

## Testing

### Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing locally
- [ ] Code coverage maintained/improved

### Manual Testing

<!-- Describe the testing you've done -->

**Steps to test:**
1. Step 1
2. Step 2
3. Step 3

**Expected behavior:**
<!-- Describe what should happen -->

**Actual behavior:**
<!-- Describe what actually happens -->

## Screenshots/Recordings

<!-- If applicable, add screenshots or screen recordings -->

## Checklist

### Code Quality

- [ ] My code follows the project's style guidelines (PEP 8, Black formatting)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

### Database

- [ ] Database migrations created (if applicable)
- [ ] Migrations tested and working
- [ ] Backward compatible (if applicable)

### Security

- [ ] No sensitive data (passwords, keys, tokens) in code
- [ ] Environment variables used for configuration
- [ ] Input validation implemented
- [ ] SQL injection prevention checked
- [ ] XSS prevention checked

### Performance

- [ ] Query optimization considered (select_related, prefetch_related)
- [ ] No N+1 query problems introduced
- [ ] Caching implemented where appropriate
- [ ] Celery tasks used for long-running operations

### Documentation

- [ ] README.md updated (if needed)
- [ ] API documentation updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] Docstrings added/updated
- [ ] Comments added for complex logic

## Deployment Notes

<!-- Any special deployment considerations? -->

- [ ] Requires environment variable changes
- [ ] Requires database migration
- [ ] Requires data migration
- [ ] Requires cache clear
- [ ] Requires Celery worker restart
- [ ] Requires configuration changes

### Environment Variables

<!-- List any new environment variables that need to be set -->

```bash
NEW_ENV_VAR=value
```

### Migration Commands

<!-- List any special commands needed -->

```bash
python manage.py migrate
python manage.py some_custom_command
```

## Breaking Changes

<!-- List any breaking changes and migration path for users -->

**None** OR:

1. Breaking change description
   - **Before:** How it worked before
   - **After:** How it works now
   - **Migration:** How to migrate

## Additional Context

<!-- Add any other context about the PR here -->

## Reviewer Notes

<!-- Specific things you want reviewers to focus on -->

- Please review the implementation of X
- Pay special attention to Y
- Alternative approaches considered: Z

---

## For Reviewers

### Review Checklist

- [ ] Code quality and style
- [ ] Test coverage adequate
- [ ] Documentation clear and complete
- [ ] No security concerns
- [ ] Performance considerations addressed
- [ ] Breaking changes properly documented
- [ ] Database migrations reviewed

### Questions for Author

<!-- Reviewers: Add your questions here -->
