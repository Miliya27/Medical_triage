"""
Unit Test for Local Network Multi-Device Sync Engine
"""

from backend.app.network.local_sync import LocalNetworkSyncEngine

def test_local_network_sync():
    engine = LocalNetworkSyncEngine()
    local_ip = engine.get_local_ip()
    print("Local LAN IP:", local_ip)
    assert local_ip is not None
    
    peers = engine.discover_local_peers()
    assert len(peers) > 0
    assert peers[0]["is_self"] is True
    print("Discovered Local Triage Peers:", peers)
    print("✅ Local Sync Engine test passed!")

if __name__ == "__main__":
    test_local_network_sync()
