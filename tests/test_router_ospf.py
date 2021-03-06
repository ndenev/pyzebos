from pyparsing import stringEnd, ParseException
from pyzebos.parsers.config.router.ospf import routerOSPF
import pytest


routerOspfParser = routerOSPF + stringEnd

router_ospf_prolouge = 'router ospf'
area_statements = [
    'area 10 authentication',
    'area 1.2.3.4 authentication',
    'area 10 authentication message-digest',
    'area 1.2.3.4 authentication message-digest',
    'area 10 default-cost 100',
    'area 1.2.3.4 default-cost 100',
    'area 10 filter-list access access-list-name in',
    'area 1.2.3.4 filter-list access access-list-name in',
    'area 10 filter-list access access-list-name out',
    'area 1.2.3.4 filter-list access access-list-name out',
    'area 10 filter-list prefix prefix-list-name in',
    'area 1.2.3.4 filter-list prefix prefix-list-name in',
    'area 10 filter-list prefix prefix-list-name out',
    'area 1.2.3.4 filter-list prefix prefix-list-name out',
    'area 10 nssa',
    'area 10 nssa default-information-originate',
    # 'area 10 nssa default-information-originate metric 10',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1 translator-role always',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1 translator-role never',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1 translator-role candidate',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1 translator-role always no-redistribution',
    # 'area 10 nssa default-information-originate metric 10 metric-type 1 translator-role always no-redistribution no-summary',
    'area 10 nssa no-redistribution',
    'area 10 nssa no-summary',
    # 'area 10 nssa translator-role always',
    # 'area 10 nssa translator-role never',
    # 'area 10 nssa translator-role candidate',
    'area 10 nssa no-summary no-redistribution',
    'area 10 nssa no-summary no-redistribution default-information-originate',
    'area 10 nssa no-redistribution default-information-originate no-summary',
    'area 10 range 10.0.0.0/24',
    'area 10 range 10.0.0.0/24 advertise',
    'area 10 range 10.0.0.0/24 not-advertise',
    'area 10 shortcut default',
    'area 10 shortcut disable',
    'area 10 shortcut enable',
    'area 10 stub',
    'area 10 stub no-summary',
    'area 10 virtual-link 1.2.3.4',
    'area 10 virtual-link 1.2.3.4 authentication',
    # 'area 10 virtual-link 1.2.3.4 authentication-key auth-key',
    # 'area 10 virtual-link 1.2.3.4 authentication authentication-key auth-key',
    'area 10 virtual-link 1.2.3.4 dead-interval 10',
    'area 10 virtual-link 1.2.3.4 hello-interval 10',
    # 'area 10 virtual-link 1.2.3.4 message-digest-key 1 md5 auth-key1 ',
    # 'area 10 virtual-link 1.2.3.4 message-digest-key 1 md5 auth-key1 auth-key2',
    # 'area 10 virtual-link 1.2.3.4 message-digest-key 1 md5 auth-key1 auth-key2 auth-key-3',
    'area 10 virtual-link 1.2.3.4 retransmit-interval 10',
    'area 10 virtual-link 1.2.3.4 transmit-delay 10',
    'auto-cost reference-bandwidth 100',
    'compatible rfc1583',
    'default-information originate always metric 100 metric-type 1 route-map route-map-name',
    'default-information originate always',
    'default-information originate metric 100 metric-type 1 route-map route-map-name',
    'default-information originate metric 100 metric-type 1',
    'default-information originate metric 100',
    'default-information originate route-map route-map-name',
    'default-information originate',
    # Summary
    'summary-address 10.20.30.0/24 not-advertise',
    'summary-address 10.20.30.0/24 tag 20',
    'summary-address 10.20.30.0/24',
    'passive-interface vlan0',
    'passive-interface vlan0 1.2.3.4',
    'network 10.20.30.0 0.0.0.255 area 10',
    'network 10.20.30.0 0.0.0.255 area 1.2.3.4',
    'network 10.20.30.0/24 area 10',
    'network 10.20.30.0/24 area 1.2.3.4',
    'maximum-area 20',
    'max-concurrent-dd 20',
    'host 1.2.3.4 area 10',
    'host 1.2.3.4 area 10 cost 20',
    'enable db-summary-opt',
    'distance 10',
    'distance ospf external 200',
    'distance ospf inter-area 20 external 200',
    'distance ospf inter-area 20',
    'distance ospf intra-area 20 external 200',
    'distance ospf intra-area 20 inter-area 20 external 200',
    'distance ospf intra-area 20 inter-area 20',
    'distance ospf intra-area 20',
    # Redistribution
    'redistribute bgp metric 100 metric-type 1 route-map route-map-name',
    'redistribute bgp metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute bgp metric 100 metric-type 1 tag 10',
    'redistribute bgp metric 100 metric-type 1',
    'redistribute bgp metric 100 route-map route-map-name',
    'redistribute bgp metric 100 tag 10',
    'redistribute bgp metric 100',
    'redistribute bgp metric-type 1',
    'redistribute bgp route-map route-map-name',
    'redistribute bgp tag 10',
    'redistribute bgp',
    'redistribute connected metric 100 metric-type 1 route-map route-map-name',
    'redistribute connected metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute connected metric 100 metric-type 1 tag 10',
    'redistribute connected metric 100 metric-type 1',
    'redistribute connected metric 100 route-map route-map-name',
    'redistribute connected metric 100 tag 10',
    'redistribute connected metric 100',
    'redistribute connected metric-type 1',
    'redistribute connected route-map route-map-name',
    'redistribute connected tag 10',
    'redistribute connected',
    'redistribute intranet metric 100 metric-type 1 route-map route-map-name',
    'redistribute intranet metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute intranet metric 100 metric-type 1 tag 10',
    'redistribute intranet metric 100 metric-type 1',
    'redistribute intranet metric 100 route-map route-map-name',
    'redistribute intranet metric 100 tag 10',
    'redistribute intranet metric 100',
    'redistribute intranet metric-type 1',
    'redistribute intranet route-map route-map-name',
    'redistribute intranet tag 10',
    'redistribute intranet',
    'redistribute isis metric 100 metric-type 1 route-map route-map-name',
    'redistribute isis metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute isis metric 100 metric-type 1 tag 10',
    'redistribute isis metric 100 metric-type 1',
    'redistribute isis metric 100 route-map route-map-name',
    'redistribute isis metric 100 tag 10',
    'redistribute isis metric 100',
    'redistribute isis metric-type 1',
    'redistribute isis route-map route-map-name',
    'redistribute isis tag 10',
    'redistribute isis',
    'redistribute kernel metric 100 metric-type 1 route-map route-map-name',
    'redistribute kernel metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute kernel metric 100 metric-type 1 tag 10',
    'redistribute kernel metric 100 metric-type 1',
    'redistribute kernel metric 100 route-map route-map-name',
    'redistribute kernel metric 100 tag 10',
    'redistribute kernel metric 100',
    'redistribute kernel metric-type 1',
    'redistribute kernel route-map route-map-name',
    'redistribute kernel tag 10',
    'redistribute kernel',
    'redistribute ospf 200 metric 100 metric-type 1 route-map route-map-name',
    'redistribute ospf 200 metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute ospf 200 metric 100 metric-type 1 tag 10',
    'redistribute ospf 200 metric 100 metric-type 1',
    'redistribute ospf 200 metric 100 route-map route-map-name',
    'redistribute ospf 200 metric 100 tag 10',
    'redistribute ospf 200 metric 100',
    'redistribute ospf 200 metric-type 1',
    'redistribute ospf 200 route-map route-map-name',
    'redistribute ospf 200 tag 10',
    'redistribute ospf 200',
    'redistribute ospf metric 100 metric-type 1 route-map route-map-name',
    'redistribute ospf metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute ospf metric 100 metric-type 1 tag 10',
    'redistribute ospf metric 100 metric-type 1',
    'redistribute ospf metric 100 route-map route-map-name',
    'redistribute ospf metric 100 tag 10',
    'redistribute ospf metric 100',
    'redistribute ospf metric-type 1',
    'redistribute ospf route-map route-map-name',
    'redistribute ospf tag 10',
    'redistribute ospf',
    'redistribute rip metric 100 metric-type 1 route-map route-map-name',
    'redistribute rip metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute rip metric 100 metric-type 1 tag 10',
    'redistribute rip metric 100 metric-type 1',
    'redistribute rip metric 100 route-map route-map-name',
    'redistribute rip metric 100 tag 10',
    'redistribute rip metric 100',
    'redistribute rip metric-type 1',
    'redistribute rip route-map route-map-name',
    'redistribute rip tag 10',
    'redistribute rip',
    'redistribute static metric 100 metric-type 1 route-map route-map-name',
    'redistribute static metric 100 metric-type 1 tag 10 route-map route-map-name',
    'redistribute static metric 100 metric-type 1 tag 10',
    'redistribute static metric 100 metric-type 1',
    'redistribute static metric 100 route-map route-map-name',
    'redistribute static metric 100 tag 10',
    'redistribute static metric 100',
    'redistribute static metric-type 1',
    'redistribute static route-map route-map-name',
    'redistribute static tag 10',
    'redistribute static',
]

def test_route_map_match_parse_ok():
    for area_statement in area_statements:
        router_ospf = '{}\n {}'.format(router_ospf_prolouge, area_statement)
        try:
            tokens = routerOspfParser.parseString(router_ospf)
        except ParseException:
            print "Router ospf:\n{}".format(router_ospf)
            raise
