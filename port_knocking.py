import socket
import time
import os
import sys

# ================= 配置区域 =================
SERVER_IP = "10.25.56.8"
KNOCK_PORTS = [666,777,888]
SSH_USER = "root"
SSH_PORT = 22
# ===========================================

def knock():
    print(f"[*] 正在向 {SERVER_IP} 发起敲门暗号...")
    for port in KNOCK_PORTS:
        print(f"[>] 敲击端口: {port}")
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)  # 关键：快速超时以确保只发 SYN
            s.connect((SERVER_IP, port))
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass  # 正常现象，无需处理
        finally:
            if s:
                s.close()
        time.sleep(0.2)
    print("[+] 暗号发送完毕，等待服务器开门...")
    time.sleep(1)

def login():
    print(f"[*] 正在尝试连接 SSH ({SSH_USER}@{SERVER_IP}:{SSH_PORT})...")
    cmd = f"ssh -o ConnectTimeout=10 -p {SSH_PORT} {SSH_USER}@{SERVER_IP}"
    exit_code = os.system(cmd)
    if exit_code != 0:
        print("[!] SSH 连接失败。请检查：")
        print("    1. 敲门序列是否被服务器接收（查看 /var/log/knockd.log）")
        print("    2. iptables 是否动态放行了你的 IP")
        print("    3. 云安全组是否开放了敲门端口（*/*/*）")

if __name__ == "__main__":
    knock()
    login()
