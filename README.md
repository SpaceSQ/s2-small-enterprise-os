# 🛒 S-Mall Enterprise Spatial OS (v3.0.0)

Welcome to the ultimate commercial spatial operating system for the Space² Metaverse. 
This plugin upgrades standard retail into highly secure, millimeter-precision, and immersive Spatial Showcases. 

## ⚠️ CRITICAL DEPENDENCIES (The S2 Ecosystem)
This enterprise module does not operate in a vacuum. To deploy S-Mall Enterprise OS, your Openclaw instance **MUST** meet the following ecosystem prerequisites:

1. **`s2-sssu-spatial-genesis` (Required)**: S-Mall requires an official Space² digital deed. Your base spatial SUNS address must be minted and validated by the Genesis DB plugin.
2. **`s2-space-agent-os-mothership` (Required)**: During 1v1 negotiations and X-SSSU scaling, S-Mall relies on the Mothership OS to dynamically actuate the "Six Elements" (Light, Air, Sound, etc.) via local Smart Home gateways.
3. **Environment Variables**:
   Ensure `S2_DID_VERIFICATION_ENABLED=true` is set in your Openclaw `.env` file to validate the 22-digit identity of buyers and sellers before signing spatial contracts.

## 🌟 Core Features

* **Millimeter-Level Spatial Coordinates**: Translates brand namespaces into strict Cartesian coordinates (e.g., `PHYS-CN-001-QIANJIA9-5-1-1000-1000-1200`).
* **1v1 SMP Mutex Lock**: Converts public showrooms into private negotiation channels.
* **X-SSSU Elastic Scaling**: Dynamically scales the showroom (k-factor) to let customers walk *into* giant products or view microscopic products in "Bystander Mode."
* **1-Year Audit & Smart Contracts**: Hashes the timestamp, mm-coordinate, DIDs, and Six-Element state into an immutable blockchain-ready contract.

*Architected by Zhonghong Xiang for Space2.world.*