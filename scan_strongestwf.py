from pywifi import PyWiFi, const, Profile
import time


def initialize_wifi_interface():
    wifi = PyWiFi()
    return wifi.interfaces()[0]  # Lấy interface đầu tiên


def scan_wifi_to_list(iface):
    iface.scan()
    print("Đang quét danh sách các mạng WiFi...")
    time.sleep(5)
    scan_results = iface.scan_results()

    wifi_list = []
    for ap in scan_results:
        wifi_info = {
            "SSID": ap.ssid,
            "Signal": ap.signal,
            "Auth": ap.akm  # Phương thức bảo mật
        }
        wifi_list.append(wifi_info)
    return wifi_list


def display_wifi_list(wifi_list):
    if not wifi_list:
        print("Không tìm thấy mạng WiFi nào.")
        return
    print("\nDanh sách các mạng WiFi khả dụng:")
    for i, wifi in enumerate(wifi_list, start=1):
        print(f"{i}. SSID: {wifi['SSID']}, Tín hiệu: {wifi['Signal']}, Bảo mật: {wifi['Auth']}")


def find_strongest_ap(wifi_list):
    if not wifi_list:
        return None
    return max(wifi_list, key=lambda wifi: wifi["Signal"])


def connect_to_wifi(iface, ssid, password=""):
    iface.disconnect()
    time.sleep(1)
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Chỉ hỗ trợ WPA2-PSK
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    new_profile = iface.add_network_profile(profile)

    iface.connect(new_profile)
    time.sleep(5)

    if iface.status() == const.IFACE_CONNECTED:
        print(f"\nĐã kết nối thành công vào {ssid}")
    else:
        print(f"\nKhông thể kết nối vào {ssid}. Kiểm tra lại mật khẩu hoặc tín hiệu mạng.")


def main():
    iface = initialize_wifi_interface()
    wifi_list = scan_wifi_to_list(iface)
    display_wifi_list(wifi_list)

    strongest_ap = find_strongest_ap(wifi_list)
    if strongest_ap:
        print(f"\nMạng WiFi mạnh nhất: {strongest_ap['SSID']} ({strongest_ap['Signal']})")
        password = input(f"Nhập mật khẩu cho {strongest_ap['SSID']} (nếu có): ")
        connect_to_wifi(iface, strongest_ap['SSID'], password)
    else:
        print("\nKhông tìm thấy mạng WiFi nào để kết nối.")


if __name__ == "__main__":
    main()
