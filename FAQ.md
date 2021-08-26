# Frequently Asked Questions (FAQs)

<br>

### How to version the Ansible Collection

Collection versions use [Semantic Versioning](https://semver.org/) for version numbers. Please read the official documentation for details and examples. In summary:

* Increment major (for example: x in x.y.z) version number for an incompatible API change.
* Increment minor (for example: y in x.y.z) version number for new functionality in a backwards compatible manner (for example new modules/plugins, parameters, return values).
* Increment patch (for example: z in x.y.z) version number for backwards compatible bug fixes

<br>

### How to install the Ansible Collection


#### Installing a collection using the tarball from your build

```bash
ansible-galaxy collection install esp-bitbucket-1.1.0.tar.gz --force --ignore-certs --no-deps
```

You can also provide the path to the directory containing your collections:

```bash
ansible-galaxy collection install --ignore-certs --no-deps --force --collections-path ./ansible_project/collections/ esp-bitbucket-1.1.0.tar.gz
```

```bash
ansible-galaxy collection install --ignore-certs --no-deps --force --collections-path /var/lib/awx/custom_venv/python3-ansible2.10/lib/python3.6/site-packages/ esp-bitbucket-1.1.0.tar.gz
```

<br>

#### Installing a collection from a git repository

Preferred installation method is installing a collection from a git repository.

Create `requirements.yml` file and provide required version of the collection(s), e.g.:

```yaml
collections:
  - name: https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git
    type: git
    version: 1.3.1
    #version: develop    
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

<br>

### How do I upgrade to the latest version

```bash
ansible-galaxy collection install git+https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git --force
```

<br>

### How do I install an older version

```bash
ansible-galaxy collection install git+https://bitbucket.example.com/scm/PROJECT/esp.bitbucket.git,1.3.0 --force
```

<br>

### How to find the version of the ESP Ansible Collection installed

The below command lists all the collections installed in your system and their versions. You can check the version for the entry `esp.bitbucket`

```
ansible-galaxy collection list
```

*Note: You need ansible >= 2.10 to run the above command*

<br>

### What are the dependencies for using ESP Ansible Collections

You need `ansible >= 2.10`.

<br>

### How to use collections in a playbook

Once installed, you can reference a collection content by its fully qualified collection name (FQCN):

```yaml
- hosts: all
  tasks:
    - esp.bitbucket.mymodule:
        option1: value        
```

This works for roles or any type of plugin distributed within the collection:

```yaml
- hosts: all
  tasks:
    - import_role:
        name: esp.bitbucket.myrole

    - esp.bitbucket.mymodule:
        option1: value       
```

The `collections` keyword lets you define a list of collections that your role or playbook should search for unqualified module and action names. So you can use the `collections` keyword, then simply refer to modules and action plugins by their short-form names throughout that role or playbook, e.g.:

```yaml
- hosts: all
  collections:
    - esp.bitbucket
  tasks:
    - import_role:
        name: myrole

    - mymodule:
        option1: value       
```

