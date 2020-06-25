#!/bin/bash
echo Enter your domain name
IFS=. read -r -a domainname
echo Enter your username to perform ldapsearch on Domain $domainname
read domainuser
echo Enter your ldap server name or IP
read ldapsrv
echo Enter your group name
read groupname

if [ "${#domainname[@]}" = 4 ]; then
OBJECT_ID=$(ldapsearch -H ldap://$ldapsrv -x -W -D "$domainuser@${domainname[0]}.${domainname[1]}.${domainname[2]}.${domainname[3]}" -b "CN=$groupname,CN=Users,DC=${domainname[0]},DC=${domainname[1]},DC=${domainname[2]},DC=${domainname[3]}" | grep -i "objectSid::" | cut -d ":" -f3 | xargs)
elif [ "${#domainname[@]}" = 3 ]; then
OBJECT_ID=$(ldapsearch -H ldap://$ldapsrv -x -W -D "$domainuser@${domainname[0]}.${domainname[1]}.${domainname[2]}" -b "CN=$groupname,CN=Users,DC=${domainname[0]},DC=${domainname[1]},DC=${domainname[2]}" | grep -i "objectSid::" | cut -d ":" -f3 | xargs)
elif [ "${#domainname[@]}" = 2 ]; then
OBJECT_ID=$(ldapsearch -H ldap://$ldapsrv -x -W -D "$domainuser@${domainname[0]}.${domainname[1]}" -b "CN=$groupname,CN=Users,DC=${domainname[0]},DC=${domainname[1]}" | grep -i "objectSid::" | cut -d ":" -f3 | xargs)
elif [ "${#domainname[@]}" = 1 ]; then
OBJECT_ID=$(ldapsearch -H ldap://$ldapsrv -x -W -D "$domainuser@${domainname[0]}" -b "CN=$groupname,CN=Users,DC=${domainname[0]}" | grep -i "objectSid::" | cut -d ":" -f3 | xargs)
else
echo The number of your domain is out of this script, please update the script
exit 0
fi

#    https://serverfault.com/questions/851864/get-sid-by-its-objectsid-using-ldapsearch/852338#852338

# Decode it, hex-dump it and store it in an array
H="$(echo -n $OBJECT_ID | base64 -d -i | hexdump -v -e '1/1 "%02X"')"

# SID Structure: https://technet.microsoft.com/en-us/library/cc962011.aspx
# LESA = Little Endian Sub Authority
# BESA = Big Endian Sub Authority
# LERID = Little Endian Relative ID
# BERID = Big Endian Relative ID

BESA2=${H:16:8}
BESA3=${H:24:8}
BESA4=${H:32:8}
BESA5=${H:40:8}
BERID=${H:48:10}

LESA1=${H:4:12}
LESA2=${BESA2:6:2}${BESA2:4:2}${BESA2:2:2}${BESA2:0:2}
LESA3=${BESA3:6:2}${BESA3:4:2}${BESA3:2:2}${BESA3:0:2}
LESA4=${BESA4:6:2}${BESA4:4:2}${BESA4:2:2}${BESA4:0:2}
LESA5=${BESA5:6:2}${BESA5:4:2}${BESA5:2:2}${BESA5:0:2}
LERID=${BERID:6:2}${BERID:4:2}${BERID:2:2}${BERID:0:2}

SID="S-1-$((16#$LESA1))-$((16#$LESA2))-$((16#$LESA3))-$((16#$LESA4))-$((16#$LESA5))-$((16#$LERID))"
echo "${SID}"

