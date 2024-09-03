# Task API charm

Charmhub package name: task-api
More information: <https://charmhub.io/task-api>

## Overview

The [task-api](https://charmhub.io/task-api) is a subordinate charm that provides webhooks to run commands in a deployed application.

This charm allows for the configuration of custom actions that can be triggered through webhooks.

It aims to provided an external trigger to allow things to be done programmatically in the units
without the need to ssh'ing into units.

This charm is useful for Juju admins who need to automate tasks in a multitude of
applications using different charms or would like to grant limited access to users, e.g: restarting a service.
