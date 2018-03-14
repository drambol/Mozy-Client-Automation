
from __future__ import print_function  # backwards compatibility with >=  2.6

import datetime
import re
import time
import sys
import pyVmomi
from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
import requests


# Disable SSL warnings in output
requests.packages.urllib3.disable_warnings()


class VMHelper(object):
    '''Creates connection with vShera, rename_vm, create snapshot,
    revert to current snapshot, power on, power off.
    TODO: Add all actions with VMs which provided below the class'''

    def __init__(self, host='10.29.98.99', user='root',
                 pwd='password', port='443'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.si = None
        self.session_id = None

    def connect(self):
        '''initiats connection'''
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            self.si = SmartConnect(host=self.host, user=self.user,
                                   pwd=self.pwd, port=self.port)
            if not self.si:
                raise RuntimeError("Failed to establish connection to VC")
            # doing this means you don't need to remember to disconnect you
            # script/objects
            atexit.register(Disconnect, self.si)
        except vmodl.MethodFault as error:
            return -1
        return self.si

    def is_connected(self):
        '''
        Checks if connection is alive'''
        if self.connect():
            self.session_id = self.si.content.sessionManager.currentSession.key
        return self.session_id

    def snapshot_create(self, vmname, name=None):
        '''create snapshot of VM
           returns true if everythong is fine'''
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        if name is None:
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%m%d%H%M", timeArray)
            name = "Snapshot"+"_"+otherStyleTime
        task = vm.CreateSnapshot(name, memory=False, quiesce=False)
        _wait_for_task(task)

    def snapshot_revert(self, vmname):
        '''revert to specified shapshot of VM or current snapshot
        if the name is not provided
        returns True if everythong is fine'''
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        task = vm.RevertToCurrentSnapshot()
        _wait_for_task(task)

    def snapshot_revert_by_name(self, vmname, snapshot_name):
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        snapshots = vm.snapshot.rootSnapshotList
        for snapshot in snapshots:
            if snapshot_name == snapshot.name:
                snap_obj = snapshot.snapshot
                print("Reverting snapshot ", snapshot.name)
                task = snap_obj.RevertToSnapshot_Task()
                _wait_for_task(task)


    def vm_power_on(self, vmname):
        '''Power ON VM
        raises Exception if tne vm is absent
        returns true if everythong is fine'''
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            task = vm.PowerOn()
            _wait_for_task(task)

    def vm_power_off(self, vmname):
        '''Power ON VM
        raises Exception if tne vm is absent
        returns true if everythong is fine'''
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            task = vm.PowerOff()
            _wait_for_task(task)


    def vm_restart(self,vmname):
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            task = vm.ResetVM_Task()
            _wait_for_task(task)

    def vm_rename(self, vmname, newname):
        '''executes rename VM
           raises Exception if tne vm is absent
           raises Exception if a new name exists alrady
           returns the new vm name if everythong is fine'''
        if not self.is_connected():
            self.connect()
        vm = get_vm_object_by_name(self.si, vmname)
        checkname = get_vm_object_by_name(self.si, newname)
        if checkname is None:
            task = vm.Rename(newname)
            _wait_for_task(task)
        else:
            raise Exception("The name %s exists alrady" % newname)


def getvms(vm, allvms, depth=1):
    """
    Helper method to get all vms in Virtual Center.
    getvms (vm, allvms, depth = 1)
    vm is object(can be vmfolder or vm
    allvms is list which holds list of all vm objects in Virtual Center
    maxdept is how far script will go looking for vm in the folder structure
    """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            getvms(c, allvms, depth + 1)
        return

    allvms.append(vm)


def getvms_folder(vm, foldername):
    """
    Helper method to get all vms in folder in Virtual Center.
    getvms_folder (vm, folderbane)
    vm is object(can be vmfolder or vm
    foldername name of vm folder
    Return folder object or None if not found
    """
    if vm.name == foldername:
        if hasattr(vm, 'childEntity'):
            return vm
    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        vmList = vm.childEntity
        for c in vmList:
            getvms_folder(c, foldername)
    return None


def _wait_for_task(task, error_ok=True):
    """
    Helper method which waits for task to finish
    _wait_for_task(task)
    task is object of task on Virtual Center
    """
    while task.info.state != "success":
        if task.info.state == "error":
            if error_ok:
                break
            else:
                raise RuntimeError("The task failed")
        time.sleep(5)


def get_all_vm_objs_folder(si, folder):
    """
    This method returns the list of all vm objects in a folder
    get_all_vm_objs_folder()
    """
    content = si.RetrieveContent()
    allvms = []
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            vmfolder_obj = None
            for vm in vmList:
                vmfolder_obj = getvms_folder(vm, folder)
                if vmfolder_obj is not None:
                    getvms(vm, allvms)
    return allvms


def get_space_in_datastore(si, datastore_name):
    """
    Get space left in datastore in bytes
    """
    content = si.RetrieveContent()
    datastore = get_obj(content, [vim.Datastore], datastore_name)
    summary = datastore.summary
    available_space = summary.freeSpace
    return available_space


def filter_vms(vmlist, filter_list):
    """
    Filter vms from a list based on list of strings
    """
    work_vms = []
    for vm in vmlist:
        vmname = vm.name
        vm_does_not_match = False
        for filter_name in filter_list:
            if vmname.find(filter_name) == -1:
                vm_does_not_match = True
        if vm_does_not_match:
            continue
        work_vms.append(vm)
    return work_vms


def get_date_obj(vm, p):
    """
    Get date object from VM
    """
    m = p.match(vm.name)
    vmtime = None
    if m:
        vmtime = m.group(1)
    dateobj = None
    try:
        dateobj = datetime.datetime.strptime(vmtime,
                                             "%Y-%m-%d-%H-%M-%S")
    except ValueError:
        return None
    return dateobj


def get_old_product_images(product, vmlist, numdays):
    """
    Delete VMs which are older than numdays
    """
    p = re.compile(product + '-(\d.*?)-[A-Za-z].*')
    now = datetime.datetime.now()
    res_vms = []
    for vm in vmlist:
        dateobj = get_date_obj(vm, p)
        if dateobj is None:
            continue
        timedelta = now - dateobj
        agedays = timedelta.days
        if agedays < numdays:
            continue
        res_vms.append(vm)
    return res_vms


def get_latest_product_image(product, vmlist):
    """
    Get latest product image
    """
    return get_product_image(product, vmlist)


def get_product_image(product, vmlist, oldest=False):
    """
    Get latest or oldest image
    """
    p = re.compile(product + '-(\d.*?)-[A-Za-z].*')
    vm_obj = None
    vm_time = None
    if (len(vmlist) == 0 or not hasattr(vmlist[0], "AnswerVM")):
        raise RuntimeError("Either list is empty or "
                           "Object is not a VM object")
    for vm in vmlist:
        dateobj = get_date_obj(vm, p)
        if dateobj is None:
            continue
        if vm_time is None:
            vm_time = dateobj
            vm_obj = vm
        else:
            if oldest:
                if dateobj < vm_time:
                    vm_obj = vm
                    vm_time = dateobj
            else:
                if dateobj > vm_time:
                    vm_obj = vm
                    vm_time = dateobj
    return vm_obj


def get_oldest_product_image(product, vmlist):
    """
    Get oldest product image
    """
    return get_product_image(product, vmlist, oldest=True)


def get_all_vm_objs(si):
    """
    This method returns the list of all vm objects in virtual center
    get_all_vm_objs()
    """
    content = si.RetrieveContent()
    allvms = []
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for vm in vmList:
                getvms(vm, allvms)
    return allvms


def get_obj(content, vimtype, name):
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


def annotate(vm, str):
    """
    Helper method which calls vcenter to annotate a VM with string
    annotate(vm, str)
    vm - Virtual Machine object
    str - String VM will be annotated with
    """
    myspec = vim.vm.ConfigSpec()
    myspec.annotation = str
    task = vm.ReconfigVM_Task(myspec)
    _wait_for_task(task)


def create_snapshot(vm, name):
    """
    Deprecated. Use class VMHelper.
    Helper method to create snapshot
    create_snapshot(vm, name)
    vm - Virtual Machine object
    name - Name of the snapshot
    """
    task = vm.CreateSnapshot(name, memory=False, quiesce=False)
    _wait_for_task(task)


def revert_to_curr_snapshot(vm):
    """
    Deprecated. Use class VMHelper.
    Helper method to revert to current snapshot
    revert_to_curr_snapshot(vm)
    vm - Virtual Machine object
    """
    task = vm.RevertToCurrentSnapshot()
    _wait_for_task(task)


def get_vm_object_by_name(si, vmname):
    """
    Helper method to get the VM object based on name
    get_vm_object_by_name(si, vmname)

    si - Service instance
    vmname - Name of the VM
    """
    allvms = get_all_vm_objs(si)
    vm_match_list = []
    for vm in allvms:
        try:
            vm.summary.config.name
        except AttributeError:
            print("The attribute name is not there in this entity")
            continue
        if vm.summary.config.name == vmname:
            vm_match_list.append(vm)
    if len(vm_match_list) > 1:
        raise Exception("Found more then 1 VM matching name:%s" % vmname)
    if len(vm_match_list) == 1:
        return vm_match_list[0]
    return None


def power_on(vm):
    """
    Deprecated. Use class VMHelper.
    Helper method to power on (vm)
    vm - Virtual Machine object
    """
    task = vm.PowerOn()
    _wait_for_task(task)


def power_off(vm):
    """
    Helper method to power off (vm)
    vm - Virtual Machine object
    """
    task = vm.PowerOff()
    _wait_for_task(task)

def restart_vm(vm):
   """
   Helper method to restart (vm)
   vm - Virtual Machine object
   """
   task = vm.ResetVM_Task()
   _wait_for_task(task)


def delete_vm(vm):
    """
    Helper method to delete (vm)
    vm - Virtual Machine object
    """
    if vm.runtime.powerState == vim.VirtualMachine.PowerState.poweredOn:
        power_off(vm)
    task = vm.Destroy()
    _wait_for_task(task)


def mark_as_donotkill(vm):
    """
    Deprecated. Use class VMHelper.
    Helper method to modify the vm name by
    appending -donotkill flag at the end
    """
    try:
        newname = vm.summary.config.name + "-donotkill"
        vmname = vm.Rename(newname)
    except AttributeError:
        print("vm name doesn't exist")


def connect_to_vc(host=None, user=None, password=None, port=443):
    if sys.version_info >= (2, 7, 9):
        # If we aren't going to properly cert our infrastructure,
        #  I'm gonna do this sort of thing.
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE
        return SmartConnect(host=host, user=user, pwd=password, port=port,
                            sslContext=context)
    else:
        # Python too old to create context, run the command here and hope
        # pyvmomi handles it properly
        return SmartConnect(host=host, user=user, pwd=password, port=port)


def disconnect_vc(vc_instance=None):
    return Disconnect(vc_instance)


def get_vc_uuid(vc_instance=None):
    return vc_instance.RetrieveContent().about.instanceUuid


def get_vm_uuid(vm):
    return vm.config.uuid


def get_vm_by_uuid(si, uuid):
    for vm in get_all_vm_objs(si):
        try:
            if get_vm_uuid(vm) == uuid:
                return vm
        except AttributeError:
            continue
    print("Cannot find VM with uuid:%s" % uuid)
    return None


def get_vm_macs(vm):
    devices = vm.config.hardware.device
    mac_list = []
    for device in devices:
        if isinstance(device, vim.VirtualEthernetCard):
            mac_list.append(device.macAddress)
            break
    if len(mac_list) == 0:
        raise Exception("Cannot find mac address for vm")
    return mac_list


def get_vm_first_mac(vm):
    """
    Gets the 1st mac in the data structure.
    :param vm:
    :return:
    """
    return get_vm_macs(vm)[0]


def add_disk_to_vm(vc_instance=None, vm=None, size_GB=None,
                   disk_type='thin'):
    """
    Copied most of this from:
    github.com/vmware/pyvmomi-community-samples/blob/master/
    samples/add_disk_to_vm.py

    Note, this will only work when the VM has 1 scsi disk controller.
    """
    unit_number = None
    controller = None
    spec = vim.vm.ConfigSpec()
    for dev in vm.config.hardware.device:
        if hasattr(dev.backing, 'fileName'):
            unit_number = int(dev.unitNumber) + 1
            if unit_number == 7:
                unit_number += 1
            if unit_number >= 16:
                raise Exception("Too many disks on VM")
        if isinstance(dev, vim.vm.device.VirtualSCSIController):
            controller = dev

    if not controller:
        raise Exception("Could not find scsi controller")
    if not unit_number:
        raise Exception("Could not find disk unit number")

    dev_changes = []
    new_disk_kb = int(size_GB) * 1024 * 1024
    disk_spec = vim.vm.device.VirtualDeviceSpec()
    disk_spec.fileOperation = "create"
    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    disk_spec.device = vim.vm.device.VirtualDisk()
    disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
    if disk_type == 'thin':
        disk_spec.device.backing.thinProvisioned = True
    disk_spec.device.backing.diskMode = 'persistent'
    disk_spec.device.unitNumber = unit_number
    disk_spec.device.capacityInKB = new_disk_kb
    disk_spec.device.controllerKey = controller.key
    dev_changes.append(disk_spec)
    spec.deviceChange = dev_changes
    task = vm.ReconfigVM_Task(spec=spec)
    _wait_for_task(task)

if __name__ == '__main__':
    si=VMHelper().connect()
    VMHelper().snapshot_revert_by_name("win8.1_ent_x64_20","Snapshot_06281609")
    # VMHelper().vm_restart("win8.1_ent_x64_20")


