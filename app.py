import streamlit as st
import pandas as pd

from logic_ai import analyze_part_risk

st.title("🛡️ DefenseLog: Supply Chain Risk Agent")

uploaded_file = st.file_uploader("Upload BOM", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.info(f"🚀 Forward Deployed Agent active. Scanning {len(df)} components...")
    progress_bar = st.progress(0)
    results = []

    total = len(df)

    for idx, (_, row) in enumerate(df.iterrows()):
        part = row.get("Part Number", "Unknown")
        desc = row.get("Description", "")

        status, notes = analyze_part_risk(str(part), str(desc))

        results.append({
        "Part Number": part,
        "Description": desc,
        "AI Status": status,
        "AI Notes": notes
    })

        progress_bar.progress((idx + 1) / total)

    result_df = pd.DataFrame(results)

    st.success("AI Analysis Complete")
    st.dataframe(result_df, use_container_width=True)

    # Actions (Download and Reset)
    col1, col2 = st.columns([1, 1])

    with col1:
        # Allow user to download before clearing the session state
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label = "💾 Report",
            data = csv,
            file_name = "defense_log_report.csv",
            mime = 'text/csv',  
        )
    with col2:
        # Reset button to clear the session state
        if st.button("🔄 Reset"):
            st.session_state.uploader_key += 1
            # Run the script immediately
            st.rerun()
