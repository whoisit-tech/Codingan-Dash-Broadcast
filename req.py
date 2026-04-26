import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import io
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="WA Broadcast + Realisasi Bayar", page_icon="📲", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #F1F5F9; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 1400px; }

section[data-testid="stFileUploader"] { background:#fff; border-radius:10px; padding:12px 16px; border:1px solid #E2E8F0; }

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

/* Realisasi bayar cards */
.real-card { border-radius:10px; padding:18px; border:1.5px solid; margin-bottom:12px; }
.real-title { font-size:13px; font-weight:700; margin-bottom:6px; }
.real-num { font-size:28px; font-weight:800; margin-bottom:2px; }
.real-sub { font-size:11px; opacity:.75; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="background:#1E3A5F;border-radius:10px;padding:16px 24px;margin-bottom:18px;
            display:flex;justify-content:space-between;align-items:center">
  <div>
    <span style="font-size:18px;font-weight:700;color:#fff">📲 WA Broadcast + Realisasi Bayar</span>
    <span style="font-size:12px;color:rgba(255,255,255,.65);margin-left:14px">PT. BCA Finance · ASR Mobil</span>
  </div>
  <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600">
    Dashboard Terintegrasi
  </span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# UPLOAD SECTION
# ═══════════════════════════════════════════════════════════
st.markdown("### 📂 Upload File")
u1, u2, u3, u4 = st.columns(4)
with u1:
    f_sum  = st.file_uploader("📊 Summary CSV (Broadcast)", type="csv",
                               help="Kolom: DateUploaded, Sent, Delivered, Read, Failed, Total")
with u2:
    f_conv = st.file_uploader("💬 Conversation CSV (Response WA)", type="csv",
                               help="Kolom: Origin, Message Type, Message, Session, Created At, dst")
with u3:
    f_sc   = st.file_uploader("📋 File SC Excel (Jan–Mar)", type=["xlsx","xls"],
                               help="Sheet: Sc Januari, Sc Februari, Sc Maret")
with u4:
    f_rekap = st.file_uploader("💳 Rekap WAI 4W (Excel/CSV)", type=["xlsx","xls","csv"],
                                help="File rekap pembayaran, kolom No WA & Tgl Bayar")

# Check what's available
has_broadcast = f_sum is not None
has_conv      = f_conv is not None
has_sc        = f_sc is not None
has_rekap     = f_rekap is not None
has_realisasi = has_conv and (has_sc or has_rekap)

if not has_broadcast:
    st.markdown('<div class="info-box">⬆ Upload minimal <b>Summary CSV</b> untuk memulai dashboard. File lain opsional untuk fitur tambahan.</div>', unsafe_allow_html=True)
    st.stop()

st.markdown("---")


# ═══════════════════════════════════════════════════════════
# SIDEBAR CONFIG
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Konfigurasi Kolom")
    st.markdown("**Conversation CSV**")
    col_phone_conv  = st.text_input("Kolom No HP di Conversation", value="Contact",
                                     help="Kolom yang berisi no telpon nasabah di conversation CSV")
    col_origin      = st.text_input("Kolom Origin (IN/OUT)", value="Origin")
    col_msg_type    = st.text_input("Kolom Message Type", value="Message Type")
    col_msg         = st.text_input("Kolom Message / Isi Pesan", value="Message")
    col_session     = st.text_input("Kolom Session ID", value="Session")
    col_created     = st.text_input("Kolom Created At", value="Created At")

    st.markdown("---")
    st.markdown("**SC Excel**")
    col_nokontrak_sc = st.text_input("Kolom No Kontrak (SC)", value="NOKONTRAK")
    col_phone_sc     = st.text_input("Kolom No HP (SC)", value="nohp",
                                      help="Kolom no HP di SC, untuk join ke conversation")
    col_lastpaid     = st.text_input("Kolom Last Paid Date (SC)", value="lastpaiddate")
    col_ospokok      = st.text_input("Kolom OS Pokok (SC)", value="ospokok")
    col_osar         = st.text_input("Kolom OS AR (SC)", value="osar")
    col_custname     = st.text_input("Kolom Nama (SC)", value="custname")
    col_branch       = st.text_input("Kolom Cabang (SC)", value="branchname")

    st.markdown("---")
    st.markdown("**Rekap WAI**")
    col_phone_rekap  = st.text_input("Kolom No HP (Rekap)", value="no_wa",
                                      help="Kolom no HP di rekap WAI, untuk join ke conversation")
    col_nokontrak_rek = st.text_input("Kolom No Kontrak (Rekap)", value="body_param_2")
    col_tglbayar_rek  = st.text_input("Kolom Tgl Bayar (Rekap)", value="TGL BAYAR")

    st.markdown("---")
    st.markdown("**Label Response (untuk klasifikasi)**")
    st.markdown('<p style="font-size:11px;color:#64748B">Kata kunci di isi pesan untuk klasifikasi response nasabah</p>', unsafe_allow_html=True)
    kw_janji   = st.text_input("Kata kunci Janji Bayar", value="janji,bayar nanti,akan bayar,besok bayar")
    kw_sudah   = st.text_input("Kata kunci Sudah Bayar", value="sudah bayar,udah bayar,transfer,tadi bayar")
    kw_hubungi = st.text_input("Kata kunci Hubungi Kami", value="hubungi,kontak,cs,call center")
    kw_nopush  = st.text_input("Kata kunci No Push/Tidak Mau", value="tidak bisa,belum bisa,jangan,stop,unsubscribe")


# ═══════════════════════════════════════════════════════════
# LOAD & PARSE FUNCTIONS
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_summary(raw):
    txt   = raw.decode("utf-8-sig")
    delim = ";" if txt.count(";") > txt.count(",") else ","
    df    = pd.read_csv(io.StringIO(txt), delimiter=delim)
    df.columns = [c.strip() for c in df.columns]
    dcol = next((c for c in df.columns if "date" in c.lower()), df.columns[0])
    for fmt in ["%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            df["Date"] = pd.to_datetime(df[dcol].astype(str).str.split().str[0], format=fmt.split()[0])
            break
        except:
            pass
    for c in ["Sent","Delivered","Read","Failed","Canceled","Total"]:
        df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0).astype(int)
    df["Undelivered"] = (df["Sent"] - df["Delivered"]).clip(0)
    df["Unread"]      = (df["Delivered"] - df["Read"]).clip(0)
    df["Month"]       = df["Date"].dt.strftime("%B %Y")
    df["MonthSort"]   = df["Date"].dt.year * 100 + df["Date"].dt.month
    return df.sort_values("Date").reset_index(drop=True)


@st.cache_data
def load_conv(raw, col_phone, col_origin, col_msg_type, col_msg, col_session, col_created):
    txt   = raw.decode("utf-8-sig")
    delim = ";" if txt.count(";") > txt.count(",") else ","
    df    = pd.read_csv(io.StringIO(txt), delimiter=delim)
    df.columns = [c.strip() for c in df.columns]

    def find(kw, exact=False):
        if exact:
            return next((c for c in df.columns if c.strip().lower() == kw.lower()), None)
        return next((c for c in df.columns if kw.lower() in c.strip().lower()), None)

    # Flexible col detection - use config first, then fallback
    phone_col   = find(col_phone, exact=True) or find(col_phone) or find("contact") or find("phone") or find("no_hp") or find("nohp")
    origin_col  = find(col_origin, exact=True) or find("origin")
    type_col    = find(col_msg_type, exact=True) or find("message type") or find("type")
    msg_col_det = find(col_msg, exact=True) or next(
        (c for c in df.columns if "message" in c.strip().lower() and "id" not in c.strip().lower()), None)
    sess_col    = find(col_session, exact=True) or find("session")
    date_col    = find(col_created, exact=True) or find("created")

    df["_phone"] = df[phone_col].astype(str).str.strip().str.replace(r'\D','',regex=True) if phone_col else ""
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
    xls = pd.ExcelFile(raw)
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
def load_rekap(raw, fname):
    if fname.endswith(".csv"):
        txt   = raw.decode("utf-8-sig")
        delim = ";" if txt.count(";") > txt.count(",") else ","
        df    = pd.read_csv(io.StringIO(txt), delimiter=delim)
    else:
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
    """Normalize phone number to standard format"""
    s = str(s).strip()
    s = ''.join(filter(str.isdigit, s))
    if s.startswith("0"):
        s = "62" + s[1:]
    elif s.startswith("8"):
        s = "62" + s
    return s


def classify_response(msg, kw_janji, kw_sudah, kw_hubungi, kw_nopush):
    """Classify message into response category"""
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
df = load_summary(f_sum.read())

conv, phone_col_detected = None, None
if has_conv:
    conv, phone_col_detected = load_conv(
        f_conv.read(),
        col_phone_conv, col_origin, col_msg_type, col_msg, col_session, col_created
    )

df_sc = None
if has_sc:
    df_sc = load_sc(f_sc.read())

df_rekap = None
if has_rekap:
    df_rekap = load_rekap(f_rekap.read(), f_rekap.name)


# ═══════════════════════════════════════════════════════════
# FILTER BULAN
# ═══════════════════════════════════════════════════════════
months_avail = sorted(df["Month"].unique(), key=lambda m: df[df["Month"]==m]["MonthSort"].iloc[0])
sel_month = st.selectbox("📅 Filter Bulan", ["Semua Bulan"] + months_avail)

dff = df if sel_month == "Semua Bulan" else df[df["Month"] == sel_month]

T  = int(dff["Total"].sum())
S  = int(dff["Sent"].sum())
D  = int(dff["Delivered"].sum())
R  = int(dff["Read"].sum())
F  = int(dff["Failed"].sum())
UD = int(dff["Undelivered"].sum())
UR = int(dff["Unread"].sum())

def pct(a, b): return f"{a/b:.1%}" if b else "0%"
def pct_val(a, b): return a/b if b else 0


# ═══════════════════════════════════════════════════════════
# HEADER STRIP
# ═══════════════════════════════════════════════════════════
period = f"{dff['Date'].min().strftime('%d %b %Y')} – {dff['Date'].max().strftime('%d %b %Y')}"
st.markdown(f"""
<div style="background:#1E3A5F;border-radius:10px;padding:16px 24px;margin-bottom:18px;
            display:flex;justify-content:space-between;align-items:center">
  <div>
    <span style="font-size:18px;font-weight:700;color:#fff">📲 WA Broadcast — </span>
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
  {mbox("📦 Data Upload", T, "100%", "#1E293B", "#F8FAFC", "#CBD5E1")}
</div>
""", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca: st.markdown(mbox("❌ Failed Broadcast", F, f"{pct(F,T)} dari upload", "#B91C1C", "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
with cb: st.markdown(mbox("✅ Success Broadcast", S, f"{pct(S,T)} dari upload", "#15803D", "#F0FDF4", "#86EFAC"), unsafe_allow_html=True)

ca2, cb2 = st.columns(2)
with ca2: st.markdown(mbox("📬 Delivered", D, f"{pct(D,T)} dari upload", "#1D4ED8", "#EFF6FF", "#93C5FD"), unsafe_allow_html=True)
with cb2: st.markdown(mbox("📤 Sent (Belum Delivered)", UD, f"{pct(UD,T)} dari upload", "#D97706", "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

ca3, cb3 = st.columns(2)
with ca3: st.markdown(mbox("👁 Read", R, f"{pct(R,D)} dari delivered", "#0E7490", "#ECFEFF", "#67E8F9"), unsafe_allow_html=True)
with cb3: st.markdown(mbox("📭 Unread", UR, f"{pct(UR,D)} dari delivered", "#7C3AED", "#FAF5FF", "#C4B5FD"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# BUILD TABS
# ═══════════════════════════════════════════════════════════
tab_labels = ["📊 Rekap Upload"]
if conv is not None:
    tab_labels.append("💬 Response WA")
    tab_labels.append("📝 Isi Pesan")
if has_realisasi:
    tab_labels.append("🎯 Realisasi Bayar")

tab_objs = st.tabs(tab_labels)
tab_idx = {label: i for i, label in enumerate(tab_labels)}


# ═══════════════════════════════════════════════════════════
# TAB 1 — REKAP UPLOAD
# ═══════════════════════════════════════════════════════════
with tab_objs[tab_idx["📊 Rekap Upload"]]:
    st.markdown('<p class="sh">Detail per Batch Upload</p>', unsafe_allow_html=True)

    rows_html = ""
    for _, r in dff.iterrows():
        fp = r["Failed"]/r["Total"] if r["Total"] else 0
        dp = r["Delivered"]/r["Total"] if r["Total"] else 0
        rp = r["Read"]/r["Delivered"] if r["Delivered"] else 0

        def p(v, hi, lo, inv=False):
            if inv: cls = "g" if v<hi else "r" if v>lo else "o"
            else:   cls = "g" if v>hi else "r" if v<lo else "o"
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

    fp_t=F/T if T else 0; dp_t=D/T if T else 0; rp_t=R/D if D else 0
    def p_t(v, hi, lo, inv=False):
        if inv: cls = "g" if v<hi else "r" if v>lo else "o"
        else:   cls = "g" if v>hi else "r" if v<lo else "o"
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
    Fail% & Del% dihitung dari Total Upload · Read% dihitung dari Delivered</p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Tren per Batch</p>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dff["Date"], y=dff["Total"], name="Total", marker_color="#E2E8F0", opacity=0.8))
    for m, c, d in [("Delivered","#2563EB",None),("Read","#0891B2","dot"),("Failed","#DC2626",None)]:
        fig.add_trace(go.Scatter(x=dff["Date"], y=dff[m], name=m,
            line=dict(color=c, width=2, dash=d or "solid"), mode="lines+markers",
            marker=dict(size=5, color=c)))
    fig.update_layout(barmode="overlay", height=280, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
        font=dict(family="Inter", color="#64748B"),
        legend=dict(orientation="h", y=-0.25, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#E2E8F0", tickformat="%d %b"),
        yaxis=dict(gridcolor="#E2E8F0"), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    if sel_month == "Semua Bulan":
        st.markdown('<p class="sh">Rekap per Bulan</p>', unsafe_allow_html=True)
        monthly = df.groupby(["Month","MonthSort"]).agg(
            Total=("Total","sum"), Sent=("Sent","sum"), Delivered=("Delivered","sum"),
            Read=("Read","sum"), Failed=("Failed","sum"), Unread=("Unread","sum"), Uploads=("Date","count")
        ).reset_index().sort_values("MonthSort")

        m_rows = ""
        for _, r in monthly.iterrows():
            fp = r["Failed"]/r["Total"] if r["Total"] else 0
            dp = r["Delivered"]/r["Total"] if r["Total"] else 0
            rp = r["Read"]/r["Delivered"] if r["Delivered"] else 0
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
if conv is not None and "💬 Response WA" in tab_idx:
    with tab_objs[tab_idx["💬 Response WA"]]:
        cdf = conv.copy()
        if sel_month != "Semua Bulan" and cdf["_date"].notna().any():
            cdf = cdf[cdf["_date"].dt.strftime("%B %Y") == sel_month]

        in_df  = cdf[cdf["_orig"] == "IN"]
        btn_df = in_df[in_df["_type"].isin(["button","button_reply"])]
        total_sessions = cdf["_sess"].nunique()

        s1,s2,s3,s4 = st.columns(4)
        for col_obj, lbl, val, fg, bg, bd in [
            (s1, "Total Sesi",     total_sessions,      "#1D4ED8","#EFF6FF","#93C5FD"),
            (s2, "Pesan Masuk",    len(in_df),          "#15803D","#F0FDF4","#86EFAC"),
            (s3, "Button Replies", len(btn_df),         "#D97706","#FFFBEB","#FDE68A"),
            (s4, "Teks Bebas",     len(in_df[in_df["_type"]=="text"]), "#7C3AED","#FAF5FF","#C4B5FD"),
        ]:
            with col_obj:
                st.markdown(f"""<div class="mbox" style="background:{bg};border-color:{bd};color:{fg}">
                  <div class="mbox-lbl">{lbl}</div>
                  <div class="mbox-val">{val:,}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        mt_lbl = {
            "text":"Teks bebas","button":"Klik tombol","button_reply":"Balasan tombol",
            "list_reply":"Pilihan menu","image":"Foto","document":"Dokumen",
            "audio":"Pesan suara","reaction":"Emoji","sticker":"Sticker","unsupported":"Tidak didukung",
        }
        available_types = sorted(in_df["_type"].dropna().unique().tolist())
        type_options    = ["Semua Type"] + available_types
        type_labels     = ["Semua Type"] + [f"{t} — {mt_lbl.get(t, t)}" for t in available_types]

        st.markdown('<p class="sh">Filter Message Type</p>', unsafe_allow_html=True)
        sel_type_label = st.radio("Pilih tipe pesan:", options=type_labels, index=0,
                                   horizontal=True, label_visibility="collapsed")
        sel_type = type_options[type_labels.index(sel_type_label)]
        filtered_in_df = in_df if sel_type == "Semua Type" else in_df[in_df["_type"] == sel_type]

        st.markdown("<br>", unsafe_allow_html=True)
        cl, cr = st.columns([3,2])

        with cl:
            filter_label = "" if sel_type == "Semua Type" else f" &nbsp;<span style='font-size:10px;background:#DBEAFE;color:#1D4ED8;padding:2px 8px;border-radius:10px'>{sel_type}</span>"
            st.markdown(f'<p class="sh">Button Responses{filter_label}</p>', unsafe_allow_html=True)
            btn_counts = filtered_in_df["_msg"].value_counts().reset_index()
            btn_counts.columns = ["Pesan","Jumlah"]
            total_btn = int(btn_counts["Jumlah"].sum())

            if total_btn == 0:
                st.info("Tidak ada pesan di tipe & periode ini.")
            else:
                colors = ["#15803D","#1D4ED8","#DC2626","#7C3AED","#D97706","#DB2777","#0891B2"]
                bars = ""
                for i, row in btn_counts.iterrows():
                    p_val = row["Jumlah"] / total_btn
                    c = colors[i % len(colors)]
                    bars += f"""<div class="brow">
                      <div class="blbl" title="{row['Pesan']}">{str(row['Pesan'])[:26]}{"..." if len(str(row['Pesan']))>26 else ""}</div>
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
            mt.columns = ["Type","Jumlah"]
            total_mt = int(mt["Jumlah"].sum())
            mt_rows = ""
            for _, row in mt.iterrows():
                is_sel  = (sel_type != "Semua Type" and row["Type"] == sel_type)
                row_sty = "background:#EFF6FF;font-weight:700;" if is_sel else ""
                mt_rows += f"""<tr style="{row_sty}">
                  <td class="left">{row['Type']}{' ◀' if is_sel else ''}</td>
                  <td style="font-weight:600">{int(row['Jumlah']):,}</td>
                  <td><span class="pill {'b' if is_sel else 's'}">{row['Jumlah']/total_mt:.1%}</span></td>
                  <td class="left" style="color:#94A3B8;font-size:11px">{mt_lbl.get(row['Type'],'')}</td>
                </tr>"""
            st.markdown(f"""<table class="t"><thead><tr>
              <th class="left">Type</th><th>Jumlah</th><th>%</th><th class="left">Keterangan</th>
            </tr></thead><tbody>{mt_rows}</tbody></table>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — ISI PESAN
# ═══════════════════════════════════════════════════════════
if conv is not None and "📝 Isi Pesan" in tab_idx:
    with tab_objs[tab_idx["📝 Isi Pesan"]]:
        cdf2 = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf2["_date"].notna().any():
            cdf2 = cdf2[cdf2["_date"].dt.strftime("%B %Y") == sel_month]

        total_in = len(cdf2)
        st.markdown('<p class="sh">Breakdown Isi Pesan dari Nasabah</p>', unsafe_allow_html=True)

        msg_counts = (cdf2[cdf2["_msg"].str.strip() != ""]["_msg"]
                      .str.strip().value_counts().reset_index())
        msg_counts.columns = ["Pesan","Jumlah"]
        total_msg = int(msg_counts["Jumlah"].sum())

        colors_bar = ["#15803D","#1D4ED8","#DC2626","#7C3AED","#D97706","#DB2777","#0891B2","#0F766E","#9333EA","#B45309"]
        bars_html = ""
        for i, row in msg_counts.iterrows():
            pv  = row["Jumlah"] / total_msg if total_msg else 0
            clr = colors_bar[i % len(colors_bar)]
            bars_html += f"""<div class="brow">
              <div class="blbl" title="{row['Pesan']}">{str(row['Pesan'])[:28]}{"…" if len(str(row['Pesan']))>28 else ""}</div>
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
        with fc1: kw = st.text_input("🔍 Cari isi pesan", placeholder="contoh: bayar, angsuran, denda...")
        with fc2: n_rows = st.number_input("Maks baris", 20, 500, 100, 10)

        tbl_df = msg_counts.copy()
        if kw: tbl_df = tbl_df[tbl_df["Pesan"].str.contains(kw, case=False, na=False)]
        tbl_df = tbl_df.head(n_rows)

        tbl_rows = ""
        for i, row in tbl_df.iterrows():
            pv  = row["Jumlah"] / total_msg if total_msg else 0
            bar = f'<div style="background:#E2E8F0;border-radius:4px;height:10px;overflow:hidden"><div style="width:{pv*100:.1f}%;height:100%;background:#2563EB;border-radius:4px"></div></div>'
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
# TAB 4 — REALISASI BAYAR ⭐ (TAB BARU)
# ═══════════════════════════════════════════════════════════
if has_realisasi and "🎯 Realisasi Bayar" in tab_idx:
    with tab_objs[tab_idx["🎯 Realisasi Bayar"]]:

        st.markdown("""
        <div class="info-box">
        🎯 <b>Cara kerja tab ini:</b> Nasabah yang merespons WA (Conversation CSV) di-join dengan data SC/Rekap via <b>No HP</b>.
        Dari situ ketauan yang klik "Janji Bayar" / "Sudah Bayar" dll, beneran bayar atau ngga berdasarkan <b>lastpaiddate</b> di SC atau <b>Tgl Bayar</b> di Rekap WAI.
        </div>
        """, unsafe_allow_html=True)

        # ── Filter conversation by month ──
        cdf_real = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf_real["_date"].notna().any():
            cdf_real = cdf_real[cdf_real["_date"].dt.strftime("%B %Y") == sel_month]

        # ── Normalize phone in conversation ──
        cdf_real["_phone_norm"] = cdf_real["_phone"].apply(normalize_phone)

        # ── Classify response per session ──
        # Take the "representative" message per session (first button/text IN)
        sess_grp = cdf_real.sort_values("_date").groupby("_sess").first().reset_index()
        sess_grp["_kategori"] = sess_grp["_msg"].apply(
            lambda m: classify_response(m, kw_janji, kw_sudah, kw_hubungi, kw_nopush)
        )

        # Also aggregate all messages per session for better classification
        sess_msgs = cdf_real.groupby("_sess")["_msg"].apply(lambda x: " ".join(x.dropna())).reset_index()
        sess_msgs.columns = ["_sess","_all_msgs"]
        sess_grp = sess_grp.merge(sess_msgs, on="_sess", how="left")
        sess_grp["_kategori"] = sess_grp["_all_msgs"].apply(
            lambda m: classify_response(m, kw_janji, kw_sudah, kw_hubungi, kw_nopush)
        )

        # ── Build lookup table: phone → paid status ──
        paid_lookup = {}   # {normalized_phone: {"bayar": bool, "tgl": ..., "nokontrak": ..., "nama": ...}}

        if df_sc is not None:
            sc_phone_col = find_col(df_sc, [col_phone_sc, "nohp", "NoHP", "no_hp", "HP", "hp"])
            sc_paid_col  = find_col(df_sc, [col_lastpaid, "lastpaiddate", "LastPaidDate"])
            sc_nok_col   = find_col(df_sc, [col_nokontrak_sc, "NOKONTRAK", "nokontrak"])
            sc_nama_col  = find_col(df_sc, [col_custname, "custname", "CustName", "nama"])

            if sc_phone_col:
                for _, row in df_sc.iterrows():
                    raw_phone = str(row.get(sc_phone_col, "")).strip()
                    norm = normalize_phone(raw_phone)
                    if not norm or norm == "62":
                        continue
                    lp = row.get(sc_paid_col) if sc_paid_col else None
                    bayar = pd.notna(lp) and str(lp).strip() not in ["", "nan", "NaT", "None", "0"]
                    paid_lookup[norm] = {
                        "bayar": bayar,
                        "tgl_bayar": str(lp) if bayar else None,
                        "nokontrak": str(row.get(sc_nok_col, "")) if sc_nok_col else "",
                        "nama": str(row.get(sc_nama_col, "")) if sc_nama_col else "",
                        "source": "SC"
                    }
            else:
                st.markdown(f'<div class="warn-box">⚠️ Kolom No HP tidak ditemukan di SC (dicari: <b>{col_phone_sc}</b>). Kolom tersedia: {", ".join(df_sc.columns[:15].tolist())}</div>', unsafe_allow_html=True)

        if df_rekap is not None:
            rek_phone_col  = find_col(df_rekap, [col_phone_rekap, "no_wa", "NoWA", "nowa", "hp", "nohp"])
            rek_paid_col   = find_col(df_rekap, [col_tglbayar_rek, "TGL BAYAR", "tgl_bayar"])
            rek_nok_col    = find_col(df_rekap, [col_nokontrak_rek, "NOKONTRAK", "body_param_2", "body_param_1"])

            if rek_phone_col:
                for _, row in df_rekap.iterrows():
                    raw_phone = str(row.get(rek_phone_col, "")).strip()
                    norm = normalize_phone(raw_phone)
                    if not norm or norm == "62":
                        continue
                    lp = row.get(rek_paid_col) if rek_paid_col else None
                    bayar = pd.notna(lp) and str(lp).strip() not in ["", "nan", "NaT", "None", "0"]
                    # Rekap overrides only if not already marked as paid from SC
                    if norm not in paid_lookup or (bayar and not paid_lookup[norm]["bayar"]):
                        paid_lookup[norm] = {
                            "bayar": bayar,
                            "tgl_bayar": str(lp) if bayar else None,
                            "nokontrak": str(row.get(rek_nok_col, "")) if rek_nok_col else "",
                            "nama": "",
                            "source": "Rekap WAI"
                        }
            else:
                st.markdown(f'<div class="warn-box">⚠️ Kolom No HP tidak ditemukan di Rekap (dicari: <b>{col_phone_rekap}</b>). Kolom tersedia: {", ".join(df_rekap.columns[:15].tolist())}</div>', unsafe_allow_html=True)

        # ── Join session data with paid status ──
        def get_paid_info(phone_norm):
            return paid_lookup.get(phone_norm, {"bayar": None, "tgl_bayar": None, "nokontrak": "", "nama": "", "source": "Tidak Ditemukan"})

        sess_grp["_paid_info"]  = sess_grp["_phone_norm"].apply(get_paid_info)
        sess_grp["_bayar"]      = sess_grp["_paid_info"].apply(lambda x: x["bayar"])
        sess_grp["_tgl_bayar"]  = sess_grp["_paid_info"].apply(lambda x: x["tgl_bayar"])
        sess_grp["_nokontrak"]  = sess_grp["_paid_info"].apply(lambda x: x["nokontrak"])
        sess_grp["_nama"]       = sess_grp["_paid_info"].apply(lambda x: x["nama"])
        sess_grp["_datasource"] = sess_grp["_paid_info"].apply(lambda x: x["source"])

        # ── Summary stats ──
        total_resp      = len(sess_grp)
        found_in_db     = sess_grp["_bayar"].notna().sum()
        not_found       = sess_grp["_bayar"].isna().sum()

        st.markdown('<p class="sh">📊 Ringkasan Realisasi per Kategori Response</p>', unsafe_allow_html=True)

        KATEGORI_ORDER = ["Janji Bayar", "Sudah Bayar", "Hubungi Kami", "No Push", "Lainnya"]
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
            total_kat     = len(grp)
            if total_kat == 0:
                continue
            found_kat     = grp["_bayar"].notna().sum()
            bayar_kat     = grp["_bayar"].eq(True).sum()
            belum_kat     = grp["_bayar"].eq(False).sum()
            unknown_kat   = grp["_bayar"].isna().sum()
            real_pct      = bayar_kat / found_kat if found_kat else 0
            fg, bg, bd    = KATEGORI_COLORS.get(kat, ("#475569","#F1F5F9","#CBD5E1"))

            summary_data.append({
                "Kategori": kat, "Total Respons": total_kat,
                "Ada di DB": found_kat, "Sudah Bayar": bayar_kat,
                "Belum Bayar": belum_kat, "Tidak Ditemukan": unknown_kat,
                "Realisasi %": real_pct
            })

            pct_bar = f'<div style="background:#E2E8F0;border-radius:4px;height:8px;overflow:hidden"><div style="width:{real_pct*100:.1f}%;height:100%;background:{fg};border-radius:4px"></div></div>'
            pill_bayar  = f'<span class="pill g">{bayar_kat:,} bayar</span>'
            pill_belum  = f'<span class="pill r">{belum_kat:,} belum</span>'
            pill_unk    = f'<span class="pill s">{unknown_kat:,} N/A</span>'

            realisasi_rows += f"""<tr>
              <td class="left"><span style="font-weight:700;color:{fg}">{kat}</span></td>
              <td style="font-weight:700">{total_kat:,}</td>
              <td>{found_kat:,}</td>
              <td>{pill_bayar}</td>
              <td>{pill_belum}</td>
              <td>{pill_unk}</td>
              <td style="min-width:100px">
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
          <th>Sudah Bayar </th>
          <th>Belum Bayar </th>
          <th>Tdk Ditemukan </th>
          <th style="min-width:160px">Realisasi %</th>
        </tr></thead><tbody>{realisasi_rows}</tbody></table>
        </div>
        <p style="font-size:10px;color:#94A3B8;margin-top:6px">
        Realisasi % = Sudah Bayar / (Sudah Bayar + Belum Bayar) · tidak termasuk yg tidak ditemukan di DB</p>
        """, unsafe_allow_html=True)

        # ── Visual cards summary ──
        if summary_data:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="sh"> Highlight Realisasi</p>', unsafe_allow_html=True)

            janji_row = next((x for x in summary_data if x["Kategori"] == "Janji Bayar"), None)
            sudah_row = next((x for x in summary_data if x["Kategori"] == "Sudah Bayar"), None)

            hc1, hc2, hc3, hc4 = st.columns(4)
            with hc1:
                val = janji_row["Sudah Bayar"] if janji_row else 0
                tot = janji_row["Ada di DB"] if janji_row else 0
                r   = janji_row["Realisasi %"] if janji_row else 0
                st.markdown(f"""<div class="mbox" style="background:#F0FDF4;border-color:#86EFAC;color:#15803D">
                  <div class="mbox-lbl"> Janji Bayar → Beneran Bayar</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari {tot:,} yg janji</div>
                </div>""", unsafe_allow_html=True)
            with hc2:
                val = janji_row["Belum Bayar"] if janji_row else 0
                tot = janji_row["Ada di DB"] if janji_row else 0
                r   = 1 - janji_row["Realisasi %"] if janji_row else 0
                st.markdown(f"""<div class="mbox" style="background:#FEF2F2;border-color:#FECACA;color:#B91C1C">
                  <div class="mbox-lbl">❌ Janji Bayar → Ingkar Janji</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari yg janji</div>
                </div>""", unsafe_allow_html=True)
            with hc3:
                val = sudah_row["Sudah Bayar"] if sudah_row else 0
                tot = sudah_row["Ada di DB"] if sudah_row else 0
                r   = sudah_row["Realisasi %"] if sudah_row else 0
                st.markdown(f"""<div class="mbox" style="background:#EFF6FF;border-color:#93C5FD;color:#1D4ED8">
                  <div class="mbox-lbl"> Klaim Sudah Bayar → Terverifikasi</div>
                  <div class="mbox-val">{val:,}</div>
                  <div class="mbox-pct">{r:.1%} dari {tot:,} yg klaim</div>
                </div>""", unsafe_allow_html=True)
            with hc4:
                total_bayar_all = sum(x["Sudah Bayar"] for x in summary_data)
                total_ada_db    = sum(x["Ada di DB"] for x in summary_data)
                r_all = total_bayar_all / total_ada_db if total_ada_db else 0
                st.markdown(f"""<div class="mbox" style="background:#F3E8FF;border-color:#C4B5FD;color:#7C3AED">
                  <div class="mbox-lbl"> Overall Realisasi Bayar</div>
                  <div class="mbox-val">{total_bayar_all:,}</div>
                  <div class="mbox-pct">{r_all:.1%} dari {total_ada_db:,} teridentifikasi</div>
                </div>""", unsafe_allow_html=True)

        # ── Funnel Chart ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh"> Funnel Realisasi</p>', unsafe_allow_html=True)

        if summary_data:
            fig2 = go.Figure()
            cats = [x["Kategori"] for x in summary_data]
            bayar_vals = [x["Sudah Bayar"] for x in summary_data]
            belum_vals = [x["Belum Bayar"] for x in summary_data]
            unk_vals   = [x["Tidak Ditemukan"] for x in summary_data]

            fig2.add_trace(go.Bar(name="Sudah Bayar ", x=cats, y=bayar_vals,
                marker_color="#22C55E", text=bayar_vals, textposition="auto"))
            fig2.add_trace(go.Bar(name="Belum Bayar ", x=cats, y=belum_vals,
                marker_color="#EF4444", text=belum_vals, textposition="auto"))
            fig2.add_trace(go.Bar(name="Tidak Ditemukan ", x=cats, y=unk_vals,
                marker_color="#94A3B8", text=unk_vals, textposition="auto"))

            fig2.update_layout(
                barmode="group", height=300, margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
                font=dict(family="Inter", color="#64748B"),
                legend=dict(orientation="h", y=-0.3, bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(gridcolor="#E2E8F0"),
                yaxis=dict(gridcolor="#E2E8F0"),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # ── Detail tabel per nasabah ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh"> Detail per Nasabah</p>', unsafe_allow_html=True)

        kat_filter = st.selectbox("Filter Kategori", ["Semua"] + KATEGORI_ORDER, key="kat_filter_real")
        bayar_filter = st.radio("Filter Status Bayar", ["Semua","Sudah Bayar","Belum Bayar","Tidak Ditemukan"],
                                horizontal=True, key="bayar_filter_real")

        detail_df = sess_grp[[
            "_phone_norm", "_kategori", "_msg", "_bayar", "_tgl_bayar", "_nokontrak", "_nama", "_datasource", "_date"
        ]].copy()
        detail_df.columns = ["No HP", "Kategori Response", "Pesan", "Bayar", "Tgl Bayar", "No Kontrak", "Nama", "Sumber Data", "Tgl Chat"]

        if kat_filter != "Semua":
            detail_df = detail_df[detail_df["Kategori Response"] == kat_filter]
        if bayar_filter == "Sudah Bayar":
            detail_df = detail_df[detail_df["Bayar"] == True]
        elif bayar_filter == "Belum Bayar":
            detail_df = detail_df[detail_df["Bayar"] == False]
        elif bayar_filter == "Tidak Ditemukan":
            detail_df = detail_df[detail_df["Bayar"].isna()]

        detail_df["Status"] = detail_df["Bayar"].apply(
            lambda x: " Sudah Bayar" if x == True else (" Belum Bayar" if x == False else " Tidak Ditemukan")
        )
        detail_df = detail_df.drop(columns=["Bayar"])

        st.markdown(f'<p style="font-size:11px;color:#94A3B8;margin-bottom:8px">Menampilkan <b>{len(detail_df):,}</b> baris</p>', unsafe_allow_html=True)
        st.dataframe(detail_df, use_container_width=True, height=400)

        # ── Export ──
        def export_excel_df(df_out):
            buf = BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                df_out.to_excel(w, index=False, sheet_name="Realisasi")
            return buf.getvalue()

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(" Download Hasil Filter (.xlsx)",
                               export_excel_df(detail_df), "realisasi_filter.xlsx",
                               "application/vnd.ms-excel")
        with dl2:
            full_export = sess_grp[["_phone_norm","_kategori","_msg","_bayar","_tgl_bayar",
                                     "_nokontrak","_nama","_datasource","_date"]].copy()
            full_export.columns = ["No HP","Kategori","Pesan","Bayar","Tgl Bayar","No Kontrak","Nama","Sumber","Tgl Chat"]
            full_export["Status"] = full_export["Bayar"].apply(
                lambda x: "Sudah Bayar" if x == True else ("Belum Bayar" if x == False else "Tidak Ditemukan"))
            st.download_button(" Download Semua Data Realisasi (.xlsx)",
                               export_excel_df(full_export), "realisasi_semua.xlsx",
                               "application/vnd.ms-excel")

        # ── Info coverage ──
        st.markdown(f"""
        <div class="warn-box" style="margin-top:16px">
        <b>Coverage:</b> {found_in_db:,} dari {total_resp:,} sesi ({found_in_db/total_resp:.1%}) berhasil di-match ke database SC/Rekap.
        {not_found:,} sesi tidak ditemukan — kemungkinan No HP berbeda format, atau nasabah belum ada di file SC/Rekap periode ini.
        <br>Cek sidebar untuk pastiin nama kolom No HP sudah benar di masing-masing file.
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<p style="text-align:center;font-size:11px;color:#94A3B8">Dashboard WA Broadcast + Realisasi Bayar · PT. BCA Finance · ASR Mobil</p>',
    unsafe_allow_html=True
)
