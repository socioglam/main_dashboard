import socket
import logging
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
# Known bots and their validated domain suffixes
KNOWN_BOTS = {
    'Googlebot': ['.googlebot.com', '.google.com'],
    'bingbot': ['.search.msn.com'],
    'Slurp': ['.crawl.yahoo.net'],
    'DuckDuckBot': ['.duckduckgo.com'],
    'Baiduspider': ['.baidu.com', '.baidu.jp'],
    'YandexBot': ['.yandex.ru', '.yandex.com', '.yandex.net']
}

# Logger Setup
logging.basicConfig(filename='bot_visits.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def get_client_ip(request):
    """
    Case Handled: Proxy/Load Balancer.
    Ye function real IP nikalta hai agar request Cloudflare ya Proxy se aayi ho.
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def verify_bot(ip, user_agent):
    """
    Case Handled: Spoofing (Fake Bots).
    Double DNS Lookup perform karta hai authenticity check karne ke liye.
    """
    bot_name = "Unknown/User"
    is_claimed_bot = False
    
    # 1. Check User-Agent (Claim)
    for name, domains in KNOWN_BOTS.items():
        if name.lower() in user_agent.lower():
            bot_name = name
            is_claimed_bot = True
            expected_domains = domains
            break
    
    if not is_claimed_bot:
        return {"type": "Human/Unknown", "verified": False, "details": "Normal Browser"}

    # 2. Reverse DNS: IP -> Hostname
    try:
        host_info = socket.gethostbyaddr(ip)
        hostname = host_info[0] # e.g., crawl-66-249-66-1.googlebot.com
    except socket.herror:
        return {"type": bot_name, "verified": False, "details": "Reverse DNS Failed (No Hostname)"}

    # 3. Check Domain Suffix
    domain_match = any(hostname.endswith(d) for d in expected_domains)
    if not domain_match:
        return {"type": bot_name, "verified": False, "details": f"Hostname Mismatch ({hostname})"}

    # 4. Forward DNS: Hostname -> IP (Double Check)
    try:
        ip_info = socket.gethostbyname(hostname)
    except socket.gaierror:
        return {"type": bot_name, "verified": False, "details": "Forward DNS Failed"}

    # 5. Final Match
    if ip_info == ip:
        return {"type": bot_name, "verified": True, "details": f"Verified via {hostname}"}
    else:
        return {"type": bot_name, "verified": False, "details": "IP Spoofing Detected"}

@app.route('/my-link')
def track_visit():
    user_agent = request.headers.get('User-Agent', '')
    ip = get_client_ip(request)
    
    # Algorithm run karein
    bot_status = verify_bot(ip, user_agent)
    
    # Log Entry Create Karein
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "user_agent": user_agent,
        "bot_type": bot_status['type'],
        "is_verified": bot_status['verified'],
        "note": bot_status['details']
    }
    
    # Console aur File me log karein
    logging.info(str(log_entry))
    
    # --- HANDLING CASES IN RESPONSE ---
    
    if bot_status['verified']:
        print(f"✅ REAL BOT: {bot_status['type']} from {ip}")
    elif bot_status['type'] != "Human/Unknown":
        print(f"🚨 FAKE BOT: Claimed {bot_status['type']} but failed verification. IP: {ip}")
    else:
        print(f"👤 Human User visited.")

    return jsonify({
        "message": "Content served successfully", 
        "debug_info": bot_status # Production me ye line hata dein
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)