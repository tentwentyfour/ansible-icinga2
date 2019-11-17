[![Build Status](https://api.travis-ci.org/Icinga/ansible-icinga2.svg?branch=master)](https://travis-ci.org/Icinga/ansible-icinga2)

# Icinga 2 Role for Ansible

Ansible role to install and configure [Icinga 2](https://www.icinga.com/products/icinga-2/).

# This Role is in development stage

## Setup

### Limitations

The role is supported on the following platforms:

* Icinga 2 >= v2.8
* Ubuntu: 16.04, 18.04
* Debian: 8, 9, 10
* CentOS/RHEL: 6, 7

Other operating systems or versions may work but have not been tested.

## Usage

### Default behaviour

By default this role adds the official [Icinga Repository](https://packages.icinga.com) to the system and installs the
`icinga2` package.

``` yaml
- name: Default Example
  hosts: localhost
  roles:
    - icinga2
```

### Disable repository management

You may choose to use your own or the system's default repositories. Repository management can be disabled:

``` yaml
- name: Example without repository
  hosts: all
  roles:
    - icinga2
  vars:
    - i2_manage_repository: false
```

### Example: Setting up distributed monitoring

When setting up distributed monitoring, we recommend that you organise your inventory by master(s), satellites and agents of the satellites, e.g.:

```ini
[masters]
master1.fqdn
master2.fqdn

[satellites]
satellite1.fqdn
satellite2.fqdn

[agents:children]
satellite1
satellite2

[satellite1]
node1.subnet1.tld
node2.subnet1.tld

[satellite2]
node3.subnet2.tld
node4.subnet2.tld
```

_Note: You may choose to use other names than `masters`, `satellites` and `agents` by setting the variables [i2_master_group](#variable-i2_master_group), [i2_satellite_group](#variable-i2_satellite_group) and [i2_agent_group](#variable-i2_agent_group) as explained in the [variable reference](#reference) section._

Now that you have grouped your hosts appropriately, you can create variable files for the various groups (zones) and hosts that you defined in your inventory. E.g. for the above set-up, a file-structure could be:

```
- group_vars
  |- masters
  |  |- base.yml
  |  |- global-apply-rules.yml
  |  |- global-objects.yml
  |  |- global-templates.yml
  |- agents.yml
  |- all.yml
  |- satellites.yml
  |- satellite1.yml
  |- satellite2.yml
- host_vars
  |- master1.fqdn.yml
  |- master2.fqdn.yml
```

Whether you organise you variables in single files or further split them into separate files depends on the size of your set-up. In larger set-ups, it's generally recommended to split them up, since especially the `global-*.yml` files can become quite large.

#### Basic Set-up

Let's start looking at a simple host_vars example for the primary master in a multi-master set-up (e.g. `host_vars/master1.fqdn.yml`):

```yaml
---
i2_config_master: yes
i2_peer_nodes:
  - master2.fqdn.yml
i2_api_users:
  root:
    password: YF3gzWWrcB9BZagnD7L3ZwlrJljQqJiQ
    permissions:
      - status/query
      - objects/*
      - actions/*
```

As you might have guessed, the secondary master's variables file (`host_vars/master2.fqdn.yml`) looks a little similar:

```yaml
---
i2_secondary_master: yes
i2_peer_nodes:
  - master1.fqdn.yml
```

Having set those variables we made sure that both masters know which of them is the primary (and thus configuration) master and which other hosts are their peers.

The next step is to set configuration variables common to all masters in the distributed set-up. We'll do this in the `group_vars/masters/basic.yml` file:

```yaml
i2_master: yes
i2_zone: master
i2_zonename: master
i2_confd: []
i2_custom_constants:
  TicketSalt: fwe8hfbKWBHpnQIBneKiHU7XcWPsNfNca7jIOsgvwkMhR9upweeu4JHr9jtxuL0w
  ZoneName: master
```

Some of those variables are quite self-explaining, while a few others require that we briefly discuss them.
By default, icinga2 uses the master node's `NodeName` as a name for the master zone as well. In this case however, we would like to use `master` as the `zonename` for our master zone. _Note:_ The `i2_zone` variable determines which zone all hosts in this group belong to, while `i2_zonename` determines the name of the zone itself.

We also want our configuration to live inside the `zones.d` directory, which is why we disable inclusion of any other configuration directories by setting `i2_confd` to an empty list.

Last but not least, we're setting constants for the `TicketSalt` and renaming the `ZoneName` here as well. Both constants will be used later on for Icinga2's API.

This is it. With this configuration, your master nodes should be set up correctly when you apply the recipe.

#### Creating global objects

In this section, we'll see how to


#### Adding support for IDO


### Installing Icingaweb2

## Reference

- [**Variables**](#variables)
    - [Variable: i2_manage_repository](#variable-i2_manage_repository)
    - [Variable: i2_manage_package](#variable-i2_manage_package)
    - [Variable: i2_manage_package](#variable-i2_manage_epel)
    - [Variable: i2_manage_service](#variable-i2_manage_service)
    - [Variable: i2_apt_key](#variable-i2_apt_key)
    - [Variable: i2_apt_url](#variable-i2_apt_url)
    - [Variable: i2_i2_yum_key](#variable-i2_yum_key)
    - [Variable: i2_i2_yum_url](#variable-i2_yum_url)
    - [Variable: i2_confd](#variable-i2_confd)
    - [Variable: i2_timezone](#variable-i2_timezone)
    - [Variable: i2_keep_backups](#variable-i2_keep_backups)
    - [Variable: i2_manage_firewall](#variable-i2_manage_firewall)
    - [Variable: i2_include_plugins](#variable-i2_include_plugins)
    - [Variable: i2_custom_constants](#variable-i2_custom_constants)
    - [Variable: i2_host_variables](#variable-i2_host_variables)
- [**System specific variables**](#variables-os-specific)
    - [Variable: i2_conf_dir](#variable-i2_conf_dir)
    - [Variable: i2_user](#variable-i2_user)
    - [Variable: i2_group](#variable-i2_group)
    - [Variable: i2_lib_dir](#variable-i2_lib_dir)
- [**Object management**](#object-management)
    - [Variable: i2_custom_templates](#variable-i2_custom_templates)
    - [Variable: i2_custom_objects](#variable-i2_custom_objects)
    - [Variable: i2_custom_apply_rules](#variable-i2_custom_apply_rules)
    - [Variable: i2_custom_global_templates](#variable-i2_custom_global_templates)
    - [Variable: i2_custom_global_objects](#variable-i2_custom_global_objects)
    - [Variable: i2_custom_global_apply_rules](#variable-i2_custom_global_apply_rules)
    - [Variable: i2_custom_ignore_zone_directories](#variable-i2_ignore_zone_directories)
    - [Variable: i2_remove_unmanaged_objects](#variable-i2_remove_unmanaged_objects)
- [**Distributed Monitoring**](#distributed-monitoring)
    - [Variable: i2_master](#variable-i2_master)
    - [Variable: i2_config_master](#variable-i2_config_master)
    - [Variable: i2_secondary_master](#variable-i2_secondary_master)
    - [Variable: i2_peer_nodes](#variable-i2_peer_nodes)
    - [Variable: i2_zone](#variable-i2_zone)
    - [Variable: i2_zonename](#variable-i2_zonename)
    - [Variable: i2_master_group](#variable-i2_master_group)
    - [Variable: i2_satellite_group](#variable-i2_satellite_group)
    - [Variable: i2_agent_group](#variable-i2_agent_group)
    - [Variable: i2_api_users](#variable-i2_api_users)
- [**Public Key Infrastructure**](#public-key-management)
    - [Variable: i2_ca_file](#variable-i2_ca_file)
    - [Variable: i2_pki_file](#variable-i2_pki_file)
- [**IDO**](#ido)
    - [Variable: i2_setup_ido](#variable-i2_setup_ido)
    - [Variable: i2_ido_backend](#variable-i2_ido_backend)
    - [Variable: i2_ido_params](#variable-i2_ido_params)
    - [Variable: i2_ido_mysql_schema](#variable-i2_ido_mysql_schema)
- [**Feature Usage**](#feature-usage)
    - [Variable: i2_custom_features](#variable-i2_custom_features)
    - [Variable: i2_features_available_dir](#variable-i2_features_available_dir)
    - [Variable: i2_features_enabled_dir](#variable-i2_features_enabled_dir)
    - [Variable: i2_remove_unmanaged_features](#variable-i2_remove_unmanaged_features)
- [**Icingaweb2**](#icingaweb2)
    - [Variable: i2_setup_webui](#variable-i2_setup_webui)
    - [Variable: i2_webui_params](#variable-i2_webui_params)
    - [Variable: i2_webui_php_all](#variable-i2_webui_php_all)
    - [Variable: i2_webui_modules](#variable-i2_webui_modules)
    - [Variable: i2_webui_connectfrom](#variable-i2_webui_connectfrom)
    - [Variable: i2_webui_mysql_schema](#variable-i2_webui_mysql_schema)
- [**Handlers**](#handlers)
    - [Handler: start icinga2](#handler-start-icinga2)
    - [Handler: reload icinga2](#handler-reload-icinga2)

### Variables

#### Variable: `i2_manage_repository`
Whether to add the official [Icinga Repository](https://packages.icinga.com/) to the system or not. Defaults to `true`.

#### Variable: `i2_manage_package`
Whether to install packages or not. Defaults to `true`.

#### Variable: `i2_manage_epel`
Whether to install the EPEL release package. Defaults to `true`.

#### Variable: `i2_manage_service`
Whether to start, restart and reload the Icinga 2 on changes or not. Defaults to `true`.

#### Variable: `i2_apt_key`
GPG key used to verify packages on APT based system. The key will be imported. Defaults to
`https://packages.icinga.com/icinga.key`.

#### Variable: `i2_apt_url`
Repository URL for APT based systems. Defaults
to `deb http://packages.icinga.com/{{ ansible_distribution|lower }} icinga-{{ ansible_distribution_release }} main`.
This may be customized if you have a local mirror.

#### Variable: `i2_yum_key`
GPG key used to verify packages on YUM based sytems. The key URL will be added to the repository file. Defaults to
`https://packages.icinga.com/icinga.key`.

#### Variable: `i2_yum_url`
Repository URL for YUM based sytem. Defaults to `http://packages.icinga.com/epel/$releasever/release/`. This may be
customized if you have a local mirror.

#### Variable: `i2_confd`
By default, configuration located in `/etc/icinga2/conf.d` is included. This list may be modified to include additional directories or set to `[]` to not include `conf.d` at all (e.g. on distributed installations).
Defaults to `[ "conf.d" ]`.

#### Variable: `i2_include_plugins`
The [ITL](https://www.icinga.com/docs/icinga2/latest/doc/10-icinga-template-library/) comes with a set of
pre-configured check commands. This variable defines what to include. Defaults to
`["itl", "plugins", "plugins-contrib", "manubulon", "windows-plugins", "nscp"]`

#### Variable: `i2_const_plugindir`
Set `PluginDir` constant. Defaults to `{{ i2_lib_dir }}/nagios/plugins`.

#### Variable: `i2_const_manubulonplugindir`
Set `ManubulonPluginDir` constant. Defaults to `{{ i2_lib_dir }}/nagios/plugins`.

#### Variable: `i2_const_plugincontribdir`
Set `PluginContribDir` constant. Defualts to `{{ i2_lib_dir }}/nagios/plugins`.

#### Variable: `i2_const_nodename`
Set `NodeName` constant. Defaults to `{{ ansible_fqdn }}`.

#### Variable: `i2_const_zonename`
Set `ZoneName` constant. Defaults to `{{ ansible_fqdn }}`.

#### Variable: `i2_const_ticketsalt`
Set `TicketSalt` constant. Empty by default.

#### Variable: `i2_custom_constants`
Add custom constants to `constants.conf`. Must be a dictionary. Defaults to: `{}`

Some default required values are specified in `i2_default_constants` and merged with this variable. Use this variable to override these default values, or add your own constants.

Default values of `i2_default_constants`:
```yaml
  PluginDir: "{{ i2_lib_dir }}/nagios/plugins"
  ManubulonPluginDir: "{{ i2_lib_dir }}/nagios/plugins"
  PluginContribDir: "{{ i2_lib_dir }}/nagios/plugins"
  NodeName: "{{ ansible_fqdn }}"
  ZoneName: "{{ i2_zonename }}"
  TicketSalt: ""
```

Example usage:
```yaml
  vars:
    - i2_custom_constants:
        TicketSalt: "My ticket salt"
        Foo: "bar"
```

### System specific variables
The following variables are system specific and don't need to be overwritten in most cases. Be careful when making
changes to any of these variables.

#### Variable: `i2_conf_dir`
Base Icinga 2 configuration directory. Defaults to `/etc/icinga2`.

#### Variable: `i2_user`
Icinga 2 running as user. Default depends on OS.

#### Variable: `i2_group`
Icinga 2 running as group. Default depends on OS.

#### Variable: `i2_lib_dir`
Lib dir. Default depends on OS.

### Feature Usage

#### Variable: `i2_custom_features`
Features are maintained via the dictionary `i2_custom_features`.
By default features won't be managed by ansible unless `i2_custom_features` is non-empty.

There exist two levels of feature management, simple (de)-activation and activation including further customization:
- To enable or disable a feature for which configuration exists within the `features-available` directory, you may simply pass `yes` or `no`.
- To further customize a feature, that is create or modify the configuration in `features-available` and then activate it, supply a hash consisting of `type` and `attributes` keys as in the following example:

Example usage:

```yaml
vars:
  - i2_custom_features:
    debuglog: no                # Disable available feature
    checker: yes                # Enable available feature
    # Customize and enable features:
    api:                        # ObjectName
      type: ApiListener         # ObjectType
      attributes:
        accept_command: true    # ObjectAttribute
        accept_config: true     # ObjectAttribute
    graphite:
      type: GraphiteWriter
      attributes:
        host: "127.0.0.1"
        port: "2004"
```

#### Variable: `i2_remove_unmanaged_features`
The variable `i2_remove_unmanaged_features` change the behaviour of the feature handling.
It will remove all **unmanaged** `.conf` files from the directory `/etc/icinga2/features-enabled` and let you manage only your defined features. Defaults to `false`.

### Handlers

#### Handler: `start icinga2`
This handler starts Icinga 2. It is only used to make sure Icinga 2 is running. You can prevent this handler from
being triggered by setting `i2_manage_service` to false.

#### Handler: `reload icinga2`
This handler reloads Icinga 2 when configuration changes. You can prevent this handler from being triggered by setting
`i2_manage_service` to false.

## Development
A roadmap of this project is located at https://github.com/Icinga/ansible-icinga2/milestones. Please consider this
roadmap when you start contributing to the project.

### Contributing
When contributing several steps such as pull requests and proper testing implementations are required. Find a detailed
step by step guide in [CONTRIBUTING.md](CONTRIBUTING.md).

### Testing
Testing is essential in our workflow to ensure a good quality. We use Molecule to test all
components of this role. For a detailed description see [TESTING.md](TESTING.md).

## Release Notes
When releasing new versions we refer to [SemVer 1.0.0](http://semver.org/spec/v1.0.0.html) for version numbers. All steps required when creating a new
release are described in [RELEASE.md](RELEASE.md)

See also [CHANGELOG.md](CHANGELOG.md)

## Authors
[AUTHORS](AUTHORS) is generated on each release.
