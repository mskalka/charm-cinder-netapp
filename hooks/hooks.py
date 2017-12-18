#!/usr/bin/python
import json
import sys

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    service_name,
    relation_set,
    log,
    status_set
)

from charmhelpers.contrib.openstack.utils import (
    os_application_version_set,
)

from contexts import NetAppSubordinateContext

hooks = Hooks()


@hooks.hook('storage-backend-relation-joined',
            'storage-backend-relation-changed')
def storage_backend(rel_id=None):
    relation_set(relation_id=rel_id,
                 backend_name=service_name(),
                 subordinate_configuration=json.dumps(
                    NetAppSubordinateContext()()),
                 stateless=True,
                 )


if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log("Unknown Hook {} - skipping.".format(e))
    status_set('active', "Unit is ready")
    os_application_version_set('cinder-common')
