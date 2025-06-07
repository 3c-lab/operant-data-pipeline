import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import re
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle

# -------------------------------
# Configuration — change only COHORT here
# -------------------------------
COHORT = 29
BEHAVIOR_FILE    = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Behavior Sheet Auto\Cocaine_C{COHORT}_behavior_sheet.xlsx"
COHORT_INFO_FILE = rf"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Cohort Information\Cocaine C{COHORT} Updated Cohort Information.xlsx"
OUTPUT_PDF       = fr"C:\Users\udays\George Lab Dropbox\George_Lab\Team GWAS\1. Cocaine GWAS\Cocaine Graphs\C{COHORT}_behavior_graphs.pdf"

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
    # find section start
    rows = df.index[df.iloc[:,0].astype(str).str.strip()==section_name].tolist()
    if not rows:
        raise ValueError(f"Section {section_name} not found")
    start = rows[0]
    header = [str(h).strip() for h in df.iloc[start+1].fillna("")]
    data = []
    i = start + 2
    while i < len(df):
        first = str(df.iloc[i,0]).strip()
        if first in next_sections or first=="":
            break
        data.append(df.iloc[i].tolist())
        i += 1
    sec = pd.DataFrame(data, columns=header)

    # rename columns: first 3 stay, then session columns, then last 4 meta
    total = sec.shape[1]
    n_fixed_front = 4    # Rat, RFID, Drug Group, Experiment Group
    n_fixed_back  = 4    # Exit Day, Exit Code, Exit Notes, Last Good Session
    ncols = total - (n_fixed_front + n_fixed_back)
    if ncols > 0 and len(meta_session_names) >= ncols:
        sec.columns = (
            header[:n_fixed_front]                # keep Experiment Group in front
          + meta_session_names[:ncols]           # now exactly ncols session columns
          + header[-n_fixed_back:]               # the 4 “exit”-type cols
        )

    sec["Rat"]  = sec["Rat"].astype(str).str.strip()
    sec["RFID"] = sec["RFID"].astype(str).str.strip()
    return sec

def extract_meta_row(df, title):
    m = df[df.iloc[:,0].astype(str).str.strip().str.lower()==title.lower()]
    if not m.empty:
        # session metadata also starts at column E → index 4
        return m.iloc[0,4:].apply(lambda x: str(x).strip())
    return pd.Series([""]*(df.shape[1]-4))

