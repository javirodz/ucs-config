#! python
#import section test
import csv
#UCS Connection Handle
from ucsmsdk.ucshandle import UcsHandle
#Create Organization
from ucsmsdk.mometa.org.OrgOrg import OrgOrg
#UUID Pool
from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
#VLAN
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
#Sever Pool
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
#Maintenance Policy
from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy
#Power Policy
from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy
#Create IP Pool
from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock
#Create MAC Pool
from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock
#Create Network Control Policy
from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac
#FC WWNN and WWPN Pools
from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock
#Create vNIC Templates
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
#Create Local Disk Conf Policy
from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy
#Create Boot Policy
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootUsbFlashStorageImage import LsbootUsbFlashStorageImage
#Create HBA Template
from ucsmsdk.mometa.vnic.VnicSanConnTempl import VnicSanConnTempl
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
#Configuring Uplink ports
from ucsmsdk.mometa.fabric.FabricEthLanEp import FabricEthLanEp
#Configure Port Channels
from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
#Create Service Profile Template
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicFc import VnicFc
from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf
from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
from ucsmsdk.mometa.ls.LsRequirement import LsRequirement
from ucsmsdk.mometa.ls.LsPower import LsPower
from ucsmsdk.mometa.fabric.FabricVCon import FabricVCon

#Are we having iSCSI to the Hosts?
iSCSI = True
#Are we having FC to the hosts?
FC = False

#Create the handle
handle = UcsHandle("10.242.100.90","admin","password",secure=False)
#login into UCS manager
handle.login()

#reading variables from the ucs workbook
my_file=open("/Users/javirodz/Documents/ucs-book.csv", "r")
my_csv_file = csv.reader(my_file)
for row in my_csv_file:
    if row[0] == "Organization Name":
        my_Org = row[1]
        my_Full_Path_Org = "org-root/org-%s" % my_Org
    elif row[0] == "KVM Starting IP Address":
        my_kvm_pool_first = row[1]
    elif row[0] == "KVM Primary DNS IP Address":
        my_Primary_DNS = row[1]
    elif row[0] == "KVM Secondary DNS IP Address":
        my_Secondary_DNS = row[1]
    elif row[0] == "KVM Gateway":
        my_KVM_Gateway = row[1]
    elif row[0] == "KVM Ending IP Address":
        my_kvm_last_addr = row[1]
    elif row[0] == "Service Profile Template Name":
        my_SPT = row[1]
    elif row[0] == "Service Profile Name Seed":
        my_SP_Name = row[1]
        print my_SP_Name
    elif row[0] == "VLAN Name":
        VLAN_Name = row
        i=1
        while i < len(VLAN_Name):
            print VLAN_Name[i]
            i = i + 1
    elif row[0] == "VLAN ID":
        VLAN_ID = row
        i=1
        while i < len(VLAN_ID):
            print VLAN_ID[i]
            i = i + 1
    else:
        print "Bad Robot"

#Create Sub Organization
mo = OrgOrg(parent_mo_or_dn="org-root", name=my_Org, descr="Sub Organization")
handle.add_mo(mo)
handle.commit()

#Create Production VLANs
k = 1
while k < len(VLAN_ID):
    mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name=VLAN_Name[k], id=VLAN_ID[k], mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
    handle.add_mo(mo)
    handle.commit()
    print k
    k = k+1

#Create UUID Pool
mo = UuidpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", prefix="derived", descr="UUID Pool", assignment_order="sequential", name="UUID_POOL")
mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to="0001-000000000100", r_from="0001-000000000001")
handle.add_mo(mo)
handle.commit()

#Create a Server Pool
mo = ComputePool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", name="Server_Pool", descr="Server Pool")
mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="1")
mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="1")
mo_3 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="3", chassis_id="1")
mo_4 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="4", chassis_id="1")
mo_5 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="5", chassis_id="1")
#mo_6 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="6", chassis_id="1")
#mo_7 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="7", chassis_id="1")
handle.add_mo(mo)
handle.commit()

#Create Maintenance Policy
mo = LsmaintMaintPolicy(parent_mo_or_dn=my_Full_Path_Org, uptime_disr="user-ack", name="User_Ack", descr="User Ack", trigger_config="on-next-boot", sched_name="", policy_owner="local")
handle.add_mo(mo)
handle.commit()

#Create Power Policy
mo = PowerPolicy(parent_mo_or_dn=my_Full_Path_Org, fan_speed="any", policy_owner="local", name="No_Cap", prio="no-cap", descr="No Cap")
handle.add_mo(mo)
handle.commit()

