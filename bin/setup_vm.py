
"""
Clone a VM from template
"""
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import atexit
import argparse
import ssl
import random
import sys
current_working_directory = "C:\ClientQAAutomation"
sys.path.append(current_working_directory)
from configuration.global_config_loader import GLOBAL_CONFIG



def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-v', '--vm-name',
                        required=False,
                        action='store',
                        help='Name of the VM you wish to make')

    parser.add_argument('--template',
                        required=True,
                        action='store',
                        help='Name of the template/VM \
                            you are cloning from')

    parser.add_argument('--datacenter-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the Datacenter you\
                            wish to use. If omitted, the first\
                            datacenter will be used.')

    parser.add_argument('--vm-folder',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the VMFolder you wish\
                            the VM to be dumped in. If left blank\
                            The datacenter VM folder will be used')

    parser.add_argument('--datastore-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Datastore you wish the VM to end up on\
                            If left blank, VM will be put on the same \
                            datastore as the template')

    parser.add_argument('--cluster-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the cluster you wish the VM to\
                            end up on. If left blank the first cluster found\
                            will be used')

    parser.add_argument('--resource-pool',
                        required=False,
                        action='store',
                        default=None,
                        help='Resource Pool to use. If left blank the first\
                            resource pool found will be used')

    parser.add_argument('--power-on',
                        dest='power_on',
                        required=False,
                        action='store_true',
                        help='power on the VM after creation')

    parser.add_argument('--no-power-on',
                        dest='power_on',
                        required=False,
                        action='store_false',
                        help='do not power on the VM after creation')

    parser.set_defaults(power_on=True)

    args = parser.parse_args()

    return args


def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print "there was an error"
            task_done = True


def get_obj_by_name(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj

def get_template(content, vimtype, name):
    template = get_obj_by_name(content, vimtype, name)
    return template

def get_datacenter(content, vimtype, name):
    datacenter = get_obj_by_name(content, vimtype, name)
    return datacenter

def get_vm_folder(content, vimtype, name):
    vm_folder = get_obj_by_name(content, vimtype, name)
    return vm_folder

def get_datastore(content, vimtype, name):
    datastore = get_obj_by_name(content, vimtype, name)
    return datastore

def get_cluster(content, vimtype, name):
    cluster = get_obj_by_name(content, vimtype, name)
    return cluster

def get_resource_pool(content, vimtype, name):
    resource_pool = get_obj_by_name(content, vimtype, name)
    return resource_pool

def clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """
    if vm_name is None:
        suffix = random.randrange(1, 100)
        suffix = str(suffix)
        vm_name = template.name + "_" +suffix
    print template.name
    print vm_name

    if datacenter_name:
        datacenter = get_datacenter(content, [vim.Datacenter], datacenter_name)
    else:
        datacenter_name = GLOBAL_CONFIG["VM_CONFIG"]["DATACENTER"]
        datacenter = get_datacenter(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_vm_folder(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    # if none get the first one
    if datastore_name:
        datastore = get_datastore(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_datastore(
            content, [vim.Datastore], template.datastore[0].info.name)


    if cluster_name:
        cluster = get_cluster(content, [vim.ClusterComputeResource], cluster_name)
    else:
        cluster_name = GLOBAL_CONFIG["VM_CONFIG"]["CLUSTER"]
        cluster = get_cluster(content, [vim.ClusterComputeResource], cluster_name)

    # if None, get the first one
    if resource_pool:
        resource_pool = get_resource_pool(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool


    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    print "cloning VM..."
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)


def main():

    host = GLOBAL_CONFIG["VM_CONFIG"]["HOST"]
    user = GLOBAL_CONFIG["VM_CONFIG"]["USER"]
    password = GLOBAL_CONFIG["VM_CONFIG"]["PASSWORD"]
    port = GLOBAL_CONFIG["VM_CONFIG"]["PORT"]

    args = get_args()

    # connect this thing
    ssl._create_default_https_context = ssl._create_unverified_context
    si = SmartConnect(
        host=host,
        user=user,
        pwd=password,
        port=port)
    # disconnect this thing
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    template = None

    template = get_template(content, [vim.VirtualMachine], args.template)

    if template:
        clone_vm(
            content, template, args.vm_name, si,
            args.datacenter_name, args.vm_folder,
            args.datastore_name, args.cluster_name,
            args.resource_pool, args.power_on)
    else:
        print "template not found"


# start
if __name__ == "__main__":
    main()
