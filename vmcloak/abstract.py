#!/usr/bin/env python
# Copyright (C) 2014 Jurriaan Bremer.
# This file is part of VMCloak - http://www.vmcloak.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import logging
import os.path
import random
import tempfile

from vmcloak.conf import load_hwconf
from vmcloak.rand import random_serial, random_uuid

log = logging.getLogger()


class VM(object):
    FIELDS = {}
    vm_dir_required = True
    data_dir_required = True

    def __init__(self, name, vm_dir=None, data_dir=None, temp_dir=None):
        self.name = name
        self.vm_dir = vm_dir
        self.data_dir = data_dir

        self.network_idx = 0

        if self.vm_dir_required and not vm_dir:
            log.error('Please provide --vm-dir a directory for the '
                      'associated VM files.')
            log.info('Optionally this directory can be put into tmpfs for '
                     'improved speed.')
            exit(1)

        if self.data_dir_required and not data_dir:
            log.error('Please provide --data-dir a directory for the '
                      'harddisk and .iso files for the virtual machine.')
            log.info('It is recommended to store this directory on a regular '
                     'harddisk or SSD - not in tmpfs.')
            exit(1)

        if data_dir:
            self.iso_path = os.path.join(self.data_dir, '%s.iso' % self.name)
        else:
            _, self.iso_path = tempfile.mkstemp(suffix='.iso', dir=temp_dir)

    def create_vm(self):
        """Create a new Virtual Machine."""
        raise

    def delete_vm(self):
        """Delete an existing Virtual Machine and its associated files."""
        raise

    def ramsize(self, ramsize):
        """Modify the amount of RAM available for this Virtual Machine."""
        raise

    def os_type(self, os, sp):
        """Set the OS type to the OS and the Service Pack."""
        raise

    def create_hd(self, fsize):
        """Create a harddisk."""
        raise

    def attach_iso(self, iso):
        """Attach a ISO file as DVDRom drive."""
        raise

    def detach_iso(self):
        """Detach the ISO file in the DVDRom drive."""
        raise

    def set_field(self, key, value):
        """Set a specific field of a Virtual Machine."""
        raise

    def modify_mac(self, mac=None):
        """Modify the MAC address of a Virtual Machine."""
        raise

    def network_index(self):
        """Get the index for the next network interface."""
        ret = self.network_idx
        self.network_idx += 1
        return ret

    def hostonly(self, macaddr=None, index=1):
        """Configure a hostonly adapter for the Virtual Machine."""
        raise

    def bridged(self, interface, macaddr=None, index=1):
        """Configure a bridged adapter for the Virtual Machine."""
        raise

    def nat(self, macaddr=None, index=1):
        """Configure NAT for the Virtual Machine."""
        raise

    def hwvirt(self, enable=True):
        """Enable or disable the usage of Hardware Virtualization."""
        raise

    def start_vm(self, visible=False):
        """Start the associated Virtual Machine."""
        raise

    def snapshot(self, label):
        """Take a snapshot of the associated Virtual Machine."""
        raise

    def stopvm(self):
        """Stop the associated Virtual Machine."""
        raise

    def list_settings(self):
        """List all settings of a Virtual Machine."""
        raise

    def init_vm(self, profile):
        """Initialize fields as specified by `FIELDS`."""
        hwconf = load_hwconf(profile=profile)

        def _init_vm(path, fields):
            for key, value in fields.items():
                key = path + '/' + key
                if isinstance(value, dict):
                    _init_vm(key, value)
                else:
                    if isinstance(value, tuple):
                        k, v = value
                        if k not in hwconf or not hwconf[k]:
                            value = 'To be filled by O.E.M.'
                        else:
                            if k not in config:
                                config[k] = random.choice(hwconf[k])

                            value = config[k][v]

                            # Some values have to be generated randomly.
                            if value is not None:
                                if value.startswith('<SERIAL>'):
                                    length = int(value.split()[-1])
                                    value = random_serial(length)
                                elif value.startswith('<UUID>'):
                                    value = random_uuid()

                    if value is None:
                        value = "To be filled by O.E.M."

                    log.debug('Setting %r to %r.', key, value)
                    ret = self.set_field(key, value)
                    if ret:
                        log.debug(ret)

        config = {}
        _init_vm('', self.FIELDS)
