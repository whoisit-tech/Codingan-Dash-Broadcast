import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import io
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="WA Broadcast + Realisasi Bayar", page_icon=":bar_chart:", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #F1F5F9; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 1400px; }

/* File uploader — sidebar friendly */
section[data-testid="stFileUploader"] { background:transparent; border-radius:8px; padding:0; border:none; }
section[data-testid="stFileUploader"] > div { background:transparent; }
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px dashed rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    padding: 10px !important;
    min-height: unset !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(255,255,255,0.35) !important;
    background: rgba(255,255,255,0.07) !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {
    font-size: 11px !important;
    color: rgba(255,255,255,0.45) !important;
}
[data-testid="stFileUploaderDropzone"] button {
    padding: 4px 12px !important;
    font-size: 11px !important;
    height: auto !important;
    min-height: unset !important;
}

.stTabs [data-baseweb="tab-list"] { background:#E2E8F0; border-radius:8px; padding:4px; gap:2px; }
.stTabs [data-baseweb="tab"]      { border-radius:6px; color:#64748B; font-size:13px; font-weight:500; padding:6px 18px; }
.stTabs [aria-selected="true"]    { background:#fff !important; color:#1E40AF !important; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,.08); }
.stTabs [data-baseweb="tab-panel"]{ background:#fff; border:1px solid #E2E8F0; border-radius:0 0 10px 10px; padding:24px; }

.card { background:#fff; border-radius:10px; border:1px solid #E2E8F0; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,.04); margin-bottom:16px; }

.mbox { border-radius:8px; padding:14px 16px; text-align:center; border:1.5px solid; }
.mbox-lbl { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.6px; margin-bottom:6px; }
.mbox-val { font-size:24px; font-weight:700; line-height:1.1; }
.mbox-pct { font-size:11px; margin-top:3px; opacity:.8; }

.t { width:100%; border-collapse:collapse; font-size:12.5px; }
.t th { background:#F8FAFC; color:#64748B; font-size:10.5px; font-weight:600; text-transform:uppercase;
        letter-spacing:.5px; padding:9px 13px; border-bottom:2px solid #E2E8F0; text-align:center; }
.t td { padding:9px 13px; border-bottom:1px solid #F1F5F9; color:#334155; text-align:center; }
.t tr:last-child td { border-bottom:none; }
.t tr:hover td { background:#F8FAFC; }
.t .tot { background:#EFF6FF !important; font-weight:700; color:#1E40AF; }
.left { text-align:left !important; }

.pill { display:inline-block; padding:2px 8px; border-radius:12px; font-size:10.5px; font-weight:600; }
.g { background:#DCFCE7; color:#15803D; }
.r { background:#FEE2E2; color:#B91C1C; }
.o { background:#FEF3C7; color:#B45309; }
.b { background:#DBEAFE; color:#1D4ED8; }
.s { background:#F1F5F9; color:#475569; }
.p { background:#F3E8FF; color:#7C3AED; }

.brow { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.blbl { width:160px; font-size:12px; font-weight:500; color:#334155; text-align:right; flex-shrink:0; }
.btrk { flex:1; background:#F1F5F9; border-radius:5px; height:32px; overflow:hidden; }
.bfil { height:100%; border-radius:5px; display:flex; align-items:center; justify-content:flex-end; padding-right:10px; }
.bnum { font-size:13px; font-weight:700; color:#fff; }
.bpct { width:52px; font-size:11px; color:#94A3B8; text-align:right; flex-shrink:0; }

.sh { font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.8px;
      color:#64748B; border-left:3px solid #3B82F6; padding-left:9px; margin-bottom:12px; }

.info-box { background:#EFF6FF; border:1px solid #BFDBFE; border-left:4px solid #3B82F6;
            border-radius:8px; padding:11px 16px; font-size:12px; color:#1E40AF; margin-bottom:12px; }

.warn-box { background:#FFFBEB; border:1px solid #FDE68A; border-left:4px solid #F59E0B;
            border-radius:8px; padding:11px 16px; font-size:12px; color:#92400E; margin-bottom:12px; }

/* Sidebar uploader: hide the redundant drag-drop text, keep button only */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    padding: 8px 10px !important;
    min-height: unset !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    margin-bottom: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    margin-bottom: 8px !important;
}
/* Uploaded file name chip */
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
    background: rgba(34,197,94,0.12) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 6px !important;
    padding: 4px 8px !important;
    font-size: 11px !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="background:#1E3A5F;border-radius:10px;padding:16px 24px;margin-bottom:18px;
            display:flex;justify-content:space-between;align-items:center">
  <div>
    <span style="font-size:18px;font-weight:700;color:#fff">WA Broadcast + Realisasi Bayar</span>
    <span style="font-size:12px;color:rgba(255,255,255,.65);margin-left:14px">PT. BCA Finance · ASR Mobil</span>
  </div>
  <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600">
    Dashboard Terintegrasi
  </span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# SIDEBAR — UPLOAD + CONFIG
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="background:#1E3A5F;border-radius:8px;padding:10px 14px;margin-bottom:14px">
      <span style="color:#fff;font-size:14px;font-weight:700">Upload File</span>
      <span style="color:rgba(255,255,255,.5);font-size:11px;display:block;margin-top:2px">Semua format Excel (.xlsx)</span>
    </div>
    """, unsafe_allow_html=True)

    f_conv = st.file_uploader(
        "1. Conversation / Response WA",
        type=["xlsx", "xls"],
        help="Kolom: Origin, Message Type, Message, Session, Created At"
    )
    f_sc = st.file_uploader(
        "2. File SC Jan-Mar",
        type=["xlsx", "xls"],
        help="Sheet: Sc Januari, Sc Februari, Sc Maret"
    )
    f_rekap = st.file_uploader(
        "3. Rekap WAI 4W",
        type=["xlsx", "xls"],
        help="Kolom: no_wa, status, send_now, body_param_2"
    )

    files_status = {
        "Conversation": f_conv is not None,
        "SC": f_sc is not None,
        "Rekap WAI": f_rekap is not None,
    }
    status_html = "".join([
        f'<span style="display:inline-flex;align-items:center;gap:4px;margin:2px 4px 2px 0;'
        f'font-size:10.5px;font-weight:600;padding:2px 8px;border-radius:10px;'
        f'background:{"#DCFCE7" if v else "#FEE2E2"};color:{"#15803D" if v else "#B91C1C"}">'
        f'{"+" if v else "-"} {k}</span>'
        for k, v in files_status.items()
    ])
    st.markdown(f'<div style="margin:6px 0 16px">{status_html}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="font-size:12px;font-weight:700;color:#94A3B8;letter-spacing:.5px;margin-bottom:8px">KONFIGURASI KOLOM</p>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px;font-weight:600;color:#CBD5E1;margin:4px 0 2px">Conversation Excel</p>', unsafe_allow_html=True)
    col_phone_conv = st.text_input("No HP", value="Contact", key="conv_hp")
    col_origin     = st.text_input("Origin (IN/OUT)", value="Origin", key="conv_orig")
    col_msg_type   = st.text_input("Message Type", value="Message Type", key="conv_mt")
    col_msg        = st.text_input("Message", value="Message", key="conv_msg")
    col_session    = st.text_input("Session ID", value="Session", key="conv_sess")
    col_created    = st.text_input("Created At", value="Created At", key="conv_date")

    st.markdown('<p style="font-size:11px;font-weight:600;color:#CBD5E1;margin:10px 0 2px">SC Excel</p>', unsafe_allow_html=True)
    col_nokontrak_sc = st.text_input("No Kontrak", value="NOKONTRAK", key="sc_nok")
    col_lastpaid     = st.text_input("Last Paid Date", value="lastpaiddate", key="sc_lp")
    col_ospokok      = st.text_input("OS Pokok", value="ospokok", key="sc_osp")
    col_osar         = st.text_input("OS AR", value="osar", key="sc_osar")
    col_custname     = st.text_input("Nama Nasabah", value="custname", key="sc_nama")
    col_branch       = st.text_input("Cabang", value="branchname", key="sc_cab")

    st.markdown('<p style="font-size:11px;font-weight:600;color:#CBD5E1;margin:10px 0 2px">Rekap WAI</p>', unsafe_allow_html=True)
    col_phone_rekap   = st.text_input("No HP / no_wa", value="no_wa", key="rek_hp")
    col_nokontrak_rek = st.text_input("No Kontrak / body_param_2", value="body_param_2", key="rek_nok")
    col_tglbayar_rek  = st.text_input("Tgl Bayar (tidak dipakai)", value="Tanggal Bayar", key="rek_tgl", disabled=True)

    st.markdown('<p style="font-size:11px;font-weight:600;color:#CBD5E1;margin:10px 0 2px">Kata Kunci Klasifikasi</p>', unsafe_allow_html=True)
    st.caption("Pisah dengan koma")
    kw_janji   = st.text_input("Janji Bayar", value="janji,bayar nanti,akan bayar,besok bayar", key="kw_j")
    kw_sudah   = st.text_input("Sudah Bayar", value="sudah bayar,udah bayar,transfer,tadi bayar", key="kw_s")
    kw_hubungi = st.text_input("Hubungi Kami", value="hubungi,kontak,cs,call center", key="kw_h")
    kw_nopush  = st.text_input("No Push", value="tidak bisa,belum bisa,jangan,stop,unsubscribe", key="kw_n")

has_conv      = f_conv is not None
has_sc        = f_sc is not None
has_rekap     = f_rekap is not None
has_realisasi = has_conv and (has_sc or has_rekap)

if not has_rekap:
    st.markdown("""
    <div style="background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:48px 32px;text-align:center;margin-top:24px">
      <div style="font-size:16px;font-weight:700;color:#1E293B;margin-bottom:6px">Upload File untuk Memulai</div>
      <div style="font-size:13px;color:#64748B;max-width:440px;margin:0 auto">
        Upload file via panel kiri. Minimal <b>Rekap WAI 4W</b> untuk melihat data broadcast.
        Tambahkan file lainnya untuk fitur realisasi bayar.
      </div>
      <div style="margin-top:20px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap">
        <span style="background:#F0FDF4;color:#15803D;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">1. Conversation WA</span>
        <span style="background:#FFFBEB;color:#B45309;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">2. File SC</span>
        <span style="background:#EFF6FF;color:#1D4ED8;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">3. Rekap WAI (wajib)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════
# LOAD & PARSE FUNCTIONS
# ═══════════════════════════════════════════════════════════
@st.cache_data
def build_summary_from_rekap(raw):
    """Bangun tabel summary broadcast dari Rekap WAI.
    Kolom Rekap: no_wa, send_now, date, status, cek, body_param_x, dll.

    Kolom status yang dipakai:
      - 'status' : nilai mentah dari API WA (sent, delivered, read, failed, dll)
      - 'cek'    : kolom tambahan opsional (isi bebas)

    Total     = semua baris per tanggal
    Sent      = status in [sent, delivered, read]
    Delivered = status in [delivered, read]
    Read      = status == read
    Failed    = status in [failed, undelivered, error, message undelivered,
                           something went wrong, user's number is part of an experiment]
    """
    df = pd.read_excel(io.BytesIO(raw))
    df.columns = [str(c).strip() for c in df.columns]

    # --- Bangun kolom tanggal ---
    # Cek apakah ada kolom year/month/day terpisah (format Rekap WAI)
    has_ymd = all(c in [col.lower() for col in df.columns] for c in ["year", "month", "day"])

    if has_ymd:
        # Normalisasi nama kolom ke lowercase mapping
        col_map = {col.lower(): col for col in df.columns}
        yr  = pd.to_numeric(df[col_map["year"]],   errors="coerce")
        mo  = pd.to_numeric(df[col_map["month"]],  errors="coerce")
        dy  = pd.to_numeric(df[col_map["day"]],    errors="coerce")
        hr  = pd.to_numeric(df[col_map.get("hour",   "")], errors="coerce").fillna(0) if "hour"   in col_map else 0
        mi  = pd.to_numeric(df[col_map.get("minute", "")], errors="coerce").fillna(0) if "minute" in col_map else 0
        df["_date"] = pd.to_datetime(dict(year=yr, month=mo, day=dy, hour=hr, minute=mi), errors="coerce")
    else:
        # Cari kolom tanggal tunggal
        date_col = next(
            (c for c in df.columns if c.lower() in ["send_now", "date", "tanggal", "created_at"]),
            None
        )
        if date_col is None:
            date_col = next(
                (c for c in df.columns if "date" in c.lower() or "tgl" in c.lower()),
                df.columns[0]
            )
        parsed = None
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y", "%d-%m-%Y"]:
            try:
                parsed = pd.to_datetime(df[date_col], format=fmt, errors="coerce")
                if parsed.notna().sum() > 0:
                    break
            except Exception:
                pass
        if parsed is None or parsed.notna().sum() == 0:
            parsed = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
        df["_date"] = parsed

    df["_day"] = df["_date"].dt.normalize()
    # Buang baris yang tanggalnya tidak terbaca
    df = df[df["_date"].notna()].copy()

    # --- Kolom status: pakai 'status' utama ---
    status_col = next((c for c in df.columns if c.lower() == "status"), None)

    agg = df.groupby("_day").size().rename("Total").reset_index()
    agg.columns = ["Date", "Total"]

    if status_col:
        stat = df[status_col].astype(str).str.strip().str.lower()

        # Buang baris dengan status N/A sebelum hitung apapun
        valid_mask = ~stat.isin(["n/a", "na", "nan", "none", "-", ""])
        df_valid   = df[valid_mask].copy()
        stat_valid = stat[valid_mask]

        # Hitung Total hanya dari baris valid
        agg = df_valid.groupby("_day").size().rename("Total").reset_index()
        agg.columns = ["Date", "Total"]

        df_valid["_failed"]    = stat_valid.isin(["failed"]).astype(int)
        df_valid["_sent"]      = stat_valid.isin(["sent", "delivered", "read"]).astype(int)
        df_valid["_delivered"] = stat_valid.isin(["delivered", "read"]).astype(int)
        df_valid["_read"]      = stat_valid.isin(["read"]).astype(int)

        agg2 = df_valid.groupby("_day")[["_sent","_delivered","_read","_failed"]].sum().reset_index()
        agg2.columns = ["Date", "Sent", "Delivered", "Read", "Failed"]
        agg = agg.merge(agg2, on="Date", how="left")

        # Debug: simpan nilai unik status (termasuk N/A) untuk ditampilkan di sidebar
        agg.attrs["status_values"] = df[status_col].value_counts(dropna=False).to_dict()
        agg.attrs["na_dropped"]    = int((~valid_mask).sum())
    else:
        # Tidak ada kolom status — semua dianggap sent
        agg["Sent"]      = agg["Total"]
        agg["Delivered"] = 0
        agg["Read"]      = 0
        agg["Failed"]    = 0

    for c in ["Sent", "Delivered", "Read", "Failed"]:
        agg[c] = agg[c].fillna(0).astype(int)

    agg["Undelivered"] = (agg["Sent"] - agg["Delivered"]).clip(0)
    agg["Unread"]      = (agg["Delivered"] - agg["Read"]).clip(0)
    agg["Month"]       = agg["Date"].dt.strftime("%B %Y")
    agg["MonthSort"]   = agg["Date"].dt.year * 100 + agg["Date"].dt.month
    return agg.sort_values("Date").reset_index(drop=True)


@st.cache_data
def load_conv(raw, col_phone, col_origin, col_msg_type, col_msg, col_session, col_created):
    df = pd.read_excel(io.BytesIO(raw))
    df.columns = [c.strip() for c in df.columns]

    def find(kw, exact=False):
        if exact:
            return next((c for c in df.columns if c.strip().lower() == kw.lower()), None)
        return next((c for c in df.columns if kw.lower() in c.strip().lower()), None)

    phone_col   = find(col_phone, exact=True) or find(col_phone) or find("contact") or find("phone") or find("no_hp") or find("nohp")
    origin_col  = find(col_origin, exact=True) or find("origin")
    type_col    = find(col_msg_type, exact=True) or find("message type") or find("type")
    msg_col_det = find(col_msg, exact=True) or next(
        (c for c in df.columns if "message" in c.strip().lower() and "id" not in c.strip().lower()), None)
    sess_col    = find(col_session, exact=True) or find("session")
    date_col    = find(col_created, exact=True) or find("created")

    df["_phone"] = df[phone_col].astype(str).str.strip().str.replace(r'\D', '', regex=True) if phone_col else ""
    df["_orig"]  = df[origin_col].str.strip().str.upper() if origin_col else "?"
    df["_type"]  = df[type_col].str.strip().str.lower() if type_col else "?"
    df["_msg"]   = df[msg_col_det].fillna("").astype(str) if msg_col_det else ""
    df["_sess"]  = df[sess_col].astype(str) if sess_col else ""
    df["_date"]  = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce") if date_col else pd.NaT

    return df, phone_col


@st.cache_data
def load_sc(raw):
    sheets = ["Sc Januari", "Sc Februari", "Sc Maret"]
    frames = []
    xls = pd.ExcelFile(io.BytesIO(raw))
    available = xls.sheet_names
    for s in sheets:
        if s in available:
            d = xls.parse(s)
            d["_sheet"] = s
            frames.append(d)
    if not frames:
        for s in available:
            d = xls.parse(s)
            d["_sheet"] = s
            frames.append(d)
    combined = pd.concat(frames, ignore_index=True)
    combined.columns = [str(c).strip() for c in combined.columns]
    return combined


@st.cache_data
def load_rekap(raw):
    df = pd.read_excel(io.BytesIO(raw))
    df.columns = [str(c).strip() for c in df.columns]
    return df


def find_col(df, candidates):
    for c in candidates:
        for col in df.columns:
            if c.strip().lower() == col.strip().lower():
                return col
    return None


def normalize_phone(s):
    s = str(s).strip()
    s = ''.join(filter(str.isdigit, s))
    if s.startswith("0"):
        s = "62" + s[1:]
    elif s.startswith("8"):
        s = "62" + s
    return s


def classify_response(msg, kw_janji, kw_sudah, kw_hubungi, kw_nopush):
    msg_lower = msg.lower()
    for kw in kw_sudah.split(","):
        if kw.strip() and kw.strip() in msg_lower:
            return "Sudah Bayar"
    for kw in kw_janji.split(","):
        if kw.strip() and kw.strip() in msg_lower:
            return "Janji Bayar"
    for kw in kw_hubungi.split(","):
        if kw.strip() and kw.strip() in msg_lower:
            return "Hubungi Kami"
    for kw in kw_nopush.split(","):
        if kw.strip() and kw.strip() in msg_lower:
            return "No Push"
    return "Lainnya"


# ═══════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════
_rekap_raw = f_rekap.read()
df_rekap   = load_rekap(_rekap_raw)
df         = build_summary_from_rekap(_rekap_raw)   # summary dibangun dari Rekap WAI

# Tampilkan debug info di sidebar
if df.empty or df["Date"].isna().all():
    with st.sidebar:
        st.markdown("---")
        st.error("Tanggal tidak terbaca dari Rekap WAI.")
        st.markdown(f'<p style="font-size:10px;color:#F87171">Kolom yang dicoba: <b>send_now, date</b><br>Kolom tersedia: {", ".join(df_rekap.columns[:10].tolist())}</p>', unsafe_allow_html=True)

if "status_values" in df.attrs:
    with st.sidebar:
        st.markdown("---")
        st.markdown('<p style="font-size:11px;font-weight:600;color:#94A3B8;margin-bottom:4px">NILAI KOLOM STATUS DI REKAP</p>', unsafe_allow_html=True)
        sv = df.attrs["status_values"]
        rows = "".join([
            f'<tr><td style="font-size:10px;color:#CBD5E1;padding:2px 4px">{k}</td>'
            f'<td style="font-size:10px;color:#94A3B8;padding:2px 4px;text-align:right">{v:,}</td></tr>'
            for k, v in sorted(sv.items(), key=lambda x: -x[1])
        ])
        st.markdown(f'<table style="width:100%">{rows}</table>', unsafe_allow_html=True)
        na_dropped = df.attrs.get("na_dropped", 0)
        if na_dropped:
            st.markdown(f'<p style="font-size:10px;color:#F59E0B;margin-top:4px">N/A dibuang: <b>{na_dropped:,}</b> baris tidak dihitung.</p>', unsafe_allow_html=True)
        st.caption("Cek apakah nilai status sudah terbaca dengan benar di funnel atas.")

conv, phone_col_detected = None, None
if has_conv:
    conv, phone_col_detected = load_conv(
        f_conv.read(),
        col_phone_conv, col_origin, col_msg_type, col_msg, col_session, col_created
    )

df_sc = None
if has_sc:
    df_sc = load_sc(f_sc.read())


# ═══════════════════════════════════════════════════════════
# FILTER BULAN
# ═══════════════════════════════════════════════════════════
months_avail = sorted(df["Month"].unique(), key=lambda m: df[df["Month"] == m]["MonthSort"].iloc[0])
sel_month = st.selectbox("Filter Bulan", ["Semua Bulan"] + months_avail)

dff = df if sel_month == "Semua Bulan" else df[df["Month"] == sel_month]

T  = int(dff["Total"].sum())
S  = int(dff["Sent"].sum())
D  = int(dff["Delivered"].sum())
R  = int(dff["Read"].sum())
F  = int(dff["Failed"].sum())
UD = int(dff["Undelivered"].sum())
UR = int(dff["Unread"].sum())

def pct(a, b): return f"{a/b:.1%}" if b else "0%"


# ═══════════════════════════════════════════════════════════
# PERIOD HEADER
# ═══════════════════════════════════════════════════════════
try:
    period = f"{dff['Date'].min().strftime('%d %b %Y')} - {dff['Date'].max().strftime('%d %b %Y')}"
except Exception:
    period = "Periode tidak terdeteksi"
    st.warning("Kolom tanggal di Rekap WAI tidak terbaca. Cek nama kolom di sidebar (send_now / date).")
st.markdown(f"""
<div style="background:#1E3A5F;border-radius:10px;padding:16px 24px;margin-bottom:18px;
            display:flex;justify-content:space-between;align-items:center">
  <div>
    <span style="font-size:18px;font-weight:700;color:#fff">WA Broadcast</span>
    <span style="font-size:12px;color:rgba(255,255,255,.65);margin-left:14px">PT. BCA Finance · ASR Mobil · {period}</span>
  </div>
  <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600">
    {sel_month}
  </span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# FUNNEL METRICS
# ═══════════════════════════════════════════════════════════
def mbox(lbl, val, pct_str, fg, bg, border):
    return f"""<div class="mbox" style="background:{bg};border-color:{border};color:{fg}">
      <div class="mbox-lbl">{lbl}</div>
      <div class="mbox-val">{val:,}</div>
      <div class="mbox-pct">{pct_str}</div>
    </div>"""

st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:10px">
  {mbox("Data Upload", T, "100%", "#1E293B", "#F8FAFC", "#CBD5E1")}
</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    st.markdown(mbox("Failed Broadcast", F, f"{pct(F,T)} dari upload", "#B91C1C", "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
with cb:
    st.markdown(mbox("Success Broadcast", S, f"{pct(S,T)} dari upload", "#15803D", "#F0FDF4", "#86EFAC"), unsafe_allow_html=True)

ca2, cb2 = st.columns(2)
with ca2:
    st.markdown(mbox("Delivered", D, f"{pct(D,T)} dari upload", "#1D4ED8", "#EFF6FF", "#93C5FD"), unsafe_allow_html=True)
with cb2:
    st.markdown(mbox("Sent (Belum Delivered)", UD, f"{pct(UD,T)} dari upload", "#D97706", "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

ca3, cb3 = st.columns(2)
with ca3:
    st.markdown(mbox("Read", R, f"{pct(R,D)} dari delivered", "#0E7490", "#ECFEFF", "#67E8F9"), unsafe_allow_html=True)
with cb3:
    st.markdown(mbox("Unread", UR, f"{pct(UR,D)} dari delivered", "#7C3AED", "#FAF5FF", "#C4B5FD"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════
tab_labels = ["Rekap Upload"]
if conv is not None:
    tab_labels.append("Response WA")
    tab_labels.append("Isi Pesan")
    tab_labels.append("Funnel Response")
if has_realisasi:
    tab_labels.append("Realisasi Bayar")

tab_objs = st.tabs(tab_labels)
tab_idx  = {label: i for i, label in enumerate(tab_labels)}


# ═══════════════════════════════════════════════════════════
# TAB 1 — REKAP UPLOAD
# ═══════════════════════════════════════════════════════════
with tab_objs[tab_idx["Rekap Upload"]]:
    st.markdown('<p class="sh">Detail per Batch Upload</p>', unsafe_allow_html=True)

    rows_html = ""
    for _, r in dff.iterrows():
        fp = r["Failed"] / r["Total"] if r["Total"] else 0
        dp = r["Delivered"] / r["Total"] if r["Total"] else 0
        rp = r["Read"] / r["Delivered"] if r["Delivered"] else 0

        def p(v, hi, lo, inv=False):
            if inv:
                cls = "g" if v < hi else "r" if v > lo else "o"
            else:
                cls = "g" if v > hi else "r" if v < lo else "o"
            return f'<span class="pill {cls}">{v:.0%}</span>'

        rows_html += f"""<tr>
          <td class="left">{r['Date'].strftime('%d %b %Y')}</td>
          <td>{int(r['Total']):,}</td>
          <td style="color:#DC2626">{int(r['Failed']):,}</td>
          <td>{p(fp,.15,.30,inv=True)}</td>
          <td style="color:#15803D">{int(r['Sent']):,}</td>
          <td style="color:#1D4ED8">{int(r['Delivered']):,}</td>
          <td>{p(dp,.70,.50)}</td>
          <td style="color:#0E7490">{int(r['Read']):,}</td>
          <td>{p(rp,.65,.45)}</td>
          <td style="color:#7C3AED">{int(r['Unread']):,}</td>
        </tr>"""

    fp_t = F / T if T else 0
    dp_t = D / T if T else 0
    rp_t = R / D if D else 0

    def p_t(v, hi, lo, inv=False):
        if inv:
            cls = "g" if v < hi else "r" if v > lo else "o"
        else:
            cls = "g" if v > hi else "r" if v < lo else "o"
        return f'<span class="pill {cls}">{v:.1%}</span>'

    rows_html += f"""<tr class="tot">
      <td class="left">TOTAL ({len(dff)} batch)</td>
      <td>{T:,}</td><td>{F:,}</td><td>{p_t(fp_t,.15,.30,inv=True)}</td>
      <td>{S:,}</td><td>{D:,}</td><td>{p_t(dp_t,.70,.50)}</td>
      <td>{R:,}</td><td>{p_t(rp_t,.65,.45)}</td><td>{UR:,}</td>
    </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;max-height:420px;overflow-y:auto">
    <table class="t"><thead><tr>
      <th class="left">Tanggal</th><th>Total</th>
      <th>Failed</th><th>Fail%</th><th>Sent</th>
      <th>Delivered</th><th>Del%</th><th>Read</th><th>Read%</th><th>Unread</th>
    </tr></thead><tbody>{rows_html}</tbody></table></div>
    <p style="font-size:10px;color:#94A3B8;margin-top:6px">
    Fail% dan Del% dihitung dari Total Upload. Read% dihitung dari Delivered.</p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Tren per Batch</p>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dff["Date"], y=dff["Total"], name="Total", marker_color="#E2E8F0", opacity=0.8))
    for m, c, d in [("Delivered", "#2563EB", None), ("Read", "#0891B2", "dot"), ("Failed", "#DC2626", None)]:
        fig.add_trace(go.Scatter(x=dff["Date"], y=dff[m], name=m,
            line=dict(color=c, width=2, dash=d or "solid"), mode="lines+markers",
            marker=dict(size=5, color=c)))
    fig.update_layout(
        barmode="overlay", height=280, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
        font=dict(family="Inter", color="#64748B"),
        legend=dict(orientation="h", y=-0.25, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#E2E8F0", tickformat="%d %b"),
        yaxis=dict(gridcolor="#E2E8F0"), hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    if sel_month == "Semua Bulan":
        st.markdown('<p class="sh">Rekap per Bulan</p>', unsafe_allow_html=True)
        monthly = df.groupby(["Month", "MonthSort"]).agg(
            Total=("Total", "sum"), Sent=("Sent", "sum"), Delivered=("Delivered", "sum"),
            Read=("Read", "sum"), Failed=("Failed", "sum"), Unread=("Unread", "sum"), Uploads=("Date", "count")
        ).reset_index().sort_values("MonthSort")

        m_rows = ""
        for _, r in monthly.iterrows():
            fp = r["Failed"] / r["Total"] if r["Total"] else 0
            dp = r["Delivered"] / r["Total"] if r["Total"] else 0
            rp = r["Read"] / r["Delivered"] if r["Delivered"] else 0
            m_rows += f"""<tr>
              <td class="left" style="font-weight:600">{r['Month']}</td>
              <td>{int(r['Uploads'])}</td><td>{int(r['Total']):,}</td>
              <td style="color:#DC2626">{int(r['Failed']):,}</td>
              <td>{p_t(fp,.15,.30,inv=True)}</td>
              <td style="color:#15803D">{int(r['Sent']):,}</td>
              <td style="color:#1D4ED8">{int(r['Delivered']):,}</td>
              <td>{p_t(dp,.70,.50)}</td>
              <td style="color:#0E7490">{int(r['Read']):,}</td>
              <td>{p_t(rp,.65,.45)}</td>
              <td style="color:#7C3AED">{int(r['Unread']):,}</td>
            </tr>"""
        st.markdown(f"""
        <table class="t"><thead><tr>
          <th class="left">Bulan</th><th>Batch</th><th>Total</th>
          <th>Failed</th><th>Fail%</th><th>Sent</th>
          <th>Delivered</th><th>Del%</th><th>Read</th><th>Read%</th><th>Unread</th>
        </tr></thead><tbody>{m_rows}</tbody></table>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — RESPONSE WA
# ═══════════════════════════════════════════════════════════
if conv is not None and "Response WA" in tab_idx:
    with tab_objs[tab_idx["Response WA"]]:
        cdf = conv.copy()
        if sel_month != "Semua Bulan" and cdf["_date"].notna().any():
            cdf = cdf[cdf["_date"].dt.strftime("%B %Y") == sel_month]

        in_df  = cdf[cdf["_orig"] == "IN"]
        btn_df = in_df[in_df["_type"].isin(["button", "button_reply"])]
        total_sessions = cdf["_sess"].nunique()

        s1, s2, s3, s4 = st.columns(4)
        for col_obj, lbl, val, fg, bg, bd in [
            (s1, "Total Sesi",     total_sessions,                       "#1D4ED8", "#EFF6FF", "#93C5FD"),
            (s2, "Pesan Masuk",    len(in_df),                           "#15803D", "#F0FDF4", "#86EFAC"),
            (s3, "Button Replies", len(btn_df),                          "#D97706", "#FFFBEB", "#FDE68A"),
            (s4, "Teks Bebas",     len(in_df[in_df["_type"] == "text"]), "#7C3AED", "#FAF5FF", "#C4B5FD"),
        ]:
            with col_obj:
                st.markdown(f"""<div class="mbox" style="background:{bg};border-color:{bd};color:{fg}">
                  <div class="mbox-lbl">{lbl}</div>
                  <div class="mbox-val">{val:,}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        mt_lbl = {
            "text": "Teks bebas", "button": "Klik tombol", "button_reply": "Balasan tombol",
            "list_reply": "Pilihan menu", "image": "Foto", "document": "Dokumen",
            "audio": "Pesan suara", "reaction": "Reaksi", "sticker": "Sticker",
            "unsupported": "Tidak didukung",
        }
        available_types = sorted(in_df["_type"].dropna().unique().tolist())
        type_options    = ["Semua Type"] + available_types
        type_labels     = ["Semua Type"] + [f"{t} -- {mt_lbl.get(t, t)}" for t in available_types]

        st.markdown('<p class="sh">Filter Message Type</p>', unsafe_allow_html=True)
        sel_type_label = st.selectbox(
            "Pilih tipe pesan:",
            options=type_labels,
            index=0,
            label_visibility="collapsed"
        )
        sel_type = type_options[type_labels.index(sel_type_label)]
        filtered_in_df = in_df if sel_type == "Semua Type" else in_df[in_df["_type"] == sel_type]

        st.markdown("<br>", unsafe_allow_html=True)
        cl, cr = st.columns([3, 2])

        with cl:
            filter_label = "" if sel_type == "Semua Type" else \
                f" &nbsp;<span style='font-size:10px;background:#DBEAFE;color:#1D4ED8;padding:2px 8px;border-radius:10px'>{sel_type}</span>"
            st.markdown(f'<p class="sh">Button Responses dari Nasabah{filter_label}</p>', unsafe_allow_html=True)
            btn_counts = filtered_in_df["_msg"].value_counts().reset_index()
            btn_counts.columns = ["Pesan", "Jumlah"]
            total_btn = int(btn_counts["Jumlah"].sum())

            if total_btn == 0:
                st.info("Tidak ada pesan di tipe dan periode ini.")
            else:
                colors = ["#15803D", "#1D4ED8", "#DC2626", "#7C3AED", "#D97706", "#DB2777", "#0891B2"]
                bars = ""
                for i, row in btn_counts.iterrows():
                    p_val = row["Jumlah"] / total_btn
                    c = colors[i % len(colors)]
                    label_text = str(row['Pesan'])
                    bars += f"""<div class="brow">
                      <div class="blbl" title="{label_text}">{label_text[:26]}{"..." if len(label_text) > 26 else ""}</div>
                      <div class="btrk">
                        <div class="bfil" style="width:{p_val*100:.1f}%;background:{c}">
                          <span class="bnum">{int(row['Jumlah']):,}</span>
                        </div>
                      </div>
                      <div class="bpct">{p_val:.1%}</div>
                    </div>"""
                st.markdown(f"""<div class="card">
                  <p style="font-size:11px;color:#94A3B8;margin:0 0 12px">
                    Total <b>{total_btn:,}</b> pesan dari <b>{total_sessions:,}</b> sesi</p>
                  {bars}</div>""", unsafe_allow_html=True)

        with cr:
            st.markdown('<p class="sh">Breakdown Message Type</p>', unsafe_allow_html=True)
            mt = in_df["_type"].value_counts().reset_index()
            mt.columns = ["Type", "Jumlah"]
            total_mt = int(mt["Jumlah"].sum())
            mt_rows = ""
            for _, row in mt.iterrows():
                is_sel  = (sel_type != "Semua Type" and row["Type"] == sel_type)
                row_sty = "background:#EFF6FF;font-weight:700;" if is_sel else ""
                pill_cls = "b" if is_sel else "s"
                mt_rows += f"""<tr style="{row_sty}">
                  <td class="left">{row['Type']}</td>
                  <td style="font-weight:600">{int(row['Jumlah']):,}</td>
                  <td><span class="pill {pill_cls}">{row['Jumlah']/total_mt:.1%}</span></td>
                  <td class="left" style="color:#94A3B8;font-size:11px">{mt_lbl.get(row['Type'], '')}</td>
                </tr>"""
            st.markdown(f"""<table class="t"><thead><tr>
              <th class="left">Type</th><th>Jumlah</th><th>%</th><th class="left">Keterangan</th>
            </tr></thead><tbody>{mt_rows}</tbody></table>
            <p style="font-size:10px;color:#94A3B8;margin-top:8px">
            Klik filter di atas untuk menyaring isi pesan berdasarkan tipe.</p>""",
            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — ISI PESAN
# ═══════════════════════════════════════════════════════════
if conv is not None and "Isi Pesan" in tab_idx:
    with tab_objs[tab_idx["Isi Pesan"]]:
        cdf2 = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf2["_date"].notna().any():
            cdf2 = cdf2[cdf2["_date"].dt.strftime("%B %Y") == sel_month]

        total_in = len(cdf2)
        st.markdown('<p class="sh">Breakdown Isi Pesan dari Nasabah</p>', unsafe_allow_html=True)

        msg_counts = (cdf2[cdf2["_msg"].str.strip() != ""]["_msg"]
                      .str.strip().value_counts().reset_index())
        msg_counts.columns = ["Pesan", "Jumlah"]
        total_msg = int(msg_counts["Jumlah"].sum())

        colors_bar = ["#15803D", "#1D4ED8", "#DC2626", "#7C3AED", "#D97706",
                      "#DB2777", "#0891B2", "#0F766E", "#9333EA", "#B45309"]
        bars_html = ""
        for i, row in msg_counts.iterrows():
            pv  = row["Jumlah"] / total_msg if total_msg else 0
            clr = colors_bar[i % len(colors_bar)]
            label_text = str(row['Pesan'])
            bars_html += f"""<div class="brow">
              <div class="blbl" title="{label_text}">{label_text[:28]}{"..." if len(label_text) > 28 else ""}</div>
              <div class="btrk">
                <div class="bfil" style="width:{pv*100:.1f}%;background:{clr}">
                  <span class="bnum">{int(row['Jumlah']):,}</span>
                </div>
              </div>
              <div class="bpct">{pv:.1%}</div>
            </div>"""

        st.markdown(f"""<div class="card">
          <p style="font-size:11px;color:#94A3B8;margin:0 0 14px">
            Total <b>{total_msg:,}</b> pesan dari <b>{total_in:,}</b> pesan masuk</p>
          {bars_html}
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Tabel Detail Isi Pesan</p>', unsafe_allow_html=True)

        fc1, fc2 = st.columns([3, 1])
        with fc1:
            kw = st.text_input("Cari isi pesan", placeholder="contoh: bayar, angsuran, denda...")
        with fc2:
            n_rows = st.number_input("Maks baris", 20, 500, 100, 10)

        tbl_df = msg_counts.copy()
        if kw:
            tbl_df = tbl_df[tbl_df["Pesan"].str.contains(kw, case=False, na=False)]
        tbl_df = tbl_df.head(n_rows)

        st.markdown(f'<p style="font-size:11px;color:#94A3B8;margin:0 0 8px">Menampilkan <b>{len(tbl_df)}</b> baris</p>', unsafe_allow_html=True)

        tbl_rows = ""
        for i, row in tbl_df.iterrows():
            pv  = row["Jumlah"] / total_msg if total_msg else 0
            bar = (f'<div style="background:#E2E8F0;border-radius:4px;height:10px;overflow:hidden">'
                   f'<div style="width:{pv*100:.1f}%;height:100%;background:#2563EB;border-radius:4px"></div></div>')
            tbl_rows += f"""<tr>
              <td style="font-weight:600;color:#475569">{i+1}</td>
              <td class="left">{str(row['Pesan'])}</td>
              <td style="font-weight:700;color:#1D4ED8">{int(row['Jumlah']):,}</td>
              <td><span class="pill b">{pv:.1%}</span></td>
              <td style="min-width:120px">{bar}</td>
            </tr>"""

        st.markdown(f"""<div style="max-height:480px;overflow-y:auto">
        <table class="t"><thead><tr>
          <th>#</th><th class="left">Isi Pesan</th><th>Jumlah</th><th>%</th><th>Proporsi</th>
        </tr></thead><tbody>{tbl_rows}</tbody></table></div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 4 — REALISASI BAYAR
# ═══════════════════════════════════════════════════════════
if has_realisasi and "Realisasi Bayar" in tab_idx:
    with tab_objs[tab_idx["Realisasi Bayar"]]:

        st.markdown("""
        <div class="info-box">
        <b>Alur join data:</b>
        <b>Conversation.Contact</b> (no HP) &rarr; <b>Rekap.no_wa</b> &rarr; ambil <b>body_param_2</b> (no kontrak) &rarr; <b>SC.NOKONTRAK</b> &rarr; cek <b>lastpaiddate</b>.
        Status bayar <b>hanya dari SC.lastpaiddate</b>. Rekap dipakai sebagai jembatan no HP ke no kontrak saja.
        </div>
        """, unsafe_allow_html=True)

        cdf_real = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf_real["_date"].notna().any():
            cdf_real = cdf_real[cdf_real["_date"].dt.strftime("%B %Y") == sel_month]

        cdf_real["_phone_norm"] = cdf_real["_phone"].apply(normalize_phone)

        sess_grp  = cdf_real.sort_values("_date").groupby("_sess").first().reset_index()
        sess_msgs = cdf_real.groupby("_sess")["_msg"].apply(lambda x: " ".join(x.dropna())).reset_index()
        sess_msgs.columns = ["_sess", "_all_msgs"]
        sess_grp = sess_grp.merge(sess_msgs, on="_sess", how="left")
        sess_grp["_kategori"] = sess_grp["_all_msgs"].apply(
            lambda m: classify_response(m, kw_janji, kw_sudah, kw_hubungi, kw_nopush)
        )

        # ── Step 1: Bangun lookup Rekap: no_wa (norm) -> {nokontrak, tgl_bayar} ──
        # Conversation.Contact (no HP nasabah) == Rekap.no_wa
        # Rekap.body_param_2 == nokontrak nasabah
        # Rekap.Tanggal Bayar == tgl bayar aktual

        rek_lookup = {}   # {phone_norm: {nokontrak, tgl_bayar_rek, bayar_rek}}
        if df_rekap is not None:
            rek_phone_col = find_col(df_rekap, ["no_wa", "NoWA", "nowa", col_phone_rekap])
            rek_paid_col  = None  # Tidak dipakai — status bayar hanya dari SC.lastpaiddate
            rek_nok_col   = find_col(df_rekap, ["body_param_2", "body_param_1", col_nokontrak_rek, "NOKONTRAK"])

            if rek_phone_col:
                for _, row in df_rekap.iterrows():
                    norm = normalize_phone(str(row.get(rek_phone_col, "")))
                    if not norm or norm == "62":
                        continue
                    nok = str(row.get(rek_nok_col, "")).strip() if rek_nok_col else ""
                    # Rekap hanya dipakai untuk mapping no HP -> no kontrak
                    # Status bayar HANYA dari SC.lastpaiddate, bukan dari Rekap
                    if norm not in rek_lookup:
                        rek_lookup[norm] = {
                            "nokontrak": nok,
                        }
            else:
                st.markdown(
                    f'<div class="warn-box">Kolom No HP tidak ditemukan di Rekap (dicari: <b>no_wa</b>). '
                    f'Kolom tersedia: {", ".join(df_rekap.columns[:20].tolist())}</div>',
                    unsafe_allow_html=True
                )

        # ── Step 2: Bangun lookup SC: nokontrak -> {lastpaiddate, nama} ──
        # SC adalah SATU-SATUNYA sumber kebenaran status bayar
        sc_lookup = {}   # {nokontrak: {bayar_sc, tgl_bayar_sc, nama}}
        if df_sc is not None:
            sc_nok_col   = find_col(df_sc, ["NOKONTRAK", "nokontrak", col_nokontrak_sc])
            sc_paid_col  = find_col(df_sc, ["lastpaiddate", "LastPaidDate", col_lastpaid])
            sc_nama_col  = find_col(df_sc, ["custname", "CustName", col_custname])

            if sc_nok_col:
                for _, row in df_sc.iterrows():
                    nok = str(row.get(sc_nok_col, "")).strip()
                    if not nok or nok in ["", "nan", "None"]:
                        continue
                    lp    = row.get(sc_paid_col) if sc_paid_col else None
                    bayar = pd.notna(lp) and str(lp).strip() not in ["", "nan", "NaT", "None", "0"]
                    sc_lookup[nok] = {
                        "bayar_sc":    bayar,
                        "tgl_bayar_sc": str(lp) if bayar else None,
                        "nama":        str(row.get(sc_nama_col, "")) if sc_nama_col else "",
                    }
            else:
                st.markdown(
                    f'<div class="warn-box">Kolom NOKONTRAK tidak ditemukan di SC. '
                    f'Kolom tersedia: {", ".join(df_sc.columns[:20].tolist())}</div>',
                    unsafe_allow_html=True
                )

        # ── Step 3: Merge ke session — chain: Contact → Rekap → SC ──
        def get_paid_info(phone_norm):
            # Step 1: cari no kontrak via Rekap (mapping no HP -> no kontrak)
            rek = rek_lookup.get(phone_norm)
            if rek is None:
                return {
                    "bayar": None, "tgl_bayar": None,
                    "nokontrak": "", "nama": "", "source": "Tidak Ditemukan di Rekap"
                }

            nokontrak = rek["nokontrak"]

            # Step 2: cek status bayar HANYA dari SC.lastpaiddate
            sc = sc_lookup.get(nokontrak) if nokontrak else None

            if sc is not None:
                return {
                    "bayar":     sc["bayar_sc"],
                    "tgl_bayar": sc["tgl_bayar_sc"],
                    "nokontrak": nokontrak,
                    "nama":      sc["nama"],
                    "source":    "SC",
                }
            else:
                # Ketemu di Rekap tapi no kontrak tidak ada di SC
                # Status bayar UNKNOWN karena tidak bisa cek lastpaiddate
                return {
                    "bayar":     None,
                    "tgl_bayar": None,
                    "nokontrak": nokontrak,
                    "nama":      "",
                    "source":    "Rekap ada, SC tidak match",
                }

        sess_grp["_paid_info"]  = sess_grp["_phone_norm"].apply(get_paid_info)
        sess_grp["_bayar"]      = sess_grp["_paid_info"].apply(lambda x: x["bayar"])
        sess_grp["_tgl_bayar"]  = sess_grp["_paid_info"].apply(lambda x: x["tgl_bayar"])
        sess_grp["_nokontrak"]  = sess_grp["_paid_info"].apply(lambda x: x["nokontrak"])
        sess_grp["_nama"]       = sess_grp["_paid_info"].apply(lambda x: x["nama"])
        sess_grp["_datasource"] = sess_grp["_paid_info"].apply(lambda x: x["source"])

        total_resp  = len(sess_grp)
        found_in_db = sess_grp["_bayar"].notna().sum()
        not_found   = sess_grp["_bayar"].isna().sum()

        st.markdown('<p class="sh">Ringkasan Realisasi per Kategori Response</p>', unsafe_allow_html=True)

        KATEGORI_ORDER  = ["Janji Bayar", "Sudah Bayar", "Hubungi Kami", "No Push", "Lainnya"]
        KATEGORI_COLORS = {
            "Janji Bayar":  ("#15803D", "#DCFCE7", "#86EFAC"),
            "Sudah Bayar":  ("#1D4ED8", "#EFF6FF", "#93C5FD"),
            "Hubungi Kami": ("#D97706", "#FFFBEB", "#FDE68A"),
            "No Push":      ("#B91C1C", "#FEF2F2", "#FECACA"),
            "Lainnya":      ("#475569", "#F1F5F9", "#CBD5E1"),
        }

        realisasi_rows = ""
        summary_data   = []

        for kat in KATEGORI_ORDER:
            grp = sess_grp[sess_grp["_kategori"] == kat]
            total_kat   = len(grp)
            if total_kat == 0:
                continue
            found_kat   = grp["_bayar"].notna().sum()
            bayar_kat   = grp["_bayar"].eq(True).sum()
            belum_kat   = grp["_bayar"].eq(False).sum()
            unknown_kat = grp["_bayar"].isna().sum()
            real_pct    = bayar_kat / found_kat if found_kat else 0
            fg, bg, bd  = KATEGORI_COLORS.get(kat, ("#475569", "#F1F5F9", "#CBD5E1"))

            summary_data.append({
                "Kategori": kat, "Total Respons": total_kat,
                "Ada di DB": found_kat, "Sudah Bayar": bayar_kat,
                "Belum Bayar": belum_kat, "Tidak Ditemukan": unknown_kat,
                "Realisasi %": real_pct
            })

            pct_bar    = (f'<div style="background:#E2E8F0;border-radius:4px;height:8px;overflow:hidden">'
                          f'<div style="width:{real_pct*100:.1f}%;height:100%;background:{fg};border-radius:4px"></div></div>')
            pill_bayar = f'<span class="pill g">{bayar_kat:,} bayar</span>'
            pill_belum = f'<span class="pill r">{belum_kat:,} belum</span>'
            pill_unk   = f'<span class="pill s">{unknown_kat:,} N/A</span>'

            realisasi_rows += f"""<tr>
              <td class="left"><span style="font-weight:700;color:{fg}">{kat}</span></td>
              <td style="font-weight:700">{total_kat:,}</td>
              <td>{found_kat:,}</td>
              <td>{pill_bayar}</td>
              <td>{pill_belum}</td>
              <td>{pill_unk}</td>
              <td style="min-width:130px">
                <div style="display:flex;align-items:center;gap:6px">
                  <span style="font-weight:700;color:{fg};font-size:13px">{real_pct:.1%}</span>
                  {pct_bar}
                </div>
              </td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto">
        <table class="t"><thead><tr>
          <th class="left">Kategori Response</th>
          <th>Total Respons</th>
          <th>Ada di DB</th>
          <th>Sudah Bayar</th>
          <th>Belum Bayar</th>
          <th>Tdk Ditemukan</th>
          <th style="min-width:160px">Realisasi %</th>
        </tr></thead><tbody>{realisasi_rows}</tbody></table>
        </div>
        <p style="font-size:10px;color:#94A3B8;margin-top:6px">
        Realisasi % = Sudah Bayar / (Sudah Bayar + Belum Bayar). Tidak termasuk yang tidak ditemukan di DB.</p>
        """, unsafe_allow_html=True)

        if summary_data:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="sh">Highlight Realisasi</p>', unsafe_allow_html=True)

            janji_row = next((x for x in summary_data if x["Kategori"] == "Janji Bayar"), None)
            sudah_row = next((x for x in summary_data if x["Kategori"] == "Sudah Bayar"), None)

            hc1, hc2, hc3, hc4 = st.columns(4)
            with hc1:
                val = janji_row["Sudah Bayar"] if janji_row else 0
                tot = janji_row["Ada di DB"] if janji_row else 0
                r   = janji_row["Realisasi %"] if janji_row else 0
                st.markdown(f"""<div class="mbox" style="background:#F0FDF4;border-color:#86EFAC;color:#15803D">
                  <div class="mbox-lbl">Janji Bayar - Beneran Bayar</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari {tot:,} yg janji</div>
                </div>""", unsafe_allow_html=True)
            with hc2:
                val = janji_row["Belum Bayar"] if janji_row else 0
                r   = 1 - janji_row["Realisasi %"] if janji_row else 0
                st.markdown(f"""<div class="mbox" style="background:#FEF2F2;border-color:#FECACA;color:#B91C1C">
                  <div class="mbox-lbl">Janji Bayar - Ingkar Janji</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari yg janji</div>
                </div>""", unsafe_allow_html=True)
            with hc3:
                val = sudah_row["Sudah Bayar"] if sudah_row else 0
                tot = sudah_row["Ada di DB"] if sudah_row else 0
                r   = sudah_row["Realisasi %"] if sudah_row else 0
                st.markdown(f"""<div class="mbox" style="background:#EFF6FF;border-color:#93C5FD;color:#1D4ED8">
                  <div class="mbox-lbl">Klaim Sudah Bayar - Terverifikasi</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari {tot:,} yg klaim</div>
                </div>""", unsafe_allow_html=True)
            with hc4:
                total_bayar_all = sum(x["Sudah Bayar"] for x in summary_data)
                total_ada_db    = sum(x["Ada di DB"] for x in summary_data)
                r_all = total_bayar_all / total_ada_db if total_ada_db else 0
                st.markdown(f"""<div class="mbox" style="background:#F3E8FF;border-color:#C4B5FD;color:#7C3AED">
                  <div class="mbox-lbl">Overall Realisasi Bayar</div>
                  <div class="mbox-val">{total_bayar_all:,}</div>
                  <div class="mbox-pct">{r_all:.1%} dari {total_ada_db:,} teridentifikasi</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Grafik Realisasi per Kategori</p>', unsafe_allow_html=True)

        if summary_data:
            fig2 = go.Figure()
            cats       = [x["Kategori"] for x in summary_data]
            bayar_vals = [x["Sudah Bayar"] for x in summary_data]
            belum_vals = [x["Belum Bayar"] for x in summary_data]
            unk_vals   = [x["Tidak Ditemukan"] for x in summary_data]

            fig2.add_trace(go.Bar(name="Sudah Bayar", x=cats, y=bayar_vals,
                marker_color="#22C55E", text=bayar_vals, textposition="auto"))
            fig2.add_trace(go.Bar(name="Belum Bayar", x=cats, y=belum_vals,
                marker_color="#EF4444", text=belum_vals, textposition="auto"))
            fig2.add_trace(go.Bar(name="Tidak Ditemukan", x=cats, y=unk_vals,
                marker_color="#94A3B8", text=unk_vals, textposition="auto"))

            fig2.update_layout(
                barmode="group", height=300, margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
                font=dict(family="Inter", color="#64748B"),
                legend=dict(orientation="h", y=-0.3, bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="#E2E8F0"),
                yaxis=dict(gridcolor="#E2E8F0"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Detail per Nasabah</p>', unsafe_allow_html=True)

        kat_filter = st.selectbox("Filter Kategori", ["Semua"] + KATEGORI_ORDER, key="kat_filter_real")
        bayar_filter = st.radio(
            "Filter Status Bayar",
            ["Semua", "Sudah Bayar", "Belum Bayar", "Tidak Ditemukan"],
            horizontal=True, key="bayar_filter_real"
        )

        detail_df = sess_grp[[
            "_phone_norm", "_kategori", "_msg", "_bayar",
            "_tgl_bayar", "_nokontrak", "_nama", "_datasource", "_date"
        ]].copy()
        detail_df.columns = [
            "No HP", "Kategori Response", "Pesan", "Bayar",
            "Tgl Bayar", "No Kontrak", "Nama", "Sumber Data", "Tgl Chat"
        ]

        if kat_filter != "Semua":
            detail_df = detail_df[detail_df["Kategori Response"] == kat_filter]
        if bayar_filter == "Sudah Bayar":
            detail_df = detail_df[detail_df["Bayar"] == True]
        elif bayar_filter == "Belum Bayar":
            detail_df = detail_df[detail_df["Bayar"] == False]
        elif bayar_filter == "Tidak Ditemukan":
            detail_df = detail_df[detail_df["Bayar"].isna()]

        detail_df["Status"] = detail_df["Bayar"].apply(
            lambda x: "Sudah Bayar" if x is True else ("Belum Bayar" if x is False else "Tidak Ditemukan")
        )
        detail_df = detail_df.drop(columns=["Bayar"])

        st.markdown(
            f'<p style="font-size:11px;color:#94A3B8;margin-bottom:8px">Menampilkan <b>{len(detail_df):,}</b> baris</p>',
            unsafe_allow_html=True
        )
        st.dataframe(detail_df, use_container_width=True, height=400)

        def export_excel_df(df_out):
            buf = BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                df_out.to_excel(w, index=False, sheet_name="Realisasi")
            return buf.getvalue()

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "Download Hasil Filter (.xlsx)",
                export_excel_df(detail_df),
                "realisasi_filter.xlsx",
                "application/vnd.ms-excel"
            )
        with dl2:
            full_export = sess_grp[[
                "_phone_norm", "_kategori", "_msg", "_bayar",
                "_tgl_bayar", "_nokontrak", "_nama", "_datasource", "_date"
            ]].copy()
            full_export.columns = [
                "No HP", "Kategori", "Pesan", "Bayar",
                "Tgl Bayar", "No Kontrak", "Nama", "Sumber", "Tgl Chat"
            ]
            full_export["Status"] = full_export["Bayar"].apply(
                lambda x: "Sudah Bayar" if x is True else ("Belum Bayar" if x is False else "Tidak Ditemukan")
            )
            st.download_button(
                "Download Semua Data Realisasi (.xlsx)",
                export_excel_df(full_export),
                "realisasi_semua.xlsx",
                "application/vnd.ms-excel"
            )

        cov_pct = found_in_db / total_resp if total_resp else 0
        n_rekap_match  = sess_grp["_datasource"].str.contains("SC|Rekap", na=False).sum()
        n_rekap_only   = sess_grp["_datasource"].str.contains("Rekap WAI", na=False).sum()
        n_sc_match     = sess_grp["_datasource"].str.contains("^SC$", na=False).sum()
        n_not_found    = sess_grp["_datasource"].str.contains("Tidak Ditemukan", na=False).sum()

        st.markdown(f"""
        <div class="warn-box" style="margin-top:16px">
        <b>Coverage:</b> {found_in_db:,} dari {total_resp:,} sesi ({cov_pct:.1%}) berhasil di-match.
        <br>Match ke SC: <b>{n_sc_match:,}</b> &nbsp;|&nbsp;
        Fallback Rekap saja: <b>{n_rekap_only:,}</b> &nbsp;|&nbsp;
        Tidak ditemukan di Rekap: <b>{n_not_found:,}</b>
        <br>Kalau banyak yang tidak ditemukan, pastikan format No HP di Conversation sama dengan di kolom <b>no_wa</b> Rekap WAI.
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB — FUNNEL RESPONSE
# ═══════════════════════════════════════════════════════════
if conv is not None and "Funnel Response" in tab_idx:
    with tab_objs[tab_idx["Funnel Response"]]:
        import re as _re

        fr_df = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and fr_df["_date"].notna().any():
            fr_df = fr_df[fr_df["_date"].dt.strftime("%B %Y") == sel_month]

        # Gabung semua pesan per sesi
        sess_all = fr_df.groupby("_sess").agg(
            _phone=("_phone", "first"),
            _all_msgs=("_msg", lambda x: " ".join(x.dropna().astype(str))),
            _date=("_date", "first"),
        ).reset_index()
        sess_all["_phone_norm"] = sess_all["_phone"].apply(normalize_phone)

        total_sesi = len(sess_all)

        # ── Level 1: klasifikasi utama ──────────────────────
        def lvl1(msg):
            m = msg.lower()
            if _re.search(r"sudah\s*bayar|udah\s*bayar|transfer|tadi\s*bayar|sudah\s*lunas|lunas", m):
                return "Sudah Bayar"
            if _re.search(r"janji|akan\s*bayar|mau\s*bayar|siap\s*bayar|besok\s*bayar|bayar\s*nanti", m):
                return "Janji Bayar"
            if _re.search(r"hubungi|kontak\s*kami|cs|call\s*center|ke\s*kantor|datang\s*ke", m):
                return "Hubungi Kami"
            if _re.search(r"tidak\s*bisa|gabisa|belum\s*bisa|blm\s*bisa|gak\s*bisa|tidak\s*mampu|broken", m):
                return "Broken Promise"
            if _re.search(r"salah\s*nomor|bukan\s*saya|bukan\s*nasabah|wrong\s*number|tidak\s*kenal", m):
                return "Wrong Number"
            return "No Push"

        # ── Level 2: breakdown per kategori ─────────────────
        def lvl2_sudah(msg, bayar_sc):
            if bayar_sc is True:
                return "Beneran Bayar"
            if bayar_sc is False:
                return "Tidak Bayar"
            return "Unknown (tidak ada di SC)"

        def lvl2_janji(msg, bayar_sc):
            if bayar_sc is True:
                return "Real Promise"
            if bayar_sc is False:
                return "Broken Promise"
            return "Unknown"

        def lvl2_hubungi(msg):
            m = msg.lower()
            if _re.search(r"autodebet|auto\s*debet", m):          return "Minta Autodebet"
            if _re.search(r"sudah\s*bayar|udah\s*bayar|transfer", m): return "Bayar"
            if _re.search(r"cara\s*bayar|bayar\s*gimana|bagaimana\s*bayar", m): return "Minta Cara Bayar"
            if _re.search(r"nego|denda|keringanan|diskon|cicil", m): return "Nego Denda"
            if _re.search(r"ke\s*kantor|datang|kantor", m):        return "Ke Kantor"
            return "Unknown"

        def lvl2_broken(msg):
            m = msg.lower()
            if _re.search(r"tidak\s*bisa\s*bayar|gabisa\s*bayar|belum\s*ada\s*uang|belum\s*ada\s*dana", m): return "Tidak Bisa Bayar"
            if _re.search(r"cicil|nyicil|dicicil|rubah\s*jt|reschedule|restruktur", m): return "Minta Cicil/Rubah JT"
            if _re.search(r"ke\s*kantor|datang|langsung", m):      return "Ke Kantor"
            if _re.search(r"nego|denda|keringanan", m):             return "Nego Denda"
            return "Lainnya"

        # ── Build paid lookup (sama seperti tab realisasi) ───
        _rek_lkp = {}
        if df_rekap is not None:
            _rpc = find_col(df_rekap, ["no_wa", col_phone_rekap])
            _rnk = find_col(df_rekap, ["body_param_2", col_nokontrak_rek])
            if _rpc:
                for _, row in df_rekap.iterrows():
                    norm = normalize_phone(str(row.get(_rpc, "")))
                    if norm and norm != "62":
                        _rek_lkp[norm] = str(row.get(_rnk, "")).strip() if _rnk else ""

        _sc_lkp = {}
        if df_sc is not None:
            _snk = find_col(df_sc, ["NOKONTRAK", col_nokontrak_sc])
            _slp = find_col(df_sc, ["lastpaiddate", col_lastpaid])
            _snm = find_col(df_sc, ["custname", col_custname])
            if _snk:
                for _, row in df_sc.iterrows():
                    nok = str(row.get(_snk, "")).strip()
                    if nok:
                        lp = row.get(_slp) if _slp else None
                        bayar = pd.notna(lp) and str(lp).strip() not in ["", "nan", "NaT", "None", "0"]
                        _sc_lkp[nok] = {"bayar": bayar, "nama": str(row.get(_snm, "")) if _snm else ""}

        def get_bayar_sc(phone_norm):
            nok = _rek_lkp.get(phone_norm)
            if not nok:
                return None
            sc = _sc_lkp.get(nok)
            if sc is None:
                return None
            return sc["bayar"]

        # ── Klasifikasi semua sesi ───────────────────────────
        sess_all["_l1"]      = sess_all["_all_msgs"].apply(lvl1)
        sess_all["_bayar_sc"]= sess_all["_phone_norm"].apply(get_bayar_sc)

        def get_l2(row):
            l1, msg, bayar = row["_l1"], row["_all_msgs"], row["_bayar_sc"]
            if l1 == "Sudah Bayar":   return lvl2_sudah(msg, bayar)
            if l1 == "Janji Bayar":   return lvl2_janji(msg, bayar)
            if l1 == "Hubungi Kami":  return lvl2_hubungi(msg)
            if l1 == "Broken Promise":return lvl2_broken(msg)
            if l1 == "Wrong Number":  return "Wrong Number"
            return "No Push"

        sess_all["_l2"] = sess_all.apply(get_l2, axis=1)

        # ── WARNA ────────────────────────────────────────────
        L1_COLOR = {
            "Sudah Bayar":    "#15803D",
            "Janji Bayar":    "#1D4ED8",
            "No Push":        "#475569",
            "Hubungi Kami":   "#D97706",
            "Broken Promise": "#B91C1C",
            "Wrong Number":   "#0891B2",
        }
        L2_COLOR = {
            "Beneran Bayar":        "#15803D",
            "Real Promise":         "#15803D",
            "Bayar":                "#15803D",
            "Tidak Bayar":          "#B91C1C",
            "Broken Promise":       "#B91C1C",
            "Tidak Bisa Bayar":     "#B91C1C",
            "Unknown":              "#475569",
            "Unknown (tidak ada di SC)": "#475569",
            "Minta Autodebet":      "#7C3AED",
            "Minta Cara Bayar":     "#0891B2",
            "Nego Denda":           "#D97706",
            "Ke Kantor":            "#0F766E",
            "Minta Cicil/Rubah JT": "#DB2777",
            "Lainnya":              "#94A3B8",
            "Wrong Number":         "#0891B2",
            "No Push":              "#64748B",
        }

        # ── RENDER FUNNEL ────────────────────────────────────
        l1_counts = sess_all["_l1"].value_counts()
        L1_ORDER  = ["Sudah Bayar","Janji Bayar","No Push","Hubungi Kami","Broken Promise","Wrong Number"]

        st.markdown(f"""
        <div style="background:#1E3A5F;border-radius:8px;padding:10px 20px;margin-bottom:16px;
                    display:flex;justify-content:space-between;align-items:center">
          <span style="color:#fff;font-weight:700;font-size:15px">Funnel Response Nasabah</span>
          <span style="color:rgba(255,255,255,.6);font-size:12px">Total sesi: <b style="color:#fff">{total_sesi:,}</b></span>
        </div>
        """, unsafe_allow_html=True)

        # Filter L1
        sel_l1 = st.selectbox(
            "Pilih kategori untuk drill-down:",
            ["Semua"] + L1_ORDER,
            key="funnel_l1_sel"
        )

        # ── TAMPILAN BARIS FUNNEL ────────────────────────────
        def node_html(label, count, total, color, is_selected=False):
            pct_v = count / total * 100 if total else 0
            border = "3px solid #fff" if is_selected else f"2px solid {color}"
            shadow = "box-shadow:0 0 0 3px rgba(255,255,255,.3);" if is_selected else ""
            return f"""
            <div style="background:{color};border-radius:10px;padding:10px 14px;
                        {border};{shadow}display:inline-block;min-width:160px;text-align:center">
              <div style="color:#fff;font-size:12px;font-weight:600;margin-bottom:2px">{label}</div>
              <div style="color:#fff;font-size:20px;font-weight:800">{count:,}</div>
              <div style="color:rgba(255,255,255,.75);font-size:11px">({pct_v:.1f}%)</div>
            </div>"""

        # Row L1 — semua kategori
        st.markdown('<p class="sh" style="margin-top:8px">Level 1 — Kategori Utama</p>', unsafe_allow_html=True)

        cols_l1 = st.columns(len(L1_ORDER))
        for i, kat in enumerate(L1_ORDER):
            cnt = int(l1_counts.get(kat, 0))
            is_sel = (sel_l1 == kat)
            with cols_l1[i]:
                st.markdown(node_html(kat, cnt, total_sesi, L1_COLOR.get(kat,"#475569"), is_sel), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── DRILL DOWN L2 ─────────────────────────────────────
        if sel_l1 != "Semua":
            subset = sess_all[sess_all["_l1"] == sel_l1]
            n_l1   = len(subset)
            l2_counts = subset["_l2"].value_counts()

            st.markdown(f'<p class="sh">Level 2 — Breakdown <span style="color:{L1_COLOR.get(sel_l1,"#475569")}">{sel_l1}</span> ({n_l1:,} sesi)</p>', unsafe_allow_html=True)

            # Nodes L2
            cols_l2 = st.columns(min(len(l2_counts), 4))
            for i, (kat2, cnt2) in enumerate(l2_counts.items()):
                col_idx = i % len(cols_l2)
                with cols_l2[col_idx]:
                    clr2 = L2_COLOR.get(kat2, "#64748B")
                    st.markdown(node_html(kat2, cnt2, n_l1, clr2), unsafe_allow_html=True)

            # Bar chart L2
            st.markdown("<br>", unsafe_allow_html=True)
            fig_l2 = go.Figure(go.Bar(
                x=l2_counts.values.tolist(),
                y=l2_counts.index.tolist(),
                orientation="h",
                marker_color=[L2_COLOR.get(k, "#64748B") for k in l2_counts.index],
                text=[f"{v:,}  ({v/n_l1:.1%})" for v in l2_counts.values],
                textposition="outside",
                textfont=dict(size=12, color="#334155"),
            ))
            fig_l2.update_layout(
                height=max(200, len(l2_counts) * 52),
                margin=dict(l=0, r=120, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
                font=dict(family="Inter", color="#64748B"),
                xaxis=dict(gridcolor="#E2E8F0", showticklabels=False),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_l2, use_container_width=True)

            # Tabel detail sesi
            st.markdown('<p class="sh">Detail Sesi</p>', unsafe_allow_html=True)
            sel_l2 = st.selectbox(
                "Filter breakdown:",
                ["Semua"] + l2_counts.index.tolist(),
                key="funnel_l2_sel"
            )
            show_df = subset if sel_l2 == "Semua" else subset[subset["_l2"] == sel_l2]
            show_df = show_df[["_phone_norm","_l1","_l2","_all_msgs","_bayar_sc","_date"]].copy()
            show_df.columns = ["No HP","Kategori L1","Kategori L2","Pesan","Bayar (SC)","Tgl Chat"]
            show_df["Bayar (SC)"] = show_df["Bayar (SC)"].apply(
                lambda x: "Bayar" if x is True else ("Belum" if x is False else "Unknown")
            )
            st.markdown(f'<p style="font-size:11px;color:#94A3B8;margin-bottom:6px">Menampilkan <b>{len(show_df):,}</b> sesi</p>', unsafe_allow_html=True)
            st.dataframe(show_df, use_container_width=True, height=350)

            # Download
            def to_xlsx(d):
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    d.to_excel(w, index=False)
                return buf.getvalue()

            st.download_button(
                f"Download {sel_l1}{' - '+sel_l2 if sel_l2 != 'Semua' else ''} (.xlsx)",
                to_xlsx(show_df),
                f"funnel_{sel_l1.lower().replace(' ','_')}.xlsx",
                "application/vnd.ms-excel"
            )

        else:
            # Semua — tampilkan overview semua L2
            st.markdown('<p class="sh">Overview semua breakdown</p>', unsafe_allow_html=True)
            l2_all = sess_all.groupby(["_l1","_l2"]).size().reset_index(name="Jumlah")
            l2_all = l2_all.sort_values(["_l1","Jumlah"], ascending=[True, False])

            rows_html = ""
            for _, row in l2_all.iterrows():
                pv   = row["Jumlah"] / total_sesi if total_sesi else 0
                c1   = L1_COLOR.get(row["_l1"], "#475569")
                c2   = L2_COLOR.get(row["_l2"], "#64748B")
                bar  = (f'<div style="background:#E2E8F0;border-radius:4px;height:8px;overflow:hidden">'
                        f'<div style="width:{pv*100:.1f}%;height:100%;background:{c2};border-radius:4px"></div></div>')
                rows_html += f"""<tr>
                  <td class="left"><span style="font-weight:700;color:{c1}">{row['_l1']}</span></td>
                  <td class="left"><span style="font-weight:600;color:{c2}">{row['_l2']}</span></td>
                  <td style="font-weight:700">{int(row['Jumlah']):,}</td>
                  <td><span class="pill b">{pv:.1%}</span></td>
                  <td style="min-width:120px">{bar}</td>
                </tr>"""

            st.markdown(f"""<div style="max-height:500px;overflow-y:auto">
            <table class="t"><thead><tr>
              <th class="left">Kategori L1</th><th class="left">Breakdown L2</th>
              <th>Jumlah</th><th>% dari total</th><th>Proporsi</th>
            </tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB FUNNEL RESPONSE
# ═══════════════════════════════════════════════════════════
if conv is not None and "Funnel Response" in tab_idx:
    with tab_objs[tab_idx["Funnel Response"]]:
        import re as _re

        # ── Data persiapan ──────────────────────────────────────
        fr_df = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and fr_df["_date"].notna().any():
            fr_df = fr_df[fr_df["_date"].dt.strftime("%B %Y") == sel_month]

        # Gabung semua pesan per sesi
        sess_all = fr_df.groupby("_sess")["_msg"].apply(
            lambda x: " ".join(x.dropna().astype(str))
        ).reset_index()
        sess_all.columns = ["_sess", "_all_msgs"]
        sess_phone = fr_df.groupby("_sess")["_phone"].first().reset_index()
        sess_all = sess_all.merge(sess_phone, on="_sess", how="left")
        sess_all["_phone_norm"] = sess_all["_phone"].apply(normalize_phone)

        total_resp = len(sess_all)

        # ── Klasifikasi Level 1 ─────────────────────────────────
        # Urutan prioritas: Sudah Bayar > Janji Bayar > Hubungi Kami > No Push > Lainnya
        L1_RULES = [
            ("Sudah Bayar",  [r"(sudah|udah)\s*(bayar|transfer|tf|lunas)", r"(sudah\s*lunas|lunas)", r"ukti"]),
            ("Janji Bayar",  [r"(janji|akan|mau|siap|insya\s*allah|nanti)\s*(bayar|transfer|tf|lunasi)",
                               r"(besok|lusa|senin|selasa|rabu|kamis|jumat|sabtu|minggu).*(bayar|transfer)",
                               r"tanggal\s*\d+.*(bayar|transfer)"]),
            ("Hubungi Kami", [r"(hubungi|kontak|telepon|wa\s*balik|call|cs|customer\s*service)",
                               r"(minta\s*autodebet|autodebet|auto\s*debet)",
                               r"(cara\s*bayar|mau\s*bayar|gimana\s*bayar|minta\s*rekening)",
                               r"(nego|negosiasi|keringanan|diskon|restruktur|cicil)",
                               r"(salah\s*nomor|bukan\s*saya|wrong\s*number)"]),
            ("No Push",      [r"(tidak\s*bisa|gabisa|belum\s*bisa|blm\s*bisa|gak\s*bisa)",
                               r"(stop|berhenti|jangan|hapus|unsubscribe|blokir)",
                               r"(tidak\s*ada\s*uang|lagi\s*susah|belum\s*ada)"]),
        ]

        def classify_l1(msg):
            m = msg.lower()
            for label, pats in L1_RULES:
                for p in pats:
                    if _re.search(p, m):
                        return label
            return "Lainnya"

        sess_all["_l1"] = sess_all["_all_msgs"].apply(classify_l1)

        # ── Klasifikasi Level 2 ─────────────────────────────────
        L2_RULES = {
            "Sudah Bayar": [
                ("Beneran Bayar",  None),   # diisi dari SC check
                ("Tidak Terbukti", None),
                ("Unknown",        None),
            ],
            "Janji Bayar": [
                ("Real Promise",    [r"(besok|lusa|tanggal\s*\d+|tgl\s*\d+|senin|selasa|rabu|kamis|jumat|sabtu)",
                                     r"(pasti|insya\s*allah|siap)"]),
                ("Broken Promise",  None),  # diisi dari SC check (janji tapi tidak bayar)
                ("Unknown",         None),  # tidak ada di SC
            ],
            "Hubungi Kami": [
                ("Minta Autodebet", [r"(autodebet|auto\s*debet)"]),
                ("Cara Bayar",      [r"(cara\s*bayar|gimana\s*bayar|minta\s*rekening|mau\s*bayar)"]),
                ("Nego Denda",      [r"(nego|denda|keringanan|diskon|restruktur)"]),
                ("Salah Nomor",     [r"(salah\s*nomor|bukan\s*saya|wrong\s*number)"]),
                ("Lainnya",         None),
            ],
            "No Push": [
                ("Tidak Bisa Bayar",[r"(tidak\s*bisa|gabisa|belum\s*bisa|blm\s*bisa|gak\s*bisa)"]),
                ("Minta Stop",      [r"(stop|berhenti|jangan|hapus|unsubscribe|blokir)"]),
                ("Belum Ada Dana",  [r"(tidak\s*ada\s*uang|lagi\s*susah|belum\s*ada)"]),
                ("Lainnya",         None),
            ],
            "Lainnya": [
                ("Lainnya", None),
            ],
        }

        def classify_l2(msg, l1):
            rules = L2_RULES.get(l1, [])
            m = msg.lower()
            for label, pats in rules:
                if pats is None:
                    continue
                for p in pats:
                    if _re.search(p, m):
                        return label
            return rules[-1][0] if rules else "Lainnya"

        sess_all["_l2_raw"] = sess_all.apply(
            lambda r: classify_l2(r["_all_msgs"], r["_l1"]), axis=1
        )

        # ── Cross-check SC untuk Sudah Bayar & Janji Bayar ──────
        # Rebuild lookup dari paid_lookup yang sudah ada di tab Realisasi
        # Gunakan rek_lookup + sc_lookup kalau ada
        def get_bayar_status(phone_norm):
            if not has_realisasi:
                return None
            rek = rek_lookup.get(phone_norm) if "rek_lookup" in dir() else None
            if not rek:
                return None
            nok = rek.get("nokontrak","")
            sc  = sc_lookup.get(nok) if nok and "sc_lookup" in dir() else None
            if sc:
                return sc["bayar_sc"]
            return None

        sess_all["_bayar_sc"] = sess_all["_phone_norm"].apply(get_bayar_status)

        # Finalize L2 untuk Sudah Bayar & Janji Bayar pakai SC
        def finalize_l2(row):
            l1  = row["_l1"]
            l2r = row["_l2_raw"]
            bs  = row["_bayar_sc"]

            if l1 == "Sudah Bayar":
                if bs is True:  return "Beneran Bayar"
                if bs is False: return "Tidak Terbukti"
                return "Unknown"

            if l1 == "Janji Bayar":
                if bs is True:  return "Real Promise"
                if bs is False: return "Broken Promise"
                return "Unknown"

            return l2r

        sess_all["_l2"] = sess_all.apply(finalize_l2, axis=1)

        # ── Hitung untuk visualisasi ────────────────────────────
        L1_CONFIG = {
            "Sudah Bayar":  {"fg":"#15803D","bg":"#DCFCE7","bd":"#86EFAC"},
            "Janji Bayar":  {"fg":"#1D4ED8","bg":"#EFF6FF","bd":"#93C5FD"},
            "No Push":      {"fg":"#B91C1C","bg":"#FEE2E2","bd":"#FECACA"},
            "Hubungi Kami": {"fg":"#D97706","bg":"#FFFBEB","bd":"#FDE68A"},
            "Lainnya":      {"fg":"#475569","bg":"#F1F5F9","bd":"#CBD5E1"},
        }
        L2_COLORS = {
            "Beneran Bayar":"#15803D","Real Promise":"#15803D",
            "Tidak Terbukti":"#B91C1C","Broken Promise":"#B91C1C",
            "Unknown":"#475569",
            "Minta Autodebet":"#0891B2","Cara Bayar":"#1D4ED8",
            "Nego Denda":"#7C3AED","Salah Nomor":"#94A3B8",
            "Tidak Bisa Bayar":"#DC2626","Minta Stop":"#B91C1C",
            "Belum Ada Dana":"#EF4444","Lainnya":"#64748B",
        }

        # ── Filter L1 ───────────────────────────────────────────
        st.markdown('<p class="sh">Filter Kategori</p>', unsafe_allow_html=True)

        l1_counts = sess_all["_l1"].value_counts()
        l1_order  = [k for k in ["Sudah Bayar","Janji Bayar","No Push","Hubungi Kami","Lainnya"] if k in l1_counts]

        # Tombol filter L1
        btn_cols = st.columns(len(l1_order) + 1)
        if "fr_sel_l1" not in st.session_state:
            st.session_state["fr_sel_l1"] = "Semua"

        with btn_cols[0]:
            if st.button("Semua", key="fr_all",
                         type="primary" if st.session_state["fr_sel_l1"] == "Semua" else "secondary",
                         use_container_width=True):
                st.session_state["fr_sel_l1"] = "Semua"
                st.rerun()

        for i, l1 in enumerate(l1_order):
            cfg = L1_CONFIG.get(l1, L1_CONFIG["Lainnya"])
            cnt = int(l1_counts.get(l1, 0))
            with btn_cols[i+1]:
                if st.button(f"{l1} ({cnt:,})", key=f"fr_{l1}",
                             type="primary" if st.session_state["fr_sel_l1"] == l1 else "secondary",
                             use_container_width=True):
                    st.session_state["fr_sel_l1"] = l1
                    st.rerun()

        sel_l1 = st.session_state["fr_sel_l1"]
        filtered = sess_all if sel_l1 == "Semua" else sess_all[sess_all["_l1"] == sel_l1]

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Summary cards L1 ────────────────────────────────────
        st.markdown('<p class="sh">Breakdown Level 1</p>', unsafe_allow_html=True)
        card_cols = st.columns(len(l1_order))
        for i, l1 in enumerate(l1_order):
            cfg = L1_CONFIG.get(l1, L1_CONFIG["Lainnya"])
            cnt = int(l1_counts.get(l1, 0))
            pv  = cnt / total_resp if total_resp else 0
            with card_cols[i]:
                border_sty = f"border:2px solid {cfg['bd']}" if sel_l1 == l1 else f"border:1.5px solid {cfg['bd']}"
                st.markdown(f"""<div class="mbox" style="background:{cfg['bg']};{border_sty};color:{cfg['fg']}">
                  <div class="mbox-lbl">{l1}</div>
                  <div class="mbox-val">{cnt:,}</div>
                  <div class="mbox-pct">{pv:.1%} dari {total_resp:,}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Breakdown L2 ─────────────────────────────────────────
        st.markdown(f'<p class="sh">Breakdown Level 2{"  —  " + sel_l1 if sel_l1 != "Semua" else " (Semua Kategori)"}</p>', unsafe_allow_html=True)

        if sel_l1 == "Semua":
            # Tampilkan semua L2 per L1 dalam grid
            for l1 in l1_order:
                cfg   = L1_CONFIG.get(l1, L1_CONFIG["Lainnya"])
                grp   = sess_all[sess_all["_l1"] == l1]
                l2cnt = grp["_l2"].value_counts()
                total_l1 = len(grp)
                if total_l1 == 0:
                    continue

                bars = ""
                for label, cnt in l2cnt.items():
                    pv  = cnt / total_l1
                    clr = L2_COLORS.get(label, "#64748B")
                    bars += f"""<div class="brow">
                      <div class="blbl">{label}</div>
                      <div class="btrk">
                        <div class="bfil" style="width:{pv*100:.1f}%;background:{clr}">
                          <span class="bnum">{cnt:,}</span>
                        </div>
                      </div>
                      <div class="bpct">{pv:.1%}</div>
                    </div>"""

                st.markdown(f"""<div class="card" style="border-left:3px solid {cfg['bd']}">
                  <p style="font-size:12px;font-weight:700;color:{cfg['fg']};margin:0 0 10px">{l1}
                    <span style="font-size:11px;font-weight:400;color:#94A3B8;margin-left:8px">{total_l1:,} sesi</span>
                  </p>
                  {bars}
                </div>""", unsafe_allow_html=True)

        else:
            # Tampilkan L2 untuk L1 yang dipilih + tabel detail
            grp   = sess_all[sess_all["_l1"] == sel_l1]
            l2cnt = grp["_l2"].value_counts()
            total_l1 = len(grp)

            col_chart, col_tbl = st.columns([2, 3])

            with col_chart:
                bars = ""
                for label, cnt in l2cnt.items():
                    pv  = cnt / total_l1 if total_l1 else 0
                    clr = L2_COLORS.get(label, "#64748B")
                    bars += f"""<div class="brow">
                      <div class="blbl">{label}</div>
                      <div class="btrk">
                        <div class="bfil" style="width:{pv*100:.1f}%;background:{clr}">
                          <span class="bnum">{cnt:,}</span>
                        </div>
                      </div>
                      <div class="bpct">{pv:.1%}</div>
                    </div>"""
                cfg = L1_CONFIG.get(sel_l1, L1_CONFIG["Lainnya"])
                st.markdown(f"""<div class="card" style="border-left:3px solid {cfg['bd']}">
                  <p style="font-size:11px;color:#94A3B8;margin:0 0 12px">Total <b>{total_l1:,}</b> sesi kategori {sel_l1}</p>
                  {bars}
                </div>""", unsafe_allow_html=True)

            with col_tbl:
                # Filter L2
                l2_options = ["Semua"] + list(l2cnt.index)
                sel_l2 = st.selectbox("Filter sub-kategori:", l2_options, key="fr_sel_l2")

                tbl = grp if sel_l2 == "Semua" else grp[grp["_l2"] == sel_l2]

                st.markdown(f'<p style="font-size:11px;color:#94A3B8;margin:4px 0 8px">Menampilkan <b>{len(tbl):,}</b> sesi</p>', unsafe_allow_html=True)

                # Build table rows
                tbl_rows = ""
                for _, row in tbl.head(100).iterrows():
                    msg_preview = str(row["_all_msgs"])[:60] + ("..." if len(str(row["_all_msgs"])) > 60 else "")
                    clr2 = L2_COLORS.get(row["_l2"], "#64748B")
                    bayar_lbl = ""
                    if row["_bayar_sc"] is True:
                        bayar_lbl = '<span class="pill g">Bayar</span>'
                    elif row["_bayar_sc"] is False:
                        bayar_lbl = '<span class="pill r">Belum</span>'
                    else:
                        bayar_lbl = '<span class="pill s">N/A</span>'

                    tbl_rows += f"""<tr>
                      <td style="color:#64748B;font-size:10px">{str(row.get("_phone",""))[-4:]}</td>
                      <td class="left" style="font-size:11px">{msg_preview}</td>
                      <td><span class="pill" style="background:{clr2}22;color:{clr2}">{row["_l2"]}</span></td>
                      <td>{bayar_lbl}</td>
                    </tr>"""

                st.markdown(f"""<div style="max-height:400px;overflow-y:auto">
                <table class="t"><thead><tr>
                  <th>No HP</th><th class="left">Pesan</th><th>Sub-kategori</th><th>Status Bayar</th>
                </tr></thead><tbody>{tbl_rows}</tbody></table></div>
                {"" if len(tbl) <= 100 else f'<p style="font-size:10px;color:#94A3B8;margin-top:4px">Menampilkan 100 dari {len(tbl):,} baris.</p>'}
                """, unsafe_allow_html=True)

                # Download
                dl_df = tbl[["_phone_norm","_l1","_l2","_all_msgs","_bayar_sc"]].copy()
                dl_df.columns = ["No HP","Kategori","Sub-kategori","Pesan","Bayar SC"]
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    dl_df.to_excel(w, index=False)
                st.download_button(
                    "Download data ini (.xlsx)",
                    buf.getvalue(),
                    f"funnel_{sel_l1}_{sel_l2}.xlsx",
                    "application/vnd.ms-excel",
                    key="dl_funnel"
                )


# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<p style="text-align:center;font-size:11px;color:#94A3B8">'
    'Dashboard WA Broadcast + Realisasi Bayar - PT. BCA Finance - ASR Mobil</p>',
    unsafe_allow_html=True
)
