import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle
import os

# -------------------------------
# Configuration
# -------------------------------

COHORT = "26"  # change this to switch cohorts

# Paths (automatically use COHORT)
behavior_file    = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\2. Oxycodone GWAS\Oxy Behavior Sheet Auto\Oxycodone_C{COHORT}_behavior_sheet.xlsx"
tail_file        = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\2. Oxycodone GWAS\Tail Immersion\Oxy_C{COHORT}_TailImmersion.xlsx"
vf_file          = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\2. Oxycodone GWAS\Von Frey\Oxy_C{COHORT}_VonFrey.xlsx"
cohort_info_file = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\2. Oxycodone GWAS\Oxy Cohort Information\Oxycodone C{COHORT} Updated Cohort Information.xlsx"


if os.path.exists(tail_file):
    tail_df = pd.read_excel(tail_file)
    tail_df['Subject'] = tail_df['Subject'].astype(str).str.strip()
    tail_present = True
else:
    tail_df = None
    tail_present = False

if os.path.exists(vf_file):
    vf_df = pd.read_excel(vf_file)
    vf_df['Subject'] = vf_df['Subject'].astype(str).str.strip()
    vf_present = True
else:
    vf_df = None
    vf_present = False

# -------------------------------
# Helper functions
# -------------------------------

def extract_day(session_name):
    digits = re.findall(r'\d+', str(session_name))
    return int(digits[0]) if digits else None

def parse_daily_issue(issue_str, rat_id):
    return False if pd.isna(issue_str) else (rat_id in issue_str)

def extract_section(df, section_name, meta_session_names,
                    next_sections=("Rewards","Active Lever Presses","Inactive Lever Presses","Breakpoint")):
    rows = df.index[df.iloc[:,0].astype(str).str.strip()==section_name].tolist()
    if not rows:
        raise ValueError(f"Section {section_name} not found")
    start = rows[0]
    header = [str(h).strip() for h in df.iloc[start+1].fillna("")]
    data = []
    i = start + 2
    while i < len(df):
        first = str(df.iloc[i,0]).strip()
        if first in next_sections or first == "":
            break
        data.append(df.iloc[i].tolist())
        i += 1
    sec = pd.DataFrame(data, columns=header)
    total, ncols = sec.shape[1], sec.shape[1] - 8
    if ncols > 0 and len(meta_session_names) >= ncols:
        sec.columns = header[:4] + meta_session_names[:ncols] + header[-4:]
    return sec

def extract_meta_row(df, title):
    m = df[df.iloc[:,0].astype(str).str.strip().str.lower() == title.lower()]
    if not m.empty:
        return m.iloc[0,3:].apply(lambda x: str(x).strip())
    return pd.Series([""]*(df.shape[1]-4))

# -------------------------------
# Main
# -------------------------------

