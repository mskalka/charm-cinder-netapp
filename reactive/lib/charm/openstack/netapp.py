from charmhelpers.core.hookenv import (
    config,
    relation_ids,
    status_set
)
from charmhelpers.contrib.openstack.context import OSContextGenerator
import charms_openstack.charm


def check_status():
    NetAppCharm.singleton.check_status()
    status_set('Ready')


def set_relation_data():
    NetAppCharm.singleton.set_relation_data()


class NetAppCharm(charms_openstack.charm.OpenStackCharm):
    service_name = 'cinder-netapp'
    release = 'pike'
    name = 'netapp'
    packages = ['']

    def set_relation_data(self):
        rel_id = relation_ids('storage-backend')
        relation_set(
            relation_id=rel_id[0],
            backend_name=service_name(),
            subordinate_configuration=json.dumps(NetAppSubordinateContext()()),
            stateless=True,
        )

    def check_status(self):
        pass


class NetAppSubordinateContext(OSContextGenerator):
    interfaces = ['storage-backend']

    def __call__(self):
        ctxt = []
        config = config()
        service = config['volume-backend-name'] or service_name()
        for key in config.keys():
            if key is 'volume-backend-name':
                ctxt.append(('volume_backend_name', service))
            ctxt.append(([key.replace('-', '_')], config[key]))
        ctxt.append((
            'volume_driver',
            'cinder.volume.drivers.netapp.common.NetAppDriver'))
        for rid in relation_ids(self.interfaces[0]):
            self.related = True
            for unit in related_units(rid):
                return {
                    "cinder": {
                        "/etc/cinder/cinder.conf": {
                            "sections": {
                                service: ctxt
                            }
                        }
                    }
                }
