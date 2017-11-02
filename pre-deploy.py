#! python

#reading variables from a csv file
#import csv
#my_file=open("/Users/javirodz/Documents/ucs-book.csv", "r")
#my_csv_file = csv.reader(my_file)
#for row in my_vsc_file:
#print row



# trailing comma

from ucsmsdk.ucshandle import UcsHandle
# help(UcsHandle)
handle = UcsHandle("192.168.67.148","admin","password",secure=False)
handle.login()

#vars(handle)

#launch GUI
#from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
#ucs_gui_launch(handle)

#get ucs commands from the GUI
#from ucsmsdk.utils.converttopython import convert_to_ucs_python
#convert_to_ucs_python()

#Create a Sub Organization
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.org.OrgOrg import OrgOrg

mo = OrgOrg(parent_mo_or_dn="org-root", name="Sub_Org_Test", descr="Sub Org Desc")
handle.add_mo(mo)
handle.commit()
##### End-Of-PythonScript #####

#Remove Sub Organization
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Name")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#create a vlan
##### Start-Of-PythonScript #####

#create vMotion VLAN (VLAN ID 50)
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name="vMotion", id="50", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
handle.add_mo(mo)
handle.commit()

#Create Management VLAN (VLAN ID 51)
mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name="Mgmt", id="51", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
handle.add_mo(mo)
handle.commit()

#Create Production VLAN (VLAN ID 70)
mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name="Production_70", id="70", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
handle.add_mo(mo)
handle.commit()

#Create iSCSI-A VLAN on FI-A (ID 2550)
mo = FabricVlan(parent_mo_or_dn="fabric/eth-estc/A", sharing="none", name="iSCSI-A", id="2550", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
handle.add_mo(mo)
handle.commit()

#Create iSCSI-B VLAN on FI-B (ID 2551)
mo = FabricVlan(parent_mo_or_dn="fabric/eth-estc/B", sharing="none", name="iSCSI-B", id="2551", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
handle.add_mo(mo)
handle.commit()

#Create UUID Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock

mo = UuidpoolPool(parent_mo_or_dn="org-root/org-Sub_Org_Test", policy_owner="local", prefix="derived", descr="UUID Pool", assignment_order="sequential", name="UUID_POOL")
mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to="0001-000000000100", r_from="0001-000000000001")
handle.add_mo(mo)
handle.commit()
##### End-Of-PythonScript #####

#Remove UUID Pool
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Test/uuid-pool-UUID_POOL")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#Create Server Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot

mo = ComputePool(parent_mo_or_dn="org-root/org-Sub_Org_Test", policy_owner="local", name="Server_Pool", descr="Server Pool")
mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="1")
mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="1")
mo_3 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="3", chassis_id="1")
mo_4 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="4", chassis_id="1")
mo_5 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="5", chassis_id="1")
mo_6 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="7", chassis_id="1")
mo_7 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="8", chassis_id="1")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Delete Server Pool
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Test/compute-pool-Server_Pool")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#Create Maintenance Policy
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

mo = LsmaintMaintPolicy(parent_mo_or_dn="org-root/org-Sub_Org_Test", uptime_disr="user-ack", name="User_Ack", descr="User Ack", trigger_config="on-next-boot", sched_name="", policy_owner="local")
handle.add_mo(mo)
handle.commit()
##### End-Of-PythonScript #####

#Delete Maintenance Policy
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Test/maint-Usr_Ack")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#Create Power Policy
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy

mo = PowerPolicy(parent_mo_or_dn="org-root/org-Sub_Org_Test", fan_speed="any", policy_owner="local", name="No_Cap", prio="no-cap", descr="No Cap")
handle.add_mo(mo)
handle.commit()
##### End-Of-PythonScript #####

#Delete Power Policy
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Test/power-policy-No_Cap")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#Create vMedia Policy
##### Start-Of-PythonScript #####

#from ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy import CimcvmediaMountConfigPolicy
#from ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry import CimcvmediaConfigMountEntry

