"""
Flask web application for CCMS.

Upload two CSV files and view interactive case count visualizations
and drill-down details.
"""
from flask import (
    Flask, request, render_template,
    redirect, url_for, flash, jsonify, session,
)
import pandas as pd
import os
from werkzeug.utils import secure_filename

# Import core CCMS logic
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ccms.core import compute_ccms

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def analyze_clusters(df):
    """Build cluster info dict from merged dataframe."""
    clusters = {}
    for _, row in df.iterrows():
        rec_id = row["RecID"]
        er1_cluster = row["ER1 ClusterID"]
        er2_cluster = row["ER2 ClusterID"]

        if er1_cluster not in clusters:
            clusters[er1_cluster] = {
                "er2_clusters": set(),
                "er2_references": set(),
                "size_er1": 0,
                "records": [],
            }
        clusters[er1_cluster]["er2_clusters"].add(er2_cluster)
        clusters[er1_cluster]["er2_references"].update(
            df[df["ER2 ClusterID"] == er2_cluster]["RecID"]
        )
        clusters[er1_cluster]["size_er1"] += 1
        clusters[er1_cluster]["records"].append(
            {"RecID": rec_id, "ER2 ClusterID": er2_cluster}
        )

    # Convert sets to lists for JSON serialization
    for info in clusters.values():
        info["er2_clusters"] = list(info["er2_clusters"])
        info["er2_references"] = list(info["er2_references"])
    return clusters


def determine_cases(clusters):
    """Classify clusters into four CCMS cases."""
    cases = {"Unchanged": {}, "Merged": {}, "Partitioned": {}, "Overlapping": {}}
    for cid, info in clusters.items():
        n_er2 = len(info["er2_clusters"])
        same_size = info["size_er1"] == len(info["er2_references"])

        if n_er2 == 1 and same_size:
            cases["Unchanged"][cid] = info
        elif n_er2 == 1 and not same_size:
            cases["Merged"][cid] = info
        elif n_er2 > 1 and same_size:
            cases["Partitioned"][cid] = info
        elif n_er2 > 1 and not same_size:
            cases["Overlapping"][cid] = info
    return cases


def determine_singletons(df, clusters):
    """Identify singleton clusters in ER1 and ER2."""
    er2_refs = {}
    for _, row in df.iterrows():
        er2_cid = row["ER2 ClusterID"]
        if er2_cid not in er2_refs:
            er2_refs[er2_cid] = set()
        er2_refs[er2_cid].add(row["RecID"])

    er1_singletons = {
        c: list(r) for c, r in er2_refs.items() if len(r) == 1
    }
    er2_singletons = {
        c: info for c, info in clusters.items() if info["size_er1"] == 1
    }
    return er1_singletons, er2_singletons


def create_chart_data(cases, clusters, title):
    """Prepare data for ECharts visualizations."""
    bar_data = [
        {"name": case, "value": len(cids)}
        for case, cids in cases.items()
    ]
    return {"bar_data": bar_data, "pie_data": bar_data, "title": title}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        return render_template("index2.html", show_results=False)

    if "file1" not in request.files or "file2" not in request.files:
        flash("Both files are required")
        return redirect(request.url)

    file1 = request.files["file1"]
    file2 = request.files["file2"]

    if not (file1.filename and file2.filename):
        flash("No selected file")
        return redirect(request.url)

    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        flash("Allowed file types are csv")
        return redirect(request.url)

    # Save and load files
    path1 = os.path.join(app.config["UPLOAD_FOLDER"],
                         secure_filename(file1.filename))
    path2 = os.path.join(app.config["UPLOAD_FOLDER"],
                         secure_filename(file2.filename))
    file1.save(path1)
    file2.save(path2)

    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    df1.columns = ["RecID", "ER1 ClusterID"]
    df2.columns = ["RecID", "ER2 ClusterID"]
    df = pd.merge(df1, df2, on="RecID")
    df.sort_values(by=["ER1 ClusterID", "ER2 ClusterID"], inplace=True)

    # ER1 as primary
    clusters = analyze_clusters(df)
    cases_er1 = determine_cases(clusters)
    chart_er1 = create_chart_data(cases_er1, clusters,
                                  "ER1 as primary, ER2 as secondary")

    # ER2 as primary (swap columns)
    df_swap = df.rename(columns={
        "ER1 ClusterID": "ER2 ClusterID",
        "ER2 ClusterID": "ER1 ClusterID",
    })
    clusters_swap = analyze_clusters(df_swap)
    cases_er2 = determine_cases(clusters_swap)
    chart_er2 = create_chart_data(cases_er2, clusters_swap,
                                  "ER2 as primary, ER1 as secondary")

    # Singletons
    er1_sing, er2_sing = determine_singletons(df, clusters)

    # Summary report
    summary_report = build_summary(cases_er1, cases_er2, er1_sing, er2_sing)

    return render_template(
        "index2.html",
        show_results=True,
        summary={"ER1_primary": chart_er1, "ER2_primary": chart_er2},
        summary_report=summary_report,
        raw_data=df.to_dict(orient="records"),
    )


def build_summary(cases_er1, cases_er2, er1_sing, er2_sing):
    """Build plain-text summary report."""
    lines = [
        "ER1 as primary and ER2 as secondary:",
        f"  Unchanged:   {len(cases_er1['Unchanged'])}",
        f"  Merged:      {len(cases_er1['Merged'])}",
        f"  Partitioned: {len(cases_er1['Partitioned'])}",
        f"  Overlapping: {len(cases_er1['Overlapping'])}",
        "",
        "ER2 as primary and ER1 as secondary:",
        f"  Unchanged:   {len(cases_er2['Unchanged'])}",
        f"  Merged:      {len(cases_er2['Merged'])}",
        f"  Partitioned: {len(cases_er2['Partitioned'])}",
        f"  Overlapping: {len(cases_er2['Overlapping'])}",
        "",
        f"ER1 Singletons: {len(er1_sing)}",
        f"ER2 Singletons: {len(er2_sing)}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    app.run(debug=True)
