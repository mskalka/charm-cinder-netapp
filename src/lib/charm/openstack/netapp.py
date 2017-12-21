import json

from charmhelpers.core.hookenv import (
    config,
    log,
    relation_ids,
    relation_set,
    status_set,
    service_name
)

from charmhelpers.contrib.openstack.context import OSContextGenerator
import charmhelpers.contrib.openstack.utils as ch_utils
from charms_openstack.charm import OpenStackCharm


class NetAppCharm(OpenStackCharm):
    service_name = 'cinder-netapp'
    name = 'netapp'
    packages = ['']
    release = 'ocata'

    def set_relation_data(self):
        rel_id = relation_ids('storage-backend')
        if not len(rel_id):
            log("No 'storage-backend' relation detected, skipping.")
        else:
            relation_set(
                relation_id=rel_id[0],
                backend_name=config()['volume-backend-name'] or service_name(),
                subordinate_configuration=json.dumps(
                    NetAppSubordinateContext()()),
                stateless=True,
            )
            log('Relation data set for {}'.format(rel_id[0]))
        status_set('active', 'Unit is ready')


class NetAppSubordinateContext(OSContextGenerator):
    interfaces = ['storage-backend']

    def __call__(self):
        log('Generating cinder.conf stanza')
        ctxt = []
        charm_config = config()
        service = charm_config['volume-backend-name'] or service_name()
        for key in charm_config.keys():
            if key is 'volume-backend-name':
                ctxt.append(('volume_backend_name', service_name()))
            ctxt.append((key.replace('-', '_'), charm_config[key]))
        ctxt.append((
            'volume_driver',
            'cinder.volume.drivers.netapp.common.NetAppDriver'))
        for rid in relation_ids(self.interfaces[0]):
            log('Setting relation data for {}'.format(rid))
            self.related = True
            return {
                "cinder": {
                    "/etc/cinder/cinder.conf": {
                        "sections": {
                            service: ctxt
                        }
                    }
                }
            }
