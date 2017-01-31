#! python
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.org.OrgOrg import OrgOrg
from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

my_Org = "Test_Org"
my_Full_Path_Org = "org-root/org-%s" % my_Org
my_UUID_Pool = "%s/uuid-pool-UUID_POOL" % my_Full_Path_Org
my_Server_Pool = "%s/compute-pool-Server_Pool" % my_Full_Path_Org
my_Maint_Pol = "%s/maint-Usr_Ack" % my_Full_Path_Org
my_Power_Pol = "%s/power-policy-No_Cap" % my_Full_Path_Org
#create the handle
handle = UcsHandle("192.168.67.148","admin","password",secure=False)
#login into UCS manager
handle.login()

#Remove Sub Organization
mo = handle.query_dn(my_Full_Path_Org)
handle.remove_mo(mo)
handle.commit()

#Unconfigure Ports
#PC-50
mo = handle.query_dn("fabric/lan/A/pc-50")
handle.remove_mo(mo)
handle.commit()
#PC-51
mo = handle.query_dn("fabric/lan/B/pc-51")
handle.remove_mo(mo)
handle.commit()
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

mo = handle.query_dn("fabric/eth-estc/B/net-iSCSI-B")
handle.remove_mo(mo)
handle.commit()

mo = handle.query_dn("fabric/eth-estc/A/net-iSCSI-A")
handle.remove_mo(mo)
handle.commit()

#mo = handle.query_dn("fabric/lan/net-Production")
#handle.remove_mo(mo)
#handle.commit()

mo = handle.query_dn("fabric/lan/net-vMotion")
handle.remove_mo(mo)
handle.commit()

mo = handle.query_dn("fabric/lan/net-Management")
handle.remove_mo(mo)
handle.commit()

# Logout after script is executed
handle.logout()
