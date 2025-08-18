<!--
<p align="center">
  <img src="https://github.com/cthoyt/quickstatements-client/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  QuickStatements Client
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/quickstatements-client/actions/workflows/tests.yml">
        <img alt="Tests" src="https://github.com/cthoyt/quickstatements-client/actions/workflows/tests.yml/badge.svg" /></a>
    <a href="https://pypi.org/project/quickstatements_client">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/quickstatements_client" /></a>
    <a href="https://pypi.org/project/quickstatements_client">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/quickstatements_client" /></a>
    <a href="https://github.com/cthoyt/quickstatements-client/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/quickstatements_client" /></a>
    <a href='https://quickstatements_client.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/quickstatements_client/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://codecov.io/gh/cthoyt/quickstatements-client/branch/main">
        <img src="https://codecov.io/gh/cthoyt/quickstatements-client/branch/main/graph/badge.svg" alt="Codecov status" /></a>  
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-snekpack-blue" /></a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
    <a href="https://github.com/cthoyt/quickstatements-client/blob/main/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Contributor Covenant"/></a>
    <a href="https://zenodo.org/badge/latestdoi/606491168">
        <img src="https://zenodo.org/badge/606491168.svg" alt="DOI"></a>
</p>

A data model and client for Wikidata
[QuickStatements](https://quickstatements.toolforge.org).

## 💪 Getting Started

Here's how to quickly construct some QuickStatements

```python
import datetime
from quickstatements_client import DateQualifier, EntityQualifier, TextQualifier, EntityLine

subject_qid = "Q47475003"  # Charles Tapley Hoyt
subject_orcid = "0000-0003-4423-4370"
reference_url_qualifier = TextQualifier(
   predicate="S854", target=f"https://orcid.org/0000-0003-4423-4370"
)
start_date = datetime.datetime(year=2021, day=15, month=2)
start_date_qualifier = DateQualifier.start_time(start_date)
position_held_qualifier = EntityQualifier(predicate="P39", target="Q1706722")
employment_line = EntityLine(
   subject=subject_qid,
   predicate="P108",  # employer
   target="Q49121",  # Harvard medical school
   qualifiers=[reference_url_qualifier, start_date_qualifier, position_held_qualifier],
)

>>> employment_line.get_line()
'Q47475003|P108|Q49121|S854|"https://orcid.org/0000-0003-4423-4370"|P580|+2021-02-15T00:00:00Z/11|P39|Q1706722',
```

How to send some QuickStatements to the API:

```python
from quickstatements_client import QuickStatementsClient

lines = [
   employment_line,
   ...
]

client = QuickStatementsClient(token=..., username=...)
res = client.post(lines, batch_name="Test Batch")
# see also res.batch_id

import webbrowser
webbrowser.open_new_tab(res.batch_url)
```

Note: `token` and `username` are automatically looked up with `pystow` if they
aren't given. Specifically, using `pystow.get_config("quickstatements", "token)`
and `pystow.get_config("quickstatements", "username")`.

## 🚀 Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/quickstatements_client/) with uv:

```console
$ uv pip install quickstatements_client
```

or with pip:

```console
$ python3 -m pip install quickstatements_client
```

The most recent code and data can be installed directly from GitHub with uv:

```console
$ uv pip install git+https://github.com/cthoyt/quickstatements-client.git
```

or with pip:

```console
$ python3 -m pip install git+https://github.com/cthoyt/quickstatements-client.git
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are
appreciated. See
[CONTRIBUTING.md](https://github.com/cthoyt/quickstatements-client/blob/master/.github/CONTRIBUTING.md)
for more information on getting involved.

## 👋 Attribution

This code was originally written as a contribution to
[PyORCIDator](https://github.com/lubianat/pyorcidator). Special thanks to Tiago
Lubiana [@lubianat] and João Vitor [@jvfe] for discussions and testing.

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

<!--
### 🎁 Support

This project has been supported by the following organizations (in alphabetical order):

- [Biopragmatics Lab](https://biopragmatics.github.io)

-->

<!--
### 💰 Funding

This project has been supported by the following grants:

| Funding Body  | Program                                                      | Grant Number |
|---------------|--------------------------------------------------------------|--------------|
| Funder        | [Grant Name (GRANT-ACRONYM)](https://example.com/grant-link) | ABCXYZ       |
-->

### 🍪 Cookiecutter

This package was created with
[@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using
[@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack)
template.

## 🛠️ For Developers

<details>
  <summary>See developer instructions</summary>

The final section of the README is for if you want to get involved by making a
code contribution.

### Development Installation

To install in development mode, use the following:

```console
$ git clone git+https://github.com/cthoyt/quickstatements-client.git
$ cd quickstatements-client
$ uv pip install -e .
```

Alternatively, install using pip:

```console
$ python3 -m pip install -e .
```

### 🥼 Testing

After cloning the repository and installing `tox` with
`uv tool install tox --with tox-uv` or `python3 -m pip install tox tox-uv`, the
unit tests in the `tests/` folder can be run reproducibly with:

```console
$ tox -e py
```

Additionally, these tests are automatically re-run with each commit in a
[GitHub Action](https://github.com/cthoyt/quickstatements-client/actions?query=workflow%3ATests).

### 📖 Building the Documentation

The documentation can be built locally using the following:

```console
$ git clone git+https://github.com/cthoyt/quickstatements-client.git
$ cd quickstatements-client
$ tox -e docs
$ open docs/build/html/index.html
```

The documentation automatically installs the package as well as the `docs` extra
specified in the [`pyproject.toml`](pyproject.toml). `sphinx` plugins like
`texext` can be added there. Additionally, they need to be added to the
`extensions` list in [`docs/source/conf.py`](docs/source/conf.py).

The documentation can be deployed to [ReadTheDocs](https://readthedocs.io) using
[this guide](https://docs.readthedocs.io/en/stable/intro/import-guide.html). The
[`.readthedocs.yml`](.readthedocs.yml) YAML file contains all the configuration
you'll need. You can also set up continuous integration on GitHub to check not
only that Sphinx can build the documentation in an isolated environment (i.e.,
with `tox -e docs-test`) but also that
[ReadTheDocs can build it too](https://docs.readthedocs.io/en/stable/pull-requests.html).

</details>

## 🧑‍💻 For Maintainers

<details>
  <summary>See maintainer instructions</summary>

### Initial Configuration

#### Configuring ReadTheDocs

[ReadTheDocs](https://readthedocs.org) is an external documentation hosting
service that integrates with GitHub's CI/CD. Do the following for each
repository:

1. Log in to ReadTheDocs with your GitHub account to install the integration at
   https://readthedocs.org/accounts/login/?next=/dashboard/
2. Import your project by navigating to https://readthedocs.org/dashboard/import
   then clicking the plus icon next to your repository
3. You can rename the repository on the next screen using a more stylized name
   (i.e., with spaces and capital letters)
4. Click next, and you're good to go!

#### Configuring Archival on Zenodo

[Zenodo](https://zenodo.org) is a long-term archival system that assigns a DOI
to each release of your package. Do the following for each repository:

1. Log in to Zenodo via GitHub with this link:
   https://zenodo.org/oauth/login/github/?next=%2F. This brings you to a page
   that lists all of your organizations and asks you to approve installing the
   Zenodo app on GitHub. Click "grant" next to any organizations you want to
   enable the integration for, then click the big green "approve" button. This
   step only needs to be done once.
2. Navigate to https://zenodo.org/account/settings/github/, which lists all of
   your GitHub repositories (both in your username and any organizations you
   enabled). Click the on/off toggle for any relevant repositories. When you
   make a new repository, you'll have to come back to this

After these steps, you're ready to go! After you make "release" on GitHub (steps
for this are below), you can navigate to
https://zenodo.org/account/settings/github/repository/cthoyt/quickstatements-client
to see the DOI for the release and link to the Zenodo record for it.

#### Registering with the Python Package Index (PyPI)

The [Python Package Index (PyPI)](https://pypi.org) hosts packages so they can
be easily installed with `pip`, `uv`, and equivalent tools.

1. Register for an account [here](https://pypi.org/account/register)
2. Navigate to https://pypi.org/manage/account and make sure you have verified
   your email address. A verification email might not have been sent by default,
   so you might have to click the "options" dropdown next to your address to get
   to the "re-send verification email" button
3. 2-Factor authentication is required for PyPI since the end of 2023 (see this
   [blog post from PyPI](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/)).
   This means you have to first issue account recovery codes, then set up
   2-factor authentication
4. Issue an API token from https://pypi.org/manage/account/token

This only needs to be done once per developer.

#### Configuring your machine's connection to PyPI

This needs to be done once per machine.

```console
$ uv tool install keyring
$ keyring set https://upload.pypi.org/legacy/ __token__
$ keyring set https://test.pypi.org/legacy/ __token__
```

Note that this deprecates previous workflows using `.pypirc`.

### 📦 Making a Release

#### Uploading to PyPI

After installing the package in development mode and installing `tox` with
`uv tool install tox --with tox-uv` or `python3 -m pip install tox tox-uv`, run
the following from the console:

```console
$ tox -e finish
```

This script does the following:

1. Uses [bump-my-version](https://github.com/callowayproject/bump-my-version) to
   switch the version number in the `pyproject.toml`, `CITATION.cff`,
   `src/quickstatements_client/version.py`, and
   [`docs/source/conf.py`](docs/source/conf.py) to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel using
   [`uv build`](https://docs.astral.sh/uv/guides/publish/#building-your-package)
3. Uploads to PyPI using
   [`uv publish`](https://docs.astral.sh/uv/guides/publish/#publishing-your-package).
4. Push to GitHub. You'll need to make a release going with the commit where the
   version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump
   the version by minor, you can use `tox -e bumpversion -- minor` after.

#### Releasing on GitHub

1. Navigate to https://github.com/cthoyt/quickstatements-client/releases/new to
   draft a new release
2. Click the "Choose a Tag" dropdown and select the tag corresponding to the
   release you just made
3. Click the "Generate Release Notes" button to get a quick outline of recent
   changes. Modify the title and description as you see fit
4. Click the big green "Publish Release" button

This will trigger Zenodo to assign a DOI to your release as well.

### Updating Package Boilerplate

This project uses `cruft` to keep boilerplate (i.e., configuration, contribution
guidelines, documentation configuration) up-to-date with the upstream
cookiecutter package. Install cruft with either `uv tool install cruft` or
`python3 -m pip install cruft` then run:

```console
$ cruft update
```

More info on Cruft's update command is available
[here](https://github.com/cruft/cruft?tab=readme-ov-file#updating-a-project).

</details>