#mo = CimcvmediaMountConfigPolicy(parent_mo_or_dn="org-root/org-Sub_Org_Test", policy_owner="local", retry_on_mount_fail="yes", name="vMedia", descr="vMedia")
#mo_1 = CimcvmediaConfigMountEntry(parent_mo_or_dn=mo, user_id="user", description="vMedia", remote_ip_address="192.168.67.130", remote_port="0", image_name_variable="none", auth_option="default", mapping_name="vMedia-Name", image_file_name="Remote_file", device_type="cdd", mount_protocol="http", password="password", image_path="/usr/var")
#handle.add_mo(mo)

#handle.commit()
##### End-Of-PythonScript #####

#delete vMedia Policy
##### Start-Of-PythonScript #####

#mo = handle.query_dn("org-root/org-Sub_Org_Test/mnt-cfg-policy-vMedia")
#handle.remove_mo(mo)
#handle.commit()
##### End-Of-PythonScript #####

#add IP Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

mo = IppoolPool(parent_mo_or_dn="org-root/org-Sub_Org_Test", is_net_bios_enabled="disabled", name="ext_mgmt", descr="KVM", policy_owner="local", ext_managed="internal", supports_dhcp="disabled", assignment_order="sequential")
mo_1 = IppoolBlock(parent_mo_or_dn=mo, prim_dns="10.10.10.100", r_from="10.10.10.10", def_gw="10.10.10.1", sec_dns="10.10.10.200", to="10.10.10.17")
handle.add_mo(mo)

handle.commit()
##### End-Of-PythonScript #####

#Create MAC Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

mo = MacpoolPool(parent_mo_or_dn="org-root/org-Sub_Org_Test", policy_owner="local", descr="Mamagement FI-A", assignment_order="sequential", name="MGMT-A")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:A0:00:0F", r_from="00:25:B5:A0:00:00")
handle.add_mo(mo)
handle.commit()

mo = MacpoolPool(parent_mo_or_dn="org-root/org-Sub_Org_Test", policy_owner="local", descr="Mamagement FI-B", assignment_order="sequential", name="MGMT-B")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:B0:00:0F", r_from="00:25:B5:B0:00:00")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create Network Control Policy
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac

mo = NwctrlDefinition(parent_mo_or_dn="org-root/org-Sub_Org_Test", lldp_transmit="disabled", name="CDP_EN", lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="enabled", uplink_fail_action="link-down", descr="CDP Enable")
mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local", name="", descr="")
handle.add_mo(mo)

handle.commit()
##### End-Of-PythonScript #####

#Create vNIC Templates
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf

mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-Sub_Org_Test", templ_type="updating-template", name="MGMT-A", descr="Management FI-A", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="MGMT-A", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="VLAN_200")
mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN_800")
handle.add_mo(mo)
handle.commit()

mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-Sub_Org_Test", templ_type="updating-template", name="MGMT-B", descr="Management FI-B", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="MGMT-B", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="VLAN_200")
mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN_800")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create WWNN Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock

mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-Sub_Org_Test", name="WWNN_Pool", policy_owner="local", descr="WWNN Pool", assignment_order="sequential", purpose="node-wwn-assignment")
mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:00:00:25:B5:A0:00:1F", r_from="20:00:00:25:B5:A0:00:00")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create WWPN Pool
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock

mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-Sub_Org_Test", name="WWPN_Pool-A", policy_owner="local", descr="WWPN Pool FI-A", assignment_order="sequential", purpose="port-wwn-assignment")
mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:01:00:25:B5:A0:00:0F", r_from="20:01:00:25:B5:A0:00:00")
handle.add_mo(mo)
handle.commit()

mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-Sub_Org_Test", name="WWPN_Pool-B", policy_owner="local", descr="WWPN Pool FI-B", assignment_order="sequential", purpose="port-wwn-assignment")
mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:01:00:25:B5:B0:00:0F", r_from="20:01:00:25:B5:B0:00:00")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create Local Disk Conf Policy
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy

mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn="org-root/org-Sub_Org_Test", protect_config="yes", name="Local_Disk_CP", descr="Local Disk Configuration Policy Desc", flex_flash_raid_reporting_state="enable", flex_flash_state="enable", policy_owner="local", mode="any-configuration")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create Boot Policy
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootUsbFlashStorageImage import LsbootUsbFlashStorageImage

mo = LsbootPolicy(parent_mo_or_dn="org-root/org-Sub_Org_Test", name="Boot_Policy", descr="Boot Policy Desc", reboot_on_update="no", policy_owner="local", enforce_vnic_name="yes", boot_mode="legacy")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-write-drive", lun_id="0", mapping_name="", order="2")
mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
mo_2_1_1 = LsbootUsbFlashStorageImage(parent_mo_or_dn=mo_2_1, order="1")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create HBA Template
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.vnic.VnicSanConnTempl import VnicSanConnTempl
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf

mo = VnicSanConnTempl(parent_mo_or_dn="org-root/org-Sub_Org_Test", templ_type="updating-template", name="fc-a", descr="", stats_policy_name="default", switch_id="A", pin_to_group_name="", policy_owner="local", qos_policy_name="", ident_pool_name="WWPN_Pool-A", max_data_field_size="2048")
mo_1 = VnicFcIf(parent_mo_or_dn=mo, name="default")
handle.add_mo(mo)
handle.commit()

mo = VnicSanConnTempl(parent_mo_or_dn="org-root/org-Sub_Org_Test", templ_type="updating-template", name="fc-b", descr="", stats_policy_name="default", switch_id="B", pin_to_group_name="", policy_owner="local", qos_policy_name="", ident_pool_name="WWPN_Pool-B", max_data_field_size="2048")
mo_1 = VnicFcIf(parent_mo_or_dn=mo, name="default")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Create Service Profile Template
##### Start-Of-PythonScript #####

from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicFc import VnicFc
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
from ucsmsdk.mometa.ls.LsRequirement import LsRequirement
from ucsmsdk.mometa.ls.LsPower import LsPower
from ucsmsdk.mometa.fabric.FabricVCon import FabricVCon

#SPT with FC and no iSCSI
mo = LsServer(parent_mo_or_dn="org-root/org-Test_Org", vmedia_policy_name="", ext_ip_state="none", bios_profile_name="", mgmt_fw_policy_name="", agent_policy_name="", mgmt_access_policy_name="", dynamic_con_policy_name="", kvm_mgmt_policy_name="", sol_policy_name="", uuid="0", descr="SPT Description", stats_policy_name="default", policy_owner="local", ext_ip_pool_name="ext-mgmt", boot_policy_name="Boot_Policy", usr_lbl="", host_fw_policy_name="", vcon_profile_name="", ident_pool_name="UUID_POOL", src_templ_name="", type="initial-template", local_disk_policy_name="Local_Disk_CP", scrub_policy_name="", power_policy_name="default", maint_policy_name="User_Ack", name="my_SPT", resolve_remote="yes")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="1", transport="ethernet", vnic_name="MGMT-A")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="2", transport="ethernet", vnic_name="MGMT-B")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="3", transport="ethernet", vnic_name="VM-A")
mo_4 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="4", transport="ethernet", vnic_name="VM-B")
mo_5 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="5", transport="fc", vnic_name="fc-a")
mo_6 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="6", transport="fc", vnic_name="fc-b")
mo_7 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="MGMT-A", order="1", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-A", addr="derived")
mo_8 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="MGMT-B", order="2", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-B", addr="derived")
mo_9 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="VM-A", order="3", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-A", addr="derived")
mo_10 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="VM-B", order="4", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-B", addr="derived")
mo_11 = VnicFc(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", addr="derived", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", pers_bind="disabled", order="5", pers_bind_clear="no", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", max_data_field_size="2048", nw_templ_name="fc-a", name="fc-a")
mo_11_1 = VnicFcIf(parent_mo_or_dn=mo_11, name="")
mo_12 = VnicFc(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", addr="derived", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", pers_bind="disabled", order="6", pers_bind_clear="no", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", max_data_field_size="2048", nw_templ_name="fc-b", name="fc-b")
mo_12_1 = VnicFcIf(parent_mo_or_dn=mo_12, name="")
mo_13 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="WWNN_Pool", addr="pool-derived")
mo_14 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="Server_Pool", qualifier="")
mo_15 = LsPower(parent_mo_or_dn=mo, state="admin-up")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="auto")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="auto")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="auto")
mo_19 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="auto")
handle.add_mo(mo)
handle.commit()

