#! python
iSCSI=False
FC=False

if(FC and not iSCSI):
    print "FC si, iSCSI no"
elif(iSCSI and not FC):
    print "iSCSI si, FC no"
elif(iSCSI and FC):
    print "los dos"
else:
    print "Ninguno"
