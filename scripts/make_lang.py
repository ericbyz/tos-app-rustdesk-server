#!/usr/bin/env python3
"""Generate rustdesk-server.lang for the TOS App Center (26 locales, English fill)."""
NAME_EN = "RustDesk Server"
AUTHOR = "ericbyz"
DESC_EN = (
    "Self-hosted RustDesk remote-desktop server (hbbs ID/signalling + hbbr relay), "
    "packaged unmodified from upstream rustdesk/rustdesk-server (AGPL-3.0). Remote "
    "desktop sessions stay inside your network. Ships a floating-window instruction "
    "page with the client configuration (ID server, ports 21114-21119, public key)."
)
NOTE_EN = "1. Repackaged upstream rustdesk/rustdesk-server (AGPL-3.0) unmodified for TOS."
NOTE_ZH = "1. 将上游 rustdesk/rustdesk-server(AGPL-3.0)原样封装为 TOS 应用。"

PRIMARY = [
    ("zh-cn", "RustDesk 自建远控中继",
     "在 NAS 上自建 RustDesk 远控服务端:hbbs(ID/信令)+ hbbr(中继),远控流量全部走自己的网络。"
     "上游二进制原样封装(AGPL-3.0),悬浮窗内置客户端配置说明页(ID 服务器地址、端口 21114-21119、公钥查看)。"
     "服务开机自启,密钥保存于 /var/lib/rustdesk-server。"),
    ("zh-hk", "RustDesk 自建遠控中繼",
     "在 NAS 上自建 RustDesk 遠控服務端:hbbs(ID/信令)+ hbbr(中繼),遠控流量全部走自己的網絡。"
     "上游二進制原樣封裝(AGPL-3.0),懸浮窗內置客戶端配置說明頁(ID 服務器地址、端口 21114-21119、公鑰查看)。"
     "服務開機自啟,密鑰保存於 /var/lib/rustdesk-server。"),
]

ORDER = ["zh-cn", "zh-hk", "en-us", "ko-kr", "ja-jp", "de-de", "fr-fr", "it-it",
         "es-es", "hu-hu", "pl-pl", "tr-tr", "ru-ru", "pt-pt", "cs-cz", "da-dk",
         "nl-nl", "nb-no", "sv-se", "el-gr", "ro-ro", "th-th", "vi-vn", "id-id",
         "ar-sa", "he-il"]

NATIVE = {
    "ja-jp": "NAS 上で RustDesk リモートデスクトップサーバーをセルフホスト:hbbs(ID/シグナリング)+ hbbr(リレー)で遠隔操作トラフィックを全て自分のネットワーク内に。上流バイナリを無改修でパッケージ化(AGPL-3.0)。フローティングウィンドウにクライアント設定(ID サーバー、ポート 21114-21119、公開鍵)の説明ページを内蔵。",
    "ko-kr": "NAS에서 RustDesk 원격 데스크톱 서버를 셀프 호스팅: hbbs(ID/시그널링) + hbbr(릴레이)로 원격 세션 트래픽을 모두 자신의 네트워크 안에 유지합니다. 업스트림 바이너리를 무수정 패키징(AGPL-3.0)하며, 플로팅 창에 클라이언트 설정(ID 서버, 포트 21114-21119, 공개 키) 안내 페이지를 제공합니다.",
    "de-de": "Selbst gehosteter RustDesk-Remote-Desktop-Server (hbbs ID/Signalling + hbbr Relay) — Remote-Sitzungen bleiben im eigenen Netzwerk. Upstream-Binaries unverändert paketiert (AGPL-3.0), mit schwebendem Anleitungsfenster für Client-Konfiguration (ID-Server, Ports 21114-21119, öffentlicher Schlüssel).",
    "fr-fr": "Serveur RustDesk auto-hébergé (hbbs signalisation + hbbr relais) : les sessions de contrôle à distance restent dans votre réseau. Binaires upstream intacts (AGPL-3.0), avec fenêtre flottante de configuration cliente (serveur ID, ports 21114-21119, clé publique).",
    "es-es": "Servidor RustDesk autoalojado (hbbs señalización + hbbr relé): las sesiones remotas permanecen en su red. Binarios upstream intactos (AGPL-3.0), con ventana flotante de configuración del cliente (servidor ID, puertos 21114-21119, clave pública).",
    "ru-ru": "Самостоятельно размещаемый сервер RustDesk (hbbs — ID/сигналинг, hbbr — ретранслятор): трафик удалённых сессий остаётся в вашей сети. Оригинальные бинарники без изменений (AGPL-3.0), с плавающим окном инструкции для клиентов (ID-сервер, порты 21114-21119, публичный ключ).",
}

def main(out_path):
    lines = []
    for loc in ORDER:
        name, desc = NAME_EN, NATIVE.get(loc, DESC_EN)
        for l, n, d in PRIMARY:
            if l == loc:
                name, desc = n, d
                break
        note = NOTE_ZH if loc in ("zh-cn", "zh-hk") else NOTE_EN
        lines += [f"[{loc}]", f'name = "{name}"', f'auth = "{AUTHOR}"',
                  f'descript = "{desc}"', f'note = "{note}"', ""]
    open(out_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("wrote", out_path, len(ORDER), "locales")

if __name__ == "__main__":
    main("rustdesk-server.lang")