##### End-Of-PythonScript #####

#Configuring Uplink ports
from ucsmsdk.mometa.fabric.FabricEthLanEp import FabricEthLanEp
#FI-A Port-3
mo = FabricEthLanEp(parent_mo_or_dn="fabric/lan/A", eth_link_profile_name="default", name="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", usr_lbl="", slot_id="1", admin_state="enabled", port_id="3")
handle.add_mo(mo)
handle.commit()
#FI-A Port-4
mo = FabricEthLanEp(parent_mo_or_dn="fabric/lan/A", eth_link_profile_name="default", name="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", usr_lbl="", slot_id="1", admin_state="enabled", port_id="4")
handle.add_mo(mo)
handle.commit()
#FI-B Port-3
mo = FabricEthLanEp(parent_mo_or_dn="fabric/lan/B", eth_link_profile_name="default", name="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", usr_lbl="", slot_id="1", admin_state="enabled", port_id="3")
handle.add_mo(mo)
handle.commit()
#FI-B Port-4
mo = FabricEthLanEp(parent_mo_or_dn="fabric/lan/B", eth_link_profile_name="default", name="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", usr_lbl="", slot_id="1", admin_state="enabled", port_id="4")
handle.add_mo(mo)
handle.commit()
#Configure Port Channels
from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
#PC-50 with FI-A P3 and FI-A P4
mo = FabricEthLanPc(parent_mo_or_dn="fabric/lan/A", name="PC-50", descr="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="10gbps", port_id="50", lacp_policy_name="default")
mo_1 = FabricEthLanPcEp(parent_mo_or_dn=mo, eth_link_profile_name="default", name="", auto_negotiate="yes", slot_id="1", admin_state="enabled", port_id="3")
mo_2 = FabricEthLanPcEp(parent_mo_or_dn=mo, eth_link_profile_name="default", name="", auto_negotiate="yes", slot_id="1", admin_state="enabled", port_id="4")
handle.add_mo(mo)
handle.commit()
#PC-51 with FI-B P3 and FI-B P4
mo = FabricEthLanPc(parent_mo_or_dn="fabric/lan/B", name="PC-51", descr="", flow_ctrl_policy="default", admin_speed="10gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="10gbps", port_id="51", lacp_policy_name="default")
mo_1 = FabricEthLanPcEp(parent_mo_or_dn=mo, eth_link_profile_name="default", name="", auto_negotiate="yes", slot_id="1", admin_state="enabled", port_id="3")
mo_2 = FabricEthLanPcEp(parent_mo_or_dn=mo, eth_link_profile_name="default", name="", auto_negotiate="yes", slot_id="1", admin_state="enabled", port_id="4")
handle.add_mo(mo)
handle.commit()

#Unconfigure Ports
#FI-A Port-3
#mo = handle.query_dn("fabric/server/sw-A/slot-1-port-3")
#handle.remove_mo(mo)
#handle.commit()
#FI-A Port-4
#mo = handle.query_dn("fabric/server/sw-A/slot-1-port-4")
#handle.remove_mo(mo)
#handle.commit()
#FI-B Port-3
#mo = handle.query_dn("fabric/server/sw-B/slot-1-port-3")
#handle.remove_mo(mo)
#handle.commit()
#FI-B Port-4
#mo = handle.query_dn("fabric/server/sw-B/slot-1-port-4")
#handle.remove_mo(mo)
#handle.commit()
#PC-50
#mo = handle.query_dn("fabric/lan/A/pc-50")
#handle.remove_mo(mo)
#handle.commit()
#PC-51
#mo = handle.query_dn("fabric/lan/B/pc-51")
#handle.remove_mo(mo)
#handle.commit()

# Logout after script is executed
handle.logout()
