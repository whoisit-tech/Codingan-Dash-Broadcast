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

    f_sum = st.file_uploader(
        "1. Summary Broadcast",
        type=["xlsx", "xls"],
        help="Kolom: DateUploaded, Sent, Delivered, Read, Failed, Total"
    )
    f_conv = st.file_uploader(
        "2. Conversation / Response WA",
        type=["xlsx", "xls"],
        help="Kolom: Origin, Message Type, Message, Session, Created At"
    )
    f_sc = st.file_uploader(
        "3. File SC (Feb-Mar)",
        type=["xlsx", "xls"],
        help="Sheet: Sc Februari, Sc Maret"
    )
    f_rekap = st.file_uploader(
        "4. Rekap WAI 4W",
        type=["xlsx", "xls"],
        help="Kolom: no_wa, status, year, month, day, body_param_2"
    )

    files_status = {
        "Summary": f_sum is not None,
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

has_sum       = f_sum is not None
has_conv      = f_conv is not None
has_sc        = f_sc is not None
has_rekap     = f_rekap is not None
has_realisasi = has_conv and (has_sc or has_rekap)

if not has_sum:
    st.markdown("""
    <div style="background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:48px 32px;text-align:center;margin-top:24px">
      <div style="font-size:16px;font-weight:700;color:#1E293B;margin-bottom:6px">Upload File untuk Memulai</div>
      <div style="font-size:13px;color:#64748B;max-width:440px;margin:0 auto">
        Upload file via panel kiri. Minimal <b>Summary Broadcast</b> untuk melihat data broadcast.
        Tambahkan file lainnya untuk fitur realisasi bayar.
      </div>
      <div style="margin-top:20px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap">
        <span style="background:#DBEAFE;color:#1D4ED8;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">1. Summary Broadcast (wajib)</span>
        <span style="background:#F0FDF4;color:#15803D;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">2. Conversation WA</span>
        <span style="background:#FFFBEB;color:#B45309;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">3. File SC</span>
        <span style="background:#F3E8FF;color:#7C3AED;border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600">4. Rekap WAI</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════
# LOAD & PARSE FUNCTIONS
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_summary(raw):
    df = pd.read_excel(io.BytesIO(raw))
    df.columns = [c.strip() for c in df.columns]
    dcol = next((c for c in df.columns if "date" in c.lower()), df.columns[0])
    df["Date"] = pd.to_datetime(df[dcol], dayfirst=True, errors="coerce")
    for c in ["Sent", "Delivered", "Read", "Failed", "Canceled", "Total"]:
        df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0).astype(int)
    df["Undelivered"] = (df["Sent"] - df["Delivered"]).clip(0)
    df["Unread"]      = (df["Delivered"] - df["Read"]).clip(0)
    df["Month"]       = df["Date"].dt.strftime("%B %Y")
    df["MonthSort"]   = df["Date"].dt.year * 100 + df["Date"].dt.month
    return df.sort_values("Date").reset_index(drop=True)


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
            return "Lainnya"
    return "Lainnya"


# ═══════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════
df = load_summary(f_sum.read())

_rekap_raw = f_rekap.read() if has_rekap else None
df_rekap   = load_rekap(_rekap_raw) if _rekap_raw else None

# Tampilkan debug status Rekap di sidebar jika ada
if df_rekap is not None and "status_values" in df.attrs:
    with st.sidebar:
        st.markdown("---")
        st.markdown('<p style="font-size:11px;font-weight:600;color:#94A3B8;margin-bottom:4px">STATUS DI REKAP</p>', unsafe_allow_html=True)
        sv = df.attrs.get("status_values", {})
        rows = "".join([
            f'<tr><td style="font-size:10px;color:#CBD5E1;padding:2px 4px">{k}</td>'
            f'<td style="font-size:10px;color:#94A3B8;padding:2px 4px;text-align:right">{v:,}</td></tr>'
            for k, v in sorted(sv.items(), key=lambda x: -x[1])
        ])
        st.markdown(f'<table style="width:100%">{rows}</table>', unsafe_allow_html=True)

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
# BRIDGE — hitung angka Conversation dalam konteks Summary
# Semua tab pakai variabel ini agar angka nyambung
# ═══════════════════════════════════════════════════════════
# Filter conversation sesuai bulan yang dipilih
conv_filtered = None
n_balas       = 0   # jumlah sesi unik yang balas (ada di Conversation)
n_tidak_balas = 0   # Read - yang balas (tidak ada di Conversation)

if conv is not None:
    cdf_bridge = conv[conv["_orig"] == "IN"].copy()
    if sel_month != "Semua Bulan" and cdf_bridge["_date"].notna().any():
        cdf_bridge = cdf_bridge[cdf_bridge["_date"].dt.strftime("%B %Y") == sel_month]
    conv_filtered = cdf_bridge
    n_balas       = cdf_bridge["_sess"].nunique()
    # Tidak balas = Read dari Summary dikurangi yang ada di Conversation
    # (Read = yang buka pesan, sebagian balas sebagian tidak)
    n_tidak_balas = max(0, R - n_balas)


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


def mbox(lbl, val, pct_str, fg, bg, border):
    return f"""<div class="mbox" style="background:{bg};border-color:{border};color:{fg}">
      <div class="mbox-lbl">{lbl}</div>
      <div class="mbox-val">{val:,}</div>
      <div class="mbox-pct">{pct_str}</div>
    </div>"""



# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
import re as _re

def normalize_phone(s):
    s = ''.join(filter(str.isdigit, str(s).strip()))
    if s.startswith("0"):   s = "62" + s[1:]
    elif s.startswith("8"): s = "62" + s
    return s

def find_col(df, candidates):
    for c in candidates:
        for col in df.columns:
            if c.strip().lower() == col.strip().lower():
                return col
    return None

def to_xlsx(df_out):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_out.to_excel(w, index=False)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════
# TABS — 4 TAB BERSIH
# ═══════════════════════════════════════════════════════════
tabs_available = ["Rekap Broadcast"]
if has_conv:              tabs_available.append("Response Nasabah")
if has_realisasi:         tabs_available.append("Detail per Kontrak")
if has_conv:              tabs_available.append("Analisis Teks")

tab_objs = st.tabs(tabs_available)
ti = {label: i for i, label in enumerate(tabs_available)}


# ═══════════════════════════════════════════════════════════
# TAB 1 — REKAP BROADCAST (dari Summary)
# ═══════════════════════════════════════════════════════════
with tab_objs[ti["Rekap Broadcast"]]:

    # Funnel cards
    st.markdown('<p class="sh">Funnel Broadcast</p>', unsafe_allow_html=True)

    st.markdown(f'''
    <div style="display:grid;grid-template-columns:1fr;gap:6px;margin-bottom:8px">
      {mbox("Total Data Upload", T, "100% — base semua perhitungan", "#1E293B", "#F8FAFC", "#CBD5E1")}
    </div>''', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: st.markdown(mbox("Failed", F, f"{pct(F,T)} dari upload", "#B91C1C", "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
    with c2: st.markdown(mbox("Sent (Berhasil Kirim)", S, f"{pct(S,T)} dari upload", "#15803D", "#F0FDF4", "#86EFAC"), unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3: st.markdown(mbox("Delivered", D, f"{pct(D,S)} dari sent", "#1D4ED8", "#EFF6FF", "#93C5FD"), unsafe_allow_html=True)
    with c4: st.markdown(mbox("Belum Delivered", UD, f"{pct(UD,S)} dari sent", "#D97706", "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5: st.markdown(mbox("Read (Dibaca)", R, f"{pct(R,D)} dari delivered", "#0E7490", "#ECFEFF", "#67E8F9"), unsafe_allow_html=True)
    with c6: st.markdown(mbox("Unread (Tidak Dibaca)", UR, f"{pct(UR,D)} dari delivered", "#7C3AED", "#FAF5FF", "#C4B5FD"), unsafe_allow_html=True)

    # Nyambung ke Conversation
    if has_conv:
        cdf_cnt = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf_cnt["_date"].notna().any():
            cdf_cnt = cdf_cnt[cdf_cnt["_date"].dt.strftime("%B %Y") == sel_month]
        n_balas       = cdf_cnt["_sess"].nunique()
        n_tidak_balas = max(0, R - n_balas)
        st.markdown(f'''
        <div class="info-box" style="margin-top:10px">
        Dari <b>{R:,} yang membaca</b>:
        <b style="color:#15803D">{n_balas:,} ({pct(n_balas,R)}) membalas WA</b> —
        <b style="color:#B91C1C">{n_tidak_balas:,} ({pct(n_tidak_balas,R)}) tidak membalas</b>.
        Lihat breakdown balasan di tab <b>Response Nasabah</b>.
        </div>''', unsafe_allow_html=True)

    # Tabel per batch
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Detail per Batch</p>', unsafe_allow_html=True)

    rows_html = ""
    for _, r in dff.iterrows():
        fp = r["Failed"]/r["Total"] if r["Total"] else 0
        dp = r["Delivered"]/r["Total"] if r["Total"] else 0
        rp = r["Read"]/r["Delivered"] if r["Delivered"] else 0
        def pill(v, hi, lo, inv=False):
            cls = ("g" if (v<hi if inv else v>hi) else "r" if (v>lo if inv else v<lo) else "o")
            return f'<span class="pill {cls}">{v:.0%}</span>'
        rows_html += f"""<tr>
          <td class="left">{r['Date'].strftime('%d %b %Y')}</td>
          <td>{int(r['Total']):,}</td>
          <td style="color:#DC2626">{int(r['Failed']):,}</td><td>{pill(fp,.15,.30,True)}</td>
          <td style="color:#15803D">{int(r['Sent']):,}</td>
          <td style="color:#1D4ED8">{int(r['Delivered']):,}</td><td>{pill(dp,.70,.50)}</td>
          <td style="color:#0E7490">{int(r['Read']):,}</td><td>{pill(rp,.65,.45)}</td>
          <td style="color:#7C3AED">{int(r['Unread']):,}</td>
        </tr>"""

    fp_t=F/T if T else 0; dp_t=D/T if T else 0; rp_t=R/D if D else 0
    def pill_t(v,hi,lo,inv=False):
        cls=("g" if (v<hi if inv else v>hi) else "r" if (v>lo if inv else v<lo) else "o")
        return f'<span class="pill {cls}">{v:.1%}</span>'
    rows_html += f"""<tr class="tot">
      <td class="left">TOTAL ({len(dff)} batch)</td>
      <td>{T:,}</td><td>{F:,}</td><td>{pill_t(fp_t,.15,.30,True)}</td>
      <td>{S:,}</td><td>{D:,}</td><td>{pill_t(dp_t,.70,.50)}</td>
      <td>{R:,}</td><td>{pill_t(rp_t,.65,.45)}</td><td>{UR:,}</td>
    </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;max-height:400px;overflow-y:auto">
    <table class="t"><thead><tr>
      <th class="left">Tanggal</th><th>Total</th>
      <th>Failed</th><th>Fail%</th><th>Sent</th>
      <th>Delivered</th><th>Del%</th><th>Read</th><th>Read%</th><th>Unread</th>
    </tr></thead><tbody>{rows_html}</tbody></table></div>
    <p style="font-size:10px;color:#94A3B8;margin-top:4px">Fail%/Del% dari Total · Read% dari Delivered</p>
    """, unsafe_allow_html=True)

    # Trend chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Tren per Batch</p>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dff["Date"], y=dff["Total"], name="Total", marker_color="#E2E8F0", opacity=0.8))
    for m, c, d in [("Delivered","#2563EB",None),("Read","#0891B2","dot"),("Failed","#DC2626",None)]:
        fig.add_trace(go.Scatter(x=dff["Date"], y=dff[m], name=m,
            line=dict(color=c,width=2,dash=d or "solid"), mode="lines+markers", marker=dict(size=5,color=c)))
    fig.update_layout(barmode="overlay", height=260, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
        font=dict(family="Inter",color="#64748B"),
        legend=dict(orientation="h",y=-0.3,bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#E2E8F0",tickformat="%d %b"),
        yaxis=dict(gridcolor="#E2E8F0"), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — RESPONSE NASABAH
# Flow: Conversation → klasifikasi → cross-check Rekap+SC
# ═══════════════════════════════════════════════════════════
if has_conv and "Response Nasabah" in ti:
    with tab_objs[ti["Response Nasabah"]]:

        # ── Siapkan data Conversation ──
        cdf = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf["_date"].notna().any():
            cdf = cdf[cdf["_date"].dt.strftime("%B %Y") == sel_month]

        # Satu sesi bisa banyak pesan — gabung semua pesan per sesi
        sess_msgs = cdf.groupby("_sess")["_msg"].apply(
            lambda x: " ".join(x.dropna().astype(str))
        ).reset_index()
        sess_msgs.columns = ["_sess", "_all_msgs"]
        sess_info = cdf.groupby("_sess").agg(
            _phone=("_phone","first"),
            _date=("_date","min"),
            _n_pesan=("_msg","count")
        ).reset_index()
        sess = sess_msgs.merge(sess_info, on="_sess", how="left")
        sess["_phone_norm"] = sess["_phone"].apply(normalize_phone)
        n_balas = len(sess)
        n_tidak_balas = max(0, R - n_balas)

        # ── Klasifikasi pesan ──
        L1_RULES = [
            ("Sudah Bayar",  [r"\b(sudah|udah)\s*(bayar|transfer|tf|lunas)\b",
                               r"\b(sudah\s*lunas|lunas|tadi\s*bayar|bukti)\b"]),
            ("Janji Bayar",  [r"\b(janji|akan|mau|siap|insya\s*allah|nanti)\s*(bayar|transfer|tf|lunasi)\b",
                               r"\b(besok|lusa|tanggal\s*\d+|tgl\s*\d+|senin|selasa|rabu|kamis|jumat|sabtu)\b"]),
            ("Hubungi Kami", [r"\b(hubungi|kontak|telepon|wa\s*balik|call|cs)\b",
                               r"\b(minta\s*autodebet|autodebet|cara\s*bayar|gimana\s*bayar)\b",
                               r"\b(nego|denda|keringanan|diskon|restruktur|cicil)\b",
                               r"\b(salah\s*nomor|bukan\s*saya|wrong\s*number)\b"]),
            ("Tidak Bisa",   [r"\b(tidak\s*bisa|gabisa|belum\s*bisa|gak\s*bisa|blm\s*bisa)\b",
                               r"\b(stop|jangan|hapus|unsubscribe|tidak\s*ada\s*uang|lagi\s*susah)\b"]),
        ]

        L2_RULES = {
            "Sudah Bayar":  [
                ("Klaim Lunas",     [r"\b(lunas|sudah\s*lunas)\b"]),
                ("Klaim Transfer",  [r"\b(transfer|tf|kirim)\b"]),
                ("Kirim Bukti",     [r"\b(bukti|struk|foto|screenshot)\b"]),
            ],
            "Janji Bayar":  [
                ("Ada Tanggal",     [r"\b(tanggal|tgl)\s*\d+\b", r"\b(besok|lusa|senin|selasa|rabu|kamis|jumat|sabtu)\b"]),
                ("Janji Umum",      None),
            ],
            "Hubungi Kami": [
                ("Autodebet",       [r"\b(autodebet|auto\s*debet)\b"]),
                ("Cara Bayar",      [r"\b(cara\s*bayar|gimana\s*bayar|minta\s*rekening)\b"]),
                ("Nego/Cicil",      [r"\b(nego|cicil|keringanan|diskon|restruktur)\b"]),
                ("Salah Nomor",     [r"\b(salah\s*nomor|bukan\s*saya|wrong\s*number)\b"]),
            ],
            "Tidak Bisa":   [
                ("Tidak Ada Dana",  [r"\b(tidak\s*ada\s*uang|lagi\s*susah|belum\s*ada)\b"]),
                ("Minta Stop",      [r"\b(stop|jangan|hapus|unsubscribe)\b"]),
                ("Belum Bisa",      None),
            ],
        }

        def classify_l1(msg):
            m = msg.lower()
            for label, pats in L1_RULES:
                for p in pats:
                    if _re.search(p, m): return label
            return "Lainnya"

        def classify_l2(msg, l1):
            rules = L2_RULES.get(l1, [])
            m = msg.lower()
            for label, pats in rules:
                if pats is None: continue
                for p in pats:
                    if _re.search(p, m): return label
            return rules[-1][0] if rules else "Lainnya"

        sess["_l1"] = sess["_all_msgs"].apply(classify_l1)
        sess["_l2"] = sess.apply(lambda r: classify_l2(r["_all_msgs"], r["_l1"]), axis=1)

        # ── Cross-check Rekap + SC ──
        # Step 1: Rekap → mapping no HP ke no kontrak
        rek_map = {}  # {phone_norm: nokontrak}
        if df_rekap is not None:
            rp_col  = find_col(df_rekap, ["no_wa","NoWA",col_phone_rekap])
            rnk_col = find_col(df_rekap, ["body_param_2","body_param_1",col_nokontrak_rek])
            if rp_col:
                for _, row in df_rekap.iterrows():
                    norm = normalize_phone(str(row.get(rp_col,"")))
                    nok  = str(row.get(rnk_col,"")).strip() if rnk_col else ""
                    if norm and norm != "62" and nok:
                        rek_map[norm] = nok

        # Step 2: SC → status bayar per no kontrak
        sc_map = {}  # {nokontrak: {bayar, tgl, nama}}
        if df_sc is not None:
            snk_col  = find_col(df_sc, ["NOKONTRAK","nokontrak",col_nokontrak_sc])
            slp_col  = find_col(df_sc, ["lastpaiddate","LastPaidDate",col_lastpaid])
            snam_col = find_col(df_sc, ["custname","CustName",col_custname])
            if snk_col:
                for _, row in df_sc.iterrows():
                    nok = str(row.get(snk_col,"")).strip()
                    if not nok: continue
                    lp    = row.get(slp_col) if slp_col else None
                    bayar = pd.notna(lp) and str(lp).strip() not in ["","nan","NaT","None","0"]
                    sc_map[nok] = {
                        "bayar": bayar,
                        "tgl":   str(lp) if bayar else "",
                        "nama":  str(row.get(snam_col,"")) if snam_col else "",
                    }

        def get_status(phone_norm):
            nok = rek_map.get(phone_norm)
            if not nok: return None, None, None
            sc = sc_map.get(nok)
            if not sc: return None, nok, None
            return sc["bayar"], nok, sc["nama"]

        sess[["_bayar","_nokontrak","_nama"]] = sess["_phone_norm"].apply(
            lambda p: pd.Series(get_status(p))
        )

        # ── TAMPILAN ──────────────────────────────────────────
        # Header angka nyambung dari Summary
        st.markdown(f'''
        <div style="background:#1E3A5F;border-radius:8px;padding:12px 20px;margin-bottom:16px">
          <div style="color:#fff;font-weight:700;font-size:14px;margin-bottom:6px">Ringkasan Response</div>
          <div style="display:flex;gap:20px;flex-wrap:wrap">
            <span style="color:rgba(255,255,255,.6);font-size:12px">Read (Summary): <b style="color:#67E8F9">{R:,}</b></span>
            <span style="color:rgba(255,255,255,.6);font-size:12px">Membalas: <b style="color:#86EFAC">{n_balas:,} ({pct(n_balas,R)})</b></span>
            <span style="color:rgba(255,255,255,.6);font-size:12px">Tidak Membalas: <b style="color:#FCA5A5">{n_tidak_balas:,} ({pct(n_tidak_balas,R)})</b></span>
          </div>
        </div>''', unsafe_allow_html=True)

        # Funnel kotak: Read → Tidak Balas | Balas → L1 → L2
        ARW = '<span style="color:#94A3B8;font-size:18px;margin:0 4px;flex-shrink:0">&#8594;</span>'

        L1_COLOR = {
            "Sudah Bayar":"#15803D","Janji Bayar":"#1D4ED8",
            "Hubungi Kami":"#D97706","Tidak Bisa":"#B91C1C","Lainnya":"#475569"
        }
        L2_COLOR = {
            "Klaim Lunas":"#15803D","Klaim Transfer":"#0891B2","Kirim Bukti":"#7C3AED",
            "Ada Tanggal":"#1D4ED8","Janji Umum":"#3B82F6",
            "Autodebet":"#0891B2","Cara Bayar":"#1D4ED8","Nego/Cicil":"#7C3AED","Salah Nomor":"#94A3B8",
            "Tidak Ada Dana":"#DC2626","Minta Stop":"#B91C1C","Belum Bisa":"#EF4444",
            "Lainnya":"#64748B",
            "Beneran Bayar":"#15803D","Ingkar Janji":"#DC2626","Unknown":"#475569",
        }

        def node_box(label, count, base, color):
            pv = count / base * 100 if base else 0
            bg = "#1E293B" if "Unknown" in label else color
            return (
                f'<div style="background:{bg};border-radius:18px;padding:9px 13px;'
                f'text-align:center;min-width:115px;flex-shrink:0;display:inline-block">'
                f'<div style="color:rgba(255,255,255,.8);font-size:10px;font-weight:600;margin-bottom:2px">{label}</div>'
                f'<div style="color:#fff;font-size:17px;font-weight:800;line-height:1.1">{count:,}</div>'
                f'<div style="color:rgba(255,255,255,.65);font-size:10px">({pv:.1f}%)</div>'
                f'</div>'
            )

        l1_counts = sess["_l1"].value_counts()
        L1_ORDER  = ["Sudah Bayar","Janji Bayar","Hubungi Kami","Tidak Bisa","Lainnya"]

        # Baris 0: Read → Tidak Balas | Balas
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;flex-wrap:wrap">'
            f'  {node_box("Read", R, T, "#0E7490")}'
            f'  {ARW}'
            f'  <div style="display:flex;gap:6px;flex-wrap:wrap">'
            f'    {node_box("Tidak Membalas", n_tidak_balas, R, "#475569")}'
            f'    {node_box("Membalas WA", n_balas, R, "#15803D")}'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Baris L1 → L2, base = n_balas
        for l1 in L1_ORDER:
            cnt_l1 = int(l1_counts.get(l1, 0))
            if cnt_l1 == 0: continue
            clr1 = L1_COLOR.get(l1, "#475569")
            l2cnt = sess[sess["_l1"] == l1]["_l2"].value_counts()

            # L2 breakdown — tambah cross-check bayar untuk Sudah Bayar & Janji Bayar
            l2_html = ""
            if l1 in ("Sudah Bayar", "Janji Bayar"):
                grp = sess[sess["_l1"] == l1]
                n_bayar  = grp["_bayar"].eq(True).sum()
                n_belum  = grp["_bayar"].eq(False).sum()
                n_unk    = grp["_bayar"].isna().sum()
                l2_html += node_box("Beneran Bayar", n_bayar, cnt_l1, "#15803D")
                l2_html += node_box("Ingkar/Belum", n_belum, cnt_l1, "#DC2626")
                l2_html += node_box("Unknown", n_unk, cnt_l1, "#475569")
            else:
                for l2_lbl, cnt2 in l2cnt.items():
                    clr2 = L2_COLOR.get(l2_lbl, "#64748B")
                    l2_html += node_box(l2_lbl, cnt2, cnt_l1, clr2)

            st.markdown(
                f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;'
                f'margin-left:60px;flex-wrap:wrap">'
                f'  {node_box(l1, cnt_l1, n_balas, clr1)}'
                f'  {ARW}'
                f'  <div style="display:flex;gap:5px;flex-wrap:wrap">{l2_html}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Summary tabel L1
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Tabel Ringkasan per Kategori</p>', unsafe_allow_html=True)

        tbl_rows = ""
        for l1 in L1_ORDER:
            cnt_l1 = int(l1_counts.get(l1, 0))
            if cnt_l1 == 0: continue
            grp    = sess[sess["_l1"] == l1]
            n_b    = grp["_bayar"].eq(True).sum()
            n_bl   = grp["_bayar"].eq(False).sum()
            n_u    = grp["_bayar"].isna().sum()
            real_r = n_b / (n_b + n_bl) if (n_b + n_bl) > 0 else None
            real_str = f'<span class="pill g">{real_r:.1%}</span>' if real_r is not None else '<span class="pill s">-</span>'
            clr1 = L1_COLOR.get(l1,"#475569")
            tbl_rows += f"""<tr>
              <td class="left"><span style="font-weight:700;color:{clr1}">{l1}</span></td>
              <td>{cnt_l1:,}</td>
              <td><span class="pill b">{pct(cnt_l1,n_balas)}</span></td>
              <td><span class="pill g">{n_b:,}</span></td>
              <td><span class="pill r">{n_bl:,}</span></td>
              <td><span class="pill s">{n_u:,}</span></td>
              <td>{real_str}</td>
            </tr>"""

        st.markdown(f"""
        <table class="t"><thead><tr>
          <th class="left">Kategori</th><th>Jumlah Sesi</th><th>% dari Balas</th>
          <th>Beneran Bayar</th><th>Ingkar/Belum</th><th>Unknown</th><th>Realisasi %</th>
        </tr></thead><tbody>{tbl_rows}</tbody></table>
        <p style="font-size:10px;color:#94A3B8;margin-top:4px">
        Realisasi % = Beneran Bayar / (Bayar + Ingkar) — tidak termasuk Unknown (tidak ditemukan di SC)</p>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — DETAIL PER KONTRAK
# ═══════════════════════════════════════════════════════════
if has_realisasi and "Detail per Kontrak" in ti:
    with tab_objs[ti["Detail per Kontrak"]]:

        # Rebuild sess (reuse logic — simpel)
        cdf2 = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf2["_date"].notna().any():
            cdf2 = cdf2[cdf2["_date"].dt.strftime("%B %Y") == sel_month]

        sess2_msgs = cdf2.groupby("_sess")["_msg"].apply(
            lambda x: " ".join(x.dropna().astype(str))
        ).reset_index()
        sess2_msgs.columns = ["_sess","_all_msgs"]
        sess2_info = cdf2.groupby("_sess").agg(
            _phone=("_phone","first"), _date=("_date","min"),
            _n_pesan=("_msg","count"), _types=("_type", lambda x: ",".join(x.dropna().unique()))
        ).reset_index()
        sess2 = sess2_msgs.merge(sess2_info, on="_sess", how="left")
        sess2["_phone_norm"] = sess2["_phone"].apply(normalize_phone)

        def classify_l1_2(msg):
            m = msg.lower()
            for label, pats in L1_RULES:
                for p in pats:
                    if _re.search(p, m): return label
            return "Lainnya"

        sess2["_l1"] = sess2["_all_msgs"].apply(classify_l1_2)

        # Rebuild lookup (ulang karena scope)
        rek_map2 = {}
        if df_rekap is not None:
            rp2  = find_col(df_rekap, ["no_wa","NoWA",col_phone_rekap])
            rnk2 = find_col(df_rekap, ["body_param_2","body_param_1",col_nokontrak_rek])
            if rp2:
                for _, row in df_rekap.iterrows():
                    norm = normalize_phone(str(row.get(rp2,"")))
                    nok  = str(row.get(rnk2,"")).strip() if rnk2 else ""
                    if norm and norm != "62": rek_map2[norm] = nok

        sc_map2 = {}
        if df_sc is not None:
            snk2  = find_col(df_sc, ["NOKONTRAK","nokontrak",col_nokontrak_sc])
            slp2  = find_col(df_sc, ["lastpaiddate","LastPaidDate",col_lastpaid])
            snam2 = find_col(df_sc, ["custname","CustName",col_custname])
            scb2  = find_col(df_sc, ["branchname","BranchName",col_branch])
            sop2  = find_col(df_sc, ["ospokok",col_ospokok])
            sar2  = find_col(df_sc, ["osar",col_osar])
            if snk2:
                for _, row in df_sc.iterrows():
                    nok = str(row.get(snk2,"")).strip()
                    if not nok: continue
                    lp  = row.get(slp2) if slp2 else None
                    bayar = pd.notna(lp) and str(lp).strip() not in ["","nan","NaT","None","0"]
                    sc_map2[nok] = {
                        "bayar":  bayar, "tgl": str(lp) if bayar else "",
                        "nama":   str(row.get(snam2,"")) if snam2 else "",
                        "cabang": str(row.get(scb2,""))  if scb2  else "",
                        "ospokok":str(row.get(sop2,""))  if sop2  else "",
                        "osar":   str(row.get(sar2,""))  if sar2  else "",
                    }

        rows_detail = []
        for _, row in sess2.iterrows():
            nok = rek_map2.get(row["_phone_norm"],"")
            sc  = sc_map2.get(nok,{}) if nok else {}
            rows_detail.append({
                "No HP":        row["_phone_norm"],
                "No Kontrak":   nok,
                "Nama":         sc.get("nama",""),
                "Cabang":       sc.get("cabang",""),
                "Kategori":     row["_l1"],
                "Pesan":        str(row["_all_msgs"])[:120],
                "Jumlah Pesan": row["_n_pesan"],
                "Status Bayar": "Bayar" if sc.get("bayar") is True else ("Belum" if sc.get("bayar") is False else "Unknown"),
                "Tgl Bayar":    sc.get("tgl",""),
                "OS Pokok":     sc.get("ospokok",""),
                "OS AR":        sc.get("osar",""),
                "Tgl Chat":     row["_date"],
            })

        detail_df = pd.DataFrame(rows_detail)

        # Filter
        st.markdown('<p class="sh">Filter</p>', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            kat_f = st.selectbox("Kategori", ["Semua"] + L1_ORDER, key="det_kat")
        with fc2:
            stat_f = st.selectbox("Status Bayar", ["Semua","Bayar","Belum","Unknown"], key="det_stat")
        with fc3:
            kw_f = st.text_input("Cari No HP / Kontrak / Nama", key="det_kw")

        df_show = detail_df.copy()
        if kat_f  != "Semua": df_show = df_show[df_show["Kategori"] == kat_f]
        if stat_f != "Semua": df_show = df_show[df_show["Status Bayar"] == stat_f]
        if kw_f:
            mask = df_show.apply(lambda r: r.astype(str).str.contains(kw_f, case=False, na=False)).any(axis=1)
            df_show = df_show[mask]

        st.markdown(f'<p style="font-size:11px;color:#94A3B8;margin-bottom:6px">Menampilkan <b>{len(df_show):,}</b> dari <b>{len(detail_df):,}</b> sesi</p>', unsafe_allow_html=True)
        st.dataframe(df_show, use_container_width=True, height=450)

        st.download_button(
            "Download Excel",
            to_xlsx(df_show),
            f"detail_kontrak_{sel_month.replace(' ','_')}.xlsx",
            "application/vnd.ms-excel"
        )


# ═══════════════════════════════════════════════════════════
# TAB 4 — ANALISIS TEKS (regex)
# ═══════════════════════════════════════════════════════════
if has_conv and "Analisis Teks" in ti:
    with tab_objs[ti["Analisis Teks"]]:

        at_df = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and at_df["_date"].notna().any():
            at_df = at_df[at_df["_date"].dt.strftime("%B %Y") == sel_month]
        at_text = at_df[at_df["_type"] == "text"]["_msg"].dropna().astype(str)
        total_text = len(at_text)

        st.markdown(f'<div class="info-box">Menganalisis <b>{total_text:,}</b> pesan teks bebas (type = text) dari Conversation.</div>', unsafe_allow_html=True)

        NOMINAL_PATS = [
            (r"rp\.?\s*(\d[\d\.,]+)",      "Rp nominal"),
            (r"(\d[\d\.,]+)\s*(?:ribu|rb)", "X ribu/rb"),
            (r"(\d[\d\.,]+)\s*(?:juta|jt)", "X juta/jt"),
            (r"(\d[\d\.,]+)\s*k\b",         "Xk"),
        ]
        TANGGAL_PATS = [
            (r"\b(besok|esok)\b",                          "Besok"),
            (r"\b(lusa)\b",                                "Lusa"),
            (r"\b(hari\s*ini|skrg|sekarang)\b",            "Hari ini"),
            (r"\b(minggu\s*dep[ae]n)\b",                   "Minggu depan"),
            (r"\b(senin|selasa|rabu|kamis|jumat|sabtu)\b", "Nama hari"),
            (r"\btanggal\s*(\d{1,2})\b",                   "Tanggal X"),
            (r"\btgl\s*(\d{1,2})\b",                       "Tgl X"),
        ]
        KATEGORI_PATS = [
            (r"\b(sudah|udah)\s*(bayar|transfer|tf)\b",       "Konfirmasi Bayar"),
            (r"\b(sudah\s*lunas|lunas)\b",                     "Klaim Lunas"),
            (r"\b(bukti|struk|screenshot)\b",                  "Kirim Bukti"),
            (r"\b(janji|akan|mau)\s*(bayar|transfer)\b",       "Janji Bayar"),
            (r"\b(tidak\s*bisa|gabisa|belum\s*bisa)\b",        "Tidak Bisa Bayar"),
            (r"\b(cicil|nyicil|dicicil)\b",                    "Minta Cicil"),
            (r"\b(nego|denda|keringanan|restruktur)\b",        "Nego/Restruktur"),
            (r"\b(salah\s*nomor|bukan\s*saya|wrong\s*number)\b","Salah Nomor"),
            (r"\b(stop|jangan|hapus|unsubscribe)\b",           "Minta Stop"),
            (r"\b(sudah\s*lunas|lunas)\b",                     "Klaim Lunas"),
        ]

        def count_pats(series, pats):
            return {lbl: int(series.str.contains(p, case=False, regex=True, na=False).sum())
                    for p, lbl in pats if series.str.contains(p, case=False, regex=True, na=False).sum() > 0}

        def bar_html(d, total, colors):
            if not d: return '<p style="color:#94A3B8;font-size:12px">Tidak ada pola ditemukan.</p>'
            out = ""
            for i,(lbl,cnt) in enumerate(sorted(d.items(),key=lambda x:-x[1])):
                pv = cnt/total if total else 0
                c  = colors[i%len(colors)]
                out += (f'<div class="brow"><div class="blbl">{lbl[:26]}</div>'
                        f'<div class="btrk"><div class="bfil" style="width:{pv*100:.1f}%;background:{c}">'
                        f'<span class="bnum">{cnt:,}</span></div></div>'
                        f'<div class="bpct">{pv:.1%}</div></div>')
            return out

        CA = ["#2563EB","#3B82F6","#60A5FA","#93C5FD"]
        CB = ["#0F766E","#14B8A6","#2DD4BF"]
        CC = ["#7C3AED","#15803D","#DC2626","#D97706","#0891B2","#DB2777","#475569","#B45309","#0E7490","#65A30D","#9333EA","#1D4ED8"]

        nom_d = count_pats(at_text, NOMINAL_PATS)
        tgl_d = count_pats(at_text, TANGGAL_PATS)
        kat_d = count_pats(at_text, KATEGORI_PATS)

        st.markdown('<p class="sh">Deteksi Nominal Uang</p>', unsafe_allow_html=True)
        col_n1, col_n2 = st.columns([3,2])
        with col_n1:
            st.markdown(f'<div class="card">{bar_html(nom_d, total_text, CA)}</div>', unsafe_allow_html=True)
        with col_n2:
            # Statistik nominal
            all_nom = []
            for msg in at_text:
                for p, _ in NOMINAL_PATS:
                    for m in _re.finditer(p, msg.lower()):
                        try:
                            v = int(m.group(1).replace(".","").replace(",",""))
                            if "ribu" in p or "rb" in p: v *= 1000
                            elif "juta" in p or "jt" in p: v *= 1_000_000
                            elif r"\bk\b" in p: v *= 1000
                            if 1000 <= v <= 500_000_000: all_nom.append(v)
                        except: pass
            if all_nom:
                arr = np.array(all_nom)
                st.markdown(f'''<div class="card">
                  <p class="sh" style="margin-bottom:8px">Statistik Nominal</p>
                  <table class="t">
                    <tr><td class="left">Jumlah deteksi</td><td style="font-weight:700;color:#1D4ED8">{len(arr):,}</td></tr>
                    <tr><td class="left">Median</td><td style="font-weight:700">Rp {int(np.median(arr)):,}</td></tr>
                    <tr><td class="left">Rata-rata</td><td style="font-weight:700">Rp {int(np.mean(arr)):,}</td></tr>
                    <tr><td class="left">Terkecil</td><td style="font-weight:700">Rp {int(arr.min()):,}</td></tr>
                    <tr><td class="left">Terbesar</td><td style="font-weight:700">Rp {int(arr.max()):,}</td></tr>
                  </table></div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Deteksi Tanggal / Waktu Janji</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="card">{bar_html(tgl_d, total_text, CB)}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Klasifikasi Kategori via Regex</p>', unsafe_allow_html=True)
        ka1, ka2 = st.columns([3,2])
        with ka1:
            st.markdown(f'<div class="card">{bar_html(kat_d, total_text, CC)}</div>', unsafe_allow_html=True)
        with ka2:
            if kat_d:
                fig_pie = go.Figure(go.Pie(
                    labels=list(kat_d.keys()), values=list(kat_d.values()),
                    hole=0.45, textinfo="percent",
                    marker=dict(colors=CC[:len(kat_d)]),
                ))
                fig_pie.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter",color="#64748B",size=10),
                    legend=dict(font=dict(size=9),bgcolor="rgba(0,0,0,0)"))
                st.plotly_chart(fig_pie, use_container_width=True)

        # Custom regex
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Custom Regex</p>', unsafe_allow_html=True)
        cr1, cr2 = st.columns([4,1])
        with cr1: custom_pat = st.text_input("Pattern:", placeholder=r"contoh: \btransfer\b", key="cust_regex")
        with cr2: case_s = st.checkbox("Case sensitive", value=False, key="cust_case")
        if custom_pat:
            try:
                flags = 0 if case_s else _re.IGNORECASE
                matched = at_text[at_text.str.contains(custom_pat, flags=flags, regex=True, na=False)]
                st.markdown(f'<p style="font-size:12px;color:#15803D;font-weight:600">Ditemukan di <b>{len(matched):,}</b> pesan ({pct(len(matched),total_text)} dari teks bebas)</p>', unsafe_allow_html=True)
                if len(matched):
                    vc = matched.value_counts().head(30).reset_index()
                    vc.columns = ["Pesan","Jumlah"]
                    st.dataframe(vc, use_container_width=True, height=300)
            except _re.error as e:
                st.error(f"Regex tidak valid: {e}")


# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<p style="text-align:center;font-size:11px;color:#94A3B8">'
    'Dashboard WA Broadcast + Realisasi Bayar - PT. BCA Finance - ASR Mobil</p>',
    unsafe_allow_html=True
)
