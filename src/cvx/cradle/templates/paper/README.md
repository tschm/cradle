# Paper template

The template supports the fast creation of repositories of LaTeX documents.

```bash
Copying from template version None
    create  paper
    create  paper/references.bib
    create  paper/{{ project_name }}.tex
    create  README.md
    create  .gitignore
    create  .github
    create  .github/workflows
    create  .github/workflows/latex.yml
    create  Makefile
```

When you run cradle, it prompts for these variables
and replaces them in filenames and file contents.

With every push into the repo the document is compiled
and published on a draft branch.

## :warning: Private repositories

Using workflows in private repos will eat into your monthly GitHub bill.
You may want to restrict the workflow to operate only when merging on the main branch
while operating on a different branch or deactivate the flow.
