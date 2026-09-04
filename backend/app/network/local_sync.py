"""
Local Network Multi-Device Sync Engine
Enables peer-to-peer zero-WAN patient encounter syncing between field devices
on the same local Wi-Fi / phone hotspot network.
"""

import socket
import json
import httpx
from typing import List, Dict, Any, Optional

DEFAULT_SYNC_PORT = 8000

class LocalNetworkSyncEngine:
    def __init__(self, node_id: Optional[str] = None):
        self.node_id = node_id or f"node_{socket.gethostname()}"
        self.discovered_peers: List[Dict[str, Any]] = []

    def get_local_ip(self) -> str:
        """Returns the local LAN IP address of this device."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def discover_local_peers(self, ip_range_prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Discovers active triage nodes on the local subnet.
        """
        local_ip = self.get_local_ip()
        peers = [{
            "node_id": self.node_id,
            "ip": local_ip,
            "port": DEFAULT_SYNC_PORT,
            "is_self": True,
            "status": "ONLINE"
        }]
        
        # In a multi-device setup, probe local subnet IP range or broadcast mDNS
        self.discovered_peers = peers
        return peers

    async def sync_encounter_with_peer(self, peer_ip: str, encounter_data: Dict[str, Any]) -> bool:
        """
        Pushes a locally triaged patient record directly to a peer field device.
        """
        url = f"http://{peer_ip}:{DEFAULT_SYNC_PORT}/api/triage/push_sync"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.post(url, json=encounter_data)
                return resp.status_code == 200
        except Exception as e:
            print(f"⚠️ Peer sync to {peer_ip} failed: {e}")
            return False
