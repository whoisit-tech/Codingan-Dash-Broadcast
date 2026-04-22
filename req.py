import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

st.set_page_config(page_title="WA Broadcast", page_icon="📲", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #F1F5F9; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 1300px; }

/* Uploader */
section[data-testid="stFileUploader"] { background:#fff; border-radius:10px; padding:12px 16px; border:1px solid #E2E8F0; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background:#E2E8F0; border-radius:8px; padding:4px; gap:2px; }
.stTabs [data-baseweb="tab"]      { border-radius:6px; color:#64748B; font-size:13px; font-weight:500; padding:6px 18px; }
.stTabs [aria-selected="true"]    { background:#fff !important; color:#1E40AF !important; font-weight:600; box-shadow:0 1px 4px rgba(0,0,0,.08); }
.stTabs [data-baseweb="tab-panel"]{ background:#fff; border:1px solid #E2E8F0; border-radius:0 0 10px 10px; padding:24px; }

/* Cards */
.card { background:#fff; border-radius:10px; border:1px solid #E2E8F0; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,.04); margin-bottom:16px; }

/* Metric box — kaya di PPT */
.mbox { border-radius:8px; padding:14px 16px; text-align:center; border:1.5px solid; }
.mbox-lbl { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:.6px; margin-bottom:6px; }
.mbox-val { font-size:24px; font-weight:700; line-height:1.1; }
.mbox-pct { font-size:11px; margin-top:3px; opacity:.8; }

/* Table */
.t { width:100%; border-collapse:collapse; font-size:12.5px; }
.t th { background:#F8FAFC; color:#64748B; font-size:10.5px; font-weight:600; text-transform:uppercase;
        letter-spacing:.5px; padding:9px 13px; border-bottom:2px solid #E2E8F0; text-align:center; }
.t td { padding:9px 13px; border-bottom:1px solid #F1F5F9; color:#334155; text-align:center; }
.t tr:last-child td { border-bottom:none; }
.t tr:hover td { background:#F8FAFC; }
.t .tot { background:#EFF6FF !important; font-weight:700; color:#1E40AF; }
.left { text-align:left !important; }

/* Pill badges */
.pill { display:inline-block; padding:2px 8px; border-radius:12px; font-size:10.5px; font-weight:600; }
.g { background:#DCFCE7; color:#15803D; }   /* green - good */
.r { background:#FEE2E2; color:#B91C1C; }   /* red   - bad  */
.o { background:#FEF3C7; color:#B45309; }   /* orange - mid */
.b { background:#DBEAFE; color:#1D4ED8; }   /* blue */
.s { background:#F1F5F9; color:#475569; }   /* slate */

/* Horizontal bar */
.brow { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.blbl { width:150px; font-size:12px; font-weight:500; color:#334155; text-align:right; flex-shrink:0; }
.btrk { flex:1; background:#F1F5F9; border-radius:5px; height:32px; overflow:hidden; }
.bfil { height:100%; border-radius:5px; display:flex; align-items:center; justify-content:flex-end; padding-right:10px; }
.bnum { font-size:13px; font-weight:700; color:#fff; }
.bpct { width:52px; font-size:11px; color:#94A3B8; text-align:right; flex-shrink:0; }

/* Section header */
.sh { font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.8px;
      color:#64748B; border-left:3px solid #3B82F6; padding-left:9px; margin-bottom:12px; }

.info-box { background:#EFF6FF; border:1px solid #BFDBFE; border-left:4px solid #3B82F6;
            border-radius:8px; padding:11px 16px; font-size:12px; color:#1E40AF; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# UPLOAD
# ═══════════════════════════════════════════════════════════
c1, c2 = st.columns(2)
with c1:
    f_sum  = st.file_uploader(" Summary CSV", type="csv", help="Kolom: DateUploaded, Sent, Delivered, Read, Failed, Total")
with c2:
    f_conv = st.file_uploader(" Conversation CSV (opsional)", type="csv")

if not f_sum:
    st.markdown('<div class="info-box">⬆ Upload <b>Summary CSV</b> untuk memulai dashboard.</div>', unsafe_allow_html=True)
    st.stop()


# ═══════════════════════════════════════════════════════════
# PARSE
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_summary(raw):
    txt   = raw.decode("utf-8-sig")
    delim = ";" if txt.count(";") > txt.count(",") else ","
    df    = pd.read_csv(io.StringIO(txt), delimiter=delim)
    df.columns = [c.strip() for c in df.columns]

    # date
    dcol = next((c for c in df.columns if "date" in c.lower()), df.columns[0])
    for fmt in ["%d/%m/%Y %H:%M", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            df["Date"] = pd.to_datetime(df[dcol].astype(str).str.split().str[0], format=fmt.split()[0])
            break
        except Exception:
            pass

    for c in ["Sent","Delivered","Read","Failed","Canceled","Total"]:
        df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0).astype(int)

    df["Undelivered"] = (df["Sent"] - df["Delivered"]).clip(0)
    df["Unread"]      = (df["Delivered"] - df["Read"]).clip(0)
    df["Month"]       = df["Date"].dt.strftime("%B %Y")
    df["MonthSort"]   = df["Date"].dt.year * 100 + df["Date"].dt.month
    return df.sort_values("Date").reset_index(drop=True)


@st.cache_data
def load_conv(raw):
    txt   = raw.decode("utf-8-sig")
    delim = ";" if txt.count(";") > txt.count(",") else ","
    df    = pd.read_csv(io.StringIO(txt), delimiter=delim)
    df.columns = [c.strip() for c in df.columns]

    # flexible col detection
    def col(kw, exact=False):
        if exact:
            # exact match (case-insensitive)
            return next((c for c in df.columns if c.strip().lower() == kw.lower()), None)
        return next((c for c in df.columns if kw.lower() in c.strip().lower()), None)

    # Detect 'Message' column — must be exact "Message", NOT "Message ID"
    msg_col = col("message", exact=True)
    if msg_col is None:
        # fallback: find col containing "message" but NOT "id"
        msg_col = next(
            (c for c in df.columns if "message" in c.strip().lower() and "id" not in c.strip().lower()),
            None
        )

    # Detect 'Message Type' column
    msg_type_col = col("message type") or col("type")

    df["_orig"] = df[col("origin")].str.strip().str.upper() if col("origin") else "?"
    df["_type"] = df[msg_type_col].str.strip().str.lower() if msg_type_col else "?"
    df["_msg"]  = df[msg_col].fillna("").astype(str) if msg_col else ""
    df["_sess"] = df[col("session")].astype(str) if col("session") else ""
    df["_date"] = pd.to_datetime(df[col("created")], dayfirst=True, errors="coerce") if col("created") else pd.NaT

    return df


df   = load_summary(f_sum.read())
conv = load_conv(f_conv.read()) if f_conv else None


# ═══════════════════════════════════════════════════════════
# FILTER BULAN
# ═══════════════════════════════════════════════════════════
months_avail = sorted(df["Month"].unique(), key=lambda m: df[df["Month"]==m]["MonthSort"].iloc[0])
sel_month = st.selectbox(" Filter Bulan", ["Semua Bulan"] + months_avail)

dff = df if sel_month == "Semua Bulan" else df[df["Month"] == sel_month]

# Totals from filtered data
T  = int(dff["Total"].sum())
S  = int(dff["Sent"].sum())
D  = int(dff["Delivered"].sum())
R  = int(dff["Read"].sum())
F  = int(dff["Failed"].sum())
UD = int(dff["Undelivered"].sum())
UR = int(dff["Unread"].sum())

def pct(a, b):
    return f"{a/b:.1%}" if b else "0%"


# ═══════════════════════════════════════════════════════════
# HEADER STRIP
# ═══════════════════════════════════════════════════════════
period = f"{dff['Date'].min().strftime('%d %b %Y')} – {dff['Date'].max().strftime('%d %b %Y')}"
st.markdown(f"""
<div style="background:#1E3A5F;border-radius:10px;padding:16px 24px;margin-bottom:18px;
            display:flex;justify-content:space-between;align-items:center">
  <div>
    <span style="font-size:18px;font-weight:700;color:#fff"> WA Broadcast — </span>
    <span style="font-size:12px;color:rgba(255,255,255,.65);margin-left:14px">PT. BCA Finance · ASR Mobil · {period}</span>
  </div>
  <span style="background:rgba(255,255,255,.12);color:#fff;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600">
    {sel_month}
  </span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# FUNNEL — SAMA KAYAK DI PPT
# ═══════════════════════════════════════════════════════════
def mbox(lbl, val, pct_str, fg, bg, border):
    return f"""<div class="mbox" style="background:{bg};border-color:{border};color:{fg}">
      <div class="mbox-lbl">{lbl}</div>
      <div class="mbox-val">{val:,}</div>
      <div class="mbox-pct">{pct_str}</div>
    </div>"""


# Row 1: Data Upload
st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:10px">
  {mbox(" Data Upload", T, "100%", "#1E293B", "#F8FAFC", "#CBD5E1")}
</div>
""", unsafe_allow_html=True)

# Row 2: Failed | Success
ca, cb = st.columns(2)
with ca:
    st.markdown(mbox(" Failed Broadcast", F, f"{pct(F,T)} dari upload", "#B91C1C", "#FEF2F2", "#FECACA"), unsafe_allow_html=True)
with cb:
    st.markdown(mbox(" Success Broadcast", S, f"{pct(S,T)} dari upload", "#15803D", "#F0FDF4", "#86EFAC"), unsafe_allow_html=True)

# Row 3: Delivered | Sent (Undelivered)
ca2, cb2 = st.columns(2)
with ca2:
    st.markdown(mbox(" Delivered", D, f"{pct(D,T)} dari upload", "#1D4ED8", "#EFF6FF", "#93C5FD"), unsafe_allow_html=True)
with cb2:
    st.markdown(mbox(" Sent (Belum Delivered)", UD, f"{pct(UD,T)} dari upload", "#D97706", "#FFFBEB", "#FDE68A"), unsafe_allow_html=True)

# Row 4: Read | Unread
ca3, cb3 = st.columns(2)
with ca3:
    st.markdown(mbox("👁 Read", R, f"{pct(R,D)} dari delivered", "#0E7490", "#ECFEFF", "#67E8F9"), unsafe_allow_html=True)
with cb3:
    st.markdown(mbox("📭 Unread", UR, f"{pct(UR,D)} dari delivered", "#7C3AED", "#FAF5FF", "#C4B5FD"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════
tabs = [" Rekap Upload", " Response", " Isi Pesan"]
if conv is None:
    tabs = [" Rekap Upload"]

tab_objs = st.tabs(tabs)


# ───────────────────────────────────────────────────────────
# TAB 1 — REKAP UPLOAD
# ───────────────────────────────────────────────────────────
with tab_objs[0]:

    # ── Summary table per batch ──
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

    # Total row
    fp_t=F/T if T else 0; dp_t=D/T if T else 0; rp_t=R/D if D else 0
    def p_t(v, hi, lo, inv=False):
        if inv: cls = "g" if v<hi else "r" if v>lo else "o"
        else:   cls = "g" if v>hi else "r" if v<lo else "o"
        return f'<span class="pill {cls}">{v:.1%}</span>'

    rows_html += f"""<tr class="tot">
      <td class="left">TOTAL ({len(dff)} batch)</td>
      <td>{T:,}</td>
      <td>{F:,}</td><td>{p_t(fp_t,.15,.30,inv=True)}</td>
      <td>{S:,}</td>
      <td>{D:,}</td><td>{p_t(dp_t,.70,.50)}</td>
      <td>{R:,}</td><td>{p_t(rp_t,.65,.45)}</td>
      <td>{UR:,}</td>
    </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;max-height:420px;overflow-y:auto">
    <table class="t">
      <thead><tr>
        <th class="left">Tanggal</th><th>Total</th>
        <th>Failed</th><th>Fail%</th>
        <th>Sent</th>
        <th>Delivered</th><th>Del%</th>
        <th>Read</th><th>Read%</th><th>Unread</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table></div>
    <p style="font-size:10px;color:#94A3B8;margin-top:6px">
     Fail% & Del% dihitung dari Total Upload · Read% dihitung dari Delivered
    </p>
    """, unsafe_allow_html=True)

    # ── Chart ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Tren per Batch</p>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dff["Date"], y=dff["Total"], name="Total",
        marker_color="#E2E8F0", opacity=0.8))
    for m, c, d in [("Delivered","#2563EB",None),("Read","#0891B2","dot"),("Failed","#DC2626",None)]:
        fig.add_trace(go.Scatter(x=dff["Date"], y=dff[m], name=m,
            line=dict(color=c, width=2, dash=d or "solid"), mode="lines+markers",
            marker=dict(size=5, color=c)))

    fig.update_layout(
        barmode="overlay", height=280, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F8FAFC",
        font=dict(family="Inter", color="#64748B"),
        legend=dict(orientation="h", y=-0.25, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#E2E8F0", tickformat="%d %b"),
        yaxis=dict(gridcolor="#E2E8F0"), hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Monthly summary if "Semua Bulan" ──
    if sel_month == "Semua Bulan":
        st.markdown('<p class="sh">Rekap per Bulan</p>', unsafe_allow_html=True)
        monthly = df.groupby(["Month","MonthSort"]).agg(
            Total=("Total","sum"), Sent=("Sent","sum"), Delivered=("Delivered","sum"),
            Read=("Read","sum"), Failed=("Failed","sum"),
            Unread=("Unread","sum"), Uploads=("Date","count")
        ).reset_index().sort_values("MonthSort")

        m_rows = ""
        for _, r in monthly.iterrows():
            fp = r["Failed"]/r["Total"] if r["Total"] else 0
            dp = r["Delivered"]/r["Total"] if r["Total"] else 0
            rp = r["Read"]/r["Delivered"] if r["Delivered"] else 0
            m_rows += f"""<tr>
              <td class="left" style="font-weight:600">{r['Month']}</td>
              <td>{int(r['Uploads'])}</td>
              <td>{int(r['Total']):,}</td>
              <td style="color:#DC2626">{int(r['Failed']):,}</td>
              <td>{p_t(fp,.15,.30,inv=True)}</td>
              <td style="color:#15803D">{int(r['Sent']):,}</td>
              <td style="color:#1D4ED8">{int(r['Delivered']):,}</td>
              <td>{p_t(dp,.70,.50)}</td>
              <td style="color:#0E7490">{int(r['Read']):,}</td>
              <td>{p_t(rp,.65,.45)}</td>
              <td style="color:#7C3AED">{int(r['Unread']):,}</td>
            </tr>"""
        m_rows += f"""<tr class="tot">
          <td class="left">TOTAL</td><td>{int(monthly['Uploads'].sum())}</td>
          <td>{T:,}</td>
          <td>{F:,}</td><td>{p_t(F/T if T else 0,.15,.30,inv=True)}</td>
          <td>{S:,}</td>
          <td>{D:,}</td><td>{p_t(D/T if T else 0,.70,.50)}</td>
          <td>{R:,}</td><td>{p_t(R/D if D else 0,.65,.45)}</td>
          <td>{UR:,}</td>
        </tr>"""

        st.markdown(f"""
        <table class="t"><thead><tr>
          <th class="left">Bulan</th><th>Batch</th><th>Total</th>
          <th>Failed</th><th>Fail%</th>
          <th>Sent</th><th>Delivered</th><th>Del%</th>
          <th>Read</th><th>Read%</th><th>Unread</th>
        </tr></thead><tbody>{m_rows}</tbody></table>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────
# TAB 2 — RESPONSE ANALYSIS
# ───────────────────────────────────────────────────────────
if conv is not None and len(tab_objs) > 1:
    with tab_objs[1]:

        cdf = conv.copy()

        # Filter by month if selected
        if sel_month != "Semua Bulan" and cdf["_date"].notna().any():
            mo = pd.to_datetime(dff["Date"].iloc[0]).strftime("%B %Y")
            cdf = cdf[cdf["_date"].dt.strftime("%B %Y") == sel_month]

        in_df  = cdf[cdf["_orig"] == "IN"]
        btn_df = in_df[in_df["_type"].isin(["button","button_reply"])]
        total_sessions = cdf["_sess"].nunique()

        # Stats
        s1,s2,s3,s4 = st.columns(4)
        for col_obj, lbl, val, fg, bg, bd in [
            (s1, "Total Sesi",     total_sessions,    "#1D4ED8","#EFF6FF","#93C5FD"),
            (s2, "Pesan Masuk",    len(in_df),        "#15803D","#F0FDF4","#86EFAC"),
            (s3, "Button Replies", len(btn_df),       "#D97706","#FFFBEB","#FDE68A"),
            (s4, "Teks Bebas",     len(in_df[in_df["_type"]=="text"]), "#7C3AED","#FAF5FF","#C4B5FD"),
        ]:
            with col_obj:
                st.markdown(f"""<div class="mbox" style="background:{bg};border-color:{bd};color:{fg}">
                  <div class="mbox-lbl">{lbl}</div>
                  <div class="mbox-val">{val:,}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Filter Message Type (nyambung ke Button Responses) ──
        mt_lbl = {
            "text":"Teks bebas", "button":"Klik tombol",
            "button_reply":"Balasan tombol", "list_reply":"Pilihan menu",
            "image":"Foto", "document":"Dokumen",
            "audio":"Pesan suara", "reaction":"Emoji",
            "sticker":"Sticker", "unsupported":"Tidak didukung",
        }
        available_types = sorted(in_df["_type"].dropna().unique().tolist())
        type_options    = ["Semua Type"] + available_types
        type_labels     = ["Semua Type"] + [f"{t} — {mt_lbl.get(t, t)}" for t in available_types]

        st.markdown('<p class="sh">Filter Message Type</p>', unsafe_allow_html=True)
        sel_type_label = st.radio(
            "Pilih tipe pesan:",
            options=type_labels,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )
        sel_type = type_options[type_labels.index(sel_type_label)]

        filtered_in_df = in_df if sel_type == "Semua Type" else in_df[in_df["_type"] == sel_type]

        st.markdown("<br>", unsafe_allow_html=True)
        cl, cr = st.columns([3,2])

        with cl:
            filter_label = "" if sel_type == "Semua Type" else f" &nbsp;<span style='font-size:10px;background:#DBEAFE;color:#1D4ED8;padding:2px 8px;border-radius:10px'>{sel_type}</span>"
            st.markdown(f'<p class="sh">Button Responses dari Nasabah{filter_label}</p>', unsafe_allow_html=True)
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
            st.markdown(f"""<table class="t">
              <thead><tr>
                <th class="left">Type</th><th>Jumlah</th><th>%</th><th class="left">Keterangan</th>
              </tr></thead><tbody>{mt_rows}</tbody></table>
              <p style="font-size:10px;color:#94A3B8;margin-top:8px">
              Klik filter di atas untuk menyaring isi pesan berdasarkan tipe</p>""",
              unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────
# TAB 3 — ISI PESAN
# ───────────────────────────────────────────────────────────
if conv is not None and len(tab_objs) > 2:
    with tab_objs[2]:

        cdf2 = conv[conv["_orig"] == "IN"].copy()
        if sel_month != "Semua Bulan" and cdf2["_date"].notna().any():
            cdf2 = cdf2[cdf2["_date"].dt.strftime("%B %Y") == sel_month]

        total_in = len(cdf2)

        # ── Breakdown semua isi pesan (kolom Message) ──
        st.markdown('<p class="sh">Breakdown Isi Pesan dari Nasabah</p>', unsafe_allow_html=True)

        msg_counts = (
            cdf2[cdf2["_msg"].str.strip() != ""]["_msg"]
            .str.strip()
            .value_counts()
            .reset_index()
        )
        msg_counts.columns = ["Pesan", "Jumlah"]
        total_msg = int(msg_counts["Jumlah"].sum())

        colors_bar = ["#15803D","#1D4ED8","#DC2626","#7C3AED","#D97706",
                      "#DB2777","#0891B2","#0F766E","#9333EA","#B45309"]

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

        # ── Tabel lengkap dengan search ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh">Tabel Detail Isi Pesan</p>', unsafe_allow_html=True)

        fc1, fc2 = st.columns([3, 1])
        with fc1:
            kw = st.text_input(" Cari isi pesan", placeholder="contoh: bayar, angsuran, denda...")
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
          <th>#</th><th class="left">Isi Pesan</th>
          <th>Jumlah</th><th>%</th><th>Proporsi</th>
        </tr></thead><tbody>{tbl_rows}</tbody></table></div>""", unsafe_allow_html=True)
