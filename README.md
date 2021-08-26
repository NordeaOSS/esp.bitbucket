# esp.bitbucket Ansible Collection

<br>

This Bitbucket Ansible Collection provides an easy way to manage Bitbucket Server resources / assets using Ansible.

<br>

## Building collection

> This section is intended for collection developers. If you only use the collection, check [Installation](#Installation) section instead.

To build a collection, set `version: x.y.z` in your [galaxy.yml](galaxy.yml) file and run ansible-galaxy collection build from inside the root directory of the collection:

```bash
ansible-galaxy collection build --force --ignore-certs --no-deps
```

Alternatively, run [build_collection.sh](tools/build_collection.sh) script from tools directory:

```bash
./tools/build_collection.sh
```

This creates a tarball of the built collection in the current directory which can be used to install the collection, e.g.:

```bash
ansible-galaxy collection install esp-bitbucket-1.3.1.tar.gz --force --ignore-certs --no-deps
```

#### Collection versions

Check the [Frequently Asked Questions](FAQ.md) page.

#### Creating Git Tags with versions

You must create a git tag with new collection version and push this to Bitbucket. This way it will be possible to install required versions with ansible-galaxy command.

```bash
git commit -am "Commit message"
git tag -a 1.4.0 -m "version 1.4.0"
git push -u origin 1.4.0
git push
```

<br>

## Installation

Preferred installation method is installing a collection from a git repository.

Create `requirements.yml` file and provide required version of the collection(s), e.g.:

```yaml
collections:
  - name: https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git
    type: git
    version: 1.1.0
    #version: master    
```

Next, run ansible-galaxy command with `requirements.yml` file as argument:

```bash
ansible-galaxy collection install -r requirements.yml --force --ignore-certs --no-deps
```

Alternatively, you may provide a repository URL in ansible-galaxy command:

```bash
# Install a collection from a repository using the latest commit on the branch 'master'
ansible-galaxy collection install git+https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git --force --ignore-certs --no-deps

# Install a collection from a repository using version 1.1.0
ansible-galaxy collection install git+https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git,1.1.0 --force --ignore-certs --no-deps
```

For more info about installation and troubleshooting check the [Frequently Asked Questions](FAQ.md) page

<br>

## Samples

The project includes a catalog of ESP Ansible module samples that illustrate using the modules and roles to carry out common tasks.

The samples are organized in groups under [the samples directory](samples). Begin by reviewing the Readme.md file that you will find in each sample's root directory.

<br>

## Documentation

To view the module documentation, use this command:

```bash
ansible-doc esp.bitbucket.[module_name]
```

<br>

## Ansible Tower and AWX

`esp.bitbucket` Ansible Collection supports Ansible Tower and AWX. 

Simply add a reference to the collection in your `${PROJECT_NAME}/collections/requirements.yml` file explicitly providing required version, e.g.:

```yaml
collections:
  - name: https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git
    type: git
    version: 1.1.0
    #version: master    
```

AWX automatically installs dependencies from the `requirements.yml` file. You don't need to take any action on AWX.

> Note: you need `ansible >= 2.10` on AWX to properly install ansible collections from `requirements.yml` file. Please select appriopriate custom virtual env in either project or job template definition.

<br>

## Help

- For FAQs, check the [Frequently Asked Questions](FAQ.md) page.
- To file bugs or feature requests, contact authors or contribute.

<br>

## Changes

See [CHANGELOG](CHANGELOG.md).

<br>

## License

GPLv3 - GNU General Public License v3.0

<br>

## Authors

- [Krzysztof Lewandowski](mailto:Krzysztof.Lewandowski@nordea.com)
- [Pawel Smolarz](mailto:Pawel.Smolarz@nordea.com)

