from charmhelpers.core.hookenv import (
    config,
    service_name
    )

from charmhelpers.contrib.openstack.context import (
    OSContextGenerator,
    )


class NetAppIncompleteConfiguration(Exception):
    pass


class NetAppSubordinateContext(OSContextGenerator):

    def __call__(self):
        ctxt = []
        for key in config:
            ctxt.append((key.replace('-', '_'),
                        config[key]))
        service = service_name()
        # add constants at the end, then dedup with order prservation
        # this allows the user to override if they want.
        ctxt.append(('volume_backend_name', service))
        ctxt.append(('volume_driver',
                     'cinder.volume.drivers.netapp.common.NetAppDriver'))
        return {
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {
                        service: ctxt,
                    },
                }
            }
        }
