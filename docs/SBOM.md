# Summary

This documentation explains what, why, and how to use Github Actions to derive
a Software Bill of Materials for this and similar applications deployed within
the github.com ecosystem for the GSA and 18F organizations.

# What?

Per the Department of Commerce's National Telecommunications and Information
Administration leading the SBOM adoption effort in the US public and private
sector, a SBOM is the "formal record containing the details and supply chain
relationships of various components used in building software. ​An SBOM is
effectively a nested inventory: a list of ingredients that make up software
components." <sup>[1](fn1)</sup>

# How?

## Determine Language Runtimes Used in the Project 

A developer of a new or existing project will have to itemize the one or more
programming language(s) the project uses or will use. The Github Actions that
CycloneDX developers are developing target a specific language to analyze its
respective package manager and generate a SBOM from the package manager manifest.

At the time of this writing, in October 2020, the CycloneDX community supports
the following language runtimes with pre-made Github Actions.

- [.NET `.sln`, `.csproj`, and `packages.config`](https://github.com/CycloneDX/gh-dotnet-generate-sbom)
- [NodeJS](https://github.com/CycloneDX/gh-node-module-generatebom)
- [Python `requirements.txt`](https://github.com/CycloneDX/gh-python-generate-sbom)
- [PHP Composer](https://github.com/CycloneDX/gh-php-composer-generate-sbom)

For this example repository, we have chosen Python.

A final example for this repo is in [`.github/workflows/sbom.yml`]([.github/workflows/sbom.yml](https://github.com/18F/10x-dux-app/blob/19e15fe9c20dbb543b3baefdadcd7921b3795898/.github/workflows/sbom.yml)).

## Create a Github Action Configuration

Once you determine the languages you need to add you will create the action file.

Inside the directory, you will create a new Github Action like so.

```sh
mkdir -p path/to/your/repo/.github/workflows
```

## Determine Code Changes That Trigger SBOM Analysis

For any Github Action, and especially SBOM analysis, you must determine which code
changes trigger a certain job. With `git` and Github, this can focus on branches
and pull requests as the fundamental way of organizing code collections and
collaborative review by a development team.

Therefore, we begin by analyzing any pull request to merge code in any branch
with any name.

```yaml
name: Generate SBOM Report

on:
  pull_request:
    branches:
      - '*'
```

## Add Checkout Component to the Action Configuration

You must first add a step to check out the source code into the Github Action
runner for analysis.

```yaml
jobs:
  analyze-sbom:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
```

## Add Language Package Manager Setup

These important steps are specific to the language runtime(s). If you select
Python from the list of supported languages above, you will potentially use
`pipenv` job steps to bootstrap requirements and create a `requirements.txt`
file.

```yaml
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Set up pipenv
      uses: dschep/install-pipenv-action@aaac0310d5f4a052d150e5f490b44354e08fbb8c
      with:
        version: 2020.6.2
    - name: Install dependencies and generate in place requirements.txt file
      run: |
        pipenv install --dev
        pipenv lock --requirements > requirements.txt
```

The need to duplicate this information from `Pipfile` to `requirements.txt` in this
case is specific to additional tooling requirements for 10x Dependency Upgrades
and research into differential requirements of dependency scanners. If a
development team uses `requirements.txt` exclusively without any use of `pipenv`,
the final two of three steps can be skipped.

```yaml
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
```

## Analyze the Package Manager Manifest to Generate a SBOM

This step will process a Python requirements file to actually build the SBOM.

A developer team may need to customize the file paths or other options of the
scan, and it is best they refer to this [upstream documentation](https://github.com/CycloneDX/gh-python-generate-sbom/blob/master/README.md).


```yaml
    - name: Generate CycloneDX SBOM report
      uses: CycloneDX/gh-python-generate-sbom@9847fabb5866e97354c28fe5f1d6fa8b71e3b38d # current v1 tag
```

If your repo is exclusively Javascript, you would replace the above with the
following example.

```yaml
    - name: Generate CycloneDX SBOM report
      uses: CycloneDX/gh-node-module-generatebom@b5753d516608ed84f7a40eb19b7687b5828b9b2d # current v1 tag
```

If your project includes both Python and Javascript, you would add this step,
specific to Javascript, beneath the previous Python-specific steps to obtain
SBOM coverage for both languages.

## Store Results in Github Artifacts for Later Retrieval and Analysis

The final step in the job stores the resulting SBOM in CycloneDX's XML format to
the Github Artifacts for your repository as a compressed ZIP archive, including
a hash in the archive's name to uniquely fingerprinting the sum of code analyzed
using `git` internals. Storing this within the repo will allow development teams
to maintain a historical list of changes and ease further integration upstream
with one or more Software Composition Analysis tools. This integration can be
done manually, but also in bulk, thanks to the capable APIs provided by [Github for Artifacts](https://docs.github.com/en/free-pro-team@latest/rest/reference/actions#artifacts)
and its other features. Additionally, using the native Github CI/CD system
without additional authentication tokens means convenient storage without
additional configuration and/or security engineering concerns.

As configured below with `if-no-files-found` a CI job will fail if a file is not
generated. This configuration can be further enhanced to prevent pull requests
where this Github Actions workflow fails, thereby preventing any promotion of
code to a known branch that cannot generate a valid SBOM.

One successful CI run with an example report [can be retrieved here](https://github.com/18F/10x-dux-app/suites/1273719661/artifacts/19646001).

```yaml
    - name: Upload CycloneDX report to project artifacts
      uses: actions/upload-artifact@27bce4eee761b5bc643f46a8dfb41b430c8d05f6 # current v2 tag
      with:
        name: 10-dux-app-${{ github.sha }}-sbom-cyclonedx
        path: ./bom.xml
        if-no-files-found: error
```

# Why?

## Why SBOM in General?

There are a multitude of reasons for supporting SBOM, which the NTIA outlines
in detail in their whitepaper about the role and benefits of its adoption. <sup>[2](fn2)</sup>

## Why CycloneDX over Other Formats?

There are multiple popular SBOM standards with variable acceptance in the
software industry at large, per the NTIA 2019 survey of the most common.<sup>[3](fn3)</sup>

- Conside SWID (a.k.a CoSWID)
- CycloneDX
- SWID
- SPDX

We aspired to achieve the following high-level requirements:

- Use free (cost and/or licensing) tools that required minimal or no additional
cost or service approvals for developers working on GSA projects.
- Use tools with the least amount of time required to develop a custom solution
or augment existing tooling.
- Use tools that, by default or with the least amount of custom development,
supported the largest number of programming language ecosystems that GSA
development teams use.
- Use a tool that best adopts or extends formats, workflows, and concepts the
standard and its tools share with other popular development tools in GSA.

With this in mind, the most readily available tools with free licenses and
supporting tooling with the Github-native Actions continuous integration and
continuous deployment platform is CycloneDX.

<a name="fn1">1</a>: https://www.ntia.gov/files/ntia/publications/sbom_overview_20200818.pdf

<a name="fn2">2</a>: https://www.ntia.gov/files/ntia/publications/ntia_sbom_use_cases_roles_benefits-nov2019.pdf

<a name="fn3">3</a>: https://www.ntia.gov/files/ntia/publications/ntia_sbom_formats_and_standards_whitepaper_-_version_20191025.pdf

# Conclusions

Using Github Actions provided by CycloneDX is effective, but addresses several
shortcomings.

- Freely available and open-source tooling is designed for use with specific
  language runtimes.
  - The burden to create and maintain tooling for ecosystems as new languages
    rise and fall in popularity, like vendors of proprietary software, have
    minor or significant lags in development. Unlike vendor solutions, there
    is no contractual backing or incentive for changes beyond the preference
    of community developers.
  - Development teams must manage one or more configuration for each language
    they use, which is increasingly onerous as the number of repos and/or
    languages they use in each repo increases.
  - Repos with one language are easy to manage, but any repo with two or more
    languages will require SBOM output be merged.
- The easiest to implement SBOM standard with freely available or open source
  tooling is CycloneDX, but SWID is popular with SCA and enterprise management
  systems, in GSA, as well as the public and private sectors overall. SWID, and
  other older standards, do not have reliable open source utilities and/or
  readily available Github Actions. Custom development will be required.
- All configuration is focused per repository, as this is the easiest point of
  integration. Although convenient, that means automating bulk adoption will be
  difficult as engineers will need knowledge of languages and configuration for
  each repo and need to be able to code that to ease bootstrapping repos in bulk.
  A solution that will make best effort attempts at auto-detection will be most
  welcome or a proprietary alternative will be required.s
- No accessible service exists to aggregate the resulting SBOMs to analyze them
  as a whole for statistics or higher-level patterns. This prototype simply
  stores them. Future work is needed to evaluate deployment of an open-source
  solution or evaluate a propriety solution, either SaaS or on-premises.