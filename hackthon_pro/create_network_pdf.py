from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

def create_network_pdf():
    """Create a PDF document with network types information"""
    
    pdf_path = 'uploads/network_types.pdf'
    
    # Create PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 10*inch, "Computer Network Types")
    
    # Introduction
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, 9.5*inch, "There are several types of computer networks based on their size, scope, and purpose:")
    
    # Network types
    y_position = 9*inch
    
    networks = [
        ("1. Personal Area Network (PAN)", [
            "- Smallest type of network",
            "- Connects devices within a person's workspace", 
            "- Examples: Bluetooth, USB connections"
        ]),
        ("2. Local Area Network (LAN)", [
            "- Connects devices within a limited area",
            "- Usually within a building or campus",
            "- Examples: Home networks, office networks"
        ]),
        ("3. Metropolitan Area Network (MAN)", [
            "- Covers a larger area than LAN",
            "- Connects multiple LANs within a city",
            "- Examples: City-wide networks, university campuses"
        ]),
        ("4. Wide Area Network (WAN)", [
            "- Largest type of network",
            "- Spans across countries or continents",
            "- Examples: Internet, corporate networks"
        ]),
        ("5. Wireless Local Area Network (WLAN)", [
            "- LAN that uses wireless communication",
            "- Examples: WiFi networks"
        ]),
        ("6. Virtual Private Network (VPN)", [
            "- Secure network over public infrastructure",
            "- Provides encrypted communication",
            "- Examples: Corporate VPNs, remote access"
        ])
    ]
    
    for network_name, details in networks:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, y_position, network_name)
        y_position -= 0.3*inch
        
        c.setFont("Helvetica", 10)
        for detail in details:
            c.drawString(1.2*inch, y_position, detail)
            y_position -= 0.2*inch
        
        y_position -= 0.2*inch
    
    # Network topologies
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_position, "Network Topologies:")
    y_position -= 0.3*inch
    
    topologies = [
        "- Star Topology: All devices connected to central hub",
        "- Bus Topology: All devices connected to single cable", 
        "- Ring Topology: Devices connected in circular pattern",
        "- Mesh Topology: Each device connected to every other device",
        "- Tree Topology: Hierarchical structure like branches"
    ]
    
    c.setFont("Helvetica", 10)
    for topology in topologies:
        c.drawString(1*inch, y_position, topology)
        y_position -= 0.2*inch
    
    c.save()
    print(f"✅ Created PDF: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_network_pdf() 