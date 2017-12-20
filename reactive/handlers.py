import charms.reactive as reactive
import charm.openstack.netapp


@reactive.when_not('charm.installed')
def install_cinder_netapp():
    reactive.set_state('charm.installed')


@reactive.when('storage-backend.connected', 'config.changed')
def storage_backend():
    netapp.set_relation_data()
    reactive.set_state('storage-backend.available')
    netapp.check_status()