# -------------------------------
# Main
# -------------------------------
def main():
    # load behavior sheet
    df = pd.read_excel(BEHAVIOR_FILE, sheet_name="Behavior Data", header=None)
    meta_dates    = df.iloc[0,4:]
    meta_sessions = df.iloc[1,4:].astype(str).str.strip()
    meta_issues   = df.iloc[2,4:].astype(str).str.strip()
    meta_notes    = extract_meta_row(df, "Notes")

    # build meta entries
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

    # extract three behavior sections
    rewards_df  = extract_section(df, "Rewards",                meta_names)
    active_df   = extract_section(df, "Active Lever Presses",   meta_names)
    inactive_df = extract_section(df, "Inactive Lever Presses", meta_names)

    # numeric conversion on session columns only (cols index 4 through –4)
    for sec in (rewards_df, active_df, inactive_df):
        sec.iloc[:,4:-4] = sec.iloc[:,4:-4].apply(pd.to_numeric, errors="coerce")

    # load cohort info
    cohort_df = pd.read_excel(COHORT_INFO_FILE)
    if 'Rat' in cohort_df.columns and 'RAT' not in cohort_df.columns:
        cohort_df.rename(columns={'Rat':'RAT'}, inplace=True)
    cohort_df['RAT']  = cohort_df['RAT'].astype(str).str.strip()
    cohort_df['RFID'] = cohort_df['RFID'].astype(str).str.strip()

    # list of rats
    rats = rewards_df[['Rat','RFID']].drop_duplicates().reset_index(drop=True)

    # plotting parameters
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

    # --- Page 1: Cohort Averages (4×3) ---
    fig = plt.figure(figsize=(15,20))
    gs1 = fig.add_gridspec(5,3, height_ratios=[0.5,1,1,1,1], hspace=0.4, wspace=0.3)

    # big title box
    ax0 = fig.add_subplot(gs1[0,:])
    ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                            fill=False, edgecolor='black', linewidth=1.5))
    ax0.text(0.5,0.5, f"Cohort {COHORT} Averages",
             ha='center', va='center',
             fontsize=18, fontweight='bold')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
        if grp=="PR":
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        else:
            days = [e["day"] for e in entries]

        for cidx,(mname,sec_df) in enumerate(measures):
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

            ax = fig.add_subplot(gs1[ridx, cidx])
            ax.plot(days, oa, color="grey", marker="o", alpha=0.5, label="Cohort")
            ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os),
                            color="grey", alpha=0.25)
            ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
            ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms),
                            color="lightblue", alpha=0.25)
            ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
            ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs),
                            color="orange", alpha=0.25)

            ax.set_title(f"{grp} {mname}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(locator)
            ax.set_xticks(days)
            ax.set_xticklabels(days)
            if grp=="SHA":
                ax.set_ylim(0,100)
            if grp=="LGA":
                ax.set_ylim(0,300)
            ax.legend(fontsize='small')

    pp.savefig(fig)
    plt.close(fig)

    # --- Page 2: All-rats overlay (4×3) ---
    fig = plt.figure(figsize=(15,20))
    gs2 = fig.add_gridspec(5,3, height_ratios=[0.5,1,1,1,1], hspace=0.4, wspace=0.3)

    ax0 = fig.add_subplot(gs2[0,:])
    ax0.axis('off')
    ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                            fill=False, edgecolor='black', linewidth=1.5))
    ax0.text(0.5,0.5,"All Cohort Readings",
             ha='center', va='center',
             fontsize=18, fontweight='bold')

    for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
        entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
        if grp=="PR":
            entries = sorted(entries, key=lambda x: x["date"])
            days = list(range(1,len(entries)+1))
        else:
            days = [e["day"] for e in entries]

        for cidx,(_,sec_df) in enumerate(measures):
            ax = fig.add_subplot(gs2[ridx, cidx])
            for rat in rats["Rat"]:
                vals = [ sec_df.loc[sec_df['Rat']==rat, e["session"]].iloc[0]
                         if not sec_df.loc[sec_df['Rat']==rat, e["session"]].empty else np.nan
                         for e in entries ]
                ax.plot(days, vals, color="red", alpha=0.5)

            ax.set_title(f"{grp} {measures[cidx][0]}")
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Infusions" if measures[cidx][0]=="Reward" else "Number of Presses")
            ax.xaxis.set_major_locator(locator)
            ax.set_xticks(days)
            ax.set_xticklabels(days)
            if grp=="SHA":
                ax.set_ylim(0,100)
            if grp=="LGA":
                ax.set_ylim(0,300)

    pp.savefig(fig)
    plt.close(fig)

    # --- Pages 3+: per-rat detail (4×3 + top info) ---
    for _, rr in rats.iterrows():
        rat_id   = str(rr["Rat"]).strip()
        rat_rfid = str(rr["RFID"]).split(".")[0]

        ci = cohort_df[cohort_df['RAT']==rat_id]
        coat    = ci.iloc[0].get("Coat Color","None")       if not ci.empty else "None"
        dgroup  = ci.iloc[0].get("Dissection Group","None") if not ci.empty else "None"
        # surgeon = ci.iloc[0].get("Surgeon","None")          if not ci.empty else "None"

        # find Exit Code & Last Good Session
        er = rewards_df[rewards_df['Rat']==rat_id]
        ec = er.iloc[0].get("Exit Code",     np.nan) if not er.empty else np.nan
        lg = er.iloc[0].get("Last Good Session", np.nan) if not er.empty else np.nan
        ec = "None" if pd.isna(ec) else ec
        lg = "None" if pd.isna(lg) else lg

        fig = plt.figure(figsize=(15,20))
        mg  = fig.add_gridspec(5,3, height_ratios=[0.6,1,1,1,1], hspace=0.4, wspace=0.3)

        # Top info box with bold labels
        ax0 = fig.add_subplot(mg[0,:])
        ax0.axis('off')
        ax0.add_patch(Rectangle((0,0),1,1,transform=ax0.transAxes,
                                fill=False, edgecolor='black', linewidth=1.5))

        lines = [
            fr"$\bf{{Rat}}$: {rat_id}",
            fr"$\bf{{RFID}}$: {rat_rfid}",
            f"$\\bf{{Coat Color}}$: {coat}",
            f"$\\bf{{Dissection Group}}$: {dgroup}",
            f"$\\bf{{Exit Code}}$: {ec}",
            f"$\\bf{{Last Good Session}}$: {lg}"
        ]
        ax0.text(0.02,0.98, "\n".join(lines),
                 transform=ax0.transAxes, ha='left', va='top',
                 fontsize=12, linespacing=1.1)

        # now SHA / LGA / PR / Shock rows exactly as before…
        for ridx,(grp,pfx) in enumerate(session_groups.items(), start=1):
            entries = [e for e in meta_entries if any(e["session"].startswith(p) for p in pfx)]
            if grp=="PR":
                entries = sorted(entries, key=lambda x: x["date"])
                days = list(range(1,len(entries)+1))
            else:
                days = [e["day"] for e in entries]

            for cidx,(mname,sec_df) in enumerate(measures):
                rv,oa,os,ma,ms,fa,fs,flags = [],[],[],[],[],[],[],[]
                for e in entries:
                    val = sec_df.loc[sec_df['Rat']==rat_id, e["session"]]
                    v   = val.iloc[0] if not val.empty else np.nan
                    rv.append(v)
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
                    flags.append(parse_daily_issue(e["issue"], rat_id))

                ax = fig.add_subplot(mg[ridx, cidx])
                ax.plot(days, rv, color="red", marker="o", label="Rat")
                ax.plot(days, oa, color="grey", marker="o", alpha=0.5, label="Cohort")
                ax.fill_between(days, np.array(oa)-np.array(os), np.array(oa)+np.array(os),
                                color="grey", alpha=0.25)
                ax.plot(days, ma, color="lightblue", marker="o", alpha=0.5, label="Male")
                ax.fill_between(days, np.array(ma)-np.array(ms), np.array(ma)+np.array(ms),
                                color="lightblue", alpha=0.25)
                ax.plot(days, fa, color="orange", marker="o", alpha=0.5, label="Female")
                ax.fill_between(days, np.array(fa)-np.array(fs), np.array(fa)+np.array(fs),
                                color="orange", alpha=0.25)
                for d,y,f in zip(days, rv, flags):
                    if f and not pd.isna(y):
                        ax.plot(d, y, marker="o", markersize=12, color="yellow")

                ax.set_title(f"{grp} {mname}")
                ax.set_xlabel("Day")
                ax.set_ylabel("Number of Infusions" if mname=="Reward" else "Number of Presses")
                ax.xaxis.set_major_locator(locator)
                ax.set_xticks(days)
                ax.set_xticklabels(days)
                if grp=="SHA":
                    ax.set_ylim(0,100)
                if grp=="LGA":
                    ax.set_ylim(0,300)

                ax.legend(fontsize='small')

        pp.savefig(fig)
        plt.close(fig)

    pp.close()
    print(f"PDF written to: {OUTPUT_PDF}")

if __name__=="__main__":
    main()