#Create IP Pool
mo = IppoolPool(parent_mo_or_dn=my_Full_Path_Org, is_net_bios_enabled="disabled", name="ext_mgmt", descr="KVM", policy_owner="local", ext_managed="internal", supports_dhcp="disabled", assignment_order="sequential")
mo_1 = IppoolBlock(parent_mo_or_dn=mo, prim_dns=my_Primary_DNS, r_from=my_kvm_pool_first, def_gw=my_KVM_Gateway, sec_dns=my_Secondary_DNS, to=my_kvm_last_addr)
handle.add_mo(mo)
handle.commit()

#Create MAC Pools
mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="Management FI-A", assignment_order="sequential", name="MGMT-A")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:A0:00:0F", r_from="00:25:B5:A0:00:00")
handle.add_mo(mo)
handle.commit()

mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="Management FI-B", assignment_order="sequential", name="MGMT-B")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:B0:00:0F", r_from="00:25:B5:B0:00:00")
handle.add_mo(mo)
handle.commit()

mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="Production FI-A", assignment_order="sequential", name="VM-A")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:A1:00:0F", r_from="00:25:B5:A1:00:00")
handle.add_mo(mo)
handle.commit()

mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="Production FI-B", assignment_order="sequential", name="VM-B")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:B1:00:0F", r_from="00:25:B5:B1:00:00")
handle.add_mo(mo)
handle.commit()

if(iSCSI):
    mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="iSCSI FI-A", assignment_order="sequential", name="iSCSI-A")
    mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:A2:00:0F", r_from="00:25:B5:A2:00:00")
    handle.add_mo(mo)
    handle.commit()
    mo = MacpoolPool(parent_mo_or_dn=my_Full_Path_Org, policy_owner="local", descr="iSCSI FI-B", assignment_order="sequential", name="iSCSI-B")
    mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:B3:00:0F", r_from="00:25:B5:B3:00:00")
    handle.add_mo(mo)
    handle.commit()
#End Create MAC Pools

#Create Network Control Policy
mo = NwctrlDefinition(parent_mo_or_dn=my_Full_Path_Org, lldp_transmit="disabled", name="CDP_EN", lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="enabled", uplink_fail_action="link-down", descr="CDP Enable")
mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local", name="", descr="")
handle.add_mo(mo)
handle.commit()

#FC WWNN and WWPN Pools
if(FC):
        mo = FcpoolInitiators(parent_mo_or_dn=my_Full_Path_Org, name="WWNN_Pool", policy_owner="local", descr="WWNN Pool", assignment_order="sequential", purpose="node-wwn-assignment")
        mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:00:00:25:B5:A0:00:FF", r_from="20:00:00:25:B5:A0:00:00")
        handle.add_mo(mo)
        handle.commit()

        mo = FcpoolInitiators(parent_mo_or_dn=my_Full_Path_Org, name="WWPN_Pool-A", policy_owner="local", descr="WWPN Pool FI-A", assignment_order="sequential", purpose="port-wwn-assignment")
        mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:01:00:25:B5:A0:00:0F", r_from="20:01:00:25:B5:A0:00:00")
        handle.add_mo(mo)
        handle.commit()

        mo = FcpoolInitiators(parent_mo_or_dn=my_Full_Path_Org, name="WWPN_Pool-B", policy_owner="local", descr="WWPN Pool FI-B", assignment_order="sequential", purpose="port-wwn-assignment")
        mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to="20:01:00:25:B5:B0:00:0F", r_from="20:01:00:25:B5:B0:00:00")
        handle.add_mo(mo)
        handle.commit()

#Create vNIC Templates
mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="MGMT-A", descr="Management FI-A", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="MGMT-A", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="Mgmt")
mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="vMotion")
handle.add_mo(mo)
handle.commit()

mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="MGMT-B", descr="Management FI-B", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="MGMT-B", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="Mgmt")
mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="vMotion")
handle.add_mo(mo)
handle.commit()

mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="VM-A", descr="Production FI-A", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="VM-A", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
#Depending on the VLANs that will pass wot the NIC:
#mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name=Production)
#mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN_800")
handle.add_mo(mo)
handle.commit()

mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="VM-B", descr="Production FI-B", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", mtu="1500", policy_owner="local", qos_policy_name="", ident_pool_name="VM-B", cdn_source="vnic-name", nw_ctrl_policy_name="CDP_EN")
#Depending on the VLANs that will pass wot the NIC:
#mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name=Production)
#mo_2 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="VLAN_800")
handle.add_mo(mo)
handle.commit()

