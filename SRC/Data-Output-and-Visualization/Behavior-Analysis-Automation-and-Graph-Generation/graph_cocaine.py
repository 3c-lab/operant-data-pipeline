import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

# -------------------------------
# Configuration — change only COHORT here
# -------------------------------
COHORT = 30
BEHAVIOR_FILE    = rf"C:\Users\georg\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Behavior Sheet Auto\Cocaine_C{COHORT}_behavior_sheet.xlsx"
COHORT_INFO_FILE = rf"C:\Users\georg\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Cohort Information\Cocaine C{COHORT} Updated Cohort Information.xlsx"
OUTPUT_PDF       = fr"C:\Users\georg\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Graphs\C{COHORT}_behavior_graphs.pdf"

# -------------------------------
# Helper functions
# -------------------------------
def extract_day(session_name):
    m = re.search(r"\d+", str(session_name))
    return int(m.group()) if m else None

def parse_daily_issue(issue_str, rat_id):
    return False if pd.isna(issue_str) else (rat_id in issue_str)

def extract_section(df, section_name, meta_session_names,
                    next_sections=("Rewards","Active Lever Presses","Inactive Lever Presses","Breakpoint")):
    """
    Pull out one section (Rewards / Active / Inactive / Breakpoint).
    We only break when we hit the next section header, not on blank rows.
    """
    rows = df.index[df.iloc[:,0].astype(str).str.strip() == section_name].tolist()
    if not rows:
        raise ValueError(f"Section {section_name} not found")
    start = rows[0]
    header = [str(h).strip() for h in df.iloc[start+1].fillna("")]
    data = []
    i = start + 2
    while i < len(df):
        first = str(df.iloc[i,0]).strip()
        if first in next_sections:
            break
        data.append(df.iloc[i].tolist())
        i += 1

    sec = pd.DataFrame(data, columns=header)

    total = sec.shape[1]
    n_fixed_front = 4
    n_fixed_back  = 4
    ncols = total - (n_fixed_front + n_fixed_back)
    if ncols > 0 and len(meta_session_names) >= ncols:
        sec.columns = (
            header[:n_fixed_front]
          + meta_session_names[:ncols]
          + header[-n_fixed_back:]
        )

    sec["Rat"]  = sec["Rat"].astype(str).str.strip()
    sec["RFID"] = sec["RFID"].astype(str).str.strip()
    return sec

def extract_meta_row(df, title):
    m = df[df.iloc[:,0].astype(str).str.strip().str.lower() == title.lower()]
    if not m.empty:
        return m.iloc[0,4:].apply(lambda x: str(x).strip())
    return pd.Series([""]*(df.shape[1]-4))