def main():
    # Load behavior sheet
    df = pd.read_excel(behavior_file, sheet_name="Behavior Data", header=None)
    meta_dates    = df.iloc[0, 4:]
    meta_sessions = df.iloc[1, 4:].astype(str).str.strip()
    meta_issues   = df.iloc[2, 4:].astype(str).str.strip()
    meta_notes    = extract_meta_row(df, "Notes")

    # Build meta entries
    meta_entries = []
    for i, sess in enumerate(meta_sessions):
        meta_entries.append({
            "session": sess,
            "day": extract_day(sess),
            "date": pd.to_datetime(meta_dates.iloc[i]),
            "issue": meta_issues.iloc[i],
            "note": meta_notes.iloc[i] if i < len(meta_notes) else ""
        })
    meta_names = meta_sessions.tolist()

    # Extract behavior sections
    rewards_df  = extract_section(df, "Rewards", meta_names)
    active_df   = extract_section(df, "Active Lever Presses", meta_names)
    inactive_df = extract_section(df, "Inactive Lever Presses", meta_names)

    # Safely convert session columns to numeric
    for sec in (rewards_df, active_df, inactive_df):
        for c in sec.columns[3:-3]:
            sec[c] = sec[c].apply(
                lambda x: pd.to_numeric(x, errors="coerce")
                          if not isinstance(x, list) else np.nan
            )

    # Load tail, von frey, cohort info
    cohort_df = pd.read_excel(cohort_info_file)
    cohort_df['RAT']  = cohort_df['RAT'].astype(str).str.strip()
    cohort_df['RFID'] = cohort_df['RFID'].astype(str).str.strip()

    # Unique rats
    rats = rewards_df[['Rat','RFID']].drop_duplicates().reset_index(drop=True)

    # Plot settings
    session_groups = {"SHA":["SHA"], "LGA":["LGA"], "PR":["PR","TREATMENT"]}
    measures       = [("Reward", rewards_df), ("Active", active_df), ("Inactive", inactive_df)]
    line_styles    = ["-", (0, (3,1,1,1,1,1)), ":", "-."]  # for treatment markers

    trials     = [1,2,3]
    labels_map = {1:"baseline",2:"onboard before SHA",3:"onboard after LGA"}
    trials_vf  = [1,2]
    labels_vf  = {1:"baseline",2:"withdrawal"}

    output_pdf = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\2. Oxycodone GWAS\Oxy Graphs\C{COHORT}_behavior_graphs.pdf"
    pp = PdfPages(output_pdf)

    # --- Page 1: Cohort Averages + Tail & Von Frey ---
    fig = plt.figure(figsize=(15,20))
    gs1 = fig.add_gridspec(5,1, height_ratios=[0.5,1,1,1,1], hspace=0.4)

    ax0 = fig.add_subplot(gs1[0])
    ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                            fill=False,edgecolor='black',linewidth=1.5))
    ax0.text(0.5,0.5,"Cohort Averages",ha='center',va='center',
             fontsize=18,fontweight='bold')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        sub = gridspec.GridSpecFromSubplotSpec(1,3, subplot_spec=gs1[ridx], wspace=0.3)
        entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
        if grp=="PR":
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        else:
            days = [e["day"] for e in entries]

        for cidx,(mname,sec) in enumerate(measures):
            oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
            for e in entries:
                col = sec.get(e["session"], pd.Series([], dtype=float))
                cnt = col.count()
                oa.append(col.mean(skipna=True)); os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                mcol = col[sec['Rat'].astype(str).str.startswith("M", na=False)]; cntm = mcol.count()
                ma.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                fcol = col[sec['Rat'].astype(str).str.startswith("F", na=False)]; cntf = fcol.count()
                fa.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)

            ax = fig.add_subplot(sub[0,cidx])
            ax.plot(days,oa, color="grey",marker="o",alpha=0.5,label="Cohort Avg")
            ax.fill_between(days,np.array(oa)-np.array(os),np.array(oa)+np.array(os),color="grey",alpha=0.25)
            ax.plot(days,ma, color="lightblue",marker="o",alpha=0.5,label="Male Avg")
            ax.fill_between(days,np.array(ma)-np.array(ms),np.array(ma)+np.array(ms),color="lightblue",alpha=0.25)
            ax.plot(days,fa, color="orange",marker="o",alpha=0.5,label="Female Avg")
            ax.fill_between(days,np.array(fa)-np.array(fs),np.array(fa)+np.array(fs),color="orange",alpha=0.25)
            ax.set_title(f"{grp} {mname}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            if grp=="SHA":
                ax.set_ylim(0,100)
            if grp=="LGA":
                ax.set_ylim(0,300)
                if days and max(days)>14:
                    ax.axvline(14.5, color="black", linestyle="--", linewidth=1.5, alpha=0.8)
            ax.legend(fontsize='small')

    bot1 = gridspec.GridSpecFromSubplotSpec(1,2, subplot_spec=gs1[4], wspace=0.4)

    tail_ax = fig.add_subplot(bot1[0])
    tail_ax.set_title("Tail Immersion Times"); tail_ax.set_xlabel("Trial"); tail_ax.set_ylabel("Time (seconds)")
    tail_ax.set_ylim(0,15)
    if tail_present:
        oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
        for t in trials:
            col = pd.to_numeric(tail_df[f"Tail Immersion {t} Time"],errors="coerce"); cnt = col.count()
            oa.append(col.mean(skipna=True)); os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
            mcol = col[tail_df['Subject'].str.startswith("M", na=False)]; cntm = mcol.count()
            ma.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
            fcol = col[tail_df['Subject'].str.startswith("F", na=False)]; cntf = fcol.count()
            fa.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
        tail_ax.plot(trials,oa,color="grey",marker="o",alpha=0.5,label="Cohort Avg")
        tail_ax.fill_between(trials,np.array(oa)-np.array(os),np.array(oa)+np.array(os),color="grey",alpha=0.25)
        tail_ax.plot(trials,ma,color="lightblue",marker="o",alpha=0.5,label="Male Avg")
        tail_ax.fill_between(trials,np.array(ma)-np.array(ms),np.array(ma)+np.array(ms),color="lightblue",alpha=0.25)
        tail_ax.plot(trials,fa,color="orange",marker="o",alpha=0.5,label="Female Avg")
        tail_ax.fill_between(trials,np.array(fa)-np.array(fs),np.array(fa)+np.array(fs),color="orange",alpha=0.25)
        avail = [t for t in trials if not np.isnan(oa[t-1])]
        tail_ax.set_xticks(avail); tail_ax.set_xticklabels([labels_map[t] for t in avail])
        tail_ax.legend(fontsize='small')

    vf_ax = fig.add_subplot(bot1[1])
    vf_ax.set_title("Von Frey Forces"); vf_ax.set_xlabel("Trial"); vf_ax.set_ylabel("Force (g)")
    vf_ax.set_ylim(0,25)
    if vf_present:
        vo,vs,mo,ms,fo,fs = [],[],[],[],[],[]
        for t in trials_vf:
            col = pd.to_numeric(vf_df[f"Von Frey {t} Force"],errors="coerce"); cnt = col.count()
            vo.append(col.mean(skipna=True)); vs.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
            mcol = col[vf_df['Subject'].str.startswith("M", na=False)]; cntm = mcol.count()
            mo.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
            fcol = col[vf_df['Subject'].str.startswith("F", na=False)]; cntf = fcol.count()
            fo.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
        vf_ax.plot(trials_vf,vo,color="grey",marker="o",alpha=0.5,label="Cohort Avg")
        vf_ax.fill_between(trials_vf,np.array(vo)-np.array(vs),np.array(vo)+np.array(vs),color="grey",alpha=0.25)
        vf_ax.plot(trials_vf,mo,color="lightblue",marker="o",alpha=0.5,label="Male Avg")
        vf_ax.fill_between(trials_vf,np.array(mo)-np.array(ms),np.array(mo)+np.array(ms),color="lightblue",alpha=0.25)
        vf_ax.plot(trials_vf,fo,color="orange",marker="o",alpha=0.5,label="Female Avg")
        vf_ax.fill_between(trials_vf,np.array(fo)-np.array(fs),np.array(fo)+np.array(fs),color="orange",alpha=0.25)
        vf_ax.set_xticks(trials_vf); vf_ax.set_xticklabels([labels_vf[t] for t in trials_vf])
        vf_ax.legend(fontsize='small')

    pp.savefig(fig)
    plt.close(fig)

    # --- Page 2: All Cohort Readings + overlays with PR relabel & LGA line ---
    fig = plt.figure(figsize=(15,20))
    gs2 = fig.add_gridspec(5,1, height_ratios=[0.5,1,1,1,1], hspace=0.4)

    ax0 = fig.add_subplot(gs2[0]); ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                            fill=False,edgecolor='black',linewidth=1.5))
    ax0.text(0.5,0.5,"All Cohort Readings",ha='center',va='center',
             fontsize=18,fontweight='bold')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        sub = gridspec.GridSpecFromSubplotSpec(1,3, subplot_spec=gs2[ridx], wspace=0.3)
        entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
        if grp=="PR":
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        else:
            days = [e["day"] for e in entries]

        for cidx,(_,sec) in enumerate(measures):
            ax = fig.add_subplot(sub[0,cidx])
            for rat in rats["Rat"]:
                vals = [
                    sec.loc[sec['Rat'].str.strip()==rat, e["session"]].iloc[0]
                    if not sec.loc[sec['Rat'].str.strip()==rat, e["session"]].empty else np.nan
                    for e in entries
                ]
                ax.plot(days, vals, color="red", alpha=0.5)

            ax.set_title(f"{grp} {measures[cidx][0]}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if measures[cidx][0]=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
            if grp=="SHA":
                ax.set_ylim(0,100)
            if grp=="LGA":
                ax.set_ylim(0,300)
                if days and max(days)>14:
                    ax.axvline(14.5, color="black", linestyle="--", linewidth=1.5, alpha=0.8)

            if grp=="PR":
                ax.set_xticks(days)
                initial_map = {1:'V',2:'B',3:'N',4:'M'}
                labels = []
                for idx,e in enumerate(entries):
                    sess = e["session"]
                    if sess.startswith("PR") and not sess.startswith("TREATMENT"):
                        labels.append(str(days[idx]))
                    else:
                        tnum = extract_day(sess)
                        labels.append(initial_map.get(tnum,""))
                ax.set_xticklabels(labels)

    bot2 = gridspec.GridSpecFromSubplotSpec(1,2, subplot_spec=gs2[4], wspace=0.4)
    tail_ax = fig.add_subplot(bot2[0])
    tail_ax.set_title("Tail Immersion Times"); tail_ax.set_xlabel("Trial"); tail_ax.set_ylabel("Time (seconds)")
    tail_ax.set_ylim(0,15)
    if tail_present:
        for rat in rats["Rat"]:
            rd = tail_df[tail_df['Subject']==rat]
            vals = [
                pd.to_numeric(rd.iloc[0][f"Tail Immersion {t} Time"],errors="coerce")
                if not rd.empty else np.nan
                for t in trials
            ]
            tail_ax.plot(trials, vals, color="red", alpha=0.5)
        tail_ax.set_xticks(trials); tail_ax.set_xticklabels([labels_map[t] for t in trials])
        tail_ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    vf_ax = fig.add_subplot(bot2[1])
    vf_ax.set_title("Von Frey Forces"); vf_ax.set_xlabel("Trial"); vf_ax.set_ylabel("Force (g)")
    vf_ax.set_ylim(0,25)
    if vf_present:
        for rat in rats["Rat"]:
            rv = vf_df[vf_df['Subject']==rat]
            vals = [
                pd.to_numeric(rv.iloc[0][f"Von Frey {t} Force"],errors="coerce")
                if not rv.empty else np.nan
                for t in trials_vf
            ]
            vf_ax.plot(trials_vf, vals, color="red", alpha=0.5)
        vf_ax.set_xticks(trials_vf); vf_ax.set_xticklabels([labels_vf[t] for t in trials_vf])
        vf_ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    pp.savefig(fig)
    plt.close(fig)

    # --- Pages 3+: Per-rat detailed with PR relabeled ---
    for _, rr in rats.iterrows():
        rat_id   = str(rr["Rat"]).strip()
        rat_rfid = str(rr["RFID"]).split(".")[0]

        ci = cohort_df[cohort_df['RAT']==rat_id]
        coat    = ci.iloc[0].get("Coat Color","None")       if not ci.empty else "None"
        dgroup  = ci.iloc[0].get("Dissection Group","None") if not ci.empty else "None"
        surgeon = ci.iloc[0].get("Surgeon ","None")         if not ci.empty else "None"

        treatments = []
        if not ci.empty:
            for t in range(1,5):
                raw = ci.iloc[0].get(f"Treatment {t} Group", "")
                grp_name = "" if pd.isna(raw) else str(raw).strip()
                dr       = ci.iloc[0].get(f"Treatment {t} Date","")
                try:
                    dt = pd.to_datetime(dr)
                except:
                    dt = pd.NaT
                init = grp_name[0].upper() if grp_name and grp_name.upper()!="NA" else "NA"
                if pd.notna(dt) and grp_name:
                    treatments.append((t, grp_name, init, dt))

        fig = plt.figure(figsize=(15,20))
        mg = fig.add_gridspec(5,1, height_ratios=[0.6,1,1,1,1], hspace=0.4)

        # Top info box
        ax0 = fig.add_subplot(mg[0])
        ax0.axis('off')
        ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                                fill=False,edgecolor='black',linewidth=1.5))
        lines = [
            rf"$\bf{{Rat}}$: {rat_id}    $\bf{{RFID}}$: {rat_rfid}",
            f"Coat Color: {coat}    Dissection Group: {dgroup}    Surgeon: {surgeon}"
        ]
        iss = [f"{e['session']}: {m.group(1)}" for e in meta_entries
               if (m:=re.search(rf"{rat_id}:\s*([^;]+);", e["issue"]))]
        lines.append(rf"$\bf{{Issues}}$: " + ("; ".join(iss) if iss else "None"))
        er = rewards_df[rewards_df['Rat'].astype(str).str.strip()==rat_id]
        if not er.empty:
            ec = er.iloc[0].get("Exit Code", np.nan)
            ec = "None" if pd.isna(ec) else ec
        else:
            ec = "None"
        lines.append(rf"$\bf{{Exit Code}}$: {ec}")
        for t_idx,grp_name,_,dt in treatments:
            lines.append(f"Treatment {t_idx}: {grp_name} on {dt.date()}")

        ax0.text(0.02,0.98,"\n".join(lines),
                 transform=ax0.transAxes, ha='left', va='top',
                 fontsize=12, linespacing=1.1)

        # Behavior per-rat rows
        for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
            sub = gridspec.GridSpecFromSubplotSpec(1,3, subplot_spec=mg[ridx], wspace=0.3)
            entries = [e for e in meta_entries if any(e['session'].startswith(p) for p in pfx)]
            if grp=="PR":
                entries = sorted(entries, key=lambda x: x["date"])
                days = list(range(1,len(entries)+1))
            else:
                days = [e["day"] for e in entries]

            for cidx,(mname,sec) in enumerate(measures):
                oa,os,ma,ms,fa,fs,rv,flags = [],[],[],[],[],[],[],[]
                for e in entries:
                    val = sec.loc[sec['Rat'].astype(str).str.strip()==rat_id, e['session']]
                    v = val.iloc[0] if not val.empty else np.nan
                    rv.append(v)
                    col = pd.to_numeric(sec[e['session']],errors="coerce"); cnt=col.count()
                    oa.append(col.mean(skipna=True)); os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                    mcol = col[sec['Rat'].astype(str).str.startswith("M", na=False)]; cntm=mcol.count()
                    ma.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                    fcol = col[sec['Rat'].astype(str).str.startswith("F", na=False)]; cntf=fcol.count()
                    fa.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
                    flags.append(parse_daily_issue(e["issue"], rat_id))

                ax = fig.add_subplot(sub[0,cidx])
                ax.plot(days, rv,  color="red",    marker="o", label="Rat")
                ax.plot(days, oa, color="grey",   marker="o", alpha=0.5, label="Cohort Avg")
                ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os),
                                color="grey", alpha=0.25)
                ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male Avg")
                ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms),
                                color="lightblue", alpha=0.25)
                ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female Avg")
                ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs),
                                color="orange", alpha=0.25)
                for d,y,f in zip(days, rv, flags):
                    if f and not np.isnan(y):
                        ax.plot(d, y, marker="o", markersize=12, color="yellow")

                ax.set_title(f"{grp} {mname}")
                ax.set_xlabel("Day")
                ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
                ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

                if grp=="SHA":
                    ax.set_ylim(0,100)
                elif grp=="LGA":
                    ax.set_ylim(0,300)
                    if days and max(days)>14:
                        ax.axvline(14.5, color="black", linestyle="--", linewidth=1.5, alpha=0.8)
                    for t_idx, grp_name, init, dt in treatments:
                        # bracket LGA dates to find insertion point
                        lga_dates = [e["date"] for e in entries]
                        lga_days  = days
                        pos = None
                        for j in range(len(lga_dates)-1):
                            if lga_dates[j] <= dt <= lga_dates[j+1]:
                                pos = (lga_days[j] + lga_days[j+1]) / 2
                                break
                        if pos is None:
                            pos = (lga_days[0]-0.5) if dt < lga_dates[0] else (lga_days[-1]+0.5)
                        style = line_styles[t_idx-1]
                        ax.axvline(pos, color="black",
                                linestyle=style,
                                linewidth=1.5,
                                label=init)
                elif grp=="PR":
                    ax.set_xticks(days)
                    initial_map = {1:'V',2:'B',3:'N',4:'M'}
                    labels = []
                    for idx,e in enumerate(entries):
                        sess = e["session"]
                        if sess.startswith("PR") and not sess.startswith("TREATMENT"):
                            labels.append(str(days[idx]))
                        else:
                            tnum = extract_day(sess)
                            labels.append(initial_map.get(tnum,""))
                    ax.set_xticklabels(labels)

                ax.legend(fontsize='small')

        # Bottom: Tail Immersion + Von Frey + paw overlay
        bot = gridspec.GridSpecFromSubplotSpec(1,2, subplot_spec=mg[4], wspace=0.4)

        tail_ax = fig.add_subplot(bot[0])
        tail_ax.set_title("Tail Immersion Times"); tail_ax.set_xlabel("Trial"); tail_ax.set_ylabel("Time (seconds)")
        tail_ax.set_ylim(0,15)
        if tail_present:
            oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
            for t in trials:
                col = pd.to_numeric(tail_df[f"Tail Immersion {t} Time"],errors="coerce"); cnt=col.count()
                oa.append(col.mean(skipna=True)); os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                mcol = col[tail_df['Subject'].str.startswith("M", na=False)]; cntm=mcol.count()
                ma.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                fcol = col[tail_df['Subject'].str.startswith("F", na=False)]; cntf=fcol.count()
                fa.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
            rd = tail_df[tail_df['Subject']==rat_id]
            pts = [
                pd.to_numeric(rd.iloc[0][f"Tail Immersion {t} Time"],errors="coerce")
                if not rd.empty else np.nan
                for t in trials
            ]
            tail_ax.plot(trials,oa,color="grey",marker="o",alpha=0.5,label="Cohort Avg")
            tail_ax.fill_between(trials,np.array(oa)-np.array(os),np.array(oa)+np.array(os),color="grey",alpha=0.25)
            tail_ax.plot(trials,ma,color="lightblue",marker="o",alpha=0.5,label="Male Avg")
            tail_ax.fill_between(trials,np.array(ma)-np.array(ms),np.array(ma)+np.array(ms),color="lightblue",alpha=0.25)
            tail_ax.plot(trials,fa,color="orange",marker="o",alpha=0.5,label="Female Avg")
            tail_ax.fill_between(trials,np.array(fa)-np.array(fs),np.array(fa)+np.array(fs),color="orange",alpha=0.25)
            tail_ax.plot(trials,pts,color="red",marker="o",label="Rat")
            avail = [t for t in trials if not np.isnan(oa[t-1])]
            tail_ax.set_xticks(avail); tail_ax.set_xticklabels([labels_map[t] for t in avail])
            tail_ax.legend(fontsize='small')

        vf_ax = fig.add_subplot(bot[1])
        vf_ax.set_title("Von Frey Forces"); vf_ax.set_xlabel("Trial"); vf_ax.set_ylabel("Force (g)")
        vf_ax.set_ylim(0,25)
        if vf_present:
            vo,vs,mo,ms,fo,fs,rv_line = [],[],[],[],[],[],[]
            for t in trials_vf:
                col = pd.to_numeric(vf_df[f"Von Frey {t} Force"],errors="coerce"); cnt=col.count()
                vo.append(col.mean(skipna=True)); vs.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                mcol = col[vf_df['Subject'].str.startswith("M", na=False)]; cntm=mcol.count()
                mo.append(mcol.mean(skipna=True)); ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                fcol = col[vf_df['Subject'].str.startswith("F", na=False)]; cntf=fcol.count()
                fo.append(fcol.mean(skipna=True)); fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
                rv = vf_df[vf_df['Subject']==rat_id]
                val = pd.to_numeric(rv.iloc[0][f"Von Frey {t} Force"],errors="coerce") if not rv.empty else np.nan
                rv_line.append(val)

            vf_ax.plot(trials_vf,vo,color="grey",marker="o",alpha=0.5,label="Cohort Avg")
            vf_ax.fill_between(trials_vf,np.array(vo)-np.array(vs),np.array(vo)+np.array(vs),color="grey",alpha=0.25)
            vf_ax.plot(trials_vf,mo,color="lightblue",marker="o",alpha=0.5,label="Male Avg")
            vf_ax.fill_between(trials_vf,np.array(mo)-np.array(ms),np.array(mo)+np.array(ms),color="lightblue",alpha=0.25)
            vf_ax.plot(trials_vf,fo,color="orange",marker="o",alpha=0.5,label="Female Avg")
            vf_ax.fill_between(trials_vf,np.array(fo)-np.array(fs),np.array(fo)+np.array(fs),color="orange",alpha=0.25)
            vf_ax.plot(trials_vf,rv_line,color="red",marker="o",label="Rat")

            # scatter paw on VF graph
            rv = vf_df[vf_df['Subject']==rat_id]
            rp_base = [pd.to_numeric(rv.iloc[0][f"VF1_right_Force {i}"],errors="coerce") for i in range(1,4) if not rv.empty]
            rp_with = [pd.to_numeric(rv.iloc[0][f"VF2_right_Force {i}"],errors="coerce") for i in range(1,4) if not rv.empty]
            lp_base = [pd.to_numeric(rv.iloc[0][f"VF1_left_Force {i}"],errors="coerce") for i in range(1,4) if not rv.empty]
            lp_with = [pd.to_numeric(rv.iloc[0][f"VF2_left_Force {i}"],errors="coerce") for i in range(1,4) if not rv.empty]
            vf_ax.scatter([1]*len(rp_base), rp_base, color="brown", label="Right paw")
            vf_ax.scatter([2]*len(rp_with), rp_with, color="brown")
            vf_ax.scatter([1]*len(lp_base), lp_base, color="green", label="Left paw")
            vf_ax.scatter([2]*len(lp_with), lp_with, color="green")
            vf_ax.set_xticks(trials_vf); vf_ax.set_xticklabels([labels_vf[t] for t in trials_vf])
            vf_ax.legend(fontsize='small')

        pp.savefig(fig)
        plt.close(fig)

    pp.close()
    print(f"PDF created at {output_pdf}")

if __name__ == "__main__":
    main()