if(iSCSI):
    #Create iSCSI-A VLAN on FI-A (ID 1000)
    mo = FabricVlan(parent_mo_or_dn="fabric/eth-estc/A", sharing="none", name="iSCSI-A", id="1000", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
    handle.add_mo(mo)
    handle.commit()
#
    #Create iSCSI-B VLAN on FI-B (ID 2000)
    mo = FabricVlan(parent_mo_or_dn="fabric/eth-estc/B", sharing="none", name="iSCSI-B", id="2000", mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="", compression_type="included")
    handle.add_mo(mo)
    handle.commit()

    mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="iSCSI-A", descr="iSCSI FI-A", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", mtu="9000", policy_owner="local", qos_policy_name="Nimble-QoS", ident_pool_name="iSCSI-A", cdn_source="vnic-name", nw_ctrl_policy_name="Nimble-iSCSI")
    mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="iSCSI-A")
    handle.add_mo(mo)
    handle.commit()

    mo = VnicLanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="iSCSI-B", descr="iSCSI FI-B", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", mtu="9000", policy_owner="local", qos_policy_name="Nimble-QoS", ident_pool_name="iSCSI-B", cdn_source="vnic-name", nw_ctrl_policy_name="Nimble-iSCSI")
    mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="iSCSI-B")
    handle.add_mo(mo)
    handle.commit()

#Create Local Disk Conf Policy (any-configuration)
mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn=my_Full_Path_Org, protect_config="yes", name="Local_Disk_CP", descr="Local Disk Configuration Policy Desc", flex_flash_raid_reporting_state="enable", flex_flash_state="enable", policy_owner="local", mode="any-configuration")
handle.add_mo(mo)
handle.commit()

#Create Boot Policy (boot from SD)
mo = LsbootPolicy(parent_mo_or_dn=my_Full_Path_Org, name="Boot_Policy", descr="Boot Policy Desc", reboot_on_update="no", policy_owner="local", enforce_vnic_name="yes", boot_mode="legacy")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-write-drive", lun_id="0", mapping_name="", order="2")
mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
mo_2_1_1 = LsbootUsbFlashStorageImage(parent_mo_or_dn=mo_2_1, order="1")
handle.add_mo(mo)
handle.commit()

#Create HBA Template
if(FC):
    mo = VnicSanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="fc-a", descr="", stats_policy_name="default", switch_id="A", pin_to_group_name="", policy_owner="local", qos_policy_name="", ident_pool_name="WWPN_Pool-A", max_data_field_size="2048")
    mo_1 = VnicFcIf(parent_mo_or_dn=mo, name="default")
    handle.add_mo(mo)
    handle.commit()

    mo = VnicSanConnTempl(parent_mo_or_dn=my_Full_Path_Org, templ_type="updating-template", name="fc-b", descr="", stats_policy_name="default", switch_id="B", pin_to_group_name="", policy_owner="local", qos_policy_name="", ident_pool_name="WWPN_Pool-B", max_data_field_size="2048")
    mo_1 = VnicFcIf(parent_mo_or_dn=mo, name="default")
    handle.add_mo(mo)
    handle.commit()

#Configuring Uplink ports
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

#Create Service Profile Template
if (FC and not iSCSI):
    mo = LsServer(parent_mo_or_dn=my_Full_Path_Org, vmedia_policy_name="", ext_ip_state="none", bios_profile_name="", mgmt_fw_policy_name="", agent_policy_name="", mgmt_access_policy_name="", dynamic_con_policy_name="", kvm_mgmt_policy_name="", sol_policy_name="", uuid="0", descr="SPT Description", stats_policy_name="default", policy_owner="local", ext_ip_pool_name="ext-mgmt", boot_policy_name="Boot_Policy", usr_lbl="", host_fw_policy_name="", vcon_profile_name="", ident_pool_name="UUID_POOL", src_templ_name="", type="initial-template", local_disk_policy_name="Local_Disk_CP", scrub_policy_name="", power_policy_name="default", maint_policy_name="User_Ack", name=my_SPT, resolve_remote="yes")
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