# -------------------------------
# Main
# -------------------------------
def main():
    # --- Load & parse metadata ---
    df = pd.read_excel(BEHAVIOR_FILE, sheet_name="Behavior Data", header=None)
    meta_dates    = df.iloc[0,4:]
    meta_sessions = df.iloc[1,4:].astype(str).str.strip()
    meta_issues   = df.iloc[2,4:].astype(str).str.strip()
    meta_notes    = extract_meta_row(df, "Notes")

    meta_entries = []
    for i, sess in enumerate(meta_sessions):
        meta_entries.append({
            "session": sess,
            "day":     extract_day(sess),
            "date":    pd.to_datetime(meta_dates.iloc[i]),
            "issue":   meta_issues.iloc[i],
            "note":    meta_notes.iloc[i] if i < len(meta_notes) else ""
        })
    meta_names = meta_sessions.tolist()

    # Precompute PRESHOCK vs SHOCK columns
    pre_sess_all   = [s for s in meta_names if s.startswith("PRESHOCK")]
    shock_sess_all = [s for s in meta_names if s.startswith("SHOCK") and s not in pre_sess_all]

    # --- Extract each section ---
    rewards_df  = extract_section(df, "Rewards",                meta_names)
    active_df   = extract_section(df, "Active Lever Presses",   meta_names)
    inactive_df = extract_section(df, "Inactive Lever Presses", meta_names)
    for sec in (rewards_df, active_df, inactive_df):
        sec.iloc[:,4:-4] = sec.iloc[:,4:-4].apply(pd.to_numeric, errors="coerce")

    # --- Cohort info & rats list ---
    cohort_df = pd.read_excel(COHORT_INFO_FILE)
    if 'Rat' in cohort_df.columns and 'RAT' not in cohort_df.columns:
        cohort_df.rename(columns={'Rat':'RAT'}, inplace=True)
    cohort_df['RAT']  = cohort_df['RAT'].astype(str).str.strip()
    cohort_df['RFID'] = cohort_df['RFID'].astype(str).str.strip()
    rats = rewards_df[['Rat','RFID']].drop_duplicates().reset_index(drop=True)

    # --- Plot setup ---
    session_groups = {
        "SHA":   ["SHA"],
        "LGA":   ["LGA"],
        "PR":    ["PR"],
        "Shock": ["SHOCK"]
    }
    measures = [
        ("Reward",   rewards_df),
        ("Active",   active_df),
        ("Inactive", inactive_df)
    ]
    locator = ticker.MaxNLocator(integer=True)
    pp = PdfPages(OUTPUT_PDF)

    # --- Page 1: Cohort Averages ---
    fig = plt.figure(figsize=(15,20))
    gs1 = fig.add_gridspec(5,3, height_ratios=[0.5,1,1,1,1], hspace=0.4, wspace=0.3)

    ax0 = fig.add_subplot(gs1[0,:])
    ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1, transform=ax0.transAxes,
                            fill=False, edgecolor='black', linewidth=1.5))
    ax0.text(0.5,0.5, f"Cohort {COHORT} Averages",
             ha='center', va='center', fontsize=18, fontweight='bold')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        if grp == "PR":
            entries = [e for e in meta_entries if re.match(r"^PR\d+$", e["session"])]
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        elif grp == "Shock":
            days = [1,2]
        else:
            entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
            days = [e["day"] for e in entries]

        for cidx,(mname,sec_df) in enumerate(measures):
            ax = fig.add_subplot(gs1[ridx, cidx])

            if grp == "Shock":
                oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
                for sess_group in (pre_sess_all, shock_sess_all):
                    block = sec_df[sess_group].apply(pd.to_numeric, errors="coerce")
                    stacked = block.stack()
                    cnt = stacked.count()
                    oa.append(stacked.mean(skipna=True) if cnt else np.nan)
                    os.append(stacked.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                    mstk = block[sec_df['Rat'].str.startswith("M")].stack()
                    cntm = mstk.count()
                    ma.append(mstk.mean(skipna=True) if cntm else np.nan)
                    ms.append(mstk.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                    fstk = block[sec_df['Rat'].str.startswith("F")].stack()
                    cntf = fstk.count()
                    fa.append(fstk.mean(skipna=True) if cntf else np.nan)
                    fs.append(fstk.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)

                ax.plot(days, oa, color="grey", marker="o", alpha=0.5, label="Cohort")
                ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os),
                                color="grey", alpha=0.25)
                ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
                ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms),
                                color="lightblue", alpha=0.25)
                ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
                ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs),
                                color="orange", alpha=0.25)
                ax.set_xticks(days)
                ax.set_xticklabels(["Preshock","Shock"])

            else:
                oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
                for e in entries:
                    col = pd.to_numeric(sec_df[e["session"]], errors="coerce")
                    cnt = col.count()
                    oa.append(col.mean(skipna=True))
                    os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                    mcol = col[sec_df['Rat'].str.startswith("M")]
                    cntm = mcol.count()
                    ma.append(mcol.mean(skipna=True))
                    ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                    fcol = col[sec_df['Rat'].str.startswith("F")]
                    cntf = fcol.count()
                    fa.append(fcol.mean(skipna=True))
                    fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)

                ax.plot(days, oa, color="grey", marker="o", alpha=0.5, label="Cohort")
                ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os),
                                color="grey", alpha=0.25)
                ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
                ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms),
                                color="lightblue", alpha=0.25)
                ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
                ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs),
                                color="orange", alpha=0.25)

            # Page-1 styling
            ax.set_title(f"{grp} {mname}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(locator)
            # <-- FIX: show all days for SHA & LGA:
            if grp in ["SHA", "LGA"]:
                ax.set_xticks(days)
                ax.set_xticklabels(days)
            # custom y-limits
            if grp=="SHA" and mname=="Reward":
                ax.set_ylim(0,40)
            elif grp=="SHA":
                ax.set_ylim(0,100)
            if grp=="LGA" and mname=="Reward":
                ax.set_ylim(0,200)
            elif grp=="LGA":
                ax.set_ylim(0,300)

    pp.savefig(fig)
    plt.close(fig)

    # --- Page 2: All-rats overlay (4×3) with buckets & raw shock values ---
    rats_list   = [r for r in rats['Rat'] if re.match(r'^[MF]\d{4}$', r)]
    male_rats   = [r for r in rats_list if r.startswith('M')]
    female_rats = [r for r in rats_list if r.startswith('F')]

    def get_serial(r): return int(r[3:])
    male_ser   = sorted(get_serial(r) for r in male_rats)
    female_ser = sorted(get_serial(r) for r in female_rats)
    m_q1,m_q2,m_q3 = np.percentile(male_ser,   [25,50,75])
    f_q1,f_q2,f_q3 = np.percentile(female_ser, [25,50,75])

    def bucket(n,q1,q2,q3):
        if   n<=q1: return 0
        elif n<=q2: return 1
        elif n<=q3: return 2
        else:        return 3

    male_colors   = {0:'darkgreen',1:'darkblue',2:'lightgreen',3:'lightblue'}
    female_colors = {0:'brown',    1:'pink',     2:'red',       3:'orange'}

    male_handles, male_labels = [],[]
    for i in range(4):
        grp = sorted(r for r in male_rats if bucket(get_serial(r),m_q1,m_q2,m_q3)==i)
        if not grp: continue
        low,high = get_serial(grp[0]), get_serial(grp[-1])
        male_handles.append(Line2D([0],[0],color=male_colors[i],lw=2))
        male_labels.append(f"M{COHORT}{low:02d}–M{COHORT}{high:02d}")

    female_handles, female_labels = [],[]
    for i in range(4):
        grp = sorted(r for r in female_rats if bucket(get_serial(r),f_q1,f_q2,f_q3)==i)
        if not grp: continue
        low,high = get_serial(grp[0]), get_serial(grp[-1])
        female_handles.append(Line2D([0],[0],color=female_colors[i],lw=2))
        female_labels.append(f"F{COHORT}{low:02d}–F{COHORT}{high:02d}")

    fig = plt.figure(figsize=(15,20))
    gs2 = fig.add_gridspec(5,3, height_ratios=[0.5,1,1,1,1], hspace=0.4, wspace=0.3)
    ax0 = fig.add_subplot(gs2[0,:])
    ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                            fill=False,edgecolor='black',linewidth=1.5))
    ax0.text(0.5,0.6,"All Cohort Readings",
             ha='center',va='center',fontsize=18,fontweight='bold')
    leg1 = ax0.legend(male_handles, male_labels,
                      loc='center left', bbox_to_anchor=(0.02,0.5),
                      ncol=2, frameon=False, fontsize='small')
    ax0.add_artist(leg1)
    ax0.legend(female_handles, female_labels,
               loc='center right', bbox_to_anchor=(0.98,0.5),
               ncol=2, frameon=False, fontsize='small')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        if grp=="PR":
            entries = [e for e in meta_entries if re.match(r"^PR\d+$", e["session"])]
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        elif grp=="Shock":
            days = [1,2]
        else:
            entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
            days = [e["day"] for e in entries]

        for cidx,(_,sec_df) in enumerate(measures):
            ax = fig.add_subplot(gs2[ridx,cidx])

            if grp=="Shock":
                for rat in rats_list:
                    pres_vals  = sec_df.loc[sec_df['Rat']==rat, pre_sess_all]\
                                     .apply(pd.to_numeric,errors='coerce')\
                                     .values.flatten()
                    shock_vals = sec_df.loc[sec_df['Rat']==rat, shock_sess_all]\
                                     .apply(pd.to_numeric,errors='coerce')\
                                     .values.flatten()
                    nv1 = pres_vals[~np.isnan(pres_vals)]
                    nv2 = shock_vals[~np.isnan(shock_vals)]
                    val1 = nv1[0] if nv1.size>0 else np.nan
                    val2 = nv2[0] if nv2.size>0 else np.nan
                    col = (male_colors[bucket(get_serial(rat),m_q1,m_q2,m_q3)]
                           if rat.startswith('M')
                           else female_colors[bucket(get_serial(rat),f_q1,f_q2,f_q3)])
                    ax.plot(days, [val1,val2], color=col, alpha=0.7, marker='o')
                ax.set_xticks(days)
                ax.set_xticklabels(["Preshock","Shock"])

            else:
                for rat in rats_list:
                    col = (male_colors[bucket(get_serial(rat),m_q1,m_q2,m_q3)]
                           if rat.startswith('M')
                           else female_colors[bucket(get_serial(rat),f_q1,f_q2,f_q3)])
                    vals = [
                        sec_df.loc[sec_df['Rat']==rat, e["session"]].iloc[0]
                        if not sec_df.loc[sec_df['Rat']==rat, e["session"]].empty else np.nan
                        for e in entries
                    ]
                    ax.plot(days, vals, color=col, alpha=0.7)

            ax.set_title(f"{grp} {measures[cidx][0]}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if measures[cidx][0]=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(locator)
            # <-- FIX: show all days for SHA & LGA:
            if grp in ["SHA", "LGA"]:
                ax.set_xticks(days)
                ax.set_xticklabels(days)
            if grp=="SHA": ax.set_ylim(0,200)
            if grp=="LGA": ax.set_ylim(0,300)

    pp.savefig(fig)
    plt.close(fig)

    # --- Page 3: Per-rat Detail (4×3 + info) ---
    for _, rr in rats.iterrows():
        rat_id   = str(rr["Rat"]).strip()
        rat_rfid = str(rr["RFID"]).split(".")[0]
        ci       = cohort_df[cohort_df['RAT']==rat_id]
        coat     = ci.iloc[0].get("Coat Color","None")       if not ci.empty else "None"
        dgroup   = ci.iloc[0].get("Dissection Group","None") if not ci.empty else "None"
        egroup   = ci.iloc[0].get("Experiment Group","None") if not ci.empty else "None"
        er       = rewards_df[rewards_df['Rat']==rat_id]
        ec       = er.iloc[0].get("Exit Code",np.nan)        if not er.empty else np.nan
        lg       = er.iloc[0].get("Last Good Session",np.nan) if not er.empty else np.nan
        ec       = "None" if pd.isna(ec) else ec
        lg       = "None" if pd.isna(lg) else lg

        fig = plt.figure(figsize=(15,20))
        mg  = fig.add_gridspec(5,3,
            height_ratios=[0.6,1,1,1,1], hspace=0.4, wspace=0.3
        )

        ax0 = fig.add_subplot(mg[0,:])
        ax0.axis('off')
        ax0.add_patch(Rectangle((0,0),1,1, transform=ax0.transAxes,
                                fill=False, edgecolor='black', linewidth=1.5))
        ax0.text(0.02,0.98, fr"$\bf{{Rat}}$: {rat_id}",
                 transform=ax0.transAxes, ha='left', va='top', fontsize=17)
        other_lines = [
            fr"$\bf{{RFID}}$: {rat_rfid}",
            f"$\\bf{{Coat Color}}$: {coat}",
            f"$\\bf{{Dissection Group}}$: {dgroup}",
            f"$\\bf{{Experiment Group}}$: {egroup}",
            f"$\\bf{{Exit Code}}$: {ec}",
            f"$\\bf{{Last Good Session}}$: {lg}"
        ]
        ax0.text(0.02,0.80, "\n".join(other_lines),
                 transform=ax0.transAxes, ha='left', va='top',
                 fontsize=12, linespacing=1.1)

        for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
            if grp=="PR":
                entries = [e for e in meta_entries if re.match(r"^PR\d+$",e["session"])]
                entries = sorted(entries,key=lambda x:x["date"])
                days = list(range(1,len(entries)+1))
            elif grp=="Shock":
                days = [1,2]
            else:
                entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
                days = [e["day"] for e in entries]

            for cidx,(mname,sec_df) in enumerate(measures):
                ax = fig.add_subplot(mg[ridx,cidx])

                if grp=="Shock":
                    pres_vals  = sec_df.loc[sec_df['Rat']==rat_id, pre_sess_all]\
                                     .apply(pd.to_numeric,errors='coerce')\
                                     .values.flatten()
                    shock_vals = sec_df.loc[sec_df['Rat']==rat_id, shock_sess_all]\
                                     .apply(pd.to_numeric,errors='coerce')\
                                     .values.flatten()
                    nv1 = pres_vals[~np.isnan(pres_vals)]
                    nv2 = shock_vals[~np.isnan(shock_vals)]
                    val1 = nv1[0] if nv1.size>0 else np.nan
                    val2 = nv2[0] if nv2.size>0 else np.nan
                    rv   = [val1, val2]

                    oa,os,ma,ms,fa,fs = [],[],[],[],[],[]
                    for sess_group in (pre_sess_all, shock_sess_all):
                        block = sec_df[sess_group].apply(pd.to_numeric,errors='coerce')
                        stk   = block.stack()
                        cnt   = stk.count()
                        oa.append(stk.mean(skipna=True) if cnt else np.nan)
                        os.append(stk.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                        mstk = block[sec_df['Rat'].str.startswith("M")].stack()
                        cntm = mstk.count()
                        ma.append(mstk.mean(skipna=True) if cntm else np.nan)
                        ms.append(mstk.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                        fstk = block[sec_df['Rat'].str.startswith("F")].stack()
                        cntf = fstk.count()
                        fa.append(fstk.mean(skipna=True) if cntf else np.nan)
                        fs.append(fstk.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)

                    ax.plot(days, rv, color="red",    marker="o", label="Rat")
                    ax.plot(days, oa, color="grey",   marker="o", alpha=0.5, label="Cohort")
                    ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os), color="grey", alpha=0.25)
                    ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
                    ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms), color="lightblue", alpha=0.25)
                    ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
                    ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs), color="orange", alpha=0.25)
                    ax.set_xticks(days)
                    ax.set_xticklabels(["Preshock","Shock"])

                else:
                    rv,oa,os,ma,ms,fa,fs,flags = [],[],[],[],[],[],[],[]
                    for e in entries:
                        val = sec_df.loc[sec_df['Rat']==rat_id, e["session"]]
                        v   = val.iloc[0] if not val.empty else np.nan
                        rv.append(v)
                        col = pd.to_numeric(sec_df[e["session"]],errors="coerce")
                        cnt = col.count()
                        oa.append(col.mean(skipna=True))
                        os.append(col.std(skipna=True)/np.sqrt(cnt) if cnt else np.nan)
                        mcol = col[sec_df['Rat'].str.startswith("M")]
                        cntm = mcol.count()
                        ma.append(mcol.mean(skipna=True))
                        ms.append(mcol.std(skipna=True)/np.sqrt(cntm) if cntm else np.nan)
                        fcol = col[sec_df['Rat'].str.startswith("F")]
                        cntf = fcol.count()
                        fa.append(fcol.mean(skipna=True))
                        fs.append(fcol.std(skipna=True)/np.sqrt(cntf) if cntf else np.nan)
                        flags.append(parse_daily_issue(e["issue"], rat_id))

                    ax.plot(days, rv, color="red", marker="o", label="Rat")
                    ax.plot(days, oa, color="grey", marker="o", alpha=0.5, label="Cohort")
                    ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os), color="grey", alpha=0.25)
                    ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
                    ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms), color="lightblue", alpha=0.25)
                    ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
                    ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs), color="orange", alpha=0.25)
                    for d,y,f in zip(days, rv, flags):
                        if f and not pd.isna(y):
                            ax.plot(d, y, marker="o", markersize=12, color="yellow")

                ax.set_title(f"{grp} {mname}")
                ax.set_xlabel("Day")
                ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
                ax.xaxis.set_major_locator(locator)
                # <-- FIX: show all days for SHA & LGA on Page 3 too:
                if grp in ["SHA", "LGA"]:
                    ax.set_xticks(days)
                    ax.set_xticklabels(days)
                if grp=="SHA":   ax.set_ylim(0,100)
                if grp=="LGA":   ax.set_ylim(0,300)
                ax.legend(fontsize='small')

        pp.savefig(fig)
        plt.close(fig)

    pp.close()
    print(f"PDF written to: {OUTPUT_PDF}")

if __name__=="__main__":
    main()