if(iSCSI and not FC):
    mo = LsServer(parent_mo_or_dn=my_Full_Path_Org, vmedia_policy_name="", ext_ip_state="none", bios_profile_name="", mgmt_fw_policy_name="", agent_policy_name="", mgmt_access_policy_name="", dynamic_con_policy_name="", kvm_mgmt_policy_name="", sol_policy_name="", uuid="0", descr="SPT Desc", stats_policy_name="default", policy_owner="local", ext_ip_pool_name="ext-mgmt", boot_policy_name="Boot_Policy", usr_lbl="", host_fw_policy_name="", vcon_profile_name="", ident_pool_name="UUID_POOL", src_templ_name="", type="updating-template", local_disk_policy_name="Local_Disk_CP", scrub_policy_name="", power_policy_name="default", maint_policy_name="User_Ack", name=my_SPT, resolve_remote="yes")
    mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="1", transport="ethernet", vnic_name="MGMT-A")
    mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="2", transport="ethernet", vnic_name="MGMT-B")
    mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="3", transport="ethernet", vnic_name="VM-A")
    mo_4 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="4", transport="ethernet", vnic_name="VM-B")
    mo_5 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="5", transport="ethernet", vnic_name="iSCSI-A")
    mo_6 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="6", transport="ethernet", vnic_name="iSCSI-B")
    mo_7 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="MGMT-A", order="1", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-A", addr="derived")
    mo_8 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="MGMT-B", order="2", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-B", addr="derived")
    mo_9 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="VM-A", order="3", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-A", addr="derived")
    mo_10 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="VM-B", order="4", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-B", addr="derived")
    mo_11 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="iSCSI-A", order="5", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="iSCSI-A", addr="derived")
    mo_12 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="iSCSI-B", order="6", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="iSCSI-B", addr="derived")
    mo_13 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
    mo_14 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="Server_Pool", qualifier="")
    mo_15 = LsPower(parent_mo_or_dn=mo, state="admin-up")
    mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="auto")
    mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="auto")
    mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="auto")
    mo_19 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="auto")
    handle.add_mo(mo)
    handle.commit()

if(iSCSI and FC):
    mo = LsServer(parent_mo_or_dn=my_Full_Path_Org, vmedia_policy_name="", ext_ip_state="none", bios_profile_name="", mgmt_fw_policy_name="", agent_policy_name="", mgmt_access_policy_name="", dynamic_con_policy_name="", kvm_mgmt_policy_name="", sol_policy_name="", uuid="0", descr="SPT Description", stats_policy_name="default", policy_owner="local", ext_ip_pool_name="ext-mgmt", boot_policy_name="Boot_Policy", usr_lbl="", host_fw_policy_name="", vcon_profile_name="", ident_pool_name="UUID_POOL", src_templ_name="", type="updating-template", local_disk_policy_name="Local_Disk_CP", scrub_policy_name="", power_policy_name="default", maint_policy_name="User_Ack", name=my_SPT, resolve_remote="yes")
    mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="1", transport="ethernet", vnic_name="MGMT-A")
    mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="2", transport="ethernet", vnic_name="MGMT-B")
    mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="3", transport="ethernet", vnic_name="VM-A")
    mo_4 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="4", transport="ethernet", vnic_name="VM-B")
    mo_5 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="5", transport="ethernet", vnic_name="iSCSI-A")
    mo_6 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="6", transport="ethernet", vnic_name="iSCSI-B")
    mo_7 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="7", transport="fc", vnic_name="fc-a")
    mo_8 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="any", admin_host_port="ANY", order="8", transport="fc", vnic_name="fc-b")
    mo_9 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="MGMT-A", order="1", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-A", addr="derived")
    mo_10 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="MGMT-B", order="2", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="MGMT-B", addr="derived")
    mo_11 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="VM-A", order="3", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-A", addr="derived")
    mo_12 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="VM-B", order="4", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="VM-B", addr="derived")
    mo_13 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", name="iSCSI-A", order="5", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="iSCSI-A", addr="derived")
    mo_14 = VnicEther(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", nw_ctrl_policy_name="", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", name="iSCSI-B", order="6", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", mtu="1500", nw_templ_name="iSCSI-B", addr="derived")
    mo_15 = VnicFc(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", addr="derived", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="A", pin_to_group_name="", pers_bind="disabled", order="7", pers_bind_clear="no", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", max_data_field_size="2048", nw_templ_name="fc-a", name="fc-a")
    mo_15_1 = VnicFcIf(parent_mo_or_dn=mo_15, name="")
    mo_16 = VnicFc(parent_mo_or_dn=mo, cdn_prop_in_sync="yes", addr="derived", admin_host_port="ANY", admin_vcon="any", stats_policy_name="default", admin_cdn_name="", switch_id="B", pin_to_group_name="", pers_bind="disabled", order="8", pers_bind_clear="no", qos_policy_name="", adaptor_profile_name="VMWare", ident_pool_name="", cdn_source="vnic-name", max_data_field_size="2048", nw_templ_name="fc-b", name="fc-b")
    mo_16_1 = VnicFcIf(parent_mo_or_dn=mo_16, name="")
    mo_17 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="WWNN_Pool", addr="pool-derived")
    mo_18 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="Server_Pool", qualifier="")
    mo_19 = LsPower(parent_mo_or_dn=mo, state="admin-up")
    mo_20 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="auto")
    mo_21 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="auto")
    mo_22 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="auto")
    mo_23 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="auto")
    handle.add_mo(mo)
    handle.commit()

# Logout after script is executed
handle.logout()
my_file.close()
